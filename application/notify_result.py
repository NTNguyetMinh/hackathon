from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from flask import request

class NotifyResult(object):

    def execute(self):
        body = request.get_json()

        # TODO get fire control from redis
        fire_control = None

        fire_control.handle_fire_result(body)

        # TODO store fire control to redis

        return json.dumps({'result': True})

