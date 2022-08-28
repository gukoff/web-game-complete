# In memory storage

## Goal

Implement an interactive web app where you can:
- upload words to the game dictionary;
- play a game of guessing a word from the dictionary.

## Tutorial

> In this tutorial we will assume that you've completed the previous tutorial
and already have a python project with `app.py`, `src/api.py` and `src/templates`.

### Part 1. Uploading words

#### Intro

In the previous stage, we have implemented a so-called "static" website, where
you can get pages from the server, but their content is always the same.

Now it's time to **upload** data to the server! In our case, upload words to the dictionary.

To do this, we'll need:
1. a text field on the web page with a button "submit" (this will send data to the server)
2. an endpoint on the server that would accept this data.

#### 1. Create HTML page for word upload

Let's create a web page that will contain a text field for the word to upload and a button `submit`.

Create a new file `upload_word.html` in the folder `templates`:

```shell
touch templates/upload_word.html
```

Inherit it from `base.html`, like we did it in the previous stage, and put the following form inside `block content`:

```html
<form action = "/upload_word" method = "POST" enctype="multipart/form-data">
    <div class="form-group">
        <label for="secretId">Secret</label>
        <input type="text" class="form-control" id="secretId" name="secretWord" aria-describedby="secretHelp" placeholder="Secret Word">
        <small id="secretHelp" class="form-text text-muted"></small>
    </div>

	<button type="submit" class="btn btn-primary">Submit</button>
</form>
```

#### 2. Serve this HTML page on HTTP endpoint

To let users open this page, add a new endpoint in `api.py`:

```python
@app.route('/words', methods=['GET'])
def upload_word_page():
    return render_template('words.html')
```

Now start the app, and verify that you can see this form on the endpoint `/words`.

