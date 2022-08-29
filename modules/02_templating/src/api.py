from flask import Flask, render_template

app = Flask(__name__)

APP_VERSION = '0.0.1'


@app.context_processor
def inject_app_version():
    return dict(app_version=APP_VERSION)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/home_without_base')
def home_without_base():
    return render_template('home_without_base.html')


@app.route('/red')
def red_page():
    return render_template('page_red.html')


@app.route('/yellow')
def yellow_page():
    return render_template('page_yellow.html')


@app.route('/green')
def green_page():
    return render_template('page_green.html')
