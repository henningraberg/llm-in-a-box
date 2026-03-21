from models.chat import Chat
from models.chat_message import ChatMessage
from enums.enums import ChatRole


class TestChatInit:
    def test_creates_with_name(self, db_session):
        chat = Chat(name='my chat').save()
        assert chat.name == 'my chat'
        assert chat.default_model is None

    def test_creates_with_default_model(self, db_session):
        chat = Chat(name='my chat', default_model='llama3').save()
        assert chat.default_model == 'llama3'


class TestChatHistory:
    def test_returns_messages_for_chat(self, db_session):
        chat = Chat(name='test').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()
        ChatMessage(chat_id=chat.id, content='hi', role=ChatRole.ASSISTANT, model='llama3').save()

        assert len(chat.messages) == 2
        assert chat.messages[0].content == 'hello'
        assert chat.messages[1].content == 'hi'

    def test_returns_empty_for_no_messages(self, db_session):
        chat = Chat(name='empty').save()
        assert chat.messages == []

    def test_does_not_include_other_chat_messages(self, db_session):
        chat1 = Chat(name='chat1').save()
        chat2 = Chat(name='chat2').save()
        ChatMessage(chat_id=chat1.id, content='msg1', role=ChatRole.USER).save()
        ChatMessage(chat_id=chat2.id, content='msg2', role=ChatRole.USER).save()

        assert len(chat1.messages) == 1
        assert chat1.messages[0].content == 'msg1'

    def test_messages_are_ordered_by_created_at(self, db_session):
        chat = Chat(name='test').save()
        msg1 = ChatMessage(chat_id=chat.id, content='first', role=ChatRole.USER).save()
        msg2 = ChatMessage(chat_id=chat.id, content='second', role=ChatRole.ASSISTANT, model='llama3').save()
        msg3 = ChatMessage(chat_id=chat.id, content='third', role=ChatRole.USER).save()

        assert [m.id for m in chat.messages] == [msg1.id, msg2.id, msg3.id]


class TestChatGetChatHistoryAsDict:
    def test_returns_list_of_dicts(self, db_session):
        chat = Chat(name='test').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()

        result = chat.get_chat_history_as_dict()
        assert result == [{'role': 'user', 'content': 'hello'}]


class TestChatCascadeDelete:
    def test_deleting_chat_deletes_messages(self, db_session):
        chat = Chat(name='test').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()
        chat_id = chat.id

        chat.delete()
        assert ChatMessage.get_multiple(chat_id=chat_id) == []


class TestChatGuiId:
    def test_get_gui_id(self, db_session):
        chat = Chat(name='test').save()
        assert chat.get_gui_id() == f'_{chat.id}'

    def test_get_gui_id_with_hash_tag(self, db_session):
        chat = Chat(name='test').save()
        assert chat.get_gui_id_with_hash_tag() == f'#_{chat.id}'
