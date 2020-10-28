from random import randint

ROWS = 20
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
DISTANCE = WINDOW_WIDTH // ROWS

def get_pos():
    return (randint(1, 19), randint(1, 19))