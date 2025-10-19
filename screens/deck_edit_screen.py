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
        self.cards_cnt = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(id='title', classes='title')
        yield Input(id='description', placeholder='Description')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='default')
            yield Button('Save', id='save', variant='success')
        yield Label('Cards', classes='title')
        yield VerticalScroll(id='cards-list')

    def on_mount(self):
        self.load_deck()

    def create_card_row(self, idx: int, word: str = '', meaning: str = '') -> Grid:
        return Grid(
            Input(value=word, placeholder='Word', id=f'word{idx}', classes='card-data card-word', validators=Function(is_empty)),
            Input(value=meaning, placeholder='Meaning', id=f'meaning{idx}', classes='card-data card-meaning', validators=Function(is_empty)),
            Button('🗑️', id=f'remove{idx}', classes='card-data card-remove'),
            id=f'card-row{idx}',
            classes='card-grid',
        )
        
    def load_deck(self):
        cards_list = self.query_one('#cards-list')
        title_label = self.query_one('#title')
        description_input = self.query_one('#description')

        with open(self.filepath, 'r') as f:
            data = json.load(f)
            description = data['description']
            self.cards = data['cards']

        title_label.update(self.deck_title)
        description_input.value = description
        
        self.cards_cnt = len(self.cards)

        for idx, card in enumerate(self.cards):
            cards_list.mount(self.create_card_row(idx, card['word'], card['meaning']))

        cards_list.mount(Button('Add Card', id='add-card', variant='primary'))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()
        if event.button.id == 'save':
            # Check all inputs are valid before saving
            all_valid = True
            for i in range(self.cards_cnt):
                word_input = self.query_one(f'#word{i}')
                meaning_input = self.query_one(f'#meaning{i}')
                
                if not word_input.is_valid or not meaning_input.is_valid:
                    all_valid = False
                    break
            
            if not all_valid:
                self.notify('Please fill in all card fields before saving', severity='warning')
                return
            
            new_data = {}
            description_input = self.query_one('#description')
            new_data['title'] = self.deck_title
            new_data['description'] = description_input.value
            new_data['cards'] = []

            for i in range(self.cards_cnt):
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
        elif event.button.id == 'add-card':
            cards_list = self.query_one('#cards-list')
            add_card = self.query_one('#add-card')

            idx = self.cards_cnt
            cards_list.mount(self.create_card_row(idx), before=add_card)
            self.query_one(f'#word{idx}').focus()
            self.cards_cnt += 1
            cards_list.scroll_end(animate=False)
        elif event.button.id.startswith('remove'):
            idx = event.button.id.replace('remove', '')
            card_row = self.query_one(f'#card-row{idx}')
            card_row.remove()



def is_empty(value: str) -> bool:
    return value.strip()
