from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button, Header

class DeckScreen(Screen):
    TITLE = 'Deck'
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label('Deck Screen', classes='title')
        yield Button('Back to Home', id='back', variant='default')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()