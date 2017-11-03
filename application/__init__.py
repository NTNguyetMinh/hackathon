from __future__ import (
    absolute_import,
    unicode_literals,
)
import logging
from logging.handlers import RotatingFileHandler
from application.config.routes import setup_routes
from application.config.redis import *
from application.config.setting import LOG_FILE

from flask import Flask
app = Flask(__name__)



if __name__ == '__main__':
    setup_routes(app, db)

    logger = logging.getLogger('werkzeug')
    handler = RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=1)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    app.run(host='0.0.0.0', port=5000)
    # app.run()
