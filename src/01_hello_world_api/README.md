# Hello world python web API

In the first stage we're going to create a python web API with [Flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/) that will return "Hello world" on the "/" page.

1. Add and install `Flask` python package.

    >To be able to build the API, we first need to get the package of API we'll be using.

    1. Create a `requirements.txt` file in the `src/` folder

        ```sh
        touch requirements.txt
        ```

    2. Modify the contents of the `requirements.txt` with:

        ```txt
        flask
        ```

    3. Install the package

        ```sh
        pip install -r requirements.txt
        ```

2. Create the contents of the API

    1. Create an `api.py` in the `src/` folder file with the contents of

        ```python
        from flask import Flask
        app = Flask(__name__)


        @app.route('/') # Define the route the page will be served on
        def home():
            return "hello world"


        if __name__ == '__main__':
            app.run(debug=True)
        ```

3. In the root of the project (one level above `src`) create `app.py`

    ```py
    from src.api import app  # pylint: disable=unused-import
    ```

4. Run the API from the project root folder

    ```sh
    FLASK_DEBUG=1 flask run
    ```

5. Navigate to the url that the API is running at from the output of the previous command
