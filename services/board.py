from __future__ import (
    absolute_import,
    unicode_literals,
)
from services.point import Point
from services.utils import init_ship_head


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.valid_point = []
        self.remain_point = []
        self.fired_point = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.valid_point.append(Point(x, y))
                    self.remain_point.append(Point(x, y))

    def init_ship(self, ships):
        for ship in ships:
            ship_head = init_ship_head(self.width, self.height)
        pass
