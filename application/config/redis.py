from __future__ import (
    absolute_import,
    unicode_literals,
)
import pickle
from redis import Redis
from application.config.setting import REDIS_HOST, REDIS_PORT, REDIS_DB

class Db(object):
    def __init__(self, host, port, db):
        self.db = Redis(host=host, port=port, db=db)

    def set(self, key, obj):
        self.db.set(key, pickle.dumps(obj))

    def get(self, key):
        return pickle.loads(self.db.get(key))

db = Db(REDIS_HOST, REDIS_PORT, REDIS_DB)

class Base(object):
    def __init__(self, db):
        self.db = db

