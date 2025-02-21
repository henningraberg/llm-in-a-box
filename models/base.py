from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, DateTime, func
from database.db import db_engine as db


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

    def save(self):
        """Save model to database."""
        db.session.add(self)
        db.session.commit()
