from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.const import (
    SHIP,
    DIRECTION
)
from application.entity.point import Point
from random import choice


class Ship(object):

    def __init__(self, ship_type, head, direct=None, start=None):
        self.type = ship_type
        self.head = head
        self.ship_meta = SHIP[self.type]
        self.positions = []
        self.ship_direct = direct or self.init_direction()
        self.init_positions(start)

    def init_positions(self, start):
        ship_direct = self.ship_meta[self.ship_direct]
        start = start or ship_direct[0]
        for piece in ship_direct:
            x = self.head.x + piece['x'] - start['x']
            y = self.head.y + piece['y'] - start['y']
            self.positions.append(Point(x, y))

    def piece(self):
        return self.ship_meta['pieces']

    @staticmethod
    def init_direction():
        return choice(DIRECTION)
