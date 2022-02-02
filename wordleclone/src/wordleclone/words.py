import os
from random import choice
from typing import List


# Guessed letters states
STATE_CORRECT = 0
STATE_MISPLACED = 1
STATE_INCORRECT = 2


class WordManager():
    def __init__(self, base_path: str):
        """
        Initializes the word manager by loading the lists of
        allowed guesses and correct words into memory.
        """
        # Build paths to word files
        words_path = os.path.join(base_path, 'resources', 'answers.txt')
        guess_path = os.path.join(base_path, 'resources', 'allowed.txt')

        # Cache files into memory
        self.words = self.__load_from_file__(words_path)
        guesses = self.__load_from_file__(guess_path)

        # Create union of words and allowed guesses for checking later
        self.allowed = list(set(self.words).union(set(guesses)))
    
    def __load_from_file__(self, path: str) -> List[str]:
        """
        Loads a file into memory and returns a list of lines.
        """
        with open(path, 'r') as file:
            return [line.rstrip().lower() for line in file]
    
    def get_word(self) -> str:
        """
        Returns a random word from the list of possible words.
        """
        return choice(self.words)
    
    def is_allowed(self, word: str) -> bool:
        """
        Returns True if the word is in the list of allowed words.
        """
        return word in self.allowed
