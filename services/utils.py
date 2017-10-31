from __future__ import (
    absolute_import,
    unicode_literals,
)
from services.point import Point
from random import randint

def is_already_allocate(point, allocates):
    for allocated in allocates:
        if allocated.x == point.x and allocated.y == point.y:
            return True
    return False

def init_ship_head(width, height):
    x = randint(0, width-1)
    y = randint(0, height-1)
    return Point(x, y)

def just_test():
    pass