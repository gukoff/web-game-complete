# Templating

In the second stage we're going to add two new pages `/guess` and `/upload_image` and then we're going to modify the `/` to link to the new pages. To achieve this, we'll be using the [Jinja2 template engine](https://flask.palletsprojects.com/en/2.2.x/quickstart/#rendering-templates) that's built into Flask.

1. Modify `/` endpoint to return html page with two links

    1. Add `src/templates/home.html` with the below contents

        ```html
        <!doctype html>
        <html>

        <head>
            <title>{{ title }}</title>
            <link rel="stylesheet" href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://getbootstrap.com/docs/4.0/examples/starter-template/starter-template.css">
            <link rel="icon" href="https://getbootstrap.com/docs/4.0/assets/img/favicons/favicon.ico">
        </head>

        <body>
            <div class="container">
            <hr>
            <p style="text-align:center;">Hello, user</p>

            <!-- We can replace with buttons and javascript -->
            
            <a href="./upload_image">Upload Image</a>
            <p></p>
            <a href="./guess">Guess Image</a>
            <p></p>

            App Version: {{ app_version }}
            </div>

            <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
        
        </body>
        </html>
         ```

    2. Add a new global constant and modify the return value of `/` endpoint in `api.py`

        ```python

        APP_VERSION = '0.0.1'

        return render_template('home.html', app_version=APP_VERSION)

        ```

    3. Run the API and navigate to the `/`

        You should see two links and the app version set to `0.0.1`. Clicking on the links should result in a `Not found` page.

2. Add two new API endpoints for `/guess` and `/upload_image` by yourself with corresponding templates named `guess.html` and `upload_images.html`. Make sure all pages display the app version from the same global constant.

3. Split `home.html` into `base.html` and `home.html` to remove some code duplication

    1. Create `base.html` with the below contents

        ```html
        <!doctype html>
        <html>

        <head>
            <title>{{ title }}</title>
            <link rel="stylesheet" href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://getbootstrap.com/docs/4.0/examples/starter-template/starter-template.css">
            <link rel="icon" href="https://getbootstrap.com/docs/4.0/assets/img/favicons/favicon.ico">
        </head>

        <body>
            <div class="container">
            <hr>
            {% block content %}
            {% endblock %}
            <p></p>

            App Version: {{ app_version }}
            </div>

            <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>

            {% block scripts %}
            {% endblock %}
            
        </body>
        </html>

        ```

    2. Modify `home.html` with:

        ```html
        {% extends "base.html" %}

        {% block content %}

        <p style="text-align:center;">Hello, user</p>

        <!-- We can replace with buttons and javascript -->

        <a href="./upload_image">Upload Image</a>
        <p></p>
        <a href="./guess">Guess Image</a>

        {% endblock %}
        ```

4. Modify `guess.html` and `upload_images.html` to use the `base.html`
