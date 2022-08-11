import random

class InMemoryStorage:
    """
        InMemory store to store images and their guess descriptions.
    """

    def __init__(self) -> None:
        self.storage = []

    def add_guess(self, image_content, image_description: str):
        """ Store an image and description."""
        self.storage.append((image_content, image_description))

    def get_random_id(self):
        """ Get a random guess."""
        return random.randint(0, len(self.storage) - 1) if self.storage else None

    def get_image_by_id(self, key):
        """ Get an image by id."""
        if (key < 0 or key > len(self.storage) - 1):
            return None
        return self.storage[key][0]

    def get_guess_secret(self, key):
        """ Get a guess secret."""
        if (key < 0 or key > len(self.storage) - 1):
            return None
        _, guess_secret = self.storage[key]
        return guess_secret
