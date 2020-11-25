try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

import util.color as color
import util.utils as util
import models.gui.playagain as playagain
import models.gui.confirm as confirm
from models.gui.boxname import DoubleBox, SimpleBox
from models.gui.button import Button
from models.entities.board import Board
from models.entities.player import Player
from models.entities.cpu import Cpu
from db.database import Database

class Game:

    WINDOW_WIDTH = util.WINDOW_WIDTH
    WINDOW_HEIGHT = util.WINDOW_HEIGHT
    ROWS = util.ROWS
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode((Game.WINDOW_HEIGHT, Game.WINDOW_HEIGHT))
        
        self.blockSize = util.BLOCK_SIZE
        self.fps = 10
        self.clock = pygame.time.Clock()

        self.db = Database()

        self.runMenu = [True]
        self.runPlayMenu = [True]
        self.runScoreBoard = [True]
        self.runMatchHistory = [True]
        self.runOneVsOne = [True]
        self.runCpuEasy = [True]
        self.runCpuHard = [True]
        self.runDict = {
            'playmenu': self.runPlayMenu,
            'onevsone': self.runOneVsOne,
            'cpueasy': self.runCpuEasy,
            'cpuhard': self.runCpuHard
        }

        self.playButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Play', (200, 200, 140, 50), self.play_menu)
        self.scoreBoardButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Score', (200, 280, 140, 50), self.score_board)
        self.matchHistoryButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'History', (200, 360, 140, 50), self.match_history)
        self.quitButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Quit', (200, 440, 140, 50), self.quit_game)
        self.pvpButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'PvP', (200, 180, 140, 50), self.one_vs_one)
        self.cpuEasyButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'CPU Easy', (200, 260, 140, 50), self.cpu_easy)
        self.cpuHardButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'CPU Hard', (200, 340, 140, 50), self.cpu_hard)
        self.onlineLocalButton = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Online', (200, 420, 140, 50), self.online_local)
        self.backMenuButtonFromPlay = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Back',  (30, 445, 100, 50), self.back_menu_play)
        self.backMenuButtonFromScore = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Back',  (30, 445, 100, 50), self.back_menu_score)
        self.backMenuButtonFromHistory = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Back',  (30, 445, 100, 50), self.back_menu_history)
        self.resetButtonScore = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Reset',  (370, 445, 100, 50), self.reset_score)
        self.resetButtonHistory = Button(self.window, (color.DARK_BLUE, color.SOFT_BLUE), 'Reset',  (370, 445, 100, 50), self.reset_history)

    def init(self):
        self.menu()

    def menu(self):
        self.play_music('sounds/music.wav')
        while self.runMenu[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            pygame.display.set_caption('Tic Tac Toe')
            self.window.fill(color.GREY)

            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Tic Tac Toe', 70, color.BLACK)
            self.window.blit(text, textPosition)
            self.draw_buttons(self.playButton, self.scoreBoardButton, self.matchHistoryButton, self.quitButton, mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.playButton, self.scoreBoardButton, self.matchHistoryButton, self.quitButton,
                                mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed()
            )

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
            self.draw_buttons(self.pvpButton, self.cpuEasyButton, self.cpuHardButton, self.onlineLocalButton, self.backMenuButtonFromPlay, 
                                mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.pvpButton, self.cpuEasyButton, self.cpuHardButton, self.onlineLocalButton, self.backMenuButtonFromPlay, 
                                mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed())

            pygame.display.update()
        
        self.runPlayMenu[0] = True

    def score_board(self):
        while self.runScoreBoard[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            pygame.display.set_caption('Tic Tac Toe')
            self.window.fill(color.GREY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runScoreBoard[0] = False
                    self.runMenu[0] = False

            self.draw_buttons(self.backMenuButtonFromScore, self.resetButtonScore, mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.backMenuButtonFromScore, self.resetButtonScore, mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed())

            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Scoreboard', 70, color.BLACK)
            self.window.blit(text, textPosition)

            self.text, self.textRectangle = util.text_object((Game.WINDOW_WIDTH // 3, Game.WINDOW_HEIGHT // 3), 'Player', 40, color.BLACK)
            self.window.blit(self.text, self.textRectangle)

            self.text, self.textRectangle = util.text_object((Game.WINDOW_WIDTH - 180, Game.WINDOW_HEIGHT // 3), 'Score', 40, color.BLACK)
            self.window.blit(self.text, self.textRectangle)

            for i, data in enumerate(self.db.read_from_scoreboard()):
                self.text, self.textRectangle = util.text_object((Game.WINDOW_WIDTH // 3, Game.WINDOW_HEIGHT // 3 + (i + 1) * 40), str(data[0]), 30, color.RED)
                self.window.blit(self.text, self.textRectangle)

                self.text, self.textRectangle = util.text_object((Game.WINDOW_WIDTH - 180, Game.WINDOW_HEIGHT // 3 + (i + 1) * 40), str(data[1]), 30, color.RED)
                self.window.blit(self.text, self.textRectangle)
            
            pygame.display.update()
        
        self.runScoreBoard[0] = True

    def match_history(self):
        while self.runMatchHistory[0]:
            pygame.time.delay(50)
            self.clock.tick(self.fps)

            pygame.display.set_caption('Tic Tac Toe')
            self.window.fill(color.GREY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runMatchHistory[0] = False
                    self.runMenu[0] = False
            
            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 6), 'Match History', 60, color.BLACK)
            self.window.blit(text, textPosition)

            text, textPosition = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 3), 'Matches', 40, color.BLACK)
            self.window.blit(text, textPosition)

            self.draw_buttons(self.backMenuButtonFromHistory, self.resetButtonHistory, mouse=pygame.mouse.get_pos())
            self.buttons_actions(self.backMenuButtonFromHistory, self.resetButtonHistory, mouse=pygame.mouse.get_pos(), click=pygame.mouse.get_pressed())

            
            for i, data in enumerate(self.db.read_from_match_history()):   
                string = '{} [{}] vs. [{}] {}'.format(data[0], data[1], data[3], data[2])
                self.text, self.textRectangle = util.text_object((Game.WINDOW_WIDTH // 2, Game.WINDOW_HEIGHT // 3 + (i + 2) * 40), string, 30, color.RED)
                self.window.blit(self.text, self.textRectangle)

            pygame.display.update()

        self.runMatchHistory[0] = True

    def quit_game(self):
        self.runMenu[0] = False

    def back_menu_play(self):
        self.runPlayMenu[0] = False
    
    def back_menu_score(self):
        self.runScoreBoard[0] = False

    def back_menu_history(self):
        self.runMatchHistory[0] = False

    def reset_score(self):
        confirm.display(self.db, 'SCOREBOARD')
    
    def reset_history(self):
        confirm.display(self.db, 'MATCH_HISTORY')

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
        self.db.insert(self.playerOne.name, self.playerOne.score, self.playerTwo.name, self.playerTwo.score)
    
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
        self.db.insert(self.playerOne.name, self.playerOne.score, self.playerTwo.name, self.playerTwo.score)

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
        self.db.insert(self.playerOne.name, self.playerOne.score, self.playerTwo.name, self.playerTwo.score)
    
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

    def play_music(self, file):
        self.music = pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)

    def close_all(self):
        self.db.close()
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()