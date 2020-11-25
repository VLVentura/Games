import pygame

import collections
from random import randint, shuffle
from copy import deepcopy

WINDOW_HEIGHT = 540
WINDOW_WIDTH = 540
N_BLOCKS = 9

BLOCK_SIZE = WINDOW_WIDTH // N_BLOCKS

def create_board() -> list:
    board = generate_board()
    indexes = []
    
    for i in range(35):
        while True:
            row = randint(0,8)
            col = randint(0,8)
            if (row, col) not in indexes:
                indexes.append((row, col))
                break
    
    for index in indexes:
        row, col = index
        board[row][col] = None

    return board

def board_positions() -> tuple:
    blockPos = []
    gridPos = dict()

    for i in range(1, N_BLOCKS + 1):
        for j in range(1, N_BLOCKS + 1):
            blockPos.append(
                {
                    'left': BLOCK_SIZE * (j - 1), 
                    'right': BLOCK_SIZE * j, 
                    'top': BLOCK_SIZE * (i - 1), 
                    'down': BLOCK_SIZE * i
                }
            )
            gridPos[(BLOCK_SIZE * (j - 1), BLOCK_SIZE * j, BLOCK_SIZE * (i - 1), BLOCK_SIZE * i)] = (i - 1, j - 1)

    return blockPos, gridPos

def auxiliar_block_list() -> dict:
    auxiliar = dict()

    for i in range(N_BLOCKS):
        for j in range(N_BLOCKS):
            auxiliar[(i,j)] = [False] * 9
    
    return auxiliar

def text_object(pos: tuple, text: str, size: int, color: tuple, font: str='freemono') -> tuple:
    """
    It will center the text in the pos and will return the text ready to blit

    :param pos: position with the text coordinates
    :param text: your text ready to blit
    :param size: size of the text
    :param color: tuple with the RGB colors of the text  
    :param font: font supported by pygame

    :return: (text, text position)
    """
    font = pygame.font.SysFont(font, size, True)

    txt = font.render(text, 1, color)
    rect = txt.get_rect()
    rect.center = pos

    return (txt, rect)

def shift(lst, n):
    lst = collections.deque(lst)
    lst.rotate(-n)
    return list(lst)

def generate_board():
    board = []

    main = [None] * 9
    for i in range(9):
        while True:
            n = randint(1,9)
            if n not in main:
                main[i] = n
                break

    shuffle(main)
    board.append(deepcopy(main))

    for i in range(1,9):
        temp = board[i-1]
        if i % 3 != 0:
            temp = shift(temp, 3)
        else:
            temp = shift(temp, 1)
        board.append(deepcopy(temp))
    
    for l in board:
        print(l)

    return board