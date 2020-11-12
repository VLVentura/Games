try:
    import pygame 
except ModuleNotFoundError as error:
    print(error)

from copy import deepcopy

WINDOW_WIDTH = 510
WINDOW_HEIGHT = 510
ROWS = 3
BLOCK_SIZE = 170

CHAR = {
    1: 'X',
    2: 'O'
}
MARK = {
    1: pygame.image.load('X.png'),
    2: pygame.image.load('O.png')
}

def text_object(pos, text, size, color):
    font = pygame.font.SysFont('freemono', size, True)

    txt = font.render(text, 1, color)
    rect = txt.get_rect()
    rect.center = pos

    return (txt, rect)