#!/usr/bin/env python3
"""Route module for API - Get locale from request"""

from flask import Flask, request, render_template
from flask_babel import Babel
from os import getenv

app = Flask(__name__)


class Config(object):
    """Setup - Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


def get_locale():
    """Determine best match for supported languages using request headers"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel.init_app(app, locale_selector=get_locale)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Render the home page"""
    return render_template('2-index.html')


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
