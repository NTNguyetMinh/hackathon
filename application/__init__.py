from __future__ import (
    absolute_import,
    unicode_literals,
)

from application.config.routes import setup_routes
from flask import Flask
app = Flask(__name__)

setup_routes(app)

if __name__ == '__main__':
    app.run()