import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import BaseModel


@pytest.fixture()
def db_session():
    """Create an in-memory SQLite database and session for testing."""
    engine = create_engine('sqlite://', echo=False)
    BaseModel.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    test_session = TestSession()

    with patch('models.base.session', test_session):
        yield test_session

    test_session.close()
    BaseModel.metadata.drop_all(engine)
    engine.dispose()
