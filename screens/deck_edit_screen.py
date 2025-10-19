from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Grid, VerticalScroll
from textual.widgets import Label, Button, Header, Input
from textual.validation import Function
import os
import json

class DeckEditScreen(Screen):
    def __init__(self, deck_title, on_edit):
        super().__init__()
        self.deck_title = deck_title
        self.title = f'Deck Edit | {deck_title}'
        self.on_edit = on_edit

        filepath = os.path.join('./decks', f'{self.deck_title}.json')
        self.filepath = filepath
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.description = data['description']
            self.cards = data['cards']

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.deck_title, classes='title')
        yield Input(value=self.description, placeholder='Description', id='description')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='default')
            yield Button('Save', id='save', variant='success')
        yield Label('Cards', classes='title')
        yield VerticalScroll(id='cards_list')

    def on_mount(self):
        cards_list = self.query_one('#cards_list')
        for idx, card in enumerate(self.cards):
            cards_list.mount(
                Grid(
                    Input(value=card['word'], placeholder='Word', id=f'word{idx}', classes='card-input', validators=Function(is_empty)),
                    Input(value=card['meaning'], placeholder='Meaning', id=f'meaning{idx}', classes='card-input card-meaning', validators=Function(is_empty)),
                    classes='card-grid',
                )
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()
        if event.button.id == 'save':
            new_data = {}
            description_input = self.query_one('#description')
            new_data['title'] = self.deck_title
            new_data['description'] = description_input.value
            new_data['cards'] = []

            for i in range(len(self.cards)):
                word_input = self.query_one(f'#word{i}')
                meaning_input = self.query_one(f'#meaning{i}')
                new_data['cards'].append({'word': word_input.value, 'meaning': meaning_input.value})
            
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)
                self.notify(f'Edited {self.deck_title} deck', severity='information')
                self.on_edit() # call load_deck in deck screen to refresh deck datas
                self.app.pop_screen()
            except Exception as e:
                self.notify(f'Error editing deck: {e}', severity='error')


def is_empty(value: str) -> bool:
    return value.strip()
