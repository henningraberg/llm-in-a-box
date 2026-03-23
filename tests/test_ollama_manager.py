from unittest.mock import patch, MagicMock

import pytest

from enums.enums import ChatRole
from integrations.ollama_manager import OllamaManager
from models.chat import Chat
from models.chat_message import ChatMessage


class TestGetDownloadedModels:
    @patch('integrations.ollama_manager.ollama.list')
    def test_returns_list_response(self, mock_list):
        mock_list.return_value = MagicMock(models=[])
        result = OllamaManager.get_downloaded_models()
        mock_list.assert_called_once()
        assert result.models == []

    @patch('integrations.ollama_manager.ollama.list')
    def test_returns_models(self, mock_list):
        model = MagicMock(model='llama3')
        mock_list.return_value = MagicMock(models=[model])
        result = OllamaManager.get_downloaded_models()
        assert len(result.models) == 1


class TestGetModelInformation:
    @patch('integrations.ollama_manager.ollama.show')
    def test_calls_show_with_model(self, mock_show):
        mock_show.return_value = MagicMock()
        OllamaManager.get_model_information('llama3')
        mock_show.assert_called_once_with(model='llama3')


class TestDownloadModel:
    @patch('integrations.ollama_manager.ollama.pull')
    def test_yields_progress(self, mock_pull):
        mock_pull.return_value = iter([{'status': 'downloading'}, {'status': 'done'}])
        results = list(OllamaManager.download_model(model='llama3'))
        mock_pull.assert_called_once_with(model='llama3', stream=True)
        assert results == [{'status': 'downloading'}, {'status': 'done'}]

    @patch('integrations.ollama_manager.ollama.pull')
    def test_with_no_model(self, mock_pull):
        mock_pull.return_value = iter([])
        list(OllamaManager.download_model())
        mock_pull.assert_called_once_with(model=None, stream=True)


class TestDeleteModel:
    @patch('integrations.ollama_manager.ollama.delete')
    def test_calls_delete_with_model(self, mock_delete):
        mock_delete.return_value = MagicMock(status='success')
        result = OllamaManager.delete_model('llama3')
        mock_delete.assert_called_once_with(model='llama3')
        assert result.status == 'success'


class TestChat:
    @patch('integrations.ollama_manager.ollama.chat')
    def test_streams_response(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()

        chunk1 = MagicMock()
        chunk1.message.content = 'Hello'
        chunk2 = MagicMock()
        chunk2.message.content = ' world'
        mock_chat.return_value = iter([chunk1, chunk2])

        results = list(OllamaManager.chat(chat_id=chat.id, content='Hi', model=None))

        assert results == ['Hello', ' world']
        mock_chat.assert_called_once()

    @patch('integrations.ollama_manager.ollama.chat')
    def test_saves_user_message(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        mock_chat.return_value = iter([])

        list(OllamaManager.chat(chat_id=chat.id, content='Hi'))

        user_messages = [m for m in chat.messages if m.role == ChatRole.USER]
        assert len(user_messages) == 1
        assert user_messages[0].content == 'Hi'

    @patch('integrations.ollama_manager.ollama.chat')
    def test_saves_assistant_message(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()

        chunk = MagicMock()
        chunk.message.content = 'response'
        mock_chat.return_value = iter([chunk])

        list(OllamaManager.chat(chat_id=chat.id, content='Hi'))

        assistant_messages = [m for m in chat.messages if m.role == ChatRole.ASSISTANT]
        assert len(assistant_messages) == 1
        assert assistant_messages[0].content == 'response'

    @patch('integrations.ollama_manager.ollama.chat')
    def test_updates_model_when_provided(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        mock_chat.return_value = iter([])

        list(OllamaManager.chat(chat_id=chat.id, content='Hi', model='mistral'))

        db_session.refresh(chat)
        assert chat.default_model == 'mistral'

    @patch('integrations.ollama_manager.ollama.chat')
    def test_includes_history_in_messages(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        ChatMessage(chat_id=chat.id, content='old msg', role=ChatRole.USER).save()
        ChatMessage(chat_id=chat.id, content='old reply', role=ChatRole.ASSISTANT, model='llama3').save()

        mock_chat.return_value = iter([])

        list(OllamaManager.chat(chat_id=chat.id, content='new msg'))

        call_kwargs = mock_chat.call_args
        messages = call_kwargs.kwargs['messages']
        assert len(messages) == 3
        assert messages[0] == {'role': 'user', 'content': 'old msg'}
        assert messages[1] == {'role': 'assistant', 'content': 'old reply'}
        assert messages[2] == {'role': 'user', 'content': 'new msg'}


class TestChatGui:
    @patch('integrations.ollama_manager.ollama.chat')
    def test_streams_and_saves_response(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()

        chunk1 = MagicMock()
        chunk1.message.content = 'Hi'
        chunk2 = MagicMock()
        chunk2.message.content = ' there'
        mock_chat.return_value = iter([chunk1, chunk2])

        results = list(OllamaManager.chat_gui(chat=chat))

        assert results == ['Hi', ' there']

    @patch('integrations.ollama_manager.ollama.chat')
    def test_saves_accumulated_content(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()

        chunk1 = MagicMock()
        chunk1.message.content = 'Hi'
        chunk2 = MagicMock()
        chunk2.message.content = ' there'
        mock_chat.return_value = iter([chunk1, chunk2])

        list(OllamaManager.chat_gui(chat=chat))

        assistant_messages = [m for m in chat.messages if m.role == ChatRole.ASSISTANT]
        assert len(assistant_messages) == 1
        assert assistant_messages[0].content == 'Hi there'


class TestGenerateChatName:
    @patch('integrations.ollama_manager.ollama.chat')
    def test_returns_generated_name(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()
        ChatMessage(chat_id=chat.id, content='hi there', role=ChatRole.ASSISTANT, model='llama3').save()

        mock_response = MagicMock()
        mock_response.message.content = 'Greeting Chat'
        mock_chat.return_value = mock_response

        result = OllamaManager.generate_chat_name(chat=chat)

        assert result == 'Greeting Chat'

    @patch('integrations.ollama_manager.ollama.chat')
    def test_includes_naming_prompt(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='llama3').save()
        ChatMessage(chat_id=chat.id, content='hello', role=ChatRole.USER).save()

        mock_response = MagicMock()
        mock_response.message.content = 'Chat Name'
        mock_chat.return_value = mock_response

        OllamaManager.generate_chat_name(chat=chat)

        call_kwargs = mock_chat.call_args
        messages = call_kwargs.kwargs['messages']
        last_message = messages[-1]
        assert last_message['role'] == 'user'
        assert 'generate a name for this chat' in last_message['content'].lower()

    @patch('integrations.ollama_manager.ollama.chat')
    def test_uses_chat_default_model(self, mock_chat, db_session):
        chat = Chat(name='test', default_model='mistral').save()

        mock_response = MagicMock()
        mock_response.message.content = 'Name'
        mock_chat.return_value = mock_response

        OllamaManager.generate_chat_name(chat=chat)

        mock_chat.assert_called_once_with(
            messages=pytest.approx(mock_chat.call_args.kwargs['messages']), model='mistral'
        )
