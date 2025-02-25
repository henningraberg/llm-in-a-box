from textual.containers import Vertical
from textual.app import ComposeResult

from gui.widgets.chat_list import ChatList
from gui.widgets.chat_list_button import ChatListButton


class ChatListContainer(Vertical):
    DEFAULT_CSS = """
    ChatListContainer {
        width: 30%;
        dock: left;
        background: #161312 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChatListButton('Create new chat', id='create-new-chat-button', variant='success')
        yield ChatList(id='chat-list')
