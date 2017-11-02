from __future__ import (
    absolute_import,
    unicode_literals,
)
import json
from application.config.redis import Base
from application.entity.point import Point
from application.utils.utils import is_already_occupied

class Start(Base):

    def execute(self):

        # TODO get board from redis
        board = self.db.get('board')

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

