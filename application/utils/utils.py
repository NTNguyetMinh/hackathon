from __future__ import (
    absolute_import,
    unicode_literals,
)
from random import (
    randint,
    randrange
)
from application.entity.point import Point


def is_already_occupied(point, occupied):
    for allocated in occupied:
        if allocated.x == point.x and allocated.y == point.y:
            return True
    return False


def init_position(width, height):
    x = randint(0, width-1)
    y = randint(0, height-1)
    return Point(x, y)


def get_near_positions(position):
    return [Point(position.x, position.y + 1),
            Point(position.x, position.y - 1),
            Point(position.x + 1, position.y),
            Point(position.x - 1, position.y)]


def remove_occupied_position(positions, occupied):
    return [position for position in positions if not is_already_occupied(position, occupied)]


def is_double_occupied(positions, occupied):
    for position in positions:
        if is_already_occupied(position, occupied):
            return True
    return False

def pick_random(available):
    index = randrange(len(available))
    return available[index]

def get_chain_position(position, chains):
    near_positions = get_near_positions(position)
    return [point for point in chains if is_already_occupied(point, near_positions)]
