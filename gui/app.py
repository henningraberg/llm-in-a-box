from typing import Optional, Union

from textual.app import App

from enums.enums import ChatRole
from gui.views.delete_chat_screen import DeleteChatScreen
from gui.views.main_view import MainView
from textual import on, work
from textual.worker import Worker
from textual.widgets import Button, Select
from textual.containers import VerticalScroll
from textual.binding import Binding
from textual.reactive import Reactive

from gui.views.new_chat_screen import NewChatScreen
from gui.widgets.chat_history import ChatHistory
from gui.widgets.chat_list_item_button import ChatListItemButton
from gui.widgets.llm_select import LLMSelect
from integrations.ollama_manager import OllamaManager

from models.chat import Chat
from models.chat_message import ChatMessage
from gui.widgets.chat_message_text_area import ChatMessageTextArea


class TextualApp(App):
    """Main Textual application."""

    current_chat_id: Optional[int] = None
    response_worker: Worker | None = None

    object_ids = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    BINDINGS = [
        Binding('q', 'quit', 'Quit', key_display='ctrl+q'),
    ]
    CSS_PATH = 'static/styles.tcss'

    def on_mount(self) -> None:
        self.title = 'LLM IN A BOX'
        self.push_screen(MainView())

    @on(Button.Pressed, '#init-new-chat-button')
    def create_new_model(self) -> None:
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

        chat_list = self.query_one('#chat-list', VerticalScroll)

        chat_list.mount(
            ChatListItemButton(chat.name, id=chat.get_gui_id()),
            before=chat_list.children[0] if chat_list.children else None,
        )
        self.load_chat(chat_id=chat.id)

    @on(ChatListItemButton.Pressed)
    def init_chat(self, event: ChatListItemButton.Pressed) -> None:
        if type(event.button) is not ChatListItemButton:
            return

        self.abort_request_if_needed()
        chat_id = int(event.button.id.strip('_'))
        self.load_chat(chat_id)

    @on(Button.Pressed, '#abort-button')
    def abort_message(self) -> None:
        self.abort_request_if_needed()
        self.load_chat(chat_id=self.current_chat_id)

    def abort_request_if_needed(self) -> None:
        if self.response_worker and self.response_worker.is_running:
            self.response_worker.cancel()

            abort_button = self.query_one('#abort-button')
            abort_button.disabled = True

            send_button = self.query_one('#send-button')
            send_button.disabled = False

    @on(Button.Pressed, '#send-button')
    def inti_send_message(self) -> None:
        text_input = self.query_one('#message-input')
        content = text_input.text
        if content:
            self.send_message(content=content)
            text_input.text = ''
            abort_button = self.query_one('#abort-button')
            abort_button.disabled = False

    def send_message(self, content: str) -> None:
        chat = Chat.get_one(id=self.current_chat_id)

        if not chat.get_chat_history():
            max_length = 30
            if len(content) > max_length:
                chat_name = content[:max_length] + '...'
            else:
                chat_name = content
            chat.name = chat_name.replace('\n', ' ')
            chat.save()
            chat_button = self.query_one(chat.get_gui_id_with_hash_tag(), ChatListItemButton)
            chat_button.label = chat.name

        chat_message = ChatMessage(
            chat_id=chat.id, content=content, model=chat.default_model, role=ChatRole.USER
        ).save()

        history_container = self.query_one('#chat-history', ChatHistory)

        history_container.mount(ChatMessageTextArea(chat_message.content))

        ai_response_widget = ChatMessageTextArea()
        ai_response_widget.loading = True

        history_container.mount(ai_response_widget)

        history_container.action_scroll_end()

        self.response_worker = self.generate_response(chat=chat, ai_response_widget=ai_response_widget)

    @work(thread=True)
    async def generate_response(self, chat: Chat, ai_response_widget: ChatMessage) -> None:
        """Generate the AI response asynchronously and update widget dynamically."""

        send_button = self.query_one('#send-button')
        abort_button = self.query_one('#abort-button')
        send_button.disabled = True

        for word in OllamaManager().chat(chat):
            ai_response_widget.loading = False
            ai_response_widget.text += word
            history_container = self.query_one('#chat-history', ChatHistory)
            history_container.action_scroll_end()

        abort_button.disabled = True
        send_button.disabled = False

    def load_chat(self, chat_id: int) -> None:
        self.set_current_chat(chat_id)

        history_container = self.query_one('#chat-history', ChatHistory)

        # clear out old messages
        for child in list(history_container.children):
            child.remove()

        chat = Chat.get_one(id=self.current_chat_id)

        llm_selector = self.query_one('#llm-selection-2', LLMSelect)
        llm_selector.value = chat.default_model

        self.sub_title = f'chat_id={chat.id}'
        chat_history = chat.get_chat_history()

        for message in chat_history:
            history_container.mount(ChatMessageTextArea(message.content))

        self.toggle_chat_view(disabled=False)

    def toggle_chat_view(self, disabled: bool) -> None:
        llm_selector = self.query_one('#llm-selection-2')
        llm_selector.disabled = disabled

        chat_history = self.query_one('#chat-history')
        chat_history.disabled = disabled
        chat_history.action_scroll_end()

        message_input = self.query_one('#message-input')
        message_input.disabled = disabled
        message_input.text = ''

        send_button = self.query_one('#send-button')
        send_button.disabled = disabled

        delete_button = self.query_one('#init-delete-chat-button')
        delete_button.disabled = disabled

    def set_current_chat(self, chat_id: Union[int | None]) -> None:
        self.current_chat_id = chat_id
        self.sub_title = Reactive(f'chat_id = {self.current_chat_id}')

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
