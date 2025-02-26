from textual.containers import Vertical
from textual.widgets import Button
from textual.app import ComposeResult

from gui.widgets.chat_list import ChatList


class ChatListContainer(Vertical):
    def compose(self) -> ComposeResult:
        yield Button('Create new chat', id='init-new-chat-button', variant='success')
        yield ChatList(id='chat-list')
