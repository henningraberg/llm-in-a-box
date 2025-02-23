from .base import BaseModel
from sqlalchemy import Column, String

from models.chat_message import ChatMessage


class Chat(BaseModel):
    __tablename__ = 'chat'

    name = Column(String(), nullable=False)
    default_model = Column(String(), nullable=False)  # Default model set on the chat

    def __init__(self, name: str, default_model: str) -> None:
        super().__init__()
        self.name = name
        self.default_model = default_model

    @classmethod
    def get_chat_history(cls) -> list[ChatMessage]:
        return ChatMessage.get_multiple(chat_id=cls.id)

    @classmethod
    def get_chat_history_as_dict(cls) -> list[dict[str, str]]:
        return [m.to_dict() for m in cls.get_chat_history()]
