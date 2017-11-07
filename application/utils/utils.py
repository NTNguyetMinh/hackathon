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


def get_near_positions(position, width, height):
    near_positions = [Point(position.x, position.y + 1),
                      Point(position.x, position.y - 1),
                      Point(position.x + 1, position.y),
                      Point(position.x - 1, position.y)]
    return [near for near in near_positions if is_valid_position(near, width, height)]


def is_valid_position(position, width, height):
    if position.x >= width or position.y >= height:
        return False
    if position.x < 0 or position.y < 0:
        return False
    return True


def remove_position(position, occupied):
    for allocated in occupied:
        if allocated.x == position.x and allocated.y == position.y:
            occupied.remove(allocated)


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


def get_chain_position(position, chains, width, height):
    near_positions = get_near_positions(position, width, height)
    return [point for point in chains if is_already_occupied(point, near_positions)]


def is_stick_position(position, allocates, width, height):
    """
    A position is nice when it does not near any ships.
    :param position: A position need to check
    :return:
    """
    nears_position = get_near_positions(position, width, height)
    if is_double_occupied(nears_position, allocates):
        return True
    return False


