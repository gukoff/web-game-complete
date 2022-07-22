import random

class InMemoryImageStore:
    """
        InMemory store to store images.
    """
    images = []

    def store_image(self, image_content: bytes, image_description: str):
        """ Store an image and description."""
        self.images.append((image_content, image_description))

    def get_random_image(self):
        """ Get a random image."""
        return random.choice(self.images) if len(self.images) else None