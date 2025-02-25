from textual.app import ComposeResult
from textual.containers import Horizontal

from gui.widgets.chat_list_container import ChatListContainer
from gui.widgets.chat_view_container import ChatViewContainer


class ChatContainer(Horizontal):
    def compose(self) -> ComposeResult:
        yield ChatListContainer(id='chat-list-container')
        yield ChatViewContainer(id='chat-view-container')
