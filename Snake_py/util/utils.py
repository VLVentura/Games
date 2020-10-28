try:
    import pygame
except ModuleNotFoundError as error:
    print(error)

from random import randint

ROWS = 20
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
DISTANCE = WINDOW_WIDTH // ROWS

def get_pos():
    return (randint(1, 19), randint(1, 19))

def text_object(pos, text, size, color):
    font = pygame.font.SysFont('comicsans', size, True)

    txt = font.render(text, 1, color)
    rect = txt.get_rect()
    rect.center = pos

    return (txt, rect)