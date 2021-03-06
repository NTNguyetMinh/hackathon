from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.utils import (
    get_near_positions,
    remove_occupied_position,
    pick_random
)

from application.entity.point import Point
from application.entity.enemy_ship import EnemyShip


class EnemyBoard(object):
    def __init__(self, width, height, ships):
        self.width = width
        self.height = height
        self.valid_positions = []
        self.remain_positions = []
        self.fired_positions = []
        self.hit_positions = []
        self.remain_ship = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.valid_positions.append(Point(x, y))
                    self.remain_positions.append(Point(x, y))

        self.init_ships(ships)

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = EnemyShip(ship_data['type'])
                self.remain_ship.append(ship)

    def fire(self):
        fire_point = self.get_high_expect_positions()
        self.remain_positions.remove(fire_point)
        self.fired_positions.append(fire_point)
        return fire_point

    def get_high_expect_positions(self):
        high_expect_positions = []
        if self.hit_positions:
            for position in self.hit_positions:
                near_positions = get_near_positions(position)
                high_expect_positions = remove_occupied_position(near_positions, self.fired_positions)
                if high_expect_positions:
                    break
        else:
            return self.fire_random()
        if not high_expect_positions:
            return self.fire_random()
        return pick_random(high_expect_positions)

    def fire_random(self):
        fire_point = pick_random(self.remain_positions)
        self.remain_positions.remove(fire_point)
        self.fired_positions.append(fire_point)
        return fire_point
