from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, TextArea

from gui.widgets.chat_history import ChatHistory
from gui.widgets.llm_selector import LLMSelector


class ChatViewContainer(Vertical):
    DEFAULT_CSS = """
    ChatViewContainer {
        width: 70%;
        dock: right;
        background: #161312 100%;
    }
    
    ChatViewContainer >  Horizontal {
        dock: bottom;
    }
    """

    def compose(self) -> ComposeResult:
        yield LLMSelector(id='llm-selection-in-chat')
        yield ChatHistory(id='chat-history')
        with Horizontal(id='input_box'):
            yield TextArea(id='message_input')
            yield Button(label='Send', variant='success', id='send_button')
