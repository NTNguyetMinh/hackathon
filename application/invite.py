from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from application.entity.board import Board
from application.fire_control import FireControl
from flask import request

class Invite(object):

    def execute(self):
        body = request.get_json()

        session_id = body['sessionId']
        game_rule = body['gameRule']
        board = Board(game_rule['boardWidth'], game_rule['boardHeight'])
        board.init_ships(game_rule['ships'])

        fire_control = FireControl(game_rule['boardWidth'], game_rule['boardHeight'], game_rule['ships'])

        # TODO store fire control to redis
        # TODO store board to redis

        return json.dumps({'success': True})
