from textual.widgets import Button


class ChatListItemButton(Button):
    DEFAULT_CSS = """
        ChatListItemButton {
            background: #161312 100%;
            height: 3;
            color: white;
            border: round green;
            text-align: center;
            width: 100%;
            &:hover {
                border: ascii; 
                background: #161312 100%;
            }
            &:focus {
                border: ascii green;
                background: #161312 100%;
                text-style: bold;
                background-tint: $foreground 0%;
            }
        }
    """
    pass
