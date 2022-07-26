import random
import uuid

class InMemoryImageStore:
    """
        InMemory store to store images.
    """

    def __init__(self):
        # tuple of base64 image content and image description, indexed by id.
        self.images = {}

    def store_image(self, image_content: bytes, image_description: str):
        """ Store an image and description."""
        image_id = uuid.uuid1()
        self.images[image_id] = (image_content, image_description)

    def get_random_image(self):
        """ Get a random image."""
        if not images: 
            return None
        image_id = random.choice(list(self.images.keys()))
        return (image_id, self.images[image_id][0])

    def get_image_description(self, image_id):
        image = self.images.get(image_id)
        return None if image is None else image[1]
