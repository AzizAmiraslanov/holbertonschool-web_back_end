#!/usr/bin/env python3
"""Route module for the API"""

from flask import Flask, request, render_template
from flask_babel import Babel
from os import getenv

app = Flask(__name__)


class Config(object):
    """Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


# Babel setup
babel = Babel()


def get_locale():
    """Select best language from request headers"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel.init_app(app, locale_selector=get_locale)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Render home page"""
    return render_template('3-index.html')


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)