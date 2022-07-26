from app.backend.store.inmemory_image_store import InMemoryImageStore

def test_get_random_image_when_empty_store():
    store = InMemoryImageStore()
    assert store.get_random_image() is None

def test_get_random_image_when_one_image():
    store = InMemoryImageStore()
    image = (b"base64image", "a cat")
    store.store_image(image[0], image[1])
    assert store.get_random_image()[1] == image[0]

def test_get_image_description():
    store = InMemoryImageStore()
    store.images = {"id1": (b"image_content_1", "cat")}
    image_description = store.get_image_description("id1")
    assert image_description == "cat"

def test_get_image_description_empty_store():
    store = InMemoryImageStore()
    image_description = store.get_image_description("id1")
    assert image_description is None