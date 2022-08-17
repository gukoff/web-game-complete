from src.in_memory_storage import InMemoryStorage  # pylint: disable = import-error


def test_get_random_image_when_empty_store():
    store = InMemoryStorage()
    assert store.get_random_id() is None


def test_get_random_image_when_one_image():
    store = InMemoryStorage()
    image = ((r"text/plain", b"base64image"), "a cat 1")
    store.add_guess(image[0], image[1])
    assert store.get_image_by_id(0) == image[0]


def test_get_image_description():
    store = InMemoryStorage()
    store.add_guess((r"text/plain", b"image_content_1"), "cat")
    image_description = store.get_guess_secret(0)
    assert image_description == "cat"


def test_get_image_description_empty_store():
    store1 = InMemoryStorage()
    image_description = store1.get_guess_secret(0)
    assert image_description is None
