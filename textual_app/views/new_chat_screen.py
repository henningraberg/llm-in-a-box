from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical, Container

from textual_app.widgets.llm_selector import LLMSelector


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
    
    NewChatScreen > Container > Vertical > LLMSelector {
        width: 100%;
    }
    
    NewChatScreen > Container > Vertical > Horizontal > Button {
        margin: 2 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield Label('Pick a model for your new chat')
            with Vertical():
                yield LLMSelector(id='new-chat-llm-selection')
                with Horizontal():
                    yield Button('Abort', id='abort-chat-creation', variant='error')
                    yield Button('Create', id='create-chat', variant='success', disabled=True)
