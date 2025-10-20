from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, VerticalScroll, Grid
from textual.widgets import Label, Button, Header
from screens.deck_edit_screen import DeckEditScreen
from screens.deck_import_screen import DeckImportScreen
import os
import json

class DeckScreen(Screen):
    def __init__(self, deck_title):
        super().__init__()
        self.deck_title = deck_title
        self.title = f'Deck | {deck_title}'
        filepath = os.path.join('./decks', f'{self.deck_title}.json')
        self.filepath = filepath

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(id='title', classes='title')
        yield Label(id='description')
        with Horizontal(classes='button-group'):
            yield Button('Back to Home', id='back', variant='default')
            yield Button('Edit', id='edit', variant='primary')
            yield Button('Import', id='import', variant='primary')
        yield VerticalScroll(id='cards-list')

    def on_mount(self):
        self.load_deck()

    def load_deck(self):
        title_label = self.query_one('#title')
        description_label = self.query_one('#description')
        
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            description = data['description']
            cards = data['cards']
        title_label.update(self.deck_title)
        description_label.update(description)

        cards_list = self.query_one('#cards-list')
        cards_list.remove_children()
        for card in cards:
            cards_list.mount(
                Grid(
                    Label(card['word'], classes='csp-1'),
                    Label(card['meaning'], classes='csp-3'),
                    classes='card-grid',
                )
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()
        elif event.button.id == 'edit':
            self.app.push_screen(DeckEditScreen(deck_title=self.deck_title, on_edit=self.load_deck))
        elif event.button.id == 'import':
            self.app.push_screen(DeckImportScreen(deck_title=self.deck_title, on_import=self.load_deck))