try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

import util.utils as util

class Player:
    
    MARK = util.MARK
    CHAR = util.CHAR

    def __init__(self, name, player):
        self.name = name.capitalize()
        self.player = player
        self.score = 0
        self.mark = Player.MARK[self.player]
        self.char = Player.CHAR[self.player]