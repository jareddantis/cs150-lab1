"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import LEFT, RIGHT


# Guessed letters states
STATE_CORRECT = 0
STATE_MISPLACED = 1
STATE_INCORRECT = 2


class WordleClone(toga.App):
    def __init__(self):
        # Initialize app
        super().__init__(
            'Wordle Clone',
            'cs150.dantis.aureljared',
            author='Aurel Jared C. Dantis',
            description="A wordle clone made with BeeWare and Toga",
            version='0.1.0',
            home_page="https://github.com/jareddantis/wordle-app"
        )

    def on_guess(self, widget, value):
        # Build states per letter
        states = [STATE_INCORRECT for _ in len(self.word)]
        for index, letter in enumerate(list(value)):
            if letter == self.word[index]:
                states[index] = STATE_CORRECT

    def startup(self):
        main_box = toga.Box()

        # Build guess input form
        guess_label = toga.Label('Guess:', style=Pack(text_align=LEFT, padding=5))
        guess_input = toga.TextInput(style=Pack(flex=1))
        guess_button = toga.Button('Guess', on_press=self.on_guess, style=Pack(padding=5))
        guess_box = toga.Box()
        guess_box.add(guess_label)
        guess_box.add(guess_input)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return WordleClone()
