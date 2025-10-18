from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Label, Button, OptionList, Header, Input
from textual.widgets.option_list import Option
from textual.validation import ValidationResult, Validator
import os
import json
import re

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        deck_options = OptionList()
        
        if os.path.exists('./decks'):
            for filename in os.listdir('./decks'):
                if filename.endswith(".json"):
                    filepath = os.path.join('./decks', filename)
                    with open(filepath, 'r') as f:
                        try:
                            data = json.load(f)
                            if 'title' in data:
                                deck_options.add_option(Option(data['title'], id=filename))
                        except json.JSONDecodeError:
                            self.notify(f'JSON parsing error in {filename}', severity='error')
        else:
            self.notify('Decks directory not found', severity='information')

        yield Header()
        yield Label('VocaApp', classes='title')
        yield Button('Create New Deck', id='create', variant='primary')
        yield Label('Decks', classes='title')
        yield deck_options
        yield Button('Exit', id='exit', variant='error')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'create':
            self.app.push_screen(CreateScreen())
        elif event.button.id == 'exit':
            self.app.exit()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_option = event.option.id


class CreateScreen(Screen):
    TITLE = 'Create New Deck'
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Create New Deck', classes='title')
        yield Input(placeholder='Title', validators=TitleValidator(), id='title')
        yield Label(id='valid-msg')
        yield Input(placeholder='Description', id='description')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='error')
            yield Button('Create', id='create', variant='success')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()
        elif event.button.id == 'create':
            title_input = self.query_one('#title')
            desc_input = self.query_one('#description')
            title = title_input.value.strip()
            description = desc_input.value.strip()

            if not title_input.is_valid:
                return

            os.makedirs('./decks', exist_ok=True)
            file_path = os.path.join('./decks', f'{title}.json')
            data = {
                "title": title,
                "description": description,
                "cards": [] 
            }

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                self.notify(f'Created {title} deck', severity='information')
                self.app.pop_screen()
                self.app.pop_screen()
                self.app.push_screen(HomeScreen())

            except Exception as e:
                self.notify(f'Error creating deck: {e}', severity='error')

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        if event.validation_result:
            if not event.validation_result.is_valid:
                self.query_one('#valid-msg').update(event.validation_result.failure_descriptions[0])
            else:
                self.query_one('#valid-msg').update('')


class TitleValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if self.empty(value):
            return self.failure('Title cannot be empty.')
        if self.max_length(value):
            return self.failure('Title cannot exceed 30 characters.')
        if self.invalid_chars(value):
            return self.failure('Title contains invalid characters.')
        if self.already_exist(value):
            return self.failure('A deck with this title already exists.')
        return self.success()
    
    @staticmethod
    def empty(value: str) -> bool:
        return not value.strip()

    @staticmethod
    def max_length(value: str) -> bool:
        return len(value) > 30
    
    @staticmethod
    def invalid_chars(value: str) -> bool:
        return re.search(r'[\\/:*?"<>|]', value)
    
    @staticmethod
    def already_exist(value: str) -> bool:
        return os.path.exists(os.path.join('./decks', f'{value}.json'))


class DeckScreen(Screen):
    TITLE = 'Deck'
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Deck Screen', classes='title')
        yield Button('Back to Home', id='back', variant='default')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()


class VocaApp(App[str]):
    TITLE = 'VocaApp'
    CSS_PATH = "main.tcss"
    
    def on_mount(self) -> None:
        self.app.push_screen(HomeScreen())

if __name__ == '__main__':
    app = VocaApp()
    app.run()