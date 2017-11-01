from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.entity.ship import Ship
from application.entity.point import Point
from application.utils.utils import (
    init_head,
    is_already_allocate
)


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_ship = []
        self.allocates = []

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = self.init_ship(ship_data)
                self.allocates.extend(ship.position)
                self.current_ship.append(ship)

    def init_ship(self, ship_data):
        ship_type = ship_data['type']
        while True:
            ship_head = init_head(self.width, self.height)
            ship = Ship(ship_type, ship_head)
            if self.is_valid_position(ship):
                return ship

    def is_valid_position(self, ship):
        for piece in ship.position:
            if piece.x >= self.width or piece.y >= self.height:
                return False
            if is_already_allocate(piece, self.allocates):
                return False
            nears = self.get_near_position(piece, ship.position)
            for near in nears:
                if is_already_allocate(near, self.allocates):
                    return False

        return True

    def is_nice_position(self, positions):
        for position in positions:
            if is_already_allocate(position, self.allocates):
                return False

    def get_near_position(self, position, positions):
        nears = [Point(position.x, position.y + 1),
                 Point(position.x, position.y - 1),
                 Point(position.x + 1, position.y),
                 Point(position.x - 1, position.y)]
        nears = [near for near in nears if not is_already_allocate(near, positions)]
        return nears

