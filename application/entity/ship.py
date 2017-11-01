from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.const import (
    SHIP
)
from application.entity.point import Point
from application.utils.utils import (
    init_direction
)

class Ship(object):

    def __init__(self, ship_type, head):
        self.type = ship_type
        self.head = head
        self.ship_meta = SHIP[self.type]
        self.position = []
        self.ship_direct = init_direction()
        self.init_position()

    def init_position(self):
        for piece in self.ship_meta[self.ship_direct]:
            x = self.head.x + piece['x']
            y = self.head.y + piece['y']
            self.position.append(Point(x, y))

    def piece(self):
        return self.ship_meta['pieces']

    def is_shipwreck(self):
        pass
