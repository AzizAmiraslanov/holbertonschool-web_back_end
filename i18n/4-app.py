#!/usr/bin/env python3
""" Route module for the API - Force locale with URL parameter """
from flask import Flask, request, render_template
from flask_babel import Babel
from os import getenv

app = Flask(__name__)
babel = Babel()


class Config(object):
    """ Setup - Babel configuration """
    LANGUAGES = ['en', 'fr']
    # these are the inherent defaults just btw
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# set the above class object as the configuration for the app
app.config.from_object('4-app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return: 4-index.html
    """
    return render_template('4-index.html')


def get_locale() -> str:
    """ Determines best match for supported languages """
    # check if there is a locale parameter/query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
