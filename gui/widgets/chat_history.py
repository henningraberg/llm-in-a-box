from textual.containers import VerticalScroll


class ChatHistory(VerticalScroll):
    DEFAULT_CSS = """
        ChatHistory {
            scrollbar-background: black;
        }
    """

    # def compose(self) -> ComposeResult:
    #     chats = Chat.get_multiple()
    #     # reverse so the newest gets on top
    #     chats.reverse()
    #     for chat in chats:
    #         yield ChatItem(chat.name, id=f'{chat.name}-{chat.id}'.replace(' ', '-'))
