from textual.containers import VerticalScroll
from textual.app import ComposeResult

from textual_app.widgets.chat_item import ChatItem

from models.chat import Chat


class ChatList(VerticalScroll):
    DEFAULT_CSS = """
        ChatList {
            width: 100%;
            scrollbar-background: #343a40 100%;
            scrollbar-color: green;
            scrollbar-background-hover: #343a40 100%;
            scrollbar-color-active: green;
            scrollbar-color-hover: green;
        }
    """

    def compose(self) -> ComposeResult:
        chats = Chat.get_multiple()
        # reverse so the newest gets on top
        chats.reverse()
        for chat in chats:
            yield ChatItem(chat)
