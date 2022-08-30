from flask import Flask, flash, render_template, request, redirect, session
from markupsafe import Markup

from .in_memory_storage import InMemoryStorage

APP_VERSION = '0.0.1'

app = Flask(__name__)
app.secret_key = "f3cfe9ed8fae309f02079dbf"

database = InMemoryStorage()


@app.context_processor
def inject_app_version():
    return dict(app_version=APP_VERSION)


@app.route('/')
def home():
    return render_template('home.html')


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


@app.route('/words', methods=['GET'])
def upload_word_page():
    return render_template('words.html')


@app.route('/upload_word', methods=['POST'])
def upload_word():
    secret_word = request.form['secret']
    database.add_word(secret_word)
    flash("Uploaded word " + repr(secret_word))
    flash("All available words: " + repr(database.get_all_words()))
    return redirect('/')
