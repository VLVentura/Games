try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

from copy import deepcopy

import util.color as color
import util.utils as utils
from model.entities.cube import Cube

class Snake:

    KEY_MOVES = {
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1), 
        pygame.K_RIGHT: (1, 0), 
        pygame.K_DOWN: (0, 1) 
    }
    FORBIDDEN_DIRECTION = {
        pygame.K_LEFT: (1, 0),
        pygame.K_UP: (0, 1), 
        pygame.K_RIGHT: (-1, 0), 
        pygame.K_DOWN: (0, -1) 
    }
    APPEND_CUBE = {
        (1, 0): (-1, 0),
        (-1, 0): (1, 0),
        (0, -1): (0, 1),
        (0, 1): (0, -1)
    }

    def __init__(self, pos: tuple):
        self.collisionSound = pygame.mixer.Sound('sounds/collision.wav')
        self.noSound = pygame.mixer.Sound('sounds/no.wav')
        self.eatSound = pygame.mixer.Sound('sounds/eat.wav')

        self.color = color.GREEN

        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}

        self.direction = (1,0)

    def move(self, keys):
        for move in Snake.KEY_MOVES.keys():
            if len(self.body) == 1:
                if keys[move]:
                    self.update_turns(move)
            else:
                if keys[move] and self.direction != Snake.FORBIDDEN_DIRECTION[move]:
                    self.update_turns(move)
        
        for index, cube in enumerate(self.body):
            position = deepcopy(cube.pos)

            if position in self.turns:
                turn = self.turns[position]
                cube.move((turn[0], turn[1]))

                if index == len(self.body) - 1:
                    self.turns.pop(position)
            else:
                if cube.direction[0] == -1 and cube.pos[0] <= 0: 
                    cube.pos = (utils.ROWS - 1, cube.pos[1])
                elif cube.direction[0] == 1 and cube.pos[0] >= utils.ROWS - 1: 
                    cube.pos = (0, cube.pos[1])
                elif cube.direction[1] == 1 and cube.pos[1] >= utils.ROWS - 1: 
                    cube.pos = (cube.pos[0], 0)
                elif cube.direction[1] == -1 and cube.pos[1] <= 0: 
                    cube.pos = (cube.pos[0], utils.ROWS - 1)
                else:
                    cube.move(cube.direction)
    
    def draw(self, window):
        for cube in self.body:
            if cube == self.head:
                cube.draw(window, True)
            else:
                cube.draw(window)
    
    def add_cube(self):
        direction = self.body[-1].direction
        position = Snake.APPEND_CUBE[direction]

        x = self.body[-1].pos[0] + position[0]
        y = self.body[-1].pos[1] + position[1]

        self.body.append(Cube((x, y), direction))
        self.eatSound.play()
    
    def body_collision(self):
        for cube in self.body[1:]:
            if self.head.pos == cube.pos:
                pygame.mixer.music.stop()
                self.collisionSound.play()
                self.noSound.play()
                return True
                
        return False
    
    def update_turns(self, move):
        self.direction = Snake.KEY_MOVES[move]
        self.turns[deepcopy(self.head.pos)] = self.direction

