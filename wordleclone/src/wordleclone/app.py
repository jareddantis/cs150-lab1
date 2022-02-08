"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import List, Optional
from .letter import WordleLetter
from .guess_form import GuessForm
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
        self.guess_form = None
        self.guessed = False

        # Initialize list of labels for possible letters
        self.letter_list: List[WordleLetter] = []

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
    
    def enable_letter(self, letter: str):
        """
        Turns a letter green in the list of remaining possible letters.
        """
        label_index = 'abcdefghijklmnopqrstuvwxyz'.index(letter)
        self.letter_list[label_index].green = True
    
    def disable_letter(self, letter: str):
        """
        Removes a letter from the list of remaining possible letters.
        """
        label_index = 'abcdefghijklmnopqrstuvwxyz'.index(letter)
        if not self.letter_list[label_index].green:
            self.letter_list[label_index].visible = False
    
    def reset_input(self, error_msg: Optional[str] = None):
        """
        Resets the guess input box and shows an error dialog.
        """
        self.guess_form.value = ''
        if isinstance(error_msg, str):
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
        # Do nothing if already guessed
        if self.guessed:
            return

        # Do nothing if maximum guesses reached
        if self.guess == 6:
            self.main_window.error_dialog('Error', 'Maximum number of guesses reached.')

        # Do nothing if not ready yet or input is invalid
        if self.guess_form is None or not self.guess_form.validate():
            return

        # Initialize states
        states = [STATE_INCORRECT for _ in range(len(self.word))]
        remaining_letters = list(self.word)

        # Check each letter in the guess against the word
        value = self.guess_form.value
        for index, letter in enumerate(list(value)):
            if letter == self.word[index]:
                # Letter is in the word and in the correct position
                states[index] = STATE_CORRECT

                # Turn the letter green
                self.enable_letter(letter)

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

        # Check if all letters have been guessed
        if len(remaining_letters) == 0:
            self.guessed = True
            self.main_window.info_dialog('Congratulations!', 'You guessed the word!')
        else:
            if self.guess == 6:
                self.main_window.error_dialog('Error', f'Maximum number of guesses reached. The answer was: {self.word}')

        # Reset guess input box
        self.reset_input()
    
    def restart_game(self, _):
        """
        Restarts the game.
        """
        # Reset number of guesses
        self.guess = 0
        self.guessed = False

        # Reset input box
        self.reset_input()

        # Reset guess rows
        for row in self.guess_rows:
            row.reset()
        
        # Reset list of remaining letters
        for letter in self.letter_list:
            letter.reset()

        # Get a new word
        self.word = self.word_manager.get_word()

    def startup(self):
        # Create main content box
        main_box = toga.Box(style=Pack(alignment='center', direction=COLUMN, padding=10))

        # Build guess input form
        guess_form = GuessForm(self.on_guess, self.word_manager)
        main_box.add(guess_form)
        self.guess_form = guess_form

        # Build letter cheatsheet
        letter_box = toga.Box(style=Pack(flex=1, direction=ROW, padding=(20, 0)))
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            letter_label = WordleLetter(letter)
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

        # Build restart button
        restart_button = toga.Button('Restart', on_press=self.restart_game, style=Pack(padding=(30, 0, 0, 0)))
        main_box.add(restart_button)

        # Instantiate main window and show app content
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return WordleClone()
