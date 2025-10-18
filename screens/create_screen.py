from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Label, Button, Header, Input
from textual.validation import ValidationResult, Validator
import os
import json
import re

class CreateScreen(Screen):
    TITLE = 'Create New Deck'

    def __init__(self, on_create=None):
        super().__init__()
        self.on_create = on_create

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
                self.on_create() # call load_decks in home screen to refresh decks list
                self.app.pop_screen()

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
    
