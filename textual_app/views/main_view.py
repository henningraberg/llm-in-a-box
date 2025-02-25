from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer

from textual_app.widgets.chat_container import ChatContainer


class MainView(Screen):
    """Main view of the Textual app with a sidebar menu."""

    def compose(self) -> ComposeResult:
        """Create UI elements."""
        yield Header(id='header')
        yield ChatContainer()
        yield Footer(id='footer')
