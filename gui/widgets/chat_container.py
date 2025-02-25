from textual.app import ComposeResult
from textual.containers import Horizontal

from gui.widgets.chat_list_container import ChatListContainer
from gui.widgets.chat_view_container import ChatViewContainer


class ChatContainer(Horizontal):
    DEFAULT_CSS = """
    ChatContainer {
        width: 1fr;
        height: 1fr;
        border: ascii green;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChatListContainer()
        yield ChatViewContainer()
