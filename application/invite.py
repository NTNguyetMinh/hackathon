from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from application.entity.board import Board
from application.entity.point import Point
from application.utils.utils import is_already_occupied
from flask import request

class Invite(object):

    def execute(self):
        body = request.get_json()

        session_id = body['sessionId']
        game_rule = body['gameRule']
        board = Board(game_rule['boardWidth'], game_rule['boardHeight'])
        board.init_ships(game_rule['ships'])

        ships = []
        for ship in board.current_ship:
            ships.append({
                'type': ship.type,
                'positions': [{'x': position.x, 'y': position.y} for position in ship.position]
            })
        response = json.dumps(ships)
        for y in range(game_rule['boardHeight'], -1, -1):
            line = ''
            for x in range(0, game_rule['boardWidth']):
                is_allocated = is_already_occupied(Point(x, y), board.allocates)
                point = 'x' if is_allocated else ' '
                line = line + ' ' + point

            print line

        return response

