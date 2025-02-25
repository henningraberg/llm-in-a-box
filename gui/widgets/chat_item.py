from textual.widgets import Button

from models.chat import Chat


class ChatItem(Button):
    DEFAULT_CSS = """
        ChatItem {
            background: #161312 100%;
            height: 3;
            color: white;
            border: round white;
            text-align: center;
            width: 100%;
        }
        
        ChatItem:hover {
            border: ascii;  /* Change border color on hover */
        }
        
        ChatItem:focus {
            border: ascii green;
            background: black 100%;
        }
    """

    def __init__(self, chat: Chat, *args, **kwargs):
        super().__init__(chat.name, id=f'load-chat-button-{chat.id}', *args, **kwargs)
