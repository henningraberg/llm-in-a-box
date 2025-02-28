from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Horizontal, Vertical, VerticalScroll

from gui.widgets.chat_list import ChatList
from gui.widgets.llm_select import LLMSelect
from gui.widgets.text_area import InputTextArea


class MainView(Screen):
    def compose(self) -> ComposeResult:
        yield Header(id='header')
        with Horizontal(id='chat-container'):
            with Vertical(id='chat-list-container'):
                yield Button('Create new chat', id='init-new-chat-button', variant='success')
                yield ChatList(id='chat-list')
            with Vertical(id='chat-view-container'):
                disabled = not bool(getattr(self.app, 'current_chat_id'))
                with Horizontal(id='chat-view-header'):
                    yield LLMSelect(id='llm-selection-2', disabled=disabled)
                    yield Button(label='Delete chat', id='init-delete-chat-button', disabled=disabled, variant='error')
                yield VerticalScroll(id='chat-history-box', disabled=disabled)
                with Horizontal(id='input-box'):
                    yield InputTextArea(id='message-input', disabled=disabled, show_line_numbers=True)
                    with Vertical(id='input-buttons-box'):
                        yield Button(label='Send', variant='success', id='send-button', disabled=disabled)
                        yield Button(label='Abort', variant='error', id='abort-button', disabled=disabled)
        yield Footer(id='footer')
