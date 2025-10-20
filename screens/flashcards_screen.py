from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Button, Header, Static
from itertools import cycle
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
        yield Card(deck_title=self.deck_title)
        with Grid(id='flashcard-buttons-grid'):
            yield Button('Prev', id='prev', variant='default', classes='w-80')
            yield Button('Flip', id='flip', variant='primary', classes='w-80')
            yield Button('Next', id='next', variant='default', classes='w-80')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()
    
    @on(Button.Pressed, '#prev')
    def handle_prev(self) -> None:
        pass

class Card(Widget):
    def __init__(self, deck_title):
        self.deck_title = deck_title
        self.filepath = os.path.join('./decks', f'{deck_title}.json')
        super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Static(id='card-content')

    def on_mount(self):
        self.card_content = self.query_one('#card-content')
        self.load_card()

    def load_card(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            cards = data['cards']
        
        words, meanings = [], []
        for card in cards:
            words.append(card['word'])
            meanings.append(card['meaning'])
        words, meanings = cycle(words), cycle(meanings)

        now_word = next(words)
        now_meaning = next(meanings)
        self.card_content.update(now_word)