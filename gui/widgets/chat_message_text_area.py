from textual.widgets import TextArea


class ChatMessageTextArea(TextArea):
    DEFAULT_CSS = """
        ChatMessageTextArea {
            height: auto;
            border: ascii green;
            width: 100%;
        }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(read_only=True, *args, **kwargs)
