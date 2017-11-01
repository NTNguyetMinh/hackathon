from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.const import (
    SHIP
)

class EnemyShip(object):

    def __init__(self, ship_type):
        self.type = ship_type
        self.ship_meta = SHIP[self.type]
        self.position = []

    def piece(self):
        return self.ship_meta['pieces']

    def is_shipwreck(self):
        pass
