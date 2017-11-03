from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from flask import request
from application.config.redis import Base
import logging
logger = logging.getLogger('werkzeug')
class NotifyResult(Base):

    def execute(self):
        body = request.get_json()
        logger.info('Notify request: {}'.format(body))
        print body

        # TODO get fire control from redis
        fire_control = self.db.get('fire_control')

        fire_control.handle_fire_result(body)

        # TODO store fire control to redis
        self.db.set('fire_control', fire_control)

        return json.dumps({'success': True})

