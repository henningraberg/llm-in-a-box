from textual.containers import VerticalScroll
from textual.app import ComposeResult

from gui.widgets.chat_list_item_button import ChatListItemButton

from models.chat import Chat


class ChatList(VerticalScroll):
    def compose(self) -> ComposeResult:
        chats = Chat.get_multiple()
        # reverse so the newest gets on top
        chats.reverse()
        for chat in chats:
            yield ChatListItemButton(chat.name, id=chat.get_gui_id())
