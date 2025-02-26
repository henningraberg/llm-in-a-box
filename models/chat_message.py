from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enums.enums import ChatRole

from .base import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = 'chat_message'

    chat_id = Column(Integer, ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)  # ForeignKey to link Chat

    content = Column(String(), nullable=False)
    model = Column(String(), nullable=False)
    role = Column(Enum(ChatRole), nullable=False)

    chat = relationship('Chat', back_populates='messages')

    def __init__(self, chat_id: int, content: str, model: str, role: ChatRole) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.content = content
        self.model = model
        self.role = role

    def to_dict(self) -> dict:
        return {'role': self.role.value, 'content': self.content}
