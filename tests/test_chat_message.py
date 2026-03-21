import pytest

from models.chat import Chat
from models.chat_message import ChatMessage
from enums.enums import ChatRole


class TestChatMessageInit:
    def test_creates_user_message(self, db_session):
        chat = Chat(name='test').save()
        msg = ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()
        assert msg.content == 'hello'
        assert msg.role == ChatRole.USER
        assert msg.model is None
        assert msg.chat_id == chat.id

    def test_creates_assistant_message_with_model(self, db_session):
        chat = Chat(name='test').save()
        msg = ChatMessage(chat_id=chat.id, content='hi', role=ChatRole.ASSISTANT, model='llama3').save()
        assert msg.role == ChatRole.ASSISTANT
        assert msg.model == 'llama3'

    def test_assistant_message_requires_model(self, db_session):
        chat = Chat(name='test').save()
        with pytest.raises(AssertionError):
            ChatMessage(chat_id=chat.id, content='hi', role=ChatRole.ASSISTANT)

    def test_creates_system_message(self, db_session):
        chat = Chat(name='test').save()
        msg = ChatMessage(chat_id=chat.id, content='you are helpful', role=ChatRole.SYSTEM).save()
        assert msg.role == ChatRole.SYSTEM


class TestChatMessageToDict:
    def test_to_dict_returns_role_and_content(self, db_session):
        chat = Chat(name='test').save()
        msg = ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()
        assert msg.to_dict() == {'role': 'user', 'content': 'hello'}

    def test_to_dict_assistant(self, db_session):
        chat = Chat(name='test').save()
        msg = ChatMessage(chat_id=chat.id, content='hi', role=ChatRole.ASSISTANT, model='llama3').save()
        assert msg.to_dict() == {'role': 'assistant', 'content': 'hi'}


class TestChatMessageTablename:
    def test_tablename_is_chat_message(self, db_session):
        assert ChatMessage.__tablename__ == 'chat_message'
