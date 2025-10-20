from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Button, Header, Static
import os
import json

class FlashcardsScreen(Screen):
    TITLE = 'Flashcards'

    def __init__(self, deck_title=None):
        super().__init__()
        self.deck_title = deck_title
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Button('Back', id='back', variant='default')
        yield Card(deck_title=self.deck_title, id='card')
        with Grid(id='flashcard-buttons-grid'):
            yield Button('Prev', id='prev', variant='default', classes='w-80')
            yield Button('Flip', id='flip', variant='primary', classes='w-80')
            yield Button('Next', id='next', variant='default', classes='w-80')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.card = self.query_one('#card')
        if event.button.id == 'back':
            self.app.pop_screen()
        elif event.button.id == 'prev':
            self.card.prev()
        elif event.button.id == 'flip':
            self.card.flip()
        elif event.button.id == 'next':
            self.card.next()

class Card(Widget):
    def __init__(self, deck_title, **kwargs):
        self.deck_title = deck_title
        self.filepath = os.path.join('./decks', f'{deck_title}.json')
        super().__init__(**kwargs)
    
    def compose(self) -> ComposeResult:
        yield Static(id='content')

    def on_mount(self):
        self.card_content = self.query_one('#content')
        self.stat = 0 # 0: word, 1: meaning
        self.load_card()

    def update_static(self):
        if self.stat:
            self.card_content.update(self.meanings[self.idx])
        else:
            self.card_content.update(self.words[self.idx])

    def load_card(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            cards = data['cards']
        
        self.words, self.meanings = [], []
        for card in cards:
            self.words.append(card['word'])
            self.meanings.append(card['meaning'])
        self.idx = 0
        self.update_static()

    def prev(self):
        if self.idx > 0:
            self.idx -= 1
            self.stat = 0
            self.update_static()

    def next(self):
        if self.idx < len(self.words)-1:
            self.idx += 1
            self.stat = 0
            self.update_static()

    def flip(self):
        self.stat = not self.stat
        self.update_static()