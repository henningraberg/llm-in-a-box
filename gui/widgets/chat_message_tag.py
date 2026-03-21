from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label

from models.chat_message import ChatMessage


class ChatMessageTagContainer(Container):
    def __init__(self, chat_message: ChatMessage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_message = chat_message

    def compose(self) -> ComposeResult:
        if self.chat_message.model:
            yield AiChatMessageTag(self.chat_message.model)
        else:
            self.add_class('user-message')
            yield UserChatMessageTag('You')


class UserChatMessageTag(Label):
    pass


class AiChatMessageTag(Label):
    pass