> Most likely, the app will start on localhost:5000. In this case you can use this link to open the page:
> [http://localhost:5000/words](http://locahost:5000)


When you type in a word in the form and click "submit", your browser will try to
send it to the endpoint `/upload_word`. This is the endpoint we specified in the
`action` attribute of the form.

Because this endpoint doesn't exist yet, in the browser you'll see a "Not Found" page,
and in the logs of the running application you'll see the following entry:

```
127.0.0.1 - - [01/Jan/2022 11:12:34] "POST /upload_word HTTP/1.1" 404 -
```

#### 3. Accept form data on the server

Let's create the endpoint `/upload_word` that will actually accept the form data.

```python
from flask import redirect, request

@app.route('/upload_word', methods=['POST'])  # browsers send POST request when submitting a form
def upload_word():
    # request.form is a special variable in Flask that will contain the form data
    secret_word = request.form['secretWord']  # note the "name" attribute of the <input> we have in HTML
    print("Uploaded word " + repr(secret_word))
    return redirect('/')  # redirect back to the main page
```

Run the application, try uploading a word, and verify that the upload works now. 
Verify that in the application log you see the uploaded word. 

#### 4. Give user feedback

It's good to give the user know too, that the word was uploaded.

Flask has a concept of flashing that we can use. In the logic of our endpoint we 
would "flash" one or more messages, and these messages will become available 
to us when rendering a template that we show to the user.

> More detailed explanation of flashing you can find in the [documentation](https://flask.palletsprojects.com/en/2.2.x/patterns/flashing/).

First, instead of `print` in the endpoint logic, use `flask.flash`:

```python
from flask import flash

...
    flash("Uploaded word " + repr(secret_word))
...
```

Second, render the flashed messages on the page.
Better add this logic right to the base template `base.html`,
this way all pages inherited from it will learn to display flashed messages.

```html
    <div class="container">
  
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="flashes">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    </div>
```

Run the app, try uploading words again. Verify that now you get a message on the top of the page
that your word was uploaded successfully.

### Part 2. Word storage

#### Intro

Now we know how to send words to the server and back, let's store the uploaded words.
This way we'll actually be able to play the game of guessing one word of the many uploaded.

Usually one uses an external database to store data there and read if from there, but we'll start simple.
We will store everything right on the server, in the memory of our program.

#### 1. Create a class for the word storage

Let's create a new Python `class` in `src/in_memory.storage.py`:

```python
class InMemoryStorage:
    def __init__(self):
        self.storage = []

    def add_word(self, secret_word: str) -> None:
        """ Store a secret word."""
        self.storage.append(secret_word)

    def get_all_words(self):
        """ Get all words saved so far. """
        return self.storage
```

We will be able to use it like this:
```python
from src.in_memory_storage import InMemoryStorage

storage1 = InMemoryStorage()  # create a new object of this class
storage1.add_word("dog")
print(storage1.get_all_words())  # prints ['dog']
storage1.add_word("cat")
print(storage1.get_all_words())  # prints ['dog', 'cat']

storage2 = InMemoryStorage()  # create another object of this class
print(storage2.get_all_words())  # prints empty list []
storage2.add_word("boo!")
print(storage2.get_all_words())  # prints ['boo!']
```

#### 2. Save words to the in-memory storage

On the top of the file `api.py`, create our "database" - an object of the class InMemoryStorage.

```python
from src.in_memory_storage import InMemoryStorage

database = InMemoryStorage()
```

This variable will be visible to all endpoints in `api.py`, and they all will be able to read from it
or write to it.

Change the endpoint `/upload_word` so that it uses the database:

```python
from src.in_memory_storage import InMemoryStorage

database = InMemoryStorage()

@app.route('/upload_word', methods=['POST'])
def upload_word():
    secret_word = request.form['secretWord']
    database.add_word(secret_word)  # save word to the db
    flash("Uploaded word " + repr(secret_word))
    flash("All available words: " + repr(database.get_all_words()))  # display all words saved so far
    return redirect('/')
```

Run the app, try uploading words again. Verify that now you get more informative messages,
and that the server now remembers all the words you've uploaded so far.

> Caveat: Because we store words in memory, this storage is alive as long as the server itself
> is alive. If you shut down the server, its memory is released, and all saved words will be forgotten.

> Caveat: storing words in memory also doesn't play well with running Flask in DEBUG mode.
> Flask in DEBUG mode restarts the server every time you've changed something in the code,
> which again means losing all the saved words.

### Part 3. The Game

#### Intro

The game of guessing words will go as follows:

- the user visits a `/game` page;
- our server chooses a secret word the user has to guess;
- the user sends their guesses through a form until they get it right;
- if they get it right, they are congratulated and redirected back to the main page.

Note that until the user wins the game, we need to remember the secret word that they have to guess.

We did something similar when we were storing all uploaded words in the database. But this case is different:
if multiple players visit our server, we want them to play with the same, common set of words, but their
games shouldn't interfere. Each player should play their own game, they can't all share the secret word
to guess like the share the pool of possible words.

Here we'll make use a new concept - a "session". A session makes it possible to remember information 
from one request to another, and every visitor of our website has their own session. We can
save the word to guess in the session, and it will stay the same throughout the game, until we decide
to change it ourselves.

> More about sessions - in [flask docs](flashttps://flask.palletsprojects.com/en/2.2.x/api/#sessions)

#### 1. Enable flask sessions

Flask will create sessions only after we configure it some secret key.

Add a secret key to your app:

```python
app = Flask(__name__)
# This key guarantees security of the sessions, and must be kept secret.
# When creating a serious service, you should never commit a secret key in plain text 
# to the codebase. We will cut the corner here just to make sessions work,
# but you should know this is insecure. 
app.secret_key = "f3cfe9ed8fae309f02079dbf"  # random string
```

#### 2. Create the game page

Let's create an HTML page `src/templates/game.html` with a form:

```html
{% extends "base.html" %}

{% block content %}

Please guess the secret word: <br/>

<form action="/make_a_guess" method="POST">
    <input type="text" name="guessed_word"/>
    <input type="submit"/>
</form>

{% endblock %}
```

Serve it from an endpoint:

```python
@app.route('/game', methods=['GET'])
def game():
    return render_template('game.html')
```

Add a link to this new page from the main page `home.html`:

```html
<a href="./game">Play The Game</a>
```

And add a POST endpoint that would accept the form data:

```python
@app.route('/make_a_guess', methods=['POST'])
def make_a_guess():
    guessed_word = request.form['guessed_word']
    flash('Tried to guess the word ' + repr(guessed_word))
    return redirect('/game')  # redirect back to the game page
```

Start the app, verify the pages render well. (The game itself is not functional at this point)

#### 3. Choose secret word for the game

When the game starts, we should choose a secret word, save it to user's session, 
and only delete it from there when they have guessed the word correctly.

Let's modify our endpoints accordingly:

```python
import random
from flask import session, Markup


@app.route('/game', methods=['GET'])
def game():
    all_words = database.get_all_words()

    if not all_words:
        flash("No words uploaded yet! Please upload at least one word to play the game")
        return redirect("/")

    if (
        'secret_word' not in session or  # no secret word set -> need to start new game
        session['secret_word'] not in all_words  # secret word is set, but it's invalid -> need to start new game
    ):
        random_word = random.choice(all_words)  # choose a random word from the pool
        session['secret_word'] = random_word  # and save it to the session
    
    return render_template('game.html')  # let them play the game


@app.route('/make_a_guess', methods=['POST'])
def make_a_guess():
    if 'secret_word' not in session:  # this should never happen :)
        flash("You can't guess words without starting the game!")
        return redirect('/game')  # let the user start a new game

    if request.form['guessed_word'] == session['secret_word']:
        flash(Markup("You guessed right! Good job! The secret word was <b>%s</b>" % session['secret_word']))
        del session['secret_word']  # delete the word from the session as this game is finished
        return redirect('/')

    flash("You didn't guess right! Try again!")
    return redirect('/game')
```

Start the app, verify the game works!

### Part 4. Addressing security

#### Intro

To make the game work, we saved the game context - the secret word - in the flask session.

Flask stores sessions as signed cookies in the browser, and the users, if they want, can 
find this cookie and read the data in the session!

This is a security breach - the users can cheat and always guess the secret word from the first try.
Let's try to make it harder to do for them!

#### 1. Demonstrate cheating

Start the app, upload some words, and navigate to the `/game` page. 
The server at this point should choose a word for you to guess and save it to the session.

Open the cookies in your browser.

Chrome:

`Menu > More tools > Developer Tools > Application > Storage > Cookies`

Firefox:

`Menu > More tools > Web Developer Tools > Storage > Cookies`

Safari:

- [Enable dev tools](https://support.apple.com/guide/safari/use-the-developer-tools-in-the-develop-menu-sfri20948/mac)
- `Develop > Show Web Inspector > Storage > Cookies`

Edge:

`Menu > More tools > Developer Tools > Application > Storage > Cookies`

Find a cookie with name "session" and a long value starting with "ey". It contains your encoded session data.

Copy this value to https://www.base64decode.org/, and decode it. 
In the decoded data, you should see the secret word that you can use to guess th word from the first try!

#### 2. Hide the words

Instead of giving the user a secret word in plain text, let's give them the _index_ of this word in our 
storage. Since they don't have direct access to the storage, they won't know the word from the index.

Add new methods to our storage:

```python
import random
from typing import Optional

class InMemoryStorage:
    ...
    
    def get_random_word_index(self) -> Optional[int]:
        """ Get an index of a random secret word."""
        if not self.storage:
            return None  # no words saved - nothing to return
        return random.randint(0, len(self.storage) - 1)

    def get_word_by_index(self, index: int) -> Optional[str]:
        """
        Given the index in the storage, return the secret word by this index.
        """
        if not (0 <= index < len(self.storage)):
            return None  # index out of range - nothing to return
        return self.storage[index]
```

And use the index instead of the word itself during the game:

```python
@app.route('/game', methods=['GET'])
def game():
    if 'secret_word_id' in session:
        if database.get_word_by_index(session['secret_word_id']) is not None:
            return render_template('game.html')

    word_id = database.get_random_word_index()
    if word_id is None:
        flash("No words uploaded yet! Please upload at least one word to start guessing")
        return redirect("/")

    session['secret_word_id'] = word_id

    return render_template('game.html')


@app.route('/make_a_guess', methods=['POST'])
def make_a_guess():
    if 'secret_word_id' not in session:  # this should never happen
        flash("You can't guess words without starting the game first!")
        return redirect('/game')

    secret_word = database.get_word_by_index(session['secret_word_id'])

    if request.form['guessed_word'] == secret_word:
        flash(Markup("You guessed right! Good job! The secret word was <b>%s</b>" % secret_word))
        del session['secret_word_id']
        return redirect('/')

    flash("You didn't guess right! Try again!")
    return redirect('/game')
```

Run the service, play the game, verify that it works.
Decode the session cookie again, verify that now it contains just the index instead of the secret word itself. 

### Part 5. Recap

We've created a real mini-game. We learned how to:

- upload data from an HTML page to the server: using forms and POST requests;
- save data in memory to share it between all users of the server as long as the server is alive;
- save data to user sessions to share it between requests of _the same user_;
- read data from the session in the browser to demonstrate that you never should store secrets in the Flask session. 

Now you can think how you can further improve this game! For example:

- How to add hints to the game? I.e. a user would upload a word "red" with a hint "color of a tomato",
  and on the game page you'd display the hint.
- How to make the game more forgiving to spelling? I.e. when a secret word is "red", also accept a guess "Red".
- How to let user know how close they are to the answer for them to not guess blindly? I.e. we can consider
  a guess "rid" very close to "red" because they share many common letters. 
- How to restrict cheating even more? Word indexes in the session are more secure than the words  
  themselves, but eventually the player will learn what index corresponds to which word.


TODO: Potential additional topics to cover: testing and debugging
