from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Label, Button, Header
from screens.deck_edit_screen import DeckEditScreen
import os
import json

class DeckScreen(Screen):
    def __init__(self, deck_title):
        super().__init__()
        self.deck_title = deck_title
        self.title = f'Deck | {deck_title}'
        filepath = os.path.join('./decks', f'{self.deck_title}.json')
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.description = data['description']

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(id='title', classes='title')
        yield Label(id='description')
        with Horizontal(classes='button-group'):
            yield Button('Back to Home', id='back', variant='default')
            yield Button('Edit', id='edit', variant='primary')

    def on_mount(self):
        title_label = self.query_one('#title')
        description_label = self.query_one('#description')
        title_label.update(self.deck_title)
        description_label.update(self.description)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()
        elif event.button.id == 'edit':
            self.app.push_screen(DeckEditScreen(deck_title=self.deck_title))