from flask import Flask, render_template

app = Flask(__name__)

APP_VERSION = '0.0.1'


@app.route('/')
def home():
    return render_template('home.html', app_version=APP_VERSION)


@app.route('/home_without_base')
def home_without_base():
    return render_template('home_without_base.html', app_version=APP_VERSION)


@app.route('/guess')
def guess():
    return render_template('guess.html', app_version=APP_VERSION)


@app.route('/upload_image')
def upload_image():
    return render_template('upload_image.html', app_version=APP_VERSION)


if __name__ == '__main__':
    app.run(debug=True)
