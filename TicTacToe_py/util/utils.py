try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

from copy import deepcopy

WINDOW_WIDTH = 510
WINDOW_HEIGHT = 510
ROWS = 3
BLOCK_SIZE = 170

WIN_MOVES = [
    (1,4,7), (2,5,8), (3,6,9),
    (1,2,3), (4,5,6), (7,8,9),
    (1,5,9), (3,5,7)
]
POSITIONS_ON_BOARD = {
    1: (0,0), 2: (0,1), 3: (0,2),
    4: (1,0), 5: (1,1), 6: (1,2),
    7: (2,0), 8: (2,1), 9: (2,2)
}

CHAR = {
    1: 'X',
    2: 'O'
}
MARK = {
    1: pygame.image.load('img/X.png'),
    2: pygame.image.load('img/O.png')
}

def text_object(pos, text, size, color):
    font = pygame.font.SysFont('freemono', size, True)

    txt = font.render(text, 1, color)
    rect = txt.get_rect()
    rect.center = pos

    return (txt, rect)