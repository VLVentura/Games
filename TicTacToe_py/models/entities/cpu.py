try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

import util.utils as util
from random import randint
from copy import deepcopy

class Cpu:

    MARK = util.MARK
    CHAR = util.CHAR

    def __init__(self, mode, player):
        self.mode = mode.capitalize()
        self.name = 'CPU {}'.format(self.mode)
        self.player = player
        self.score = 0
        self.mark = Cpu.MARK[self.player]
        self.char = Cpu.CHAR[self.player]
        self.what_ai = {
            'Easy': self.random_ai,
            'Hard': self.find_best_move
        }

    def make_move(self, board=None):
        return self.what_ai[self.mode](board)

    def random_ai(self, board):
        return randint(1,9)

    def is_moves_left(self, board):
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ['X', 'O']:
                    return True

        return False

    def evaluate(self, board):
        for move in util.WIN_MOVES:
            x = util.POSITIONS_ON_BOARD[move[0]]
            y = util.POSITIONS_ON_BOARD[move[1]]
            z = util.POSITIONS_ON_BOARD[move[2]]

            if board[x[0]][x[1]] == board[y[0]][y[1]] == board[z[0]][z[1]] == self.cpu:
                return 10
            elif board[x[0]][x[1]] == board[y[0]][y[1]] == board[z[0]][z[1]] == self.opponent:
                return -10

        return 0
    
    def minimax(self, board, depth, isMax):
        score = self.evaluate(board)

        if score == 10 or score == -10:
            return score
        if self.is_moves_left(board) == False:
            return 0

        if isMax:
            best = -1000
            isMax = not isMax

            for i in range(3):
                for j in range(3):
                    if board[i][j] not in ['X', 'O']:
                        val = board[i][j]
                        board[i][j] = self.cpu
                        best = max(best, self.minimax(board, depth+1, isMax))
                        board[i][j] = val
        else:
            best = 1000
            isMax = not isMax

            for i in range(3):
                for j in range(3):
                    if board[i][j] not in ['X', 'O']:
                        val = board[i][j]
                        board[i][j] = self.opponent
                        best = min(best, self.minimax(board, depth+1, isMax))
                        board[i][j] = val
        
        return best
    
    def opponent_char(self):
        if self.char == 'O':
            return 'X'
        return 'O'

    def find_best_move(self, brd):
        board = deepcopy(brd.board)

        count = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] not in ['X', 'O']:
                    count += 1
        
        if count == 9:
            return randint(1,9)

        self.cpu = self.char
        self.opponent = self.opponent_char()
        
        bestScore = -1000
        bestMove = None

        for i in range(3):
            for j in range(3):
                if board[i][j] not in ['X', 'O']:
                    move = board[i][j]
                    board[i][j] = self.cpu
                    score = self.minimax(board, 0, False)
                    board[i][j] = move

                    if score > bestScore:
                        bestMove = move
                        bestScore = score
        
        return bestMove