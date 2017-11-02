from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from application.entity.point import Point
from application.utils.utils import is_already_occupied

class Start(object):

    def execute(self):

        # TODO get board from redis
        board = None

        ships = []
        for ship in board.current_ship:
            ships.append({
                'type': ship.type,
                'positions': [{'x': position.x, 'y': position.y} for position in ship.positions]
            })
        response = json.dumps(ships)
        for y in range(board.height, -1, -1):
            line = ''
            for x in range(0, board.width):
                is_allocated = is_already_occupied(Point(x, y), board.allocates)
                point = 'x' if is_allocated else ' '
                line = line + ' ' + point

            print line

        return response

