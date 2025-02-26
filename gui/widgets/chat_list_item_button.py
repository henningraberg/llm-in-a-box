from textual.widgets import Button


class ChatListItemButton(Button):
    DEFAULT_CSS = """
        ChatListItemButton {
            background: #161312 100%;
            height: 3;
            color: white;
            border: round white;
            text-align: center;
            width: 100%;
        }
        
        ChatListItemButton:hover {
            border: ascii; 
        }
        
        ChatListItemButton:focus {
            border: ascii green;
            background: black 100%;
        }
    """
    pass
