import numpy as np
import pygame
import sys

ROWS = 6
COLS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# 🎨 Light color theme
BOARD_COLOR = (173, 216, 230)         
BACKGROUND = (245, 245, 245)          
PLAYER1_COLOR = (240, 128, 128)       
PLAYER2_COLOR = (250, 250, 210)       
TEXT_COLOR = (60, 60, 60)      

pygame.init()
FONT = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(SIZE)

def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all([board[r][c + i] == piece for i in range(4)]):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all([board[r + i][c] == piece for i in range(4)]):
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all([board[r + i][c + i] == piece for i in range(4)]):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all([board[r - i][c + i] == piece for i in range(4)]):
                return True
    return False

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BOARD_COLOR, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = BACKGROUND
            if board[r][c] == 1:
                color = PLAYER1_COLOR
            elif board[r][c] == 2:
                color = PLAYER2_COLOR
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

board = create_board()
game_over = False
turn = 0
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, SQUARESIZE))
            x_pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PLAYER1_COLOR, (x_pos, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, PLAYER2_COLOR, (x_pos, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BACKGROUND, (0, 0, WIDTH, SQUARESIZE))

            col = event.pos[0] // SQUARESIZE

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn + 1)

                if winning_move(board, turn + 1):
                    winner_color = PLAYER1_COLOR if turn == 0 else PLAYER2_COLOR
                    label = FONT.render(f"Player {turn + 1} wins!", 1, TEXT_COLOR)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)
                turn ^= 1  

    if game_over:
        pygame.time.wait(3000)
