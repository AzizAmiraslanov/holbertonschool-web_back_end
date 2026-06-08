#!/usr/bin/env python3
from flask import Flask, request, render_template
from flask_babel import Babel
from os import getenv

app = Flask(__name__)

class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

babel = Babel()

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel.init_app(app, locale_selector=get_locale)

# 🔥 FIX
app.jinja_env.globals['_'] = babel.gettext


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('3-index.html')


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)