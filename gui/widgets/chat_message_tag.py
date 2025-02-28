from textual.app import ComposeResult
from textual.widgets import Label
from textual.containers import Container

from models.chat_message import ChatMessage


class ChatMessageTagContainer(Container):
    DEFAULT_CSS = """
        ChatMessageTagContainer{
            height: auto;
        }
    """

    def __init__(self, chat_message: ChatMessage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_message = chat_message

    def compose(self) -> ComposeResult:
        if self.chat_message.model:
            yield AiChatMessageTag(self.chat_message.model)
        else:
            self.styles.align_horizontal = 'right'
            yield UserChatMessageTag('You')


class UserChatMessageTag(Label):
    DEFAULT_CSS = """
    UserChatMessageTag{
        color: black;
        background: green 100%;
        text-style: bold;
    }
    """
    pass


class AiChatMessageTag(Label):
    DEFAULT_CSS = """
        AiChatMessageTag{
        color: black;
        background: green 100%;
        text-style: bold;
    }
    """
    pass
