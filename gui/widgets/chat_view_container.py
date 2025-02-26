from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, TextArea

from gui.widgets.chat_history import ChatHistory
from gui.widgets.llm_select import LLMSelect


class ChatViewContainer(Vertical):
    def compose(self) -> ComposeResult:
        disabled = not bool(getattr(self.app, 'current_chat_id'))
        with Horizontal(id='chat-view-header'):
            yield LLMSelect(id='llm-selection-2', disabled=disabled)
            yield Button(label='Delete chat', id='init-delete-chat-button', disabled=disabled, variant='error')
        yield ChatHistory(id='chat-history', disabled=disabled)
        with Horizontal(id='input-box'):
            yield TextArea(id='message-input', disabled=disabled, show_line_numbers=True)
            with Vertical(id='input-buttons-box'):
                yield Button(label='Send', variant='success', id='send-button', disabled=disabled)
                yield Button(label='Abort', variant='error', id='abort-button', disabled=disabled)
