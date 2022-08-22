import random
from typing import Optional


class InMemoryStorage:
    """
        InMemory store to store secret words.
    """

    def __init__(self):
        self.storage = []

    def add_guess(self, secret_word: str) -> None:
        """ Store a secret word."""
        self.storage.append(secret_word)

    def get_random_word_id(self) -> Optional[int]:
        """ Get an index of a random secret word."""
        if not self.storage:
            return None  # no words saved - nothing to return
        return random.randint(0, len(self.storage) - 1)

    def get_secret_word_by_id(self, index: int) -> Optional[str]:
        """
        Given the index in the storage, return the secret word by this index.
        """
        if not (0 <= index < len(self.storage)):
            return None  # index out of range
        secret_word = self.storage[index]
        return secret_word
