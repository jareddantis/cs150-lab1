"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import LEFT, COLUMN, ROW
from typing import List
from .guess_row import GuessRow
from .words import WordManager
from .constants import *


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

        # Initialize number of guesses, guess rows, and guess input box
        self.guess = 0
        self.guess_rows: List[GuessRow] = []
        self.guess_input = None

        # Initialize list of labels for possible letters
        self.letter_list = []

        # Initialize word manager and get the word for this session
        self.word_manager = WordManager(self.paths.app)
        self.word = self.word_manager.get_word()
    
    def get_instance_indices(self, word: str, search: str) -> List[int]:
        """
        Returns a list of indices for each instance of the letter in the word.
        """
        indices = []
        for index, letter in enumerate(word):
            if letter == search:
                indices.append(index)
        return indices
    
    def validate_input(self) -> bool:
        """
        Checks whether the current guess is 5 characters long,
        contains only letters, and is in the list of allowed guesses.
        """
        # Show error dialog if guess is not exactly 5 characters long
        if len(self.guess_input.value) != 5:
            self.reset_input('Guess must be exactly 5 characters long.')
            return False
        
        # Show error dialog if guess contains non-alphabet characters
        if not self.guess_input.value.isalpha():
            self.reset_input('Guess must only contain letters.')
            return False
        
        # Show error dialog if guess is not in the list of allowed guesses
        if not self.word_manager.is_allowed(self.guess_input.value):
            self.reset_input('Guess must be in the list of allowed guesses.')
            return False
        
        # Input is valid
        return True
    
    def disable_letter(self, letter: str):
        """
        Removes a letter from the list of remaining possible letters.
        """
        label_index = 'abcdefghijklmnopqrstuvwxyz'.index(letter)
        self.letter_list[label_index].enabled = False
    
    def reset_input(self, error_msg: str):
        """
        Resets the guess input box and shows an error dialog.
        """
        self.guess_input.value = ''
        self.main_window.error_dialog('Error', error_msg)

    def on_guess(self, _):
        """
        Handler for the Guess button.
        Checks the guess input value against the word and creates a list of states.
        Each state corresponds to one letter in the word, where:
            STATE_CORRECT: the letter is in the word and in the correct position.
            STATE_MISPLACED: the letter is in the word but not in the correct position.
            STATE_INCORRECT: the letter is not in the word or has already been guessed.
        """
        # Do nothing if maximum guesses reached
        if self.guess == 6:
            self.main_window.error_dialog('Error', 'Maximum number of guesses reached.')

        # Do nothing if not ready yet or input is invalid
        if self.guess_input is None or not self.validate_input():
            return

        # Initialize states
        states = [STATE_INCORRECT for _ in range(len(self.word))]
        remaining_letters = list(self.word)

        # Check each letter in the guess against the word
        value = self.guess_input.value.lower()
        for index, letter in enumerate(list(value)):
            if letter == self.word[index]:
                # Letter is in the word and in the correct position
                states[index] = STATE_CORRECT

                # Remove first occurrence of letter from remaining letters
                remaining_letters.remove(letter)
            else:
                # Is letter elsewhere in the word?
                if letter in remaining_letters:
                    # Letter is in the word but not in the correct position.
                    # How many times does this letter occur in the word?
                    correct_i = self.get_instance_indices(self.word, letter)
                    guess_i = self.get_instance_indices(value, letter)

                    # Check that this letter has not occurred more than that in the guess.
                    if guess_i.index(index) + 1 > len(correct_i):
                        # This letter has already occurred enough times,
                        # so it is incorrect.
                        states[index] = STATE_INCORRECT
                        self.disable_letter(letter)
                    else:
                        # This letter has not exceeded the number of times
                        # it appears in the original word, so it is only misplaced.
                        states[index] = STATE_MISPLACED
                else:
                    # Letter is nowhere in the word.
                    self.disable_letter(letter)
                    states[index] = STATE_INCORRECT
        
        # Update appropriate guess row
        self.guess_rows[self.guess].update(list(value), states)
        self.guess += 1

    def startup(self):
        # Create main content box
        main_box = toga.Box(style=Pack(alignment='center', direction=COLUMN, padding=10))

        # Build guess input form
        guess_label = toga.Label('Guess:', style=Pack(text_align=LEFT, padding=5, flex=1))
        guess_input = toga.TextInput(style=Pack(flex=2))
        guess_button = toga.Button('Guess', on_press=self.on_guess, style=Pack(padding=(5, 0)))
        guess_box = toga.Box()
        guess_box.add(guess_label)
        guess_box.add(guess_input)
        main_box.add(guess_box)
        main_box.add(guess_button)

        # Build letter cheatsheet
        letter_box = toga.Box(style=Pack(flex=1, direction=ROW, padding=(10, 0)))
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            letter_label = toga.Label(letter, style=Pack(
                flex=1,
                text_align='center'
            ))
            self.letter_list.append(letter_label)
            letter_box.add(letter_label)
        main_box.add(letter_box)

        # Build word display, which is a 6x5 grid of boxes
        word_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding_top=10))
        for _ in range(6):
            row = GuessRow()
            self.guess_rows.append(row)
            word_box.add(row)
        main_box.add(word_box)

        # Save guess input box for later
        self.guess_input = guess_input

        # Instantiate main window and show app content
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return WordleClone()
