from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enums.enums import ChatRole

from .base import BaseModel


class ChatMessage(BaseModel):
    __tablename__ = 'chat_message'

    message = Column(String(), nullable=False)
    model = Column(String(), nullable=False)
    role = Column(Enum(ChatRole), nullable=False)

    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)  # ForeignKey to link Chat
    chat = relationship('Chat', back_populates='chat_message')  # Define relationship to Chat
