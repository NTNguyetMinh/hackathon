from __future__ import (
    absolute_import,
    unicode_literals,
)
# import logging
# from logging.handlers import RotatingFileHandler
import pickle
from redis import Redis
from application.config.setting import REDIS_HOST, REDIS_PORT, REDIS_DB, LOG_FILE

class Db(object):
    def __init__(self, host, port, db):
        self.db = Redis(host=host, port=port, db=db)

    def set(self, key, obj):
        self.db.set(key, pickle.dumps(obj))

    def get(self, key):
        value = self.db.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

db = Db(REDIS_HOST, REDIS_PORT, REDIS_DB)

# class Log(object):
#     def __init__(self, path_file=LOG_FILE, logger_name='werkzeug', maxBytes=10000):
#         logger = logging.getLogger(logger_name)
#         handler = RotatingFileHandler(path_file, maxBytes=maxBytes, backupCount=1)
#         formatter = logging.Formatter(
#             "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#
#         self.logger = logger
#
#     def get(self):
#         return self.logger
#
# log = Log()

class Base(object):
    def __init__(self, db):
        self.db = db


