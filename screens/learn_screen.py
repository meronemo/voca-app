from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Container, Vertical
from textual.widgets import Button, Header, Static, ProgressBar
from utils.file_io import get_deck_path, read_json
import random

class LearnScreen(Screen):
    TITLE = 'Learn'

    def __init__(self, deck_title=None):
        super().__init__()
        self.deck_title = deck_title
        self.filepath = get_deck_path(deck_title)
        
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield ProgressBar(show_percentage=False, show_eta=False)
            yield Static(id='progress-num')
        yield Button('Back', id='back', variant='default')
        with Container(id='question-container'):
            yield Static(id='question-text')
        with Vertical(id='choices-container'):
            yield Button('', id='choice0', classes='choice-button')
            yield Button('', id='choice1', classes='choice-button')
            yield Button('', id='choice2', classes='choice-button')
            yield Button('', id='choice3', classes='choice-button')
        yield Static(id='result-message')

    def on_mount(self):
        self.question_text = self.query_one('#question-text')
        self.progress_num = self.query_one('#progress-num')
        self.progress_bar = self.query_one(ProgressBar)
        self.result_message = self.query_one('#result-message')
        self.load_cards()
    
    def load_cards(self):
        data = read_json(self.filepath, default={})
        cards = data.get('cards', [])
        
        if not cards:
            self.notify('No cards in this deck', severity='warning')
            self.app.pop_screen()
            return
        
        self.cards = list(cards)
        random.shuffle(self.cards)
        
        self.idx = 0
        self.total = len(self.cards)
        self.correct_count = 0
        
        self.progress_bar.update(total=self.total)
        self.progress_bar.advance(0)
        
        self.show_question()

    def show_question(self):
        if self.idx >= self.total:
            self.show_results()
            return
        
        current_card = self.cards[self.idx]
        self.current_word = current_card['word']
        self.correct_answer = current_card['meaning']
        
        self.progress_num.update(f'{self.idx + 1}/{self.total}')
        self.progress_bar.update(progress=self.idx + 1)
        
        self.question_text.update(f"What is the meaning of:\n\n{self.current_word}")
        
        # Generate 4 choices
        all_meanings = [card['meaning'] for card in self.cards]
        wrong_meanings = [m for m in all_meanings if m != self.correct_answer]
        
        if len(wrong_meanings) >= 3:
            choices = random.sample(wrong_meanings, 3) + [self.correct_answer]
        else:
            choices = wrong_meanings + [self.correct_answer]
            while len(choices) < 4:
                choices.append(f"[No answer {len(choices)}]")
        
        random.shuffle(choices)
        
        # Update choice buttons
        for i in range(4):
            button = self.query_one(f'#choice{i}')
            button.label = choices[i]
            button.disabled = False
            button.variant = 'default'
        
        self.result_message.update('')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'back':
            self.app.pop_screen()
        elif event.button.id.startswith('choice'):
            self.check_answer(event.button)

    def check_answer(self, button: Button) -> None:
        selected_answer = button.label
        
        # Disable all choice buttons
        for i in range(4):
            choice_button = self.query_one(f'#choice{i}')
            choice_button.disabled = True
        
        if selected_answer == self.correct_answer:
            button.variant = 'success'
            self.result_message.update('Correct!')
            self.correct_count += 1
        else:
            button.variant = 'error'
            self.result_message.update(f'Wrong! Correct answer: {self.correct_answer}')
            for i in range(4):
                choice_button = self.query_one(f'#choice{i}')
                if choice_button.label == self.correct_answer:
                    choice_button.variant = 'success'
        
        # Move to next question after delay
        self.idx += 1
        self.set_timer(1.5, self.show_question)

    def show_results(self):
        percentage = int((self.correct_count / self.total) * 100)
        self.question_text.update(f"Quiz Complete!\n\nScore: {self.correct_count}/{self.total} ({percentage}%)")
        
        for i in range(4):
            choice_button = self.query_one(f'#choice{i}')
            choice_button.display = False
        
        self.result_message.update('')
