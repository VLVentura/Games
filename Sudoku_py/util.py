import pygame

WINDOW_HEIGHT = 540
WINDOW_WIDTH = 540
N_BLOCKS = 9

BLOCK_SIZE = WINDOW_WIDTH // N_BLOCKS

def text_object(pos, text, size, color):
    font = pygame.font.SysFont('freemono', size, True)

    txt = font.render(text, 1, color)
    rect = txt.get_rect()
    rect.center = pos

    return (txt, rect)