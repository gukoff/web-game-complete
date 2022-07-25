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

    @staticmethod
    def test_get_image_description():
        store = InMemoryImageStore()
        store.images = {"id1": ("image_content_1", "cat")}
        image_description = store.get_image_description("id1")
        assert image_description == "cat"

    @staticmethod
    def test_get_image_description_empty_store():
        store = InMemoryImageStore()
        image_description = store.get_image_description("id1")
        assert image_description is None