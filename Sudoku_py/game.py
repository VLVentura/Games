import pygame

import time

import color
import util
from board import Board

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((util.WINDOW_WIDTH, util.WINDOW_HEIGHT))
        self.startTime = time.time()

        self.keysPressed = {
            pygame.K_1: 1, pygame.K_KP1: 1,
            pygame.K_2: 2, pygame.K_KP2: 2,
            pygame.K_3: 3, pygame.K_KP3: 3,
            pygame.K_4: 4, pygame.K_KP4: 4,
            pygame.K_5: 5, pygame.K_KP5: 5,
            pygame.K_6: 6, pygame.K_KP6: 6,
            pygame.K_7: 7, pygame.K_KP7: 7,
            pygame.K_8: 8, pygame.K_KP8: 8,
            pygame.K_9: 9, pygame.K_KP9: 9,
            pygame.K_ESCAPE: 'clean'
        }

        self.run = True
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.board = Board(self.window)

    def init(self):
        while self.run:
            pygame.display.set_caption('Sudoku - Time: {}'.format(self.time_elapsed(time.time() - self.startTime)))

            pygame.time.delay(50)
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            self.board.get_player_input(self.player_input())
            self.board.draw(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

            pygame.display.update()
    
    def player_input(self):
        val = None

        keys = pygame.key.get_pressed()
        for key in self.keysPressed.keys():
            if keys[key]:
                val = self.keysPressed[key]
        
        pygame.time.delay(45)
        return val
    
    def time_elapsed(self, sec):
        minutes = int(sec // 60)
        sec = int(sec % 60)
        return '{}m{}s'.format(minutes, sec)