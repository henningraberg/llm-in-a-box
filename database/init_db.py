from database.db import db_engine
from models.base import BaseModel

# ruff: noqa: F401
from models.chat_message import ChatMessage
from models.chat import Chat
# ruff: noqa

# Create tables
BaseModel.metadata.create_all(db_engine)

print('✅ Database tables created successfully!')
