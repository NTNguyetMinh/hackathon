from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from flask import request
from application.config.redis import Base

class Turn(Base):

    def execute(self):
        body = request.get_json()

        print body
        # TODO get fire control from redis
        fire_control = self.db.get('fire_control')

        fire_point = fire_control.fire()

        # TODO store fire control to redis
        self.db.set('fire_control', fire_control)

        response = {'firePosition': {
            'x': fire_point.x,
            'y': fire_point.y
        }}

        return json.dumps(response)

