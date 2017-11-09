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
from application.utils.const import (
    NON_STICK_P,
    PLAYER_ID,
    HISTORY_MODE
)
logger = logging.getLogger('werkzeug')

class Start(Base):

    def execute(self):

        body = request.get_json()
        logger.info('Start request: {}'.format(body))
        print body

        # TODO get board from redis
        session_id = body['sessionId']
        board = self.db.get('board_{}'.format(session_id))

        fire_control = self.db.get('fire_control_{}'.format(session_id))

        player_id1 = body['player1']['id']
        player_id2 = body['player2']['id']

        if player_id1 in NON_STICK_P or player_id2 in NON_STICK_P:
            fire_control.stick_mode = False
            logger.info('ENABLE STICK MODE FOR MATCH {} VS {}'.format(player_id1, player_id2))
        if player_id1 != PLAYER_ID:
            head_list = self.db.get('head_list_{}'.format(player_id1))
            fire_control.competitor = player_id1
        else:
            head_list = self.db.get('head_list_{}'.format(player_id2))
            fire_control.competitor = player_id2
        if HISTORY_MODE:
            fire_control.head_list = head_list or []
        logger.info('HISTORY HEADS LEN OF {} IS {}'.format(fire_control.competitor, len(fire_control.head_list)))

        self.db.set('fire_control_{}'.format(session_id), fire_control)

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

