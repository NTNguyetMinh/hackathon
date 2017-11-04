from __future__ import (
    absolute_import,
    unicode_literals,
)

from math import floor
from random import random


class Score(object):
    def __init__(self, x=0, y=0, lr=0, tb=0):
        self.x = x
        self.y = y
        self.fire = False

        self.left_to_right = 0 or lr
        self.right_to_left = 0
        self.top_to_bottom = 0 or tb
        self.bottom_to_top = 0

    def add_xy(self, rl, bt):
        self.right_to_left = 0 or rl
        self.bottom_to_top = 0 or bt

    def get_score(self):
        if self.fire:
            return 0
        vertical_score = self.left_to_right + self.right_to_left - abs(self.left_to_right - self.right_to_left)
        horizontal_score = self.top_to_bottom + self.bottom_to_top - abs(self.top_to_bottom - self.bottom_to_top)
        score = vertical_score * horizontal_score
        if score < 80:
            return score

        # 80% chance of getting 61
        if floor(random()*5):
            return 61
        # 20% chance of getting 67
        return 67
