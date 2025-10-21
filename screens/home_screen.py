from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Label, Button, OptionList, Header
from textual.widgets.option_list import Option
from screens.create_screen import CreateScreen
from screens.deck_screen import DeckScreen
from utils.file_io import read_json, DECKS_DIR
import os

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('VocaApp', classes='title')
        with Horizontal(classes='button-group'):
            yield Button('Create New Deck', id='create', variant='primary')
            yield Button('Exit App', id='exit', variant='error')
        yield Label('Decks', classes='title')
        yield OptionList(id='deck-list')
    
    def on_mount(self):
        self.load_decks()

    def load_decks(self):
        deck_list = self.query_one('#deck-list')
        deck_list.clear_options()
        if os.path.exists(DECKS_DIR):
            for filename in os.listdir(DECKS_DIR):
                if filename.endswith(".json"):
                    filepath = os.path.join(DECKS_DIR, filename)
                    data = read_json(filepath)
                    if data and 'title' in data:
                        deck_list.add_option(Option(data['title']))
                    elif data is None:
                        self.notify(f'JSON parsing error in {filename}', severity='error')
        else:
            self.notify('Decks directory not found', severity='information')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'create':
            self.app.push_screen(CreateScreen(on_create=self.load_decks))
        elif event.button.id == 'exit':
            self.app.exit()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_option = event.option.prompt
        self.app.push_screen(DeckScreen(deck_title=selected_option))