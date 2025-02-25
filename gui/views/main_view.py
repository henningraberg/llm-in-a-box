from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer

from gui.widgets.chat_container import ChatContainer


class MainView(Screen):
    """Main view of the Textual app with a sidebar menu."""

    def compose(self) -> ComposeResult:
        """Create UI elements."""
        yield Header(id='header')
        yield ChatContainer(id='chat-container')
        yield Footer(id='footer')
