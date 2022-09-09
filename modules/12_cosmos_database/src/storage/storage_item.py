from dataclasses import dataclass


@dataclass(frozen=True)
class StorageItem:
    image_bytes: bytes
    image_content_type: str
    secret_word: str
