from __future__ import (
    absolute_import,
    unicode_literals,
)
from random import (
    randrange
)

from application.entity.point import Point
from application.entity.ship import Ship
from application.utils.utils import (
    init_head,
    is_already_allocate
)


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.valid_point = []
        self.remain_point = []
        self.fired_point = []
        self.current_ship = []
        self.allocates = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.valid_point.append(Point(x, y))
                    self.remain_point.append(Point(x, y))

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = self.__init_ship(ship_data)
                self.allocates.extend(ship.position)
                self.current_ship.append(ship)

    def __init_ship(self, ship_data):
        ship_type = ship_data['type']
        while True:
            ship_head = init_head(self.width, self.height)
            ship = Ship(ship_type, ship_head)
            if self.__is_valid_position(ship):
                return ship

    def __is_valid_position(self, ship):
        for piece in ship.position:
            if piece.x >= self.width or piece.y >= self.height:
                return False
            if is_already_allocate(piece, self.allocates):
                return False
        return True

    def fire(self):
        fire_point = randrange(len(self.remain_point))
        self.remain_point.pop(fire_point)
        self.fired_point.append(fire_point)
        return fire_point
