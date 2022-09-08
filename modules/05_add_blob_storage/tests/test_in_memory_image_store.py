from src.in_memory_storage import InMemoryStorage, StorageItem  # pylint: disable = import-error


def test_is_empty():
    storage = InMemoryStorage()
    assert storage.is_empty()

    storage.add(StorageItem(
        image_url="image_url",
        secret_word="a cat 1",
    ))
    assert not storage.is_empty()


def test_get_random_index_when_one_item():
    storage = InMemoryStorage()
    storage.add(StorageItem(
        image_url="image1",
        secret_word="a cat 1",
    ))
    # when there's only one item, the only index we can get from the method is 0
    assert storage.get_random_item_index() == 0


def test_get_random_image_when_one_image():
    storage = InMemoryStorage()
    storage_item = StorageItem(
        image_url="image1",
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
        image_url="image1",
        secret_word="a cat 1",
    ))

    assert storage.has_index(0)
    assert not storage.has_index(1)
    assert not storage.has_index(2)

    storage.add(StorageItem(
        image_url="image2",
        secret_word="a cat 2",
    ))

    assert storage.has_index(0)
    assert storage.has_index(1)
    assert not storage.has_index(2)
