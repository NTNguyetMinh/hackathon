from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from flask import request

class Turn(object):

    def execute(self):
        # TODO get fire control from redis
        fire_control = None

        fire_point = fire_control.fire()

        # TODO store fire control to redis

        response = {'firePosition': {
            'x': fire_point.x,
            'y': fire_point.y
        }}

        return json.dumps(response)

