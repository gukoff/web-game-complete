import random

class InMemoryImageStore:
    """
        InMemory store to store images.
    """
    
    def __init__(self) -> None:
        self.images = []    

    def store_image(self, image_content, image_description: str):
        """ Store an image and description."""
        self.images.append((image_content, image_description))

    def get_random_id(self):
        """ Get a random image."""
        return random.randint(0, len(self.images) - 1) if self.images else None

    def get_image_by_id(self, key):
        """ Get an image by id."""
        if (key < 0 or key > len(self.images) - 1):
            return None
        return self.images[key][0]
    
    def get_image_description(self, key):
        """ Get an image description."""
        if (key < 0 or key > len(self.images) - 1):
            return None
        _, image_description = self.images[key]
        return image_description