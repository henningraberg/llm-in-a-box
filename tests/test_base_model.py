import pytest

from models.chat import Chat


class TestBaseModelSave:
    def test_save_persists_record(self, db_session):
        chat = Chat(name='test').save()
        assert chat.id is not None
        assert db_session.get(Chat, chat.id) is not None

    def test_save_returns_self(self, db_session):
        chat = Chat(name='test')
        result = chat.save()
        assert result is chat


class TestBaseModelDelete:
    def test_delete_removes_record(self, db_session):
        chat = Chat(name='test').save()
        chat_id = chat.id
        chat.delete()
        assert db_session.get(Chat, chat_id) is None


class TestBaseModelToDict:
    def test_to_dict_contains_columns(self, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        d = chat.to_dict()
        assert d['name'] == 'test'
        assert d['default_model'] == 'llama3'
        assert 'id' in d
        assert 'created_at' in d
        assert 'updated_at' in d


class TestBaseModelOne:
    def test_one_returns_matching_record(self, db_session):
        chat = Chat(name='test').save()
        result = Chat.one(id=chat.id)
        assert result.id == chat.id

    def test_one_raises_on_none(self, db_session):
        with pytest.raises(LookupError, match='got none'):
            Chat.one(id=999)

    def test_one_raises_on_multiple(self, db_session):
        Chat(name='dup').save()
        Chat(name='dup').save()
        with pytest.raises(LookupError, match='got multiple'):
            Chat.one(name='dup')


class TestBaseModelOneOrNone:
    def test_one_or_none_returns_record(self, db_session):
        chat = Chat(name='test').save()
        result = Chat.one_or_none(id=chat.id)
        assert result is not None
        assert result.id == chat.id

    def test_one_or_none_returns_none(self, db_session):
        result = Chat.one_or_none(id=999)
        assert result is None

    def test_one_or_none_raises_on_multiple(self, db_session):
        Chat(name='dup').save()
        Chat(name='dup').save()
        with pytest.raises(LookupError, match='got multiple'):
            Chat.one_or_none(name='dup')


class TestBaseModelGetMultiple:
    def test_get_multiple_returns_all_matching(self, db_session):
        Chat(name='a').save()
        Chat(name='a').save()
        Chat(name='b').save()
        results = Chat.get_multiple(name='a')
        assert len(results) == 2

    def test_get_multiple_returns_empty_list(self, db_session):
        results = Chat.get_multiple(name='nonexistent')
        assert results == []


class TestBaseModelQuery:
    def test_query_filters_by_kwargs(self, db_session):
        Chat(name='target').save()
        Chat(name='other').save()
        results = Chat.query(name='target').all()
        assert len(results) == 1
        assert results[0].name == 'target'

    def test_query_raises_on_invalid_attribute(self, db_session):
        with pytest.raises(ValueError, match='does not have attribute'):
            Chat.query(nonexistent='value')
