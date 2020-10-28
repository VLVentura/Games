
import util.color as color
from model.entities.cube import Cube

class Food:
    def __init__(self, pos, color=color.GREEN):
        self.color = color
        self.fruit = Cube(pos, color=self.color)
    
    def draw(self, window):
        self.fruit.draw(window)