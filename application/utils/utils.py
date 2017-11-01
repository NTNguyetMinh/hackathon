from __future__ import (
    absolute_import,
    unicode_literals,
)
from random import (
    randint,
    choice
)

from application.entity.point import Point
from application.utils.const import DIRECTION


def is_already_allocate(point, allocates):
    for allocated in allocates:
        if allocated.x == point.x and allocated.y == point.y:
            return True
    return False

def init_head(width, height):
    x = randint(0, width-1)
    y = randint(0, height-1)
    return Point(x, y)

def init_direction():
    choice(DIRECTION)

