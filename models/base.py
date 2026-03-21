from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, Query
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy import DateTime, func

from database.db import session

from datetime import datetime
from typing import Self


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def save(self) -> Self:
        session.add(self)
        session.commit()
        return self

    def delete(self) -> None:
        session.delete(self)
        session.commit()

    @classmethod
    def one(cls, **kwargs) -> Self:
        result = cls.one_or_none(**kwargs)

        if result is None:
            raise LookupError('requested one, got none')

        return result

    @classmethod
    def one_or_none(cls, **kwargs) -> Self | None:
        try:
            return cls.query(**kwargs).one_or_none()
        except MultipleResultsFound:
            raise LookupError('requested one_or_none, got multiple')

    @classmethod
    def get_multiple(cls, **kwargs) -> list[Self]:
        return cls.query(**kwargs).order_by(cls.created_at).all()

    @classmethod
    def query(cls, **kwargs) -> Query:
        query = session.query(cls)
        for key, value in kwargs.items():
            if not hasattr(cls, key):
                raise ValueError(f'{cls.__name__} does not have attribute {key}')
            query = query.filter(getattr(cls, key) == value)
        return query.order_by(cls.created_at)
