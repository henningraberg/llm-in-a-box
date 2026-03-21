from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Container


class DeleteChatScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Label('Are you sure?')
            with Horizontal():
                yield Button('Yes', id='confirm-button', variant='success')
                yield Button('No', id='cancel-button', variant='error')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == 'confirm-button')
