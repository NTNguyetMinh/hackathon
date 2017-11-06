from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from application.config.redis import Base
from application.entity.board import Board
from application.fire_control import FireControl
from flask import request
import logging

logger = logging.getLogger('werkzeug')

class Invite(Base):

    def execute(self):
        body = request.get_json()
        logger.info('Invite request: {}'.format(body))
        #
        print body

        session_id = body['sessionId']
        game_rule = body['gameRule']
        board = Board(game_rule['boardWidth'], game_rule['boardHeight'])
        board.init_ships(game_rule['ships'])

        fire_control = FireControl(game_rule['boardWidth'], game_rule['boardHeight'], game_rule['ships'])

        # TODO store fire control to redis
        # TODO store board to redis
        self.db.set('board_{}'.format(session_id), board)
        self.db.set('fire_control_{}'.format(session_id), fire_control)

        return json.dumps({'success': True})
