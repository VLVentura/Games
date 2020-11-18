try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

from copy import deepcopy

import util.utils as util
import util.color as color

class Board:

    ROWS = util.ROWS
    WIN_MOVES = util.WIN_MOVES
    BOARD = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    
    def __init__(self, playerOne, playerTwo):
        self.blockSize = util.BLOCK_SIZE

        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.playerTurn = True

        self.imgs = []
        self.board = deepcopy(Board.BOARD)
        self.positionsOnBoard = util.POSITIONS_ON_BOARD
        self.whereToDraw = {
            1: (self.blockSize // 2, self.blockSize // 2),
            2: (self.blockSize + self.blockSize // 2, self.blockSize // 2),
            3: (self.blockSize * 2 + self.blockSize // 2, self.blockSize // 2),
            4: (self.blockSize // 2, self.blockSize + self.blockSize // 2),
            5: (self.blockSize + self.blockSize // 2, self.blockSize + self.blockSize // 2),
            6: (self.blockSize * 2 + self.blockSize // 2, self.blockSize + self.blockSize // 2),
            7: (self.blockSize // 2, self.blockSize * 2 + self.blockSize // 2),
            8: (self.blockSize + self.blockSize // 2, self.blockSize * 2 + self.blockSize // 2),
            9: (self.blockSize * 2 + self.blockSize // 2, self.blockSize * 2 + self.blockSize // 2)
        }
    
    def get_player_move(self, mouse, click):
        if click[0]:
            if mouse[0] < self.blockSize and mouse[1] < self.blockSize:
                return  1
            elif self.blockSize < mouse[0] < 2 * self.blockSize and mouse[1] < self.blockSize:
                return  2
            elif mouse[0] > 2 * self.blockSize and mouse[1] < self.blockSize:
                return  3
            elif mouse[0] < self.blockSize and self.blockSize < mouse[1] < 2 * self.blockSize:
                return  4
            elif self.blockSize < mouse[0] < 2 * self.blockSize and self.blockSize < mouse[1] < 2 * self.blockSize:
                return  5
            elif mouse[0] > 2 * self.blockSize and self.blockSize < mouse[1] < 2 * self.blockSize:
                return  6
            elif mouse[0] < self.blockSize and mouse[1] > self.blockSize:
                return  7
            elif self.blockSize < mouse[0] < 2 * self.blockSize and mouse[1] > 2 * self.blockSize:
                return  8
            elif mouse[0] > 2 * self.blockSize and mouse[1] > 2 * self.blockSize:
                return  9

    def is_valid_move(self, move):
        if move:
            row, col = self.positionsOnBoard[move]
            if self.board[row][col] not in ['X', 'O']:
                imgPos = self.__get_img_pos(move, self.whose_turn().mark)
                self.board[row][col] = self.whose_turn().char
                self.imgs.append((self.whose_turn().mark, imgPos))
                return True

        return False
    
    def has_winner(self):
        for move in Board.WIN_MOVES:
            x = self.positionsOnBoard[move[0]]
            y = self.positionsOnBoard[move[1]]
            z = self.positionsOnBoard[move[2]]
            if self.board[x[0]][x[1]] == self.board[y[0]][y[1]] == self.board[z[0]][z[1]]:
                self.winnerChar = self.board[x[0]][x[1]]
                return True
        
        return False 

    def whos_won(self):
        if self.playerOne.char == self.winnerChar:
            return self.playerOne
        
        return self.playerTwo

    def is_full(self):
        for row in self.board:
            for char in row:
                if char not in ['X', 'O']:
                    return False
        
        return True
    
    def whose_turn(self):
        if self.playerTurn == True:
            return self.playerOne
        
        return self.playerTwo

    def draw_board(self, window):
        window.fill(color.WHITE)
        self.__draw_grid(window)
        self.__draw_marks(window)
    
    def restart(self, isEven):
        self.imgs = []
        self.board = deepcopy(Board.BOARD)
        
        temp = self.playerOne.char, self.playerOne.mark
        self.playerOne.char, self.playerOne.mark = self.playerTwo.char, self.playerTwo.mark
        self.playerTwo.char, self.playerTwo.mark = temp[0], temp[1]

        if isEven:
            self.playerTurn = False
        else:
            self.playerTurn = True
    
    def __draw_grid(self, window):
        for r in range(1, Board.ROWS):
            pygame.draw.line(window, color.BLACK, (0, r * self.blockSize), (util.WINDOW_WIDTH, r * self.blockSize), 2)
            pygame.draw.line(window, color.BLACK, (r * self.blockSize, 0), (r * self.blockSize, util.WINDOW_WIDTH), 2)
    
    def __draw_marks(self, window):
        for img in self.imgs:
            window.blit(img[0], img[1])
    
    def __get_img_pos(self, move, mark):
        rect = mark.get_rect()
        rect.centerx = self.whereToDraw[move][0]
        rect.centery = self.whereToDraw[move][1]
        return rect