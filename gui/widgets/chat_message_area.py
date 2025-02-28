from typing import Optional

from textual.app import ComposeResult

from gui.widgets.chat_message_tag import ChatMessageTagContainer
from gui.widgets.text_area import ChatMessageTextArea
from models.chat_message import ChatMessage
from textual.containers import Vertical


class ChatMessageArea(Vertical):
    DEFAULT_CSS = """
        ChatMessageArea{
            margin-top: 1;
            margin-right: 1;
            margin-left: 1;
            height: auto;
        }
    """
    text_area: Optional[ChatMessageTextArea] = None

    def __init__(self, chat_message: ChatMessage, **kwargs):
        super().__init__(**kwargs)
        self.chat_message = chat_message
        self.text_area = ChatMessageTextArea(self.chat_message.content)

    def compose(self) -> ComposeResult:
        yield ChatMessageTagContainer(self.chat_message)
        yield self.text_area
