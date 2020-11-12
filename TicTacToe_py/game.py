try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

import color
import util
import playagain
from board import Board
from player import Player
from cpu import Cpu
from boxname import DoubleBox, SimpleBox
from button import Button

class Game:

    WINDOW_WIDTH = util.WINDOW_WIDTH
    WINDOW_HEIGHT = util.WINDOW_HEIGHT
    ROWS = util.ROWS
    
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.window = pygame.display.set_mode((Game.WINDOW_HEIGHT, Game.WINDOW_HEIGHT))
        
        self.blockSize = util.BLOCK_SIZE
        self.fps = 10
        self.clock = pygame.time.Clock()

        self.runMenu = [True]
        self.runPlayMenu = [True]
        self.runOneVsOne = [True]
        self.runCpuEasy = [True]
        self.runCpuHard = [True]
        self.runDict = {
            'playmenu': self.runPlayMenu,
            'onevsone': self.runOneVsOne,
            'cpueasy': self.runCpuEasy,
            'cpuhard': self.runCpuHard
        }

        self.playButton = Button(self.window, (color.BLACK, color.WHITE), 'Play', (200, 200, 100, 50), self.play_menu)
        self.pvpButton = Button(self.window, (color.BLACK, color.WHITE), 'PvP', (200, 180, 140, 50), self.one_vs_one)
        self.cpuEasyButton = Button(self.window, (color.BLACK, color.WHITE), 'CPU Easy', (200, 260, 140, 50), self.cpu_easy)
        self.cpuHardButton = Button(self.window, (color.BLACK, color.WHITE), 'CPU Hard', (200, 340, 140, 50), self.cpu_hard)
        self.onlineLocalButton = Button(self.window, (color.BLACK, color.WHITE), 'Online', (200, 420, 140, 50), self.online_local)
        self.backMenuButton = Button(self.window, (color.BLACK, color.WHITE), 'Back',  (30, 445, 100, 50), self.back_menu)

    def init(self):
        self.menu()

    def menu(self):
        while self.runMenu[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            pygame.display.set_caption('Tic Tac Toe')
            self.window.fill(color.GREY)

            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Tic Tac Toe', 70, color.BLACK)
            self.window.blit(text, textPosition)
            self.draw_buttons(self.playButton, mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.playButton, mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runMenu[0] = False

            pygame.display.update()

        self.close_all()
    
    def play_menu(self):
        while self.runPlayMenu[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runPlayMenu[0] = False
                    self.runMenu[0] = False

            pygame.display.set_caption('Tic Tac Toe')
            self.window.fill(color.GREY)

            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Play', 70, color.BLACK)
            self.window.blit(text, textPosition)
            self.draw_buttons(self.pvpButton, self.cpuEasyButton, self.cpuHardButton, self.onlineLocalButton, self.backMenuButton, 
                                mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.pvpButton, self.cpuEasyButton, self.cpuHardButton, self.onlineLocalButton, self.backMenuButton, 
                                mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed())

            pygame.display.update()
        
        self.runPlayMenu[0] = True

    def back_menu(self):
        self.runPlayMenu[0] = False

    def one_vs_one(self):
        box = DoubleBox()
        self.playerOne = Player(box.names[0], 1)
        self.playerTwo = Player(box.names[1], 2)
        board = Board(self.playerOne, self.playerTwo)
        
        while self.runOneVsOne[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)
            
            pygame.display.set_caption(
                '{} [{}] vs. [{}] {}  |  Turn: {} (\'{}\')'
                .format(self.playerOne.name, self.playerOne.score, self.playerTwo.score, self.playerTwo.name, 
                board.whose_turn().name, board.whose_turn().char)
            )
            self.draw_board_and_update(board)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.runOneVsOne[0] = False
                        self.runPlayMenu[0] = False
                        self.runMenu[0] = False
                move = board.get_player_move(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                if self.runOneVsOne[0] == False or board.is_valid_move(move):
                    break

            self.draw_board_and_update(board)
            self.check_end_game(board, 'onevsone')
            
            board.playerTurn = not board.playerTurn
        
        self.runOneVsOne[0] = True
    
    def cpu_easy(self):
        box = SimpleBox()
        self.playerOne = Player(box.name, 1)
        self.playerTwo = Cpu('easy', 2)
        board = Board(self.playerOne, self.playerTwo)
        self.round = 1
        
        while self.runCpuEasy[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)
            
            pygame.display.set_caption(
                '{} [{}] vs. [{}] {}  |  Turn: {} (\'{}\')'
                .format(self.playerOne.name, self.playerOne.score, self.playerTwo.score, self.playerTwo.name, 
                board.whose_turn().name, board.whose_turn().char)
            )
            self.draw_board_and_update(board)

            if board.whose_turn() == self.playerOne:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.runCpuEasy[0] = False
                            self.runPlayMenu[0] = False
                            self.runMenu[0] = False
                    move = board.get_player_move(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                    if self.runCpuEasy[0] == False or board.is_valid_move(move):
                        break
            else:
                while True:
                    move = self.playerTwo.make_move()
                    if board.is_valid_move(move):
                        break

            board.playerTurn = not board.playerTurn
            
            self.draw_board_and_update(board)
            self.check_end_game(board, 'cpueasy')
        
        self.runCpuEasy[0] = True

    def cpu_hard(self):
        box = SimpleBox()
        self.playerOne = Player(box.name, 1)
        self.playerTwo = Cpu('hard', 2)
        board = Board(self.playerOne, self.playerTwo)
        self.round = 1
        
        while self.runCpuHard[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)
            
            pygame.display.set_caption(
                '{} [{}] vs. [{}] {}  |  Turn: {} (\'{}\')'
                .format(self.playerOne.name, self.playerOne.score, self.playerTwo.score, self.playerTwo.name, 
                board.whose_turn().name, board.whose_turn().char)
            )
            self.draw_board_and_update(board)

            if board.whose_turn() == self.playerOne:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.runCpuHard[0] = False
                            self.runPlayMenu[0] = False
                            self.runMenu[0] = False
                    move = board.get_player_move(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                    if self.runCpuHard[0] == False or board.is_valid_move(move):
                        break
            else:
                while True:
                    move = self.playerTwo.make_move(board)
                    if board.is_valid_move(move):
                        break

            board.playerTurn = not board.playerTurn
            
            self.draw_board_and_update(board)
            self.check_end_game(board, 'cpuhard')
        
        self.runCpuHard[0]
    
    def online_local(self):
        pass

    def check_end_game(self, board, function):
        if board.has_winner():
            winner = board.whos_won()
            winner.score += 1
            self.runDict[function][0] = playagain.display_question(winner.name)
            if self.runDict[function][0]:
                self.round += 1
                board.restart(self.is_even_round())
        elif board.is_full():
            self.runDict[function][0] = playagain.display_question(None, 'tie')
            if self.runDict[function][0]:
                self.round += 1
                board.restart(self.is_even_round())

    def is_even_round(self):
        if self.round % 2 == 0:
            return True
        
        return False

    def draw_board_and_update(self, board):
        board.draw_board(self.window)
        pygame.display.update()

    def draw_buttons(self, *args, **kwargs):
        for button in args:
            button.draw(kwargs['mouse'])
    
    def buttons_actions(self, *args, **kwargs):
        for button in args:
            button.action(kwargs['mouse'], kwargs['click'])

    def close_all(self):
        pygame.font.quit()
        pygame.quit()