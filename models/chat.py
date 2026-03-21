from typing import Optional

from .base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Chat(BaseModel):
    name: Mapped[str] = mapped_column(String(), nullable=False)
    default_model: Mapped[Optional[str]] = mapped_column(default=None)

    messages = relationship('ChatMessage', back_populates='chat', cascade='all, delete-orphan', order_by='ChatMessage.created_at')

    def __init__(self, name: str, default_model: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.default_model = default_model

    def get_chat_history_as_dict(self) -> list[dict[str, str]]:
        return [m.to_dict() for m in self.messages]

    def get_gui_id(self) -> str:
        return f'_{self.id}'

    def get_gui_id_with_hash_tag(self) -> str:
        return f'#{self.get_gui_id()}'
