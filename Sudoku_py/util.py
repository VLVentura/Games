import pygame

WINDOW_HEIGHT = 540
WINDOW_WIDTH = 540
N_BLOCKS = 9

BLOCK_SIZE = WINDOW_WIDTH // N_BLOCKS

def create_board() -> list:
    board = []
    for i in range(N_BLOCKS + 1):
        board.append([None] * N_BLOCKS)
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