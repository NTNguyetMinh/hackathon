from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.utils.utils import (
    is_already_occupied,
    get_near_positions,
    is_double_occupied,
    is_valid_position,
    remove_position,
    remove_occupied_position,
    pick_random
)
from application.utils.const import (
    MAX_ATTEMPT,
    PLAYER_ID,
    HIT,
    VERTICAL,
    HORIZONTAL,
    OIL_RIG
)
from application.entity.point import Point
from application.entity.enemy_ship import EnemyShip
from application.entity.ship import Ship
import logging

logger = logging.getLogger('werkzeug')

class FireControl(object):
    def __init__(self, width, height, ships):
        self.width = width
        self.height = height
        self.remain_positions = []
        self.fired_positions = []
        self.hit_positions = []
        self.remain_ships = []
        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    self.remain_positions.append(Point(x, y))
        logger.info('init fire control')
        self.init_ships(ships)

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = EnemyShip(ship_data['type'])
                self.remain_ships.append(ship)

    def fire(self):
        fire_point = self.get_high_expect_positions_2()
        if is_already_occupied(fire_point, self.remain_positions):
            remove_position(fire_point, self.remain_positions)
        self.fired_positions.append(fire_point)
        return fire_point

    def get_high_expect_positions(self):
        high_expect_positions = []
        if self.hit_positions:
            for position in self.hit_positions:
                near_positions = get_near_positions(position, self.width, self.height)
                high_expect_positions = remove_occupied_position(near_positions, self.fired_positions)
                if high_expect_positions:
                    break
        if not high_expect_positions:
            return self.fire_random()
        return pick_random(high_expect_positions)

    def fire_random(self):
        for i in range(0, MAX_ATTEMPT):
            fire = pick_random(self.remain_positions)
            near_positions = get_near_positions(fire, self.width, self.height)
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

        self.hit_positions = remove_occupied_position(ship_positions, self.hit_positions)

    def handle_fire_result(self, response):
        shot_result = response['shotResult']
        if shot_result['playerId'] != PLAYER_ID:
            return True

        if shot_result['status'] == HIT:
            shot_position = shot_result['position']
            self.hit_positions.append(Point(shot_position['x'], shot_position['y']))

        if shot_result.get('recognizedWholeShip'):
            self.shipwreck(shot_result['recognizedWholeShip'])

    # def get_chain_hit(self):
    #     chain_hits = get_chain_position(self.hit_positions[0], self.hit_positions, self.width, self.height)
    #     chain_hits.append(self.hit_positions[0])
    #     return chain_hits

    def get_high_expect_positions_2(self):
        remain_positions = []
        for position in self.hit_positions:
            ships = []
            for ship_type in self.remain_ship_type():
                ship = Ship(ship_type, position, HORIZONTAL)
                remain_position = self.get_remain_position(ship)
                if remain_position:
                    remain_positions.append(remain_position)
                    ships.append(ship)
                ship = Ship(ship_type, position, VERTICAL)
                remain_position = self.get_remain_position(ship)
                if ship_type != OIL_RIG and remain_position:
                    remain_positions.append(remain_position)
                    ships.append(ship)
        if remain_positions:
            remain_positions.sort(key=lambda tub: len(tub))
            return remain_positions[0][0]
        return self.fire_random()

    def remain_ship_type(self):
        remain_types = [ship.type for ship in self.remain_ships]
        return list(set(remain_types))

    def get_remain_position(self, ship):
        """
        Check position of ship is valid on board or not
        And position of this ship is fire but not hit
        And must one piece of ship is not fire yet
        :param ship:
        :return:
        """
        remain_position = []
        if not remove_occupied_position(self.hit_positions, ship.positions):
            return remain_position
        for position in ship.positions:
            # Does not outside board
            if not is_valid_position(position, self.width, self.height):
                return []
            if not is_already_occupied(position, self.hit_positions) and \
                    is_already_occupied(position, self.fired_positions):
                return []
            if is_already_occupied(position, self.remain_positions):
                remain_position.append(position)
        return remain_position
