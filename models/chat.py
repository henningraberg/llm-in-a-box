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

    def get_chat_history(self) -> list[ChatMessage]:
        return ChatMessage.get_multiple(chat_id=self.id)

    def get_chat_history_as_dict(self) -> list[dict[str, str]]:
        return [m.to_dict() for m in self.get_chat_history()]
