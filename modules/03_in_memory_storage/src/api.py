from flask import Flask, flash, render_template, request, redirect, session
from .in_memory_storage import InMemoryStorage

APP_VERSION = '0.0.1'

app = Flask(__name__)
app.secret_key = "f3cfe9ed8fae309f02079dbf"

database = InMemoryStorage()


@app.route('/')
def home():
    return render_template('home.html')


@app.context_processor
def inject_app_version():
    return dict(app_version=APP_VERSION)


@app.route('/guess')
def guess():
    if database.get_guess_secret(session['selection']):
        return render_template('guess.html')

    img_id = database.get_random_id()
    if img_id is None:
        flash("no images uploaded yet")
        return redirect("/")

    session['selection'] = img_id

    return render_template('guess.html')


@app.route('/guess_result', methods=['POST'])
def guess_result():
    result = request.form
    secret_description = database.get_guess_secret(session['selection'])

    if result['guess_secret'] == secret_description:
        flash("You guessed right!")
        session['selection'] = None
        return render_template('home.html')

    flash("You didn't guess right! Try again!")
    return render_template('guess.html', result=result)


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    result = request.form

    if request.method == "GET":
        return render_template('upload_image.html', result=result)

    database.add_guess(request.form['secret'])
    flash("file uploaded with a secret " + request.form['secret'])
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)
