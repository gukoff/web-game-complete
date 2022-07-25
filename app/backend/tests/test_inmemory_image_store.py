from store.inmemory_image_store import InMemoryImageStore

class TestInMemoryImageStore():

    def test_get_random_image_when_empty_store(self):
        store = InMemoryImageStore()
        assert store.get_random_image() == None

    def test_get_random_image_when_one_image(self):
        store = InMemoryImageStore()
        image = ("base64image", "a cat")
        store.store_image(image[0], image[1])
        assert store.get_random_image() == image