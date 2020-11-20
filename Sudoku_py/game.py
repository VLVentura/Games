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
        
        self.mode = None
        self.selectedSquare = None

    def init(self):
        while self.run:
            pygame.display.set_caption('Sudoku')

            pygame.time.delay(50)
            self.clock.tick(self.fps)

            self.window.fill(color.FLAT_GREY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            positions = [] #left, right, upper, down
            for i in range(1,10):
                for j in range(1,10):
                    positions.append((60 * j - 60, 60 * j, 60 * i - 60, 60 * i))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            for pos in positions:
                if pos[0] < mouse[0] < pos[1] and pos[2] < mouse[1] < pos[3]:
                    if click[0]:
                        self.mode = 1
                        clr = color.TEAL
                        self.selectedSquare = (pos[0], pos[2], self.blockSize, self.blockSize)
                    elif click[2]:
                        self.mode = 2
                        clr = color.BLUE_GREY
                        self.selectedSquare = (pos[0], pos[2], self.blockSize, self.blockSize)
            
            if self.mode != None:
                pygame.draw.rect(self.window, clr, self.selectedSquare)

            for i in range(0,10):
                if i % 3 == 0:
                    n = 3
                else:
                    n = 1
                pygame.draw.line(self.window, color.LIGHT_BLUE, (0, i * 60), (600, i * 60), n)
                pygame.draw.line(self.window, color.LIGHT_BLUE, (i * 60, 0), (i * 60, 600), n)

            for pos in positions:
                if pos[0] < mouse[0] < pos[1] and pos[2] < mouse[1] < pos[3]:
                    pygame.draw.rect(self.window, color.RED, (pos[0], pos[2], self.blockSize, self.blockSize), 2)
            
            aux = 2
            if self.mode == 2:
                text, pos = util.text_object((self.selectedSquare[0] + 20 * aux - 10, self.selectedSquare[1] + 10), '1', 15, color.BLACK)
                self.window.blit(text, pos)

            for i in range(10):
                text, pos = util.text_object((i * 60 - 30, 30), '1', 35, color.BLACK)
                self.window.blit(text, pos)
                text, pos = util.text_object((30, i * 60 - 30), '1', 35, color.BLACK)
                self.window.blit(text, pos)

            pygame.display.update()