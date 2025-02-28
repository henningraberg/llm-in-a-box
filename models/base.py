from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Query
from sqlalchemy import Column, Integer, DateTime, func

from database.db import session

from typing_extensions import Self


@as_declarative()
class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        """Convert model to dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def save(self) -> Self:
        """Save model to database."""
        if self not in session:
            session.add(self)
        session.commit()
        return self

    def delete(self) -> None:
        session.delete(self)
        session.commit()

    @classmethod
    def get_one(cls, **kwargs) -> Self:
        results = cls.query(**kwargs).all()

        assert not len(results) > 1, 'requested one, got multiple'

        assert not len(results) < 1, 'requested one, got none'

        return results[0]

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
