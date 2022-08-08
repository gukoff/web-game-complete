from flask import Flask, Response, flash, render_template, request, redirect, session
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


@app.route('/guess_image_display')
def guess_image():
    try:
        image_data = database.get_image_by_id(session['selection'])
        if image_data is None:
            return Response(status=401, response="no session set")
        content_type, img_bytes = image_data
        if (img_bytes is None or content_type is None):
            raise Exception("Error fetching img_bytes or content_type")
        return Response(img_bytes, mimetype=content_type)

    except Exception as exp:  # pylint: disable=broad-except
        return Response(status=500, response=exp.__str__())


@app.route('/result_guess', methods=['POST'])
def result_guess():
    result = request.form
    secret_description = database.get_guess_secret(
        session['selection'])
    if (result['guess_secret'] == secret_description):
        flash("You guessed right!")
    else:
        flash("You didn't guess! Try again!")
    return render_template('result_guess.html', result=result)


def secure_filename(path):
    return path.replace("/", "_").replace(".", "_").replace("\\", "_").replace(" ", "_")


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    result = request.form

    if request.method == "GET":
        return render_template('upload_image.html', result=result)

    file = request.files['image']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected files')
        return redirect(request.url)
    database.add_guess(
        (file.content_type, file.stream.read()), request.form['secret'])
    flash("file uploaded with a secret " + request.form['secret'])
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)
