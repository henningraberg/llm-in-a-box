from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Container


class DeleteChatScreen(ModalScreen):
    DEFAULT_CSS = """
        DeleteChatScreen {
        align: center middle;
    }

    DeleteChatScreen > Container {
        width: auto;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }

    DeleteChatScreen > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }

    DeleteChatScreen > Container > Horizontal {
        width: auto;
        height: auto;
    }

    DeleteChatScreen > Container > Horizontal > Button {
        margin: 2 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Container():
            yield Label('Are you sure?')
            with Horizontal():
                yield Button('Yes', id='delete-chat-button', variant='success')
                yield Button('No', id='abort-chat-deletion-button', variant='error')
