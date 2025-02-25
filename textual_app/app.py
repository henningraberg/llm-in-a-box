from textual.app import App
from textual_app.views.main_view import MainView
from textual import on
from textual.widgets import Button, Select
from textual.containers import VerticalScroll
from textual.binding import Binding

from textual_app.views.new_chat_screen import NewChatScreen
from textual_app.widgets.chat_history import ChatHistory
from textual_app.widgets.chat_item import ChatItem

from models.chat import Chat
from textual_app.widgets.chat_message import ChatMessage
from textual_app.widgets.llm_selector import LLMSelector


class TextualApp(App):
    """Main Textual application."""

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
        chat_list.mount(ChatItem(chat), before=chat_list.children[0])

    @on(Button.Pressed)
    def load_chat(self, event: Button.Pressed) -> None:
        if 'load-chat-button-' not in event.button.id:
            return

        history_container = self.query_one('#chat-history', ChatHistory)

        # clear out old messages
        for child in list(history_container.children):
            child.remove()

        chat_id = int(event.button.id.split('-')[-1])

        chat = Chat.get_one(id=chat_id)

        llm_selector = self.query_one('#llm-selection-in-chat', LLMSelector)
        llm_selector.value = chat.default_model

        self.sub_title = f'chat_id={chat.id}'
        chat_history = chat.get_chat_history()

        for message in chat_history:
            history_container.mount(ChatMessage(message.content))

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.select.id == 'new-chat-llm-selection':
            if event.value != Select.BLANK:
                button = self.query_one('#create-chat', Button)
                button.disabled = False
            else:
                button = self.query_one('#create-chat', Button)
                button.disabled = True
        # elif event.select.id == 'llm-selection-in-chat':
        #     if event.value != Select.BLANK:
        #         chat = chat
