from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.config.routes import setup_routes
from application.config.redis import *
from flask import Flask
app = Flask(__name__)

if __name__ == '__main__':
    setup_routes(app, db, log.logger)
    app.run(host='0.0.0.0', port=5000)
    # app.run()
