from toga import Box, Label, TextInput, Button
from toga.style import Pack
from toga.style.pack import LEFT, COLUMN
from typing import Callable, Optional
from .words import WordManager


class GuessForm(Box):
    def __init__(self, on_guess: Callable, word_mgr: WordManager):
        super().__init__(style=Pack(direction=COLUMN))

        # Store WordManager instance for validation
        self.word_manager = word_mgr

        # Build guess input row
        input_box = Box(style=Pack(flex=1))
        guess_label = Label('Guess:', style=Pack(text_align=LEFT, padding=5, flex=1))
        guess_input = TextInput(style=Pack(flex=2), validators=[self._validate_input])
        input_box.add(guess_label)
        input_box.add(guess_input)
        self._guess_input = guess_input

        # Build guess button
        guess_button = Button('Guess', on_press=on_guess, style=Pack(padding=(5, 0)))

        # Build guess form
        self.add(input_box)
        self.add(guess_button)

    @property
    def value(self) -> str:
        return self._guess_input.value

    @value.setter
    def value(self, value: str):
        self._guess_input.value = value

    def validate(self) -> bool:
        """
        Validates the current guess.
        """
        return self._guess_input.validate()

    def _validate_input(self, value: str) -> Optional[str]:
        """
        Checks whether the current guess is 5 characters long,
        contains only letters, and is in the list of allowed guesses.
        """
        # Show error if guess is not exactly 5 characters long
        if len(value) != 5:
            return 'Guess must be exactly 5 characters long.'
        
        # Show error if guess contains non-alphabet characters
        if not value.isalpha():
            return 'Guess must only contain letters.'
        
        # Show error if guess is not in the list of allowed guesses
        if self.word_manager is not None and self.word_manager.is_allowed(value):
            return 'Guess must be in the list of allowed guesses.'
        
        # Input is valid
        return None
