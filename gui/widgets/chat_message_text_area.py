from textual.widgets import TextArea


class ChatMessageTextArea(TextArea):
    DEFAULT_CSS = """
        ChatMessageTextArea {
            border: dashed black;
            height: auto;
        }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(read_only=True, *args, **kwargs)
