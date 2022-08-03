from ..inmemory_image_store import InMemoryImageStore

def test_get_random_image_when_empty_store():
    store = InMemoryImageStore()
    assert store.get_random_id() is None

def test_get_random_image_when_one_image():
    store = InMemoryImageStore()
    image = ((r"text/plain", b"base64image"), "a cat 1")
    store.store_image(image[0], image[1])
    assert store.get_image_by_id(0) == image[0]

def test_get_image_description():
    store = InMemoryImageStore()
    store.images = [((r"text/plain", b"image_content_1"), "cat")]
    image_description = store.get_image_description(0)
    assert image_description == "cat"

def test_get_image_description_empty_store():
    store1 = InMemoryImageStore()
    image_description = store1.get_image_description(0)
    assert image_description is None