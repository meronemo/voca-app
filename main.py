from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Label, Button, OptionList, Header, Input
from textual.widgets.option_list import Option

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('VocaApp', classes='title')
        yield Button('Create New Deck', id='create', variant='primary')
        yield Label('Decks', classes='title')
        yield OptionList(
            Option('Example 1'),
            Option('Example 2'),
            Option('Example 3'),
        )
        yield Button('Exit', id='exit', variant='error')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'create':
            self.app.push_screen(CreateScreen())
        elif event.button.id == 'exit':
            self.app.exit()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        selected_option = event.option.prompt

class CreateScreen(Screen):
    TITLE = 'Create New Deck'
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Create New Deck', classes='title')
        yield Input(placeholder='Title')
        with Horizontal(classes='button-group'):
            yield Button('Cancel', id='cancel', variant='error')
            yield Button('Create', id='create', variant='success')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel':
            self.app.pop_screen()


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