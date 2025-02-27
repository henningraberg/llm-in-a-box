from typing import Generator, Optional

import ollama

from models.chat import Chat
from models.chat_message import ChatMessage

from enums.enums import ChatRole


class OllamaManager:
    def __init__(self):
        pass

    @staticmethod
    def get_installed_models() -> ollama.ListResponse:
        return ollama.list()

    @staticmethod
    def get_model_information(model: str) -> ollama.ShowResponse:
        return ollama.show(name=model)

    @staticmethod
    def install_model(model: Optional[str] = None) -> Generator:
        for x in ollama.pull(name=model, stream=True):
            yield x

    @staticmethod
    def delete_model(model: str) -> ollama.StatusResponse:
        return ollama.delete(name=model)

    @staticmethod
    def create_message_and_chat(chat_id: int, content: str, model: Optional[str] = None) -> Generator:
        chat = Chat.get_one(id=chat_id)

        if model:
            chat.default_model = model
            chat.save()

        message_history = chat.get_chat_history_as_dict()

        new_message = ChatMessage(chat_id=chat.id, role=ChatRole.USER, model=chat.default_model, content=content).save()

        message_history.append(new_message.to_dict())

        ai_response = ''
        for chunked_response in ollama.chat(messages=message_history, stream=True, model=chat.default_model):
            ai_response += chunked_response.message.content
            yield chunked_response.message.content

        ChatMessage(chat_id=chat.id, role=ChatRole.ASSISTANT, model=chat.default_model, content=ai_response).save()

    @staticmethod
    def chat(chat: Chat) -> Generator:
        message_history = chat.get_chat_history_as_dict()
        ai_response = ChatMessage(chat_id=chat.id, role=ChatRole.ASSISTANT, model=chat.default_model, content='')
        for chunked_response in ollama.chat(messages=message_history, stream=True, model=chat.default_model):
            ai_response.content += chunked_response.message.content
            ai_response.save()
            yield chunked_response.message.content

    @staticmethod
    def generate_chat_name(chat: Chat) -> str:
        message_history = chat.get_chat_history_as_dict()
        message_history.append(
            ChatMessage(
                chat_id=chat.id,
                role=ChatRole.USER,
                model=chat.default_model,
                content='With 30 letters or less, give this chat history a name. Give only the name as a result.'
                'Don\'t include any ",',
            ).to_dict()
        )
        return ollama.chat(messages=message_history, model=chat.default_model).message.content
