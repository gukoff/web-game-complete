from flask import Flask, flash, render_template, request, redirect, session
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


@app.route('/guess', methods=['GET'])
def guess():
    if 'secret_word_id' in session:
        if database.get_secret_word_by_id(session['secret_word_id']) is not None:
            return render_template('guess.html')

    word_id = database.get_random_word_id()
    if word_id is None:
        flash("No words uploaded yet! Please upload at least one word to start guessing")
        return redirect("/")

    session['secret_word_id'] = word_id

    return render_template('guess.html')


@app.route('/make_a_guess', methods=['POST'])
def make_a_guess():
    secret_word = database.get_secret_word_by_id(session['secret_word_id'])

    if request.form['guessed_word'] == secret_word:
        flash("You guessed right! Good job!")
        del session['secret_word_id']
        return redirect('/')

    flash("You didn't guess right! Try again!")
    return redirect('/guess')


@app.route('/upload_word', methods=['GET', 'POST'])
def upload_word():
    if request.method == "GET":
        return render_template('upload_word.html')

    secret_word = request.form['secret']
    database.add_guess(secret_word)
    flash("Uploaded the secret " + repr(secret_word))
    return redirect('/')
