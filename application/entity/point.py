from __future__ import (
    absolute_import,
    unicode_literals,
)

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fire = False
        self.hit = False

    def is_fired(self):
        return self.fire

    def fire(self):
        self.fire = True

    def is_hit(self):
        return self.hit