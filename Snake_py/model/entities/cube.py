try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

import util.color as color
import util.utils as utils

class Cube:
    def __init__(self, pos, direction=(1,0), color=color.RED):
        self.pos = pos
        self.direction = direction
        self.color = color
        self.distance = utils.DISTANCE

    def move(self, pos: tuple):
        x = self.pos[0] + pos[0]
        y = self.pos[1] + pos[1]
        
        self.pos = (x, y)
        self.direction = pos
    
    def draw(self, window, eyes=False):
        pygame.draw.rect(
            window, self.color, 
            (self.pos[0] * self.distance + 1, self.pos[1] * self.distance + 1, self.distance, self.distance)
        )
        if eyes: 
            center = self.distance // 2
            radius = 3
            circleMiddle = (self.pos[0] * self.distance + center - radius, self.pos[1] * self.distance + 8)
            circleMiddle2 = (self.pos[0] * self.distance + self.distance - radius * 2, self.pos[1] * self.distance + 8)
            pygame.draw.circle(window, color.BLACK, circleMiddle, radius)
            pygame.draw.circle(window, color.BLACK, circleMiddle2, radius)