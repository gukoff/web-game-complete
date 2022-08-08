from inspect import _void
import random


class InMemoryStorage:
    """
        InMemory store to store images and their guess descriptions.
    """

    def __init__(self) -> None:
        self.storage = []

    def add_guess(self, secret: str) -> _void:
        """ Store an image and description."""
        self.storage.append((secret))

    def get_random_id(self) -> _void:
        """ Get a random guess."""
        return random.randint(0, len(self.storage) - 1) if self.storage else None

    def get_guess_secret(self, key: int) -> str:
        """ Get a guess secret."""
        if (key not in self.storage):
            return None
        guess_secret = self.storage[key]
        return guess_secret
