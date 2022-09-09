from dataclasses import dataclass


@dataclass(frozen=True)
class StorageItem:
    image_url: str
    secret_word: str

