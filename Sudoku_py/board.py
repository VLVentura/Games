import pygame

from copy import deepcopy

import util
import color

class Board:
    def __init__(self, window):
        self.window = window

        self.board = util.create_board()
        self.originalBoard = deepcopy(self.board)

        self.blockSize = util.BLOCK_SIZE
        self.blocksPositions, self.gridPositions = util.board_positions()
        
        self.auxiliarBlocksList = util.auxiliar_block_list()
        self.auxiliarBlocksPositions = dict()
        
        self.mode = None
        self.selectedBlock = None
        self.selectedBlockColor = None
        self.selectBlockPosition = None

    def draw(self, mouse, click):
        self.window.fill(color.FLAT_GREY)
        self.draw_selected_block(mouse, click)
        self.draw_grid()
        self.draw_red_block(mouse)
        self.draw_board()
    
    def draw_solver(self):
        self.window.fill(color.FLAT_GREY)
        self.draw_grid()
        self.draw_board()
        pygame.display.update()
        pygame.time.delay(100)
    
    def get_player_input(self, val):
        if val == 'clean':
            self.mode = None
            self.selectedBlock = None
            self.selectedBlockColor = None
            self.selectBlockPosition = None

        if self.mode == 1:
            if val:
                row, col = self.selectBlockPosition
                self.board[row][col] = val
        elif self.mode == 2:
            if val:
                row, col = self.selectBlockPosition
                self.board[row][col] = 0
                self.auxiliarBlocksList[(row, col)][val-1] = not self.auxiliarBlocksList[(row, col)][val-1]
    
    def solver(self, board=None):
        if board == None:
            board = self.board

        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find
        
        for i in range(1,10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i

                self.draw_solver()

                if self.solver(board):
                    return True
                
                board[row][col] = None

                self.draw_solver()
        
        return False
    
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] in [0, None]:
                    return (i, j)
        return None
    
    def valid(self, board, num, pos):
        # Checking row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        
        # Checking column
        for i in range(9):
            if board[i][pos[1]] == num and pos[1] != i:
                return False
        
        # Checking mini grid
        x = pos[1] // 3
        y = pos[0] // 3

        for i in range(y * 3, 3 * (y + 1)):
            for j in range(x * 3, 3 * (x + 1)):
                if board[i][j] == num and (i, j) != pos:
                    return False
        
        return True

    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] in [0, None]:
                    return False
        return True
    
    def has_won(self):
        pass

    def draw_grid(self):
        for i in range(util.N_BLOCKS + 1):
            n = 1 if i % 3 != 0 else 3
            pygame.draw.line(self.window, color.LIGHT_BLUE, (0, i * self.blockSize), (util.WINDOW_WIDTH, i * self.blockSize), n)
            pygame.draw.line(self.window, color.LIGHT_BLUE, (i * self.blockSize, 0), (i * self.blockSize, util.WINDOW_HEIGHT), n)
    
    def draw_red_block(self, mouse):
        for block in self.blocksPositions:
            if block['left'] < mouse[0] < block['right'] and block['top'] < mouse[1] < block['down']:
                pygame.draw.rect(self.window, color.RED, (block['left'], block['top'], self.blockSize, self.blockSize), 2)
    
    def draw_selected_block(self, mouse, click):
        for block in self.blocksPositions:
            if block['left'] < mouse[0] < block['right'] and block['top'] < mouse[1] < block['down']:
                if click[0]:
                    self.mode = 1
                    self.selectedBlockColor = color.TEAL
                    self.selectedBlock = (block['left'], block['top'], self.blockSize, self.blockSize)
                    self.selectBlockPosition = self.gridPositions[(block['left'], block['right'], block['top'], block['down'])]
                elif click[2]:
                    self.mode = 2
                    self.selectedBlockColor = color.BLUE_GREY
                    self.selectedBlock = (block['left'], block['top'], self.blockSize, self.blockSize)
                    self.selectBlockPosition = self.gridPositions[(block['left'], block['right'], block['top'], block['down'])]

        if self.mode != None:
            pygame.draw.rect(self.window, self.selectedBlockColor, self.selectedBlock)
    
    def draw_board(self):
        for i in range(util.N_BLOCKS):
            for j in range(util.N_BLOCKS):
                if self.board[i][j] == 0:
                    self.draw_small_numbers(i, j)
                elif self.board[i][j]:
                    text, pos = util.text_object((j * 60 + 30,  i * 60 + 30), str(self.board[i][j]), 35, color.BLACK)
                    self.window.blit(text, pos)
    
    def draw_small_numbers(self, row, col):
        whatToDraw = self.auxiliarBlocksList[(row, col)]
        if (row, col) not in self.auxiliarBlocksPositions.keys():
            self.auxiliarBlocksPositions[(row, col)] = {'left': self.selectedBlock[0], 'top': self.selectedBlock[1]}
        block = self.auxiliarBlocksPositions[(row, col)]

        left = block['left'] + 10
        top = block['top'] + 10

        for i, val in enumerate(whatToDraw):
            n = i + 1
            text, pos = util.text_object((left, top), str(n), 15, color.BLACK)
            left += 20
            if n % 3 == 0:
                top += 20
                left = block['left'] + 10

            if val:
                self.window.blit(text, pos)