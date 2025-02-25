from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, TextArea

from gui.widgets.chat_history import ChatHistory
from gui.widgets.llm_selector import LLMSelector


class ChatViewContainer(Vertical):
    def compose(self) -> ComposeResult:
        disabled = not bool(self.app.sub_title)
        yield LLMSelector(id='llm-selection-in-chat', disabled=disabled)
        yield ChatHistory(id='chat-history', disabled=disabled)
        with Horizontal(id='input-box'):
            yield TextArea(id='message-input', disabled=disabled, show_line_numbers=True)
            with Vertical(id='input-buttons-box'):
                yield Button(label='Send', variant='success', id='send-button', disabled=disabled)
                yield Button(label='Abort', variant='error', id='abort-button', disabled=disabled)
