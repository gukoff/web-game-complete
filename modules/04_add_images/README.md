# Add Images

## Goal

Implement an interactive web app where you can:
- upload pairs (image, word), where the word describes the image, to the game database;
- play a game of guessing the word from the image.

## Tutorial

> In this tutorial we will assume that you've completed the previous tutorial
and already have a game where you guess words but without an image hint.

In the previous stage, we created a game with words. The difference is now we also have images. 
Images need to be uploaded, stored, and shown to the user on the game page.
Therefore, we'll need to extend functionality of the HTML upload form, 
the endpoint that accepts form data, the storage format, and the game page.

### Part 1. Upload images

#### Intro

HTML forms are perfectly capable of uploading files, not only text.
You've seen this many times: a button "Upload file" where you can
attach a file from your local computer before form submission.
This is exactly what we'll do to upload the images.

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

_(If the secret item index in your session is called something else than `secret_item_id`, 
use the right name here)_

Run the game, and check that you can see the image that describes this word on the game page.

The game is now complete!

### Part 4. Unit tests for InMemoryStorage

#### Intro

In a professional setting, we always try to cover the code with automatic tests
as much as possible.

This has many benefits, including:
- you don't need to restart the app and test it manually after every change, 
  you can press a button and the tests will verify correctness in a matter of seconds;
- somebody else can contribute to your project even if they don't understand it
  fully - they can run tests and make sure they haven't broken anything;
- you can configure GitHub to automatically run tests on every pull request and after
  merging code to the main branch, ensuring correctness of the code in the repo.

There are many types of tests. Now we will focus on the so-called **unit tests** - 
fast tests with a small scope - and will test our InMemoryStorage.

#### 1. Install testing framework

We will use `pytest`, one of the popular testing frameworks for Python.

To install it, add `pytest` to your `requirements.txt` file.
Your IDE will most likely react to the change in this file and automatically 
install pytest, but to be surem you can manually reinstall all dependencies
by calling `pip install -r requirements.txt` in the project folder.

#### 2. Create your first test 

In the root of your project, where you have the `src` folder, create a new 
folder `tests`. In this folder, create a file `test_in_memory_image_store.py`
with a following function:

```python
from src.in_memory_storage import InMemoryStorage


def test_is_empty():
    storage = InMemoryStorage()  # create empty storage
    assert storage.is_empty()  # verify it's empty when it's just created
```

Run this test by running `pytest` in the root folder of your project.
You should see a report about a successful test run:

```txt
============================================================== test session starts ===============================================================
platform linux -- Python 3.10.6, pytest-7.1.3, pluggy-1.0.0
rootdir: /workspaces/my-web-game/
collected 1 item                                                                                                                                 

tests/test_in_memory_image_store.py .                                                                                                      [100%]

=============================================================== 1 passed in 0.05s ================================================================
```

Notice how we didn't give pytest a direct path to our test, but it still found it.
This is made possible by pytest's [test discovery](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#conventions-for-python-test-discovery).
As long as you prefix your test files and test functions with "test_", pytest
will find them and consider them tests.

#### 3. Add a second test

To the same file, add another function:

```python
from src.in_memory_storage import StorageItem


def test_get_random_index_when_one_item():
    storage = InMemoryStorage()
    storage.add(StorageItem(
        image_content_type="text/plain",
        image_bytes=b"not important",
        secret_word="cat",
    ))
    # when there's only one item, the only index we can get from the method is 0
    assert storage.get_random_item_index() == 0
```

Execute `pytest` again, verify that now it has successfully run more tests.

#### 3. Write more tests!

Now it's your turn! 

Write tests for the rest of the methods of InMemoryStorage.
It's very good to have multiple tests for the same method,
if you can think of multiple scenarios that are worth testing.

### Part 5. Recap

We've developed web-game where you can guess a word from the image.
We learned how to:
- upload files to the server from an HTML form;
- work with uploaded files in flask
- use `dataclass` to group multiple objects in the same "container" class;
- test our code with `pytest`;

Now you can think how you can further improve this game! For example:

- How to ensure the uploaded files are actually images?
- How to limit the acceptable image size?
- How would you test the endpoints of the flask application? 
