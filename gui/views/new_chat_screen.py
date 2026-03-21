from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select
from textual.containers import Horizontal, Vertical, Container

from gui.widgets.llm_select import LLMSelect


class NewChatScreen(ModalScreen[str | None]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Label('Pick a model for your new chat')
            with Vertical():
                yield LLMSelect(id='llm-selection')
                with Horizontal():
                    yield Button('Abort', id='abort-button', variant='error')
                    yield Button('Create', id='create-button', variant='success', disabled=True)

    def on_select_changed(self, event: Select.Changed) -> None:
        self.query_one('#create-button', Button).disabled = event.value == Select.BLANK

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'create-button':
            self.dismiss(self.query_one('#llm-selection', LLMSelect).value)
        else:
            self.dismiss(None)
