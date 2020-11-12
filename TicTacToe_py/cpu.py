try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

import util
from random import randint

class Cpu:

    MARK = util.MARK
    CHAR = util.CHAR

    def __init__(self, mode, player):
        self.mode = mode.capitalize()
        self.name = 'CPU {}'.format(self.mode)
        self.player = player
        self.score = 0
        self.mark = Cpu.MARK[self.player]
        self.char = Cpu.CHAR[self.player]
        self.what_ai = {
            'Easy': self.random_ai,
            'Hard': self.minimax_ai
        }

    def make_move(self, board=None):
        return self.what_ai[self.mode](board)

    def random_ai(self, board):
        return randint(1,9)

    def minimax_ai(self, board):
        pass

    def minimax_score(self, board, player, cpu):
        pass