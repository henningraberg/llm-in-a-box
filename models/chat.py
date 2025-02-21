from .base import BaseModel
from sqlalchemy import Column, String


class Chat(BaseModel):
    __tablename__ = 'chat'

    name = Column(String(), nullable=False)
