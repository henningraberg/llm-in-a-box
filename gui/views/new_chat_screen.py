from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical, Container

from gui.widgets.llm_select import LLMSelect


class NewChatScreen(ModalScreen):
    DEFAULT_CSS = """
        NewChatScreen {
        align: center middle;
    }

    NewChatScreen > Container {
        width: auto;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }

    NewChatScreen > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }
    
    NewChatScreen > Container > Vertical {
        width: auto;
        height: auto;
    }
    
    NewChatScreen > Container > Vertical > Horizontal {
        width: auto;
        height: auto;
    }
    
    NewChatScreen > Container > Vertical > LLMSelect {
        width: 100%;
        margin-top: 2; 
    }
    
    NewChatScreen > Container > Vertical > Horizontal > Button {
        margin: 2 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield Label('Pick a model for your new chat')
            with Vertical():
                yield LLMSelect(id='llm-selection-1')
                with Horizontal():
                    yield Button('Abort', id='abort-chat-creation-button', variant='error')
                    yield Button('Create', id='create-new-chat-button', variant='success', disabled=True)
