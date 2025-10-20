from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal
from textual.widgets import Label, Button, Header, TextArea
import os
import json

class DeckImportScreen(ModalScreen):
    TITLE = 'Import Cards'

    def __init__(self, deck_title=None, on_import=None):
        super().__init__()
        self.deck_title = deck_title
        self.on_import = on_import
        self.filepath = os.path.join('./decks', f'{deck_title}.json')
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Import Cards', classes='title')
        yield Label('Format: each line = one card, separate the word and meaning with a single space')
        yield TextArea(placeholder='Data', id='import-data')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='error')
            yield Button('Import', id='import', variant='success')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()
        elif event.button.id == 'import':
            data_input = self.query_one('#import-data')
            data = data_input.text
            if validate(data):
                self.import_cards(data)
            else:
                self.notify('Invalid format', severity='error')

    def import_cards(self, data: str) -> None:
        lines = data.strip().split('\n')
        new_cards = []
        for line in lines:
            word, meaning = line.strip().split(None, 1)
            new_cards.append({'word': word, 'meaning': meaning})

        with open(self.filepath, 'r') as f:
            deck_data = json.load(f)
            deck_data['cards'].extend(new_cards)
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(deck_data, f, ensure_ascii=False, indent=4)
        self.notify(f'Saved imported cards', severity='information')
        self.on_import() # call load_deck in deck screen to refresh deck datas
        self.app.pop_screen()

def validate(value: str) -> bool:
    lines = value.strip().split('\n')
    for line in lines:
        parts = line.strip().split(None, 1) # split on first whitespace
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
    return True

