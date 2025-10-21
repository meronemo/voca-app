from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid, Horizontal, Container
from textual.widgets import Button, Header, Static, ProgressBar
import os
import json

class FlashcardsScreen(Screen):
    TITLE = 'Flashcards'

    def __init__(self, deck_title=None):
        super().__init__()
        self.deck_title = deck_title
        self.filepath = os.path.join('./decks', f'{deck_title}.json')
        
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ProgressBar(show_percentage=False, show_eta=False)
            yield Static(id='num')
        yield Button('Back', id='back', variant='default')
        with Container(id='flashcard-container'):
            yield Static(id='flashcard-content')
        with Grid(id='flashcard-buttons-grid'):
            yield Button('Prev', id='prev', variant='default', classes='w-80')
            yield Button('Flip', id='flip', variant='primary', classes='w-80')
            yield Button('Next', id='next', variant='default', classes='w-80')

    def on_mount(self):
        self.card_content = self.query_one('#flashcard-content')
        self.num = self.query_one('#num')
        self.progress_bar = self.query_one(ProgressBar)
        self.stat = 0 # 0: word, 1: meaning
        self.load_card()
    
    def load_card(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            cards = data['cards']
        
        self.words, self.meanings = [], []
        for card in cards:
            self.words.append(card['word'])
            self.meanings.append(card['meaning'])
        self.idx = 0
        self.card_cnt = len(self.words)
        self.progress_bar.update(total=self.card_cnt)
        self.progress_bar.advance(1)
        self.update_static()

    def update_static(self):
        self.num.update(f'{str(self.idx+1)}/{str(self.card_cnt)}')
        if self.stat:
            self.card_content.update(self.meanings[self.idx])
        else:
            self.card_content.update(self.words[self.idx])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.card = self.query_one('#flashcard-container')
        if event.button.id == 'back':
            self.app.pop_screen()
        elif event.button.id == 'prev':
            if self.idx > 0:
                self.idx -= 1
                self.stat = 0
                self.progress_bar.advance(-1)
                self.update_static()
        elif event.button.id == 'flip':
            self.stat = not self.stat
            self.update_static()
        elif event.button.id == 'next':
            if self.idx < len(self.words)-1:
                self.idx += 1
                self.stat = 0
                self.progress_bar.advance(1)
                self.update_static()
