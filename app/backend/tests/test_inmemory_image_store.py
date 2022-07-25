from app.backend.store.inmemory_image_store import InMemoryImageStore

class TestInMemoryImageStore():

    @staticmethod
    def test_get_random_image_when_empty_store():
        store = InMemoryImageStore()
        assert store.get_random_image() == None

    @staticmethod
    def test_get_random_image_when_one_image():
        store = InMemoryImageStore()
        image = ("base64image", "a cat")
        store.store_image(image[0], image[1])
        assert store.get_random_image()[1] == image[0]