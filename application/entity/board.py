from __future__ import (
    absolute_import,
    unicode_literals,
)
from application.entity.ship import Ship
from application.utils.utils import (
    init_position,
    is_already_occupied,
    get_near_positions,
    is_double_occupied,
    is_valid_position
)
from application.utils.const import MAX_ATTEMPT


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_ship = []
        self.allocates = []

    def init_ships(self, ships):
        for ship_data in ships:
            for index in range(int(ship_data['quantity'])):
                ship = self.init_ship(ship_data)
                # can not init ship after 500 times attempt
                # re-init whole board
                if not ship:
                    self.allocates = []
                    self.current_ship = []
                    return self.init_ships(ships)
                self.allocates.extend(ship.positions)
                self.current_ship.append(ship)

    def init_ship(self, ship_data):
        """
        Ship meta data ``{"type": "BB", "quantity": 4}``
        :param ship_data:
        :return:
        """
        ship_type = ship_data['type']
        # try to init ship in 500 times
        for i in range(0, MAX_ATTEMPT):
            # random head position of ship
            ship_head = init_position(self.width, self.height)
            # from this head random direction of ship
            # and init whole ship data
            ship = Ship(ship_type, ship_head)

            # check position of ship is valid or not
            if self.is_valid_ship(ship):
                return ship
        else:
            return None

    def is_valid_ship(self, ship):
        """
        Check position of ship is overlap other ship or not.
        Optional: support nice position
        :param ship:
        :return:
        """
        for piece in ship.positions:
            # Does not outside board
            if not is_valid_position(piece, self.width, self.height):
                return False
            # Does not overlap other ship
            if is_already_occupied(piece, self.allocates):
                return False
            # Does not near any ship
            if not self.is_nice_position(piece):
                return False
        return True

    def is_nice_position(self, position):
        """
        A position is nice when it does not near any ships.
        :param position: A position need to check
        :return:
        """
        nears_position = get_near_positions(position, self.width, self.height)
        if is_double_occupied(nears_position, self.allocates):
            return False
        return True
