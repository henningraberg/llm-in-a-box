from __future__ import annotations

from textual import on, work
from textual.app import App
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Button, Select
from textual.worker import Worker

from database.db import session
from enums.enums import ChatRole
from gui.views.delete_chat_screen import DeleteChatScreen
from gui.views.main_view import MainView
from gui.views.new_chat_screen import NewChatScreen
from gui.widgets.chat_list_item_button import ChatListItemButton
from gui.widgets.chat_message_area import ChatMessageArea
from gui.widgets.llm_select import LLMSelect
from gui.widgets.text_area import ChatMessageTextArea
from integrations.ollama_manager import OllamaManager
from models.chat import Chat
from models.chat_message import ChatMessage


class TextualApp(App):
    """Main Textual application."""

    BINDINGS = [Binding('ctrl+q', description='Exit application', action='quit')]
    CSS_PATH = 'static/styles.tcss'

    current_chat_id: int | None = None
    response_worker: Worker | None = None

    def on_mount(self) -> None:
        self.title = 'LLM IN A BOX'
        self.push_screen(MainView())
        ascii_art = '+----+\n| 🤖 |\n+----+'
        self.notify(ascii_art, title=f'Welcome to {self.title}!')

    # --- Screen navigation ---

    @on(Button.Pressed, '#init-new-chat-button')
    def init_create_new_chat(self) -> None:
        self.push_screen(NewChatScreen(), callback=self.on_new_chat_dismissed)

    def on_new_chat_dismissed(self, model: str | None) -> None:
        if model is None:
            return
        chat = Chat(default_model=model, name='New chat').save()
        self.abort_llm_response_if_needed()
        chat_list = self.query_one('#chat-list', VerticalScroll)
        chat_list.mount(
            ChatListItemButton(chat.name, id=chat.get_gui_id()),
            before=chat_list.children[0] if chat_list.children else None,
        )
        self.load_chat(chat_id=chat.id)

    @on(Button.Pressed, '#init-delete-chat-button')
    def init_delete_chat(self) -> None:
        self.push_screen(DeleteChatScreen(), callback=self.on_delete_chat_dismissed)

    def on_delete_chat_dismissed(self, confirmed: bool) -> None:
        if not confirmed:
            return
        self.abort_llm_response_if_needed()
        chat = Chat.one(id=self.current_chat_id)
        self.query_one(chat.get_gui_id_with_hash_tag(), ChatListItemButton).remove()
        chat.delete()

        chats = Chat.get_multiple()
        if chats:
            self.load_chat(chat_id=chats[-1].id)
        else:
            self.toggle_chat_view(disabled=True)
            self.set_current_chat(chat_id=None)

    # --- Chat interaction ---

    @on(ChatListItemButton.Pressed)
    def on_chat_selected(self, event: ChatListItemButton.Pressed) -> None:
        if not isinstance(event.button, ChatListItemButton):
            return
        self.abort_llm_response_if_needed()
        chat_id = int(event.button.id.strip('_'))
        self.load_chat(chat_id)

    @on(LLMSelect.Changed, '#llm-selection-2')
    def on_model_changed(self, event: LLMSelect.Changed) -> None:
        if event.value != Select.BLANK:
            chat = Chat.one(id=self.current_chat_id)
            chat.default_model = event.value
            chat.save()

    @on(Button.Pressed, '#send-button')
    def init_send_message(self) -> None:
        text_input = self.query_one('#message-input')
        content = text_input.text
        if content:
            self.send_message(content=content)
            text_input.text = ''
            self.query_one('#abort-button').disabled = False

    @on(Button.Pressed, '#abort-button')
    def abort_message(self) -> None:
        self.abort_llm_response_if_needed()
        self.load_chat(chat_id=self.current_chat_id)

    # --- Business logic ---

    def abort_llm_response_if_needed(self) -> None:
        if self.response_worker and self.response_worker.is_running:
            session.rollback()
            self.response_worker.cancel()
            self.query_one('#abort-button').disabled = True
            self.query_one('#send-button').disabled = False

    def send_message(self, content: str) -> None:
        """Send a message to Ollama and handle the response."""
        chat = Chat.one(id=self.current_chat_id)
        chat_message = ChatMessage(chat_id=chat.id, content=content, role=ChatRole.USER).save()

        history_container = self.query_one('#chat-history-container', VerticalScroll)
        history_container.mount(ChatMessageArea(chat_message))

        dummy_chat_message = ChatMessage(chat_id=chat.id, role=ChatRole.ASSISTANT, content='', model=chat.default_model)
        ai_response = ChatMessageArea(dummy_chat_message)
        ai_response.text_area.loading = True
        history_container.mount(ai_response)

        self.scroll_history_container_to_end(history_container)
        self.response_worker = self.generate_response(chat=chat, ai_response_text_area=ai_response.text_area)

    @work(thread=True)
    async def generate_response(self, chat: Chat, ai_response_text_area: ChatMessageTextArea) -> None:
        """Generate the AI response asynchronously and update widget dynamically."""
        send_button = self.query_one('#send-button')
        abort_button = self.query_one('#abort-button')
        history_container = self.query_one('#chat-history-container', VerticalScroll)
        send_button.disabled = True

        for word in OllamaManager().chat_gui(chat):
            ai_response_text_area.loading = False
            ai_response_text_area.text += word
            self.scroll_history_container_to_end(history_container)

        abort_button.disabled = True
        send_button.disabled = False
        if chat.name == 'New chat':
            self.generate_chat_name(chat)

    @work(thread=True)
    async def generate_chat_name(self, chat: Chat) -> None:
        """Generate a descriptive chat name asynchronously."""
        try:
            chat.name = OllamaManager().generate_chat_name(chat)
            chat.save()
            button = self.query_one(chat.get_gui_id_with_hash_tag(), ChatListItemButton)
            button.label = chat.name
            button.refresh()
        except Exception:
            pass

    # --- UI helpers ---

    def load_chat(self, chat_id: int) -> None:
        """Load chat history and set the current chat."""
        self.set_current_chat(chat_id)

        history_container = self.query_one('#chat-history-container', VerticalScroll)
        if history_container.children:
            history_container.remove_children()

        chat = Chat.one(id=self.current_chat_id)

        llm_selector = self.query_one('#llm-selection-2', LLMSelect)
        llm_selector.value = chat.default_model

        history_container.mount(*[ChatMessageArea(message) for message in chat.messages])
        self.scroll_history_container_to_end(history_container)
        self.toggle_chat_view(disabled=False)

    def toggle_chat_view(self, disabled: bool) -> None:
        """Toggle the disabled state of the chat view widgets."""
        self.query_one('#llm-selection-2').disabled = disabled
        self.query_one('#chat-history-container', VerticalScroll).disabled = disabled

        message_input = self.query_one('#message-input')
        message_input.disabled = disabled
        message_input.text = ''

        self.query_one('#send-button').disabled = disabled
        self.query_one('#init-delete-chat-button').disabled = disabled

    def set_current_chat(self, chat_id: int | None) -> None:
        """Set the current chat and update sidebar highlighting."""
        previous_chat_id = self.current_chat_id
        self.current_chat_id = chat_id

        if previous_chat_id and self.current_chat_id:
            self.query_one(f'#_{previous_chat_id}', ChatListItemButton).remove_class('selected')

        if not self.current_chat_id:
            self.sub_title = ''
            if previous_chat_id:
                history_container = self.query_one('#chat-history-container', VerticalScroll)
                if history_container.children:
                    history_container.remove_children()
            return

        self.query_one(f'#_{self.current_chat_id}', ChatListItemButton).add_class('selected')
        self.sub_title = f'chat_id = {self.current_chat_id}'

    @staticmethod
    def scroll_history_container_to_end(container: VerticalScroll) -> None:
        if container.allow_vertical_scroll and container.children:
            container.scroll_end(animate=False)
