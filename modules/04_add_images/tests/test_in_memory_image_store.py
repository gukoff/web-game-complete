from src.in_memory_storage import InMemoryStorage, StorageItem  # pylint: disable = import-error


def test_get_random_image_when_empty_storage():
    storage = InMemoryStorage()
    assert storage.get_random_item_index() is None


def test_get_random_image_when_one_image():
    storage = InMemoryStorage()
    storage_item = StorageItem(
        image_content_type="text/plain",
        image_bytes=b"base64image",
        secret_word="a cat 1",
    )
    storage.add(storage_item)
    assert storage.get_random_item_index() == 0
    assert storage.get_item_by_index(0) == storage_item
