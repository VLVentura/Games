import pygame

import color
import util

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((util.WINDOW_WIDTH, util.WINDOW_HEIGHT))

        self.run = True
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.blockSize = util.BLOCK_SIZE
    
    def init(self):
        while self.run:
            pygame.display.set_caption('Sudoku')

            pygame.time.delay(50)
            self.clock.tick(self.fps)

            self.window.fill(color.FLAT_GREY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            for i in range(0,10):
                if i % 3 == 0:
                    n = 3
                else:
                    n = 1
                pygame.draw.line(self.window, color.LIGHT_BLUE, (0, i * 60), (600, i * 60), n)
                pygame.draw.line(self.window, color.LIGHT_BLUE, (i * 60, 0), (i * 60, 600), n)

            for i in range(10):
                text, pos = util.text_object((i * 60 - 30, 30), '1', 35, color.BLACK)
                self.window.blit(text, pos)
                text, pos = util.text_object((30, i * 60 - 30), '1', 35, color.BLACK)
                self.window.blit(text, pos)
            
            positions = [] #left, right, upper, down
            for i in range(1,10):
                for j in range(1,10):
                    positions.append((60 * j - 60, 60 * j, 60 * i - 60, 60 * i))

            mouse = pygame.mouse.get_pos()
            for pos in positions:
                if pos[0] < mouse[0] < pos[1] and pos[2] < mouse[1] < pos[3]:
                    pygame.draw.rect(self.window, color.RED, (pos[0], pos[2], self.blockSize, self.blockSize), 2)

            pygame.display.update()