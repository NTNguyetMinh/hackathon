from __future__ import (
    absolute_import,
    unicode_literals,
)

class Score(object):

    def __init__(self, x, y, lr, tb):
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
        return vertical_score * horizontal_score
