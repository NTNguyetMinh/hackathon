from __future__ import (
    absolute_import,
    unicode_literals,
)
from datetime import date

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0

LOG_FILE = 'logs/game_{}.log'.format(date.today())


