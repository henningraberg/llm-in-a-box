from typing import Optional

from .base import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.chat_message import ChatMessage


class Chat(BaseModel):
    __tablename__ = 'chat'

    name = Column(String(), nullable=False)
    default_model = Column(String(), nullable=False)

    messages = relationship('ChatMessage', back_populates='chat', cascade='all, delete-orphan')

    def __init__(self, name: str, default_model: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.default_model = default_model

    def get_chat_history(self) -> list[ChatMessage]:
        return ChatMessage.get_multiple(chat_id=self.id)

    def get_chat_history_as_dict(self) -> list[dict[str, str]]:
        return [m.to_dict() for m in self.get_chat_history()]

    def get_gui_id(self) -> str:
        return f'_{self.id}'

    def get_gui_id_with_hash_tag(self) -> str:
        return f'#{self.get_gui_id()}'
