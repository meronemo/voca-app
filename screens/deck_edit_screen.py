from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Grid
from textual.widgets import Label, Button, Header, Input, ListView, ListItem
import os
import json

class DeckEditScreen(Screen):
    def __init__(self, deck_title):
        super().__init__()
        self.deck_title = deck_title
        self.title = f'Deck Edit | {deck_title}'
        filepath = os.path.join('./decks', f'{self.deck_title}.json')
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.description = data['description']
            self.cards = data['cards']

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(value=self.deck_title, placeholder='Title', id='title', classes='title')
        yield Input(value=self.description, placeholder='Description', id='description')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='default')
            yield Button('Save', id='save', variant='success')
        yield Label('Cards', classes='title')
        yield ListView(id='cards_list', disabled=True)

    def on_mount(self):
        cards_list = self.query_one('#cards_list')
        for card in self.cards:
            item = ListItem(
                        Grid(
                            Input(value=card['word'], placeholder='Word'),
                            Input(value=card['meaning'], placeholder='Meaning', id='card_meaning'),
                            id='card_grid',
                        )
                    )
            cards_list.append(item)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()