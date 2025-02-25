from typing import Optional

from textual.widgets import Label

from enums.enums import ChatRole
from models.chat_message import ChatMessage as ChatMessageModel


class ChatMessage(Label):
    DEFAULT_CSS = """
        ChatMessage {
        }
    """

    def __init__(self, chat_message: Optional[ChatMessageModel] = None, *args, **kwargs):
        content = ''

        if chat_message:
            content = f'SENDER: {chat_message.role}'
            if chat_message.role == ChatRole.ASSISTANT:
                content += f' | MODEL: {chat_message.model}'
            content += f' | TIME: {chat_message.created_at} \n >>> {chat_message.content}'

        super().__init__(content, markup=False, *args, **kwargs)
