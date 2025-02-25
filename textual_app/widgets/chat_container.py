from textual.app import ComposeResult
from textual.containers import Horizontal

from textual_app.widgets.chat_list_container import ChatListContainer
from textual_app.widgets.chat_view_container import ChatViewContainer


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
