from typing import Optional

from textual.app import App

from enums.enums import ChatRole
from gui.views.main_view import MainView
from textual import on, work
from textual.widgets import Button, Select
from textual.containers import VerticalScroll
from textual.binding import Binding
from textual.reactive import Reactive

from gui.views.new_chat_screen import NewChatScreen
from gui.widgets.chat_history import ChatHistory
from gui.widgets.chat_item import ChatItem
from integrations.ollama_manager import OllamaManager

from models.chat import Chat
from models.chat_message import ChatMessage as ChatMessageModel
from gui.widgets.chat_message import ChatMessage
from gui.widgets.llm_selector import LLMSelector


class TextualApp(App):
    """Main Textual application."""

    current_chat_id: Optional[int] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    BINDINGS = [  # 🆕
        Binding('q', 'quit', 'Quit', key_display='ctrl+q'),
    ]
    CSS_PATH = 'static/styles.tcss'

    def on_mount(self) -> None:
        self.title = 'LLM IN A BOX'
        self.push_screen(MainView())

    @on(Button.Pressed, '#create-new-chat-button')
    def create_new_model(self) -> None:
        self.push_screen(NewChatScreen())

    @on(Button.Pressed, '#no')
    def back_to_app(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, '#abort-chat-creation')
    def abort_model_creation(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, '#create-chat')
    def create_chat(self) -> None:
        model_selection_widget = self.query_one('#new-chat-llm-selection', Select)
        chat = Chat(default_model=model_selection_widget.value, name='New chat').save()
        self.app.pop_screen()

        chat_list = self.query_one('#chat-list', VerticalScroll)
        # Update chat list by adding the new chat to the top.
        chat_list.mount(ChatItem(chat), before=chat_list.children[0] if chat_list.children else None)

        self.load_chat(chat_id=chat.id)

    @on(Button.Pressed)
    def button_pressed(self, event: Button.Pressed) -> None:
        if 'load-chat-button-' in event.button.id:
            chat_id = int(event.button.id.split('-')[-1])
            self.load_chat(chat_id=chat_id)
            return

        if 'send-button' == event.button.id:
            text_input = self.query_one('#message-input')
            content = text_input.text
            if content:
                self.send_message(content=content)
                text_input.text = ''

    def send_message(self, content: str) -> None:
        manager = OllamaManager()
        chat = Chat.get_one(id=self.current_chat_id)

        if not chat.get_chat_history():
            max_length = 30
            if len(content) > max_length:
                chat_name = content[:max_length] + '...'
            else:
                chat_name = content
            chat.name = chat_name.replace('\n', ' ')
            chat.save()
            chat_button = self.query_one(f'#load-chat-button-{chat.id}')
            chat_button.label = chat.name

        # Create and save the user message
        chat_message = ChatMessageModel(
            chat_id=chat.id, content=content, model=chat.default_model, role=ChatRole.USER
        ).save()

        history_container = self.query_one('#chat-history', ChatHistory)

        # Mount the user's message immediately
        history_container.mount(ChatMessage(chat_message=chat_message))

        # Create the AI message widget
        new_ai_message_widget = ChatMessage()

        # Mount the AI widget safely from the main thread
        history_container.mount(new_ai_message_widget)

        history_container.action_scroll_end()

        # Start background task to fetch AI response
        self.generate_response(
            manager=manager,
            content=content,
            chat=chat,
            widget=new_ai_message_widget,
        )

    @work(thread=True)
    async def generate_response(
        self, manager: OllamaManager, content: str, chat: ChatMessageModel, widget: ChatMessage
    ):
        """Generate the AI response asynchronously and update widget dynamically."""
        widget_content = ''

        for word in manager.chat(content=content, chat_id=chat.id, model=chat.default_model):
            widget_content += word
            widget.update(widget_content)
            history_container = self.query_one('#chat-history', ChatHistory)
            history_container.action_scroll_end()

    def load_chat(self, chat_id: int) -> None:
        self.set_current_chat(chat_id)

        history_container = self.query_one('#chat-history', ChatHistory)

        # clear out old messages
        for child in list(history_container.children):
            child.remove()

        chat = Chat.get_one(id=self.current_chat_id)

        llm_selector = self.query_one('#llm-selection-in-chat', LLMSelector)
        llm_selector.value = chat.default_model

        self.sub_title = f'chat_id={chat.id}'
        chat_history = chat.get_chat_history()

        for message in chat_history:
            history_container.mount(ChatMessage(chat_message=message))

        self.enable_chat_view()

    def enable_chat_view(self) -> None:
        llm_selector = self.query_one('#llm-selection-in-chat')
        llm_selector.disabled = False

        chat_history = self.query_one('#chat-history')
        chat_history.disabled = False
        chat_history.action_scroll_end()

        message_input = self.query_one('#message-input')
        message_input.disabled = False
        message_input.text = ''

        send_button = self.query_one('#send-button')
        send_button.disabled = False

    def set_current_chat(self, chat_id: int):
        self.current_chat_id = chat_id
        self.sub_title = Reactive(f'chat_id = {self.current_chat_id}')

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.select.id == 'new-chat-llm-selection':
            if event.value != Select.BLANK:
                button = self.query_one('#create-chat', Button)
                button.disabled = False
            else:
                button = self.query_one('#create-chat', Button)
                button.disabled = True
        elif event.select.id == 'llm-selection-in-chat':
            if event.value != Select.BLANK:
                chat = Chat.get_one(id=self.current_chat_id)
                chat.default_model = event.value
                chat.save()
