from .db import db_engine
from models.base import BaseModel

# ruff: noqa: F401
from models.chat_message import ChatMessage
from models.chat import Chat
# ruff: noqa


def clean_db() -> None:
    # Drop all tables
    BaseModel.metadata.drop_all(bind=db_engine)
