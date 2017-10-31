from __future__ import (
    absolute_import,
    unicode_literals,
)
from services.const import (
    SHIP
)
from services.point import Point
from services.utils import is_already_allocate

class Ship(object):

    def __init__(self, ship_type, head):
        self.type = ship_type
        self.head = head
        self.ship_meta = SHIP[self.type]
        self.position = []
        self.init_position()

    def init_position(self):
        for piece in self.ship_meta['horizontal']:
            x = self.head.x + piece['x']
            y = self.head.y + piece['y']
            self.position.append(Point(x, y))

    def is_valid_position(self, width, height, allocates):
        for piece in self.position:
            if piece.x >= width or piece.y >= height:
                return False
            if is_already_allocate(piece, allocates):
                return False
        return True

    def piece(self):
        return self.ship_meta['pieces']

    def is_shipwreck(self):
        pass
