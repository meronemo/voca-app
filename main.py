from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Container, Center, Vertical
from textual.widgets import Label, Button, OptionList
from textual.widgets.option_list import Option

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Center():
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
            self.app.push_screen(HomeScreen())
        elif event.button.id == 'exit':
            self.app.exit()

class VocaApp(App[str]):
    TITLE = 'VocaApp'
    CSS_PATH = "main.tcss"
    
    def on_mount(self) -> None:
        self.app.push_screen(HomeScreen())

if __name__ == '__main__':
    app = VocaApp()
    app.run()