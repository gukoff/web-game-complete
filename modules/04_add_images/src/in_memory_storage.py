import random
from dataclasses import dataclass


@dataclass(frozen=True)
class StorageItem:
    image_bytes: bytes
    image_content_type: str
    secret_word: str


class InMemoryStorage:
    """
    InMemory storage to store game items: secret words and hint images.
    """

    def __init__(self):
        self.storage: list[StorageItem] = []

    def add(self, item: StorageItem) -> None:
        """ Store a secret word with the image."""
        self.storage.append(item)

    def get_all_secrets(self) -> list[str]:
        """ Get all secret words saved so far. """
        return [item.secret_word for item in self.storage]

    def has_index(self, index: int) -> bool:
        """ Does the storage contain the given index? """
        return 0 <= index < len(self.storage)

    def get_random_item_index(self) -> int:
        """ Get an index of a random secret image."""
        return random.randint(0, len(self.storage) - 1)

    def get_item_by_index(self, index: int) -> StorageItem:
        """
        Return the item by the index from the storage.
        """
        return self.storage[index]

    def is_empty(self) -> bool:
        """
        Is the storage empty?
        """
        return not self.storage
