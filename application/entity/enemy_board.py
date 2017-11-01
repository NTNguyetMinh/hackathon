from __future__ import (
    absolute_import,
    unicode_literals,
)
from random import (
    randrange
)

from application.entity.point import Point
from application.entity.enemy_ship import EnemyShip


class EnemyBoard(object):
    def __init__(self, width, height, ships):
        self.width = width
        self.height = height
        self.valid_point = []
        self.remain_point = []
        self.fired_point = []
        self.remain_ship = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.valid_point.append(Point(x, y))
                    self.remain_point.append(Point(x, y))

        self.init_ships(ships)

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = EnemyShip(ship_data['type'])
                self.remain_ship.append(ship)

    def fire(self):
        fire_point = randrange(len(self.remain_point))
        self.remain_point.pop(fire_point)
        self.fired_point.append(fire_point)
        return fire_point
