from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, OptionList, Header
from textual.widgets.option_list import Option
from screens.create_screen import CreateScreen
import os
import json

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('VocaApp', classes='title')
        yield Button('Create New Deck', id='create', variant='primary')
        yield Label('Decks', classes='title')
        yield OptionList(id='deck-list')
        yield Button('Exit', id='exit', variant='error')
    
    def on_mount(self):
        self.load_decks()

    def load_decks(self):
        deck_list = self.query_one('#deck-list')
        deck_list.clear_options()
        if os.path.exists('./decks'):
            for filename in os.listdir('./decks'):
                if filename.endswith(".json"):
                    filepath = os.path.join('./decks', filename)
                    with open(filepath, 'r') as f:
                        try:
                            data = json.load(f)
                            if 'title' in data:
                                deck_list.add_option(Option(data['title'], id=filename))
                        except json.JSONDecodeError:
                            self.notify(f'JSON parsing error in {filename}', severity='error')
        else:
            self.notify('Decks directory not found', severity='information')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'create':
            self.app.push_screen(CreateScreen(on_create=self.load_decks))
        elif event.button.id == 'exit':
            self.app.exit()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_option = event.option.id