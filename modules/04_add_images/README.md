# Add Images

## Goal

Implement an interactive web app where you can:
- upload pairs (image + secret word) to the game database (word describes the image);
- play a game of guessing the word from the image.

In the previous stage, we created an app where we upload and store words.
Now we will also upload images. Images need to be uploaded, stored,
and shown to the user on the game page, therefore we'll extend the
HTML upload form, endpoint that accepts data from it, storage format, 
and the game page.

## Tutorial

> In this tutorial we will assume that you've completed the previous tutorial
and already have a game where you guess words but without an image hint.

### Part 1. Upload images

#### Intro

#### 1. Add a second input to the form 

In the previous stage we've created the file `words.html` with a 
form for word upload. Add a new input field with type "file" to the form, e.g.:

```html
<div class="form-group">
    <label for="Image">Image</label>
    <input type="file" class="form-control" id="imageId" name="image" placeholder="image" required>
    <small id="imageHelp" class="form-text text-muted">Image that describes the word</small>
</div>
```

Now, when you submit a form, both the word and the selected image will be uploaded
to the server.

#### 2. Accept the image on the server

In flask, uploaded files can be accessed through a special variable `request.files`.

Add the following code to the endpoint that accepts the form data:

```python
...
    secret_word = request.form['secretWord']
    image_file = request.files['image']  # 'image' is the name of the input in HTML

    image_bytes = image_file.stream.read()  # actual image content
    image_content_type = image_file.content_type  # mime type, e.g. image/png, image/jpeg

    flash('Uploaded %s bytes of type %s' % (len(image_bytes), image_content_type))
```

Run the app, upload an image, and verify that you see a notification about a successful upload. 
It should say something like `Uploaded 829646 bytes of type image/jpeg`.

### Part 2. Store images

#### Intro

We will modify `InMemoryStorage` to be able to store mor than just words
Now that we need to store more than just words, it's time to make `InMemoryStorage` 
more "generic". This means, make the storage less independent of the type of the stored
items.

#### 1. Generic item type

Instead of just words, we now need to store combinations of `(word, image)`.

Let's make our storage oblivious to the exact object types that it stores, 
and  always store objects of a new class `StorageItem`.

This `StorageItem` class will encapsulate whatever data we want to store: 
before it could be a single word, now it will be `(word, image)`, later
we might want to add more and more stuff to it.

Such classes are called data-transfer-object (or DTOs), and a handy way
to create them in Python are dataclasses. Create the following class
in `in_memory_storage.py`:

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # 'frozen' makes it immutable - always good by default
class StorageItem:
    secret_word: str  # now only contains a secret word, but later we'll add an image here!
```

#### 2. Migrate InMemoryStorage to using StorageItem

Let's change `InMemoryStorage` to operate `StorageItem`-s instead of 
secret words directly. 

You can use this implementation as an example:

```python
class InMemoryStorage:
    def __init__(self):
        self.storage: list[StorageItem] = []

    def add(self, item: StorageItem) -> None:
        self.storage.append(item)

    def get_all_secrets(self) -> list[str]:
        return [item.secret_word for item in self.storage]

    def has_index(self, index: int) -> bool:
        return 0 <= index < len(self.storage)

    def get_random_item_index(self) -> int:  # raises exception if empty
        return random.randint(0, len(self.storage) - 1)

    def get_item_by_index(self, index: int) -> StorageItem:  # raises exception if empty
        return self.storage[index]

    def is_empty(self) -> bool:
        return not self.storage
```

Don't forget to update the places where this storage is used! 

E.g. before you could write:

```python
database.add_word(word)
...
word = database.get_word_by_index(0)
```

But now it will be:

```python
database.add(StorageItem(secret_word=word))
...
item = database.get_item_by_index(0)
word = item.secret_word
```

These are quite a few changes, and it's easy to make a mistake! 
After you're done, please run the app and verify that everything still works 
like it used to.

#### 3. Add images to the StorageItem

Remember how we receive the image along with the word? Let's store the image too!
Extend `StorageItem` with the image-related fields:

```python
@dataclass(frozen=True)
class StorageItem:
    image_bytes: bytes
    image_content_type: str
    secret_word: str
```

And when you create a storage item, pass these new fields to the constructor:

```python
...
    image_bytes = image_file.stream.read()
    image_content_type = image_file.content_type
    database.add(StorageItem(
        image_bytes=image_bytes,
        image_content_type=image_content_type,
        secret_word=secret_word,
    ))
```

#### 4. Revisit naming

Go through the code and find where it doesn't make sense to call things "word" anymore.

Maybe you'd like to rename the endpoint "/upload_word" to "upload_image", or
the session variable "secret_word_id" to "secret_item_id".

Find the naming that makes the most sense for you.

And if you changed anything, run the app and verify it works well.

### Part 3. Game

#### Intro

Now that the image is stored, we can display it during the game as a "hint"
for the word to guess.

There are many ways to do it. We'll do it this way:
- make all images available by the item id on a new endpoint, i.e. make all images publicly available by links.
- inject the right image link to the game page when rendering it.

#### 1. Make images available in the API

Flask uses a special variable `request.args` to store URL parameters.

Add the following endpoint ot your code:

```python
@app.route('/image', methods=['GET'])
def get_image():
    item_id = int(request.args['item_id'])
    item = database.get_item_by_index(item_id)
    return Response(item.image_bytes, mimetype=item.image_content_type)
```

Now each image has its own public link!

Run the app, upload an image, and verify that you can see this image
`/image?item_id=0`. 
Upload another one, and verify you can see it on `/image?item_id=1`.

#### 2. Inject the link to the image to the game page

This is surprisingly easy to do.
The index of the item to guess is stored in the flask session, 
and jinja can access the session when rendering a template.

Add the following line to `game.html`: 

```html
<img src="/image?item_id={{ session['secret_item_id'] }}" style="max-height:800px;max-width:800px;height:auto;width:auto;">
```

(If the index value in your session is called something else than `secret_item_id`, 
use the right name here)

Run the game, and check that you can see the image that describes this word on the game page.

### Part 4. Unit tests

- TODO

### Part 5. Recap

Now you can think how you can further improve this game! For example:

- How to ensure the uploaded files are actually images?
- How to limit the acceptable image size?
