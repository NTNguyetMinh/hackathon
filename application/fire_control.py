from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.utils import (
    get_near_positions,
    remove_occupied_position,
    pick_random,
    is_already_occupied,
    is_double_occupied
)
from application.utils.const import MAX_ATTEMPT
from application.entity.point import Point
from application.entity.enemy_ship import EnemyShip


class FireControl(object):
    def __init__(self, width, height, ships):
        self.remain_positions = []
        self.fired_positions = []
        self.hit_positions = []
        self.remain_ships = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.remain_positions.append(Point(x, y))

        self.init_ships(ships)

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = EnemyShip(ship_data['type'])
                self.remain_ships.append(ship)

    def fire(self):
        fire_point = self.get_high_expect_positions()
        if is_already_occupied(fire_point, self.remain_positions):
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
        if not high_expect_positions:
            return self.fire_random()
        return pick_random(high_expect_positions)

    def fire_random(self):
        for i in range(0, MAX_ATTEMPT):
            fire = pick_random(self.remain_positions)
            near_positions = get_near_positions(fire)
            if not is_double_occupied(near_positions, self.fired_positions):
                return fire
        return pick_random(self.remain_positions)

    def shipwreck(self, recognized_ship):
        # remove this ship in remain ship
        for ship in self.remain_ships:
            if ship.type == recognized_ship['type']:
                self.remain_ships.remove(ship)
                break
        ship_positions = []
        for position in recognized_ship['positions']:
            ship_positions.append(Point(position['x'], position['y']))

        self.hit_positions = remove_occupied_position(self.hit_positions, ship_positions)
