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
from application.utils.const import *
from application.entity.score import Score
from application.entity.point import Point
from application.entity.enemy_ship import EnemyShip
from application.entity.ship import Ship
import logging
from math import floor
from random import random

logger = logging.getLogger('werkzeug')


class FireControl(object):
    def __init__(self, width, height, ships):
        self.width = width
        self.height = height
        self.remain_positions = []
        self.fired_positions = []
        self.hit_positions = []
        self.remain_ships = []
        self.high_prioritize = []
        self.matrix = [[Score() for y in range(self.height)] for x in range(self.width)]

        # TODO use for data mining
        self.history_hit = []

        # self.init_high_prioritize(width, height)
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

    def init_high_prioritize(self, width, height):
        half_width = int(width/2)
        half_height = int(height/2)
        width -= 1
        height -= 1
        self.high_prioritize = [Point(0, 0), Point(0, half_height), Point(0, height),
                                Point(width, 0), Point(width, half_height), Point(width, height),
                                Point(half_width, 0), Point(half_width, half_height), Point(half_width, height)]

    def fire(self):
        if self.hit_positions:
            return self.hunt_ship()
        return self.find_ship()

    def get_nearby_positions(self):
        high_expect_positions = []
        if self.hit_positions:
            for position in self.hit_positions:
                near_positions = get_near_positions(position, self.width, self.height)
                high_expect_positions = remove_occupied_position(near_positions, self.fired_positions)
                if high_expect_positions:
                    break
        if not high_expect_positions:
            return self.find_ship()
        return pick_random(high_expect_positions)

    def find_ship(self):
        next_shot = self.mining_data()
        if next_shot:
            if not is_already_occupied(next_shot, self.fired_positions):
                return next_shot
        if self.high_prioritize:
            next_shot = self.high_prioritize.pop(0)
            if not is_already_occupied(next_shot, self.fired_positions):
                return next_shot
        if FIND_ALGORITHM == SCORE:
            return self.get_shot_coordinates()
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
        shot_position = shot_result['position']
        fire_point = Point(shot_position['x'], shot_position['y'])
        if is_already_occupied(fire_point, self.remain_positions):
            remove_position(fire_point, self.remain_positions)
        self.fired_positions.append(fire_point)
        self.matrix[shot_position['x']][shot_position['y']].fire = True
        if shot_result['status'] == HIT:
            self.history_hit.append(fire_point)
            self.hit_positions.append(fire_point)

        if shot_result.get('recognizedWholeShip'):
            self.shipwreck(shot_result['recognizedWholeShip'])

    def hunt_ship(self):
        remain_positions = []
        for delta in range(0, 5):
            for position in self.hit_positions:
                for ship_type in self.remain_ship_type():
                    for ship_start in SHIP[ship_type][HORIZONTAL]:
                        ship = Ship(ship_type, position, HORIZONTAL, ship_start)
                        remain_position = self.get_remain_position(ship, delta)
                        if remain_position:
                            remain_positions.append(remain_position)
                    for ship_start in SHIP[ship_type][VERTICAL]:
                        ship = Ship(ship_type, position, VERTICAL, ship_start)
                        remain_position = self.get_remain_position(ship, delta)
                        if ship_type != OIL_RIG and remain_position:
                            remain_positions.append(remain_position)
            if remain_positions:
                logger.info('Remain positions: {}'.format(len(remain_positions)))
                break
        # logger.info('Remain positions: {}'.format(render_position(remain_positions, self.width, self.height)))
        remain_positions.sort(key=lambda tub: len(tub))
        self.render_position(remain_positions)
        if remain_positions:
            return remain_positions[0][0]
        return self.get_nearby_positions()

    def remain_ship_type(self):
        remain_types = [ship.type for ship in self.remain_ships]
        return list(set(remain_types))

    def get_remain_position(self, ship, delta):
        """
        Check position of ship is valid on board or not
        And position of this ship is fire but not hit
        And must one piece of ship is not fire yet
        :param ship:
        :return:
        """
        remain_position = []
        notin_ship = remove_occupied_position(self.hit_positions, ship.positions)
        if len(notin_ship) > delta:
            return remain_position
        for position in ship.positions:
            # Does not outside board
            if not is_valid_position(position, self.width, self.height):
                return []
            if not is_already_occupied(position, self.hit_positions) and \
                    is_already_occupied(position, self.fired_positions):
                return []
            if not is_already_occupied(position, self.fired_positions):
                remain_position.append(position)
        return remain_position

    def render_position(self, positions):
        remain = positions[0] if positions else []
        for y in range(self.height, -1, -1):
            line = 'y:' + str(y) + ' '
            for x in range(0, self.width):
                if is_already_occupied(Point(x, y), remain):
                    line += '  v'
                elif is_already_occupied(Point(x, y), self.hit_positions):
                    line += '  o'
                elif is_already_occupied(Point(x, y), self.fired_positions):
                    line += '  x'
                else:
                    line += '   '

            print line
        line = 'x:  '
        for x in range(0, self.width):
            line += '  ' + str(x)
        print line

        return line

    def get_shot_coordinates(self):
        """
        Use this
        http://christopherstoll.org/2012/06/battleship-ai-algorithm-using-dynamic.html
        :return:
        """
        high_score_n = 5
        high_score_xs = [0, 0, 0, 0, 0, 0]
        high_score_ys = [0, 0, 0, 0, 0, 0]
        high_score_val = [0, 0, 0, 0, 0, 0]
        score_picker = int(floor(random() * high_score_n))
        for x in range(self.width):
            for y in range(self.height):
                is_fire = False
                if not self.matrix[x][y].fire:
                    ltr = 0
                    if x > 0:
                        if self.matrix[x - 1][y]:
                            ltr = self.matrix[x - 1][y].left_to_right
                    ttb = 0
                    if y > 0:
                        if self.matrix[x][y - 1]:
                            ttb = self.matrix[x][y - 1].top_to_bottom
                else:
                    ltr = -1
                    ttb = -1
                    is_fire = True
                self.matrix[x][y] = Score(x, y, ltr + 1, ttb + 1, is_fire)
        for x in range(self.width - 1, -1, -1):
            for y in range(self.height - 1, -1, -1):
                if not self.matrix[x][y].fire:
                    rtl = 0
                    if x < self.width - 1:
                        if self.matrix[x + 1][y]:
                            rtl = self.matrix[x + 1][y].right_to_left
                    btt = 0
                    if y < self.height - 1:
                        if self.matrix[x][y + 1]:
                            btt = self.matrix[x][y + 1].bottom_to_top
                else:
                    rtl = -1
                    btt = -1
                self.matrix[x][y].add_xy(rtl + 1, btt + 1)
                if (x + y) % 2 == 0:
                    temp_score = self.matrix[x][y].get_score()
                    if temp_score > high_score_val[high_score_n]:
                        for i in range(high_score_n):
                            if temp_score > high_score_val[i]:
                                high_score_xs.insert(i, x)
                                high_score_ys.insert(i, y)
                                high_score_val.insert(i, temp_score)
                                break
                    elif temp_score == high_score_val[high_score_n]:
                        if not floor(random()*7):
                            for i in range(high_score_n):
                                if temp_score > high_score_val[i]:
                                    high_score_xs.insert(i, x)
                                    high_score_ys.insert(i, y)
                                    high_score_val.insert(i, temp_score)
                                    break
        self.print_score()
        # if high_score_val[score_picker]:
        for picker in range(len(high_score_val)):
            point = Point(high_score_xs[score_picker], high_score_ys[score_picker])
            if is_already_occupied(point, self.remain_positions):
                return point
        return Point(high_score_xs[0], high_score_ys[0])

    def mining_data(self):
        """
        Use mining data here
        :return: - None: not found anything useful
        """
        # TODO chi viet ham mining data o day nhe
        return None

    def print_score(self):
        for y in range(self.height - 1, -1, -1):
            line = 'y:' + str(y) + ' '
            for x in range(0, self.width):
                line += '  ' + str(self.matrix[x][y].get_score())
            print line
        line = 'x:  '
        for x in range(0, self.width):
            line += '  ' + str(x)
        print line

    def get_y(self, x, y):
        if x % 2 == 0:
            return y
        else:
            return y + 1

    def get_pre_point_x(self, x, y):
        if x % 2 == 0:
            return self.matrix[x + 1][y]

