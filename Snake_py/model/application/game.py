try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

from random import randint

import util.color as color
import util.utils as utils
from model.entities.snake import Snake
from model.entities.food import Food

class Game:

    ROWS = utils.ROWS
    WINDOW_WIDTH = utils.WINDOW_WIDTH
    WINDOW_HEIGHT = utils.WINDOW_HEIGHT

    def __init__(self):
        try:
            pygame.init()
            pygame.mixer.init()
        except pygame.error as error:
            print(error)
            exit()

        self.window = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        self.music = pygame.mixer.music.load('sounds/bgm.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.fps = 15
        self.run = True
        self.clock = pygame.time.Clock()

        self.score = 0
        self.blockSize = utils.DISTANCE
        self.snake = Snake(utils.get_pos())
        self.food = Food(utils.get_pos())

    def init(self):
        while self.run:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            
            keys = pygame.key.get_pressed()
            self.snake.move(keys)
            self.check_collision()
            self.redraw_window()
        
        self.close_all()
    
    def redraw_window(self):
        pygame.display.set_caption('Snake Game - Score: {}'.format(self.score))
        self.window.fill(color.BLACK)
        self.draw_grid()
        self.snake.draw(self.window)
        self.food.draw(self.window)
        pygame.display.update()
    
    def draw_grid(self):
        for r in range(1, Game.ROWS):
            pygame.draw.line(self.window, color.WHITE, (0, r * self.blockSize), (Game.WINDOW_WIDTH, r * self.blockSize))
            pygame.draw.line(self.window, color.WHITE, (r * self.blockSize, 0), (r * self.blockSize, Game.WINDOW_HEIGHT))
    
    def check_collision(self):
        if self.snake.head.pos == self.food.fruit.pos:
            foodPos = utils.get_pos()
            for cube in self.snake.body:
                if cube.pos == foodPos:
                    foodPos = utils.get_pos()

            self.food.fruit.pos = foodPos
            self.snake.add_cube()
            self.score += 1
        elif len(self.snake.body) != 1 and self.snake.body_collision():
            pygame.time.delay(4100)
            self.close_all()    
            exit()

    def close_all(self):
        pygame.mixer.quit()
        pygame.quit()