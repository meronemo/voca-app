from textual.app import App
from screens.home_screen import HomeScreen

class VocaApp(App[str]):
    TITLE = 'VocaApp'
    CSS_PATH = "main.tcss"
    
    def on_mount(self) -> None:
        self.app.push_screen(HomeScreen())

if __name__ == '__main__':
    app = VocaApp()
    app.run()