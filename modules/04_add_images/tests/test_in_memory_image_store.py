from src.in_memory_storage import InMemoryStorage, StorageItem  # pylint: disable = import-error


def test_get_random_image_when_empty_storage():
    storage = InMemoryStorage()
    assert storage.is_empty()


def test_get_random_image_when_one_item():
    storage = InMemoryStorage()
    storage.add(StorageItem(
        image_content_type="text/plain",
        image_bytes=b"base64image",
        secret_word="a cat 1",
    ))
    # when there's only one item, the only index we can get from the method is 0
    assert storage.get_random_item_index() == 0


def test_get_random_image_when_one_image():
    storage = InMemoryStorage()
    storage_item = StorageItem(
        image_content_type="text/plain",
        image_bytes=b"base64image",
        secret_word="a cat 1",
    )
    storage.add(storage_item)
    assert storage.get_item_by_index(0) == storage_item


def test_has_index():
    storage = InMemoryStorage()

    assert not storage.has_index(0)
    assert not storage.has_index(1)
    assert not storage.has_index(2)

    storage.add(StorageItem(
        image_content_type="text/plain",
        image_bytes=b"base64image",
        secret_word="a cat 1",
    ))

    assert storage.has_index(0)
    assert not storage.has_index(1)
    assert not storage.has_index(2)

    storage.add(StorageItem(
        image_content_type="text/plain",
        image_bytes=b"base64image",
        secret_word="a cat 2",
    ))

    assert storage.has_index(0)
    assert storage.has_index(1)
    assert not storage.has_index(2)
