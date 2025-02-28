from textual.widgets import TextArea
from textual.binding import Binding

import pyperclip


class TextAreaWithBinding(TextArea):
    BINDINGS = [
        Binding('ctrl+c', action='copy_selection', description='Copy selection'),
        Binding('ctrl+a', action='select_all', description='Select all text'),
        Binding('ctrl+q', description='Exit application', action='quit'),
    ]

    def action_copy_selection(self):
        """Copy to the clipboard of the machine the app is running on"""
        text_to_copy = self.selected_text
        try:
            pyperclip.copy(text_to_copy)
        except pyperclip.PyperclipException as exc:
            # Show a toast popup if we fail to copy.
            self.notify(
                str(exc),
                title='Clipboard error',
                severity='error',
            )
        else:
            self.notify(f'Copied {len(text_to_copy)} characters!', title='Copied selection')

    def action_select_all(self):
        """Select all text in the text area."""
        self.select_all()


class ChatMessageTextArea(TextAreaWithBinding):
    DEFAULT_CSS = """
        ChatMessageTextArea {
            height: auto;
            border: ascii green;
            width: 100%;
        }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(read_only=True, *args, **kwargs)


class InputTextArea(TextAreaWithBinding):
    pass
