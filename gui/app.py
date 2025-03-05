from typing import Optional, Union

from textual.app import App

from database.db import session
from enums.enums import ChatRole
from gui.views.delete_chat_screen import DeleteChatScreen
from gui.views.main_view import MainView
from textual import on, work
from textual.worker import Worker
from textual.widgets import Button, Select
from textual.containers import VerticalScroll
from textual.binding import Binding

from gui.views.new_chat_screen import NewChatScreen
from gui.widgets.chat_list_item_button import ChatListItemButton
from gui.widgets.chat_message_area import ChatMessageArea
from gui.widgets.llm_select import LLMSelect
from integrations.ollama_manager import OllamaManager

from models.chat import Chat
from models.chat_message import ChatMessage


class TextualApp(App):
    """Main Textual application."""

    current_chat_id: Optional[int] = None
    response_worker: Optional[Worker] = None

    object_ids = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    BINDINGS = [Binding('ctrl+q', description='Exit application', action='quit')]

    CSS_PATH = 'static/styles.tcss'

    def on_mount(self) -> None:
        self.title = 'LLM IN A BOX'
        self.push_screen(MainView())
        ascii_art = '+----+\n| 🤖 |\n+----+'
        self.notify(ascii_art, title=f'Welcome to {self.title}!')

    @on(Button.Pressed, '#init-new-chat-button')
    def init_create_new_chat(self) -> None:
        self.push_screen(NewChatScreen())

    @on(Button.Pressed, '#abort-chat-creation-button')
    def abort_model_creation(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, '#abort-chat-deletion-button')
    def abort_chat_deletion(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, '#delete-chat-button')
    def delete_chat(self) -> None:
        self.app.pop_screen()

        self.abort_llm_response_if_needed()

        chat = Chat.get_one(id=self.current_chat_id)

        button_widget = self.query_one(chat.get_gui_id_with_hash_tag(), ChatListItemButton)
        button_widget.remove()

        chat.delete()
        chats = Chat.get_multiple()

        if len(chats) > 0:
            self.load_chat(chat_id=chats[-1].id)
        else:
            self.toggle_chat_view(disabled=True)
            self.set_current_chat(chat_id=None)

    @on(Button.Pressed, '#init-delete-chat-button')
    def init_delete_chat(self) -> None:
        self.push_screen(DeleteChatScreen())

    @on(Button.Pressed, '#create-new-chat-button')
    def create_chat(self) -> None:
        model_selection_widget = self.query_one('#llm-selection-1', LLMSelect)
        chat = Chat(default_model=model_selection_widget.value, name='New chat').save()

        self.app.pop_screen()

        self.abort_llm_response_if_needed()

        chat_list = self.query_one('#chat-list', VerticalScroll)

        chat_list.mount(
            ChatListItemButton(chat.name, id=chat.get_gui_id()),
            before=chat_list.children[0] if chat_list.children else None,
        )
        self.load_chat(chat_id=chat.id)

    @on(ChatListItemButton.Pressed)
    def init_chat(self, event: ChatListItemButton.Pressed) -> None:
        # todo: for some reason Button instances triggers this method. Fix this.
        if not isinstance(event.button, ChatListItemButton):
            return

        self.abort_llm_response_if_needed()
        chat_id = int(event.button.id.strip('_'))
        self.load_chat(chat_id)

    @on(Button.Pressed, '#abort-button')
    def abort_message(self) -> None:
        self.abort_llm_response_if_needed()
        self.load_chat(chat_id=self.current_chat_id)

    @on(LLMSelect.Changed, '#llm-selection-1')
    def select_model_for_new_chat(self, event: LLMSelect.Changed) -> None:
        if event.value != Select.BLANK:
            button = self.query_one('#create-new-chat-button', Button)
            button.disabled = False
        else:
            button = self.query_one('#create-new-chat-button', Button)
            button.disabled = True

    @on(LLMSelect.Changed, '#llm-selection-2')
    def select_model_for_existing_chat(self, event: LLMSelect.Changed) -> None:
        if event.value != Select.BLANK:
            chat = Chat.get_one(id=self.current_chat_id)
            chat.default_model = event.value
            chat.save()

    @on(Button.Pressed, '#send-button')
    def inti_send_message(self) -> None:
        """Initiate sending a message to the chat."""
        text_input = self.query_one('#message-input')
        content = text_input.text
        if content:
            self.send_message(content=content)
            text_input.text = ''
            abort_button = self.query_one('#abort-button')
            abort_button.disabled = False

    def abort_llm_response_if_needed(self) -> None:
        if self.response_worker and self.response_worker.is_running:
            session.rollback()
            self.response_worker.cancel()
            abort_button = self.query_one('#abort-button')
            abort_button.disabled = True

            send_button = self.query_one('#send-button')
            send_button.disabled = False

    def send_message(self, content: str) -> None:
        """Send a message to Ollama and handles the response."""
        chat = Chat.get_one(id=self.current_chat_id)

        chat_message = ChatMessage(chat_id=chat.id, content=content, role=ChatRole.USER).save()

        history_container = self.query_one('#chat-history-container', VerticalScroll)

        history_container.mount(ChatMessageArea(chat_message))

        dummy_chat_message = ChatMessage(chat_id=chat.id, role=ChatRole.ASSISTANT, content='', model=chat.default_model)
        ai_response = ChatMessageArea(dummy_chat_message)

        ai_response_text_area = ai_response.text_area
        ai_response_text_area.loading = True

        history_container.mount(ai_response)

        self.scroll_history_container_to_end(history_container)

        self.response_worker = self.generate_response(chat=chat, ai_response_text_area=ai_response_text_area)

    @work(thread=True)
    async def generate_response(self, chat: Chat, ai_response_text_area: ChatMessage) -> None:
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
        """Thread to generate chat name async."""
        try:
            ollama_manager = OllamaManager()

            chat.name = ollama_manager.generate_chat_name(chat)
            chat.save()

            button = self.query_one(chat.get_gui_id_with_hash_tag(), ChatListItemButton)
            button.label = chat.name

            button.refresh()
        except Exception:
            pass

    def load_chat(self, chat_id: int) -> None:
        """Load chat history and set the current chat."""
        self.set_current_chat(chat_id)

        history_container = self.query_one('#chat-history-container', VerticalScroll)

        if history_container.children:
            history_container.remove_children()

        chat = Chat.get_one(id=self.current_chat_id)

        llm_selector = self.query_one('#llm-selection-2', LLMSelect)
        llm_selector.value = chat.default_model

        self.set_current_chat(chat_id=chat.id)

        chat_history = chat.get_chat_history()

        history_container.mount(*[ChatMessageArea(message) for message in chat_history])

        self.scroll_history_container_to_end(history_container)

        self.toggle_chat_view(disabled=False)

    def toggle_chat_view(self, disabled: bool) -> None:
        """Toggle the disable attribute on chat view."""
        llm_selector = self.query_one('#llm-selection-2')
        llm_selector.disabled = disabled

        chat_history = self.query_one('#chat-history-container', VerticalScroll)
        chat_history.disabled = disabled

        message_input = self.query_one('#message-input')
        message_input.disabled = disabled
        message_input.text = ''

        send_button = self.query_one('#send-button')
        send_button.disabled = disabled

        delete_button = self.query_one('#init-delete-chat-button')
        delete_button.disabled = disabled

    def set_current_chat(self, chat_id: Union[int, None]) -> None:
        """Set the current chat."""
        previous_chat_id = self.current_chat_id
        self.current_chat_id = chat_id

        if previous_chat_id and self.current_chat_id:
            button = self.query_one(f'#_{previous_chat_id}', ChatListItemButton)
            button.styles.reset()
            button.refresh()

        if not self.current_chat_id:
            self.current_chat_id = None
            self.sub_title = ''

            if previous_chat_id:
                history_container = self.query_one('#chat-history-container', VerticalScroll)
                if history_container.children:
                    history_container.remove_children()

            return

        button = self.query_one(f'#_{self.current_chat_id}', ChatListItemButton)
        button.styles.border = ('ascii', 'green')
        self.sub_title = f'chat_id = {self.current_chat_id}'

    @staticmethod
    def scroll_history_container_to_end(container: VerticalScroll) -> None:
        if container.allow_vertical_scroll and container.children:
            container.scroll_end(animate=False)
