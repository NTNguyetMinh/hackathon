from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
import logging
from flask import request
from application.config.redis import Base
from application.entity.point import Point
from application.utils.utils import is_already_occupied
logger = logging.getLogger('werkzeug')

class Start(Base):

    def execute(self):

        body = request.get_json()
        logger.info('Start request: {}'.format(body))
        print body

        # TODO get board from redis
        session_id = body['sessionId']
        board = self.db.get('board_{}'.format(session_id))

        ships = []
        for ship in board.current_ship:
            ships.append({
                'type': ship.type,
                'positions': [{'x': position.x, 'y': position.y} for position in ship.positions]
            })
        response = json.dumps({'ships': ships})
        for y in range(board.height, -1, -1):
            line = ''
            for x in range(0, board.width):
                is_allocated = is_already_occupied(Point(x, y), board.allocates)
                point = 'x' if is_allocated else ' '
                line = line + ' ' + point

            print line

        return response

