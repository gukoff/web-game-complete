import random
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StorageItem:
    image_bytes: bytes
    image_content_type: str
    secret_word: str


class InMemoryStorage:
    """
        InMemory store to store secret images.
    """

    def __init__(self):
        self.storage: list[StorageItem] = []

    def add(self, item: StorageItem) -> None:
        """ Store a secret image."""
        self.storage.append(item)

    def get_all_secrets(self) -> list[str]:
        """ Get all images saved so far. """
        return [item.secret_word for item in self.storage]

    def has_index(self, index: int) -> bool:
        return 0 <= index < len(self.storage)

    def get_random_item_index(self) -> Optional[int]:
        """ Get an index of a random secret image."""
        if not self.storage:
            return None  # no images saved - nothing to return
        return random.randint(0, len(self.storage) - 1)

    def get_item_by_index(self, index: int) -> StorageItem:
        """
        Return the item by the index from the storage.
        """
        return self.storage[index]
