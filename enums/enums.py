from enum import Enum


class ChatRole(Enum):
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'

    def is_system(self) -> bool:
        return self == ChatRole.SYSTEM

    def is_assistant(self) -> bool:
        return self == ChatRole.ASSISTANT

    def is_user(self) -> bool:
        return self == ChatRole.USER
