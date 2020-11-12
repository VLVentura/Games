try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

import color 
import util

class Button:
    def __init__(self, window, clr, text, pos, function):
        self.window = window
        self.color = clr
        self.pos = pos
        self.function = function

        self.center = ((self.pos[2] // 2) + self.pos[0], (self.pos[3] // 2) + self.pos[1])
        self.text, self.textRectangle = util.text_object(self.center, text, 28, color.BLACK)
    
    def draw(self, mouse):
        if self.pos[0] < mouse[0] < self.pos[0] + self.pos[2] and self.pos[1] < mouse[1] < self.pos[1] + self.pos[3]:
            pygame.draw.rect(self.window, self.color[1], self.pos)
        else:
            pygame.draw.rect(self.window, self.color[0], self.pos)
        
        self.window.blit(self.text, self.textRectangle)

    def action(self, mouse, click):
        if self.pos[0] < mouse[0] < self.pos[0] + self.pos[2] and self.pos[1] < mouse[1] < self.pos[1] + self.pos[3]:
            if click[0]:
                self.function()

    