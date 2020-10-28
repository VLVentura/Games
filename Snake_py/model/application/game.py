try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

from random import randint

import util.color as color
import util.utils as utils
from model.entities.snake import Snake
from model.entities.food import Food
from model.gui.button import Button

class Game:

    ROWS = utils.ROWS
    WINDOW_WIDTH = utils.WINDOW_WIDTH
    WINDOW_HEIGHT = utils.WINDOW_HEIGHT

    def __init__(self):
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.font.init()
        except pygame.error as error:
            print(error)
            exit()

        self.window = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        pygame.mixer.music.set_volume(0.1)

        self.text, self.textRectangle = utils.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Snake Game', 75, color.GREY)

        self.playButton = Button(self.window, (color.DARK_BLUE, color.LIGHT_BLUE), 'Play',  (200, 200, 100, 50), self.play)
        self.optionsButton = Button(self.window, (color.DARK_GREEN, color.LIGHT_GREEN), 'Score',  (200, 280, 100, 50), self.score)
        self.quitButton = Button(self.window, (color.DARK_YELLOW, color.LIGHT_YELLOW), 'Quit',  (200, 360, 100, 50), self.quit_game)
        self.backMenuButton = Button(self.window, (color.DARK_GREEN, color.LIGHT_GREEN), 'Back',  (30, 420, 100, 50), self.back_menu)

        self.fps = 15
        self.runMenu = True
        self.runPlay = True
        self.runOptions = True
        self.clock = pygame.time.Clock()

        self.score = 0
        self.blockSize = utils.DISTANCE
        self.snake = Snake(utils.get_pos())
        self.food = Food(utils.get_pos())

    def init(self):
        self.menu()
    
    def menu(self):
        self.play_music('sounds/menu_music.mp3')
        while self.runMenu:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            pygame.display.set_caption('Snake Game')
            self.window.fill(color.BLACK)
            self.window.blit(self.text, self.textRectangle)
        
            self.check_event()
            
            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()
            self.draw_buttons(self.playButton, self.optionsButton, self.quitButton)
            self.buttons_actions(self.playButton, self.optionsButton, self.quitButton)
            
            pygame.display.update()

        self.close_all()
    
    def play(self):
        self.play_music('sounds/game_music.mp3')
        while self.runPlay:
            pygame.time.delay(50)
            self.clock.tick(self.fps)
        
            self.check_event('play')

            keys = pygame.key.get_pressed()
            self.snake.move(keys)
            self.check_collision()
            self.redraw_window()
        
        self.play_music('sounds/menu_music.mp3')
        self.runPlay = True
        self.snake = Snake(utils.get_pos())
        self.food = Food(utils.get_pos())
        self.score = 0
    
    def score(self):
        while self.runOptions:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            self.check_event('options')

            self.text, self.textRectangle = utils.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Score Board', 75, color.GREY)

            pygame.display.set_caption('Snake Game')
            self.window.fill(color.BLACK)
            self.window.blit(self.text, self.textRectangle)

            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()
            self.draw_buttons(self.backMenuButton)
            self.buttons_actions(self.backMenuButton)
            
            pygame.display.update()
        
        self.text, self.textRectangle = utils.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Snake Game', 75, color.GREY)
        self.runOptions = True

    def quit_game(self):
        self.runMenu = False

    def back_menu(self):
        self.runOptions = False
    
    def check_event(self, func='main'):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if func == 'play':
                    self.runPlay = False
                elif func == 'options':
                    self.runOptions = False
                self.runMenu = False
    
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
    
    def draw_buttons(self, *args, **kwargs):
        for button in args:
            button.draw(self.mouse)
    
    def buttons_actions(self, *args, **kwargs):
        for button in args:
            button.action(self.mouse, self.click)
    
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
            self.runPlay = False
    
    def play_music(self, file):
        self.music = pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
    
    def stop_music(self):
        pygame.mixer.music.stop()

    def close_all(self):
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()