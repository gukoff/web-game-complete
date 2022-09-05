from flask import Flask, flash, render_template, request, redirect, session, Response
from markupsafe import Markup

from .in_memory_storage import InMemoryStorage, StorageItem

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
    if database.is_empty():
        flash("No images uploaded yet! Please upload at least one image to start guessing")
        return redirect("/")

    if ('secret_item_id' not in session or
        not database.has_index(session['secret_item_id'])
    ):
        # need to renew 'secret_item_id' in the session.
        # it's either missing or left over from the old version of the app
        session['secret_item_id'] = database.get_random_item_index()

    return render_template('game.html')  # continue the game

@app.route('/image', methods=['GET'])
def get_image():
    item_id = int(request.args['item_id'])
    item = database.get_item_by_index(item_id)
    return Response(item.image_bytes, mimetype=item.image_content_type)


@app.route('/make_a_guess', methods=['POST'])
def make_a_guess():
    secret_item_id = session['secret_item_id']
    secret_item = database.get_item_by_index(secret_item_id)

    if request.form['guessed_word'] == secret_item.secret_word:
        flash(Markup("You guessed right! Good job! The secret word was <b>%s</b>" % secret_item.secret_word))
        del session['secret_item_id']
        return redirect('/')

    flash("You didn't guess right! Try again!")
    return redirect('/game')


@app.route('/images', methods=['GET'])
def upload_image_page():
    return render_template('images.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    secret_word = request.form['secretWord']
    image_file = request.files['image']

    if not secret_word:
        flash('No secret word added! Please try uploading again')
        return redirect('/images')

    # If the user submits the form but doesn't select a file,
    # the browser submits an empty file without a filename.
    if not image_file.filename:
        flash('No file selected! Please try uploading again')
        return redirect('/images')

    image_bytes = image_file.stream.read()
    image_content_type = image_file.content_type
    database.add(StorageItem(
        image_bytes=image_bytes,
        image_content_type=image_content_type,
        secret_word=secret_word,
    ))
    flash("Uploaded image with secret word:" + repr(secret_word))
    flash("All available secret words:: " + repr(database.get_all_secrets()))
    return redirect('/images')
