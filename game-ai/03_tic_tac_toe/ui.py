"""
Tic-Tac-Toe: Pygame Rendering (The View)
This file handles drawing the game state to the screen.
"""
import pygame
import sys

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

class TicTacToeUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tic Tac Toe AI')
        self.screen.fill(BG_COLOR)
        self.draw_lines()

    def draw_lines(self):
        # 1 horizontal
        pygame.draw.line(self.screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        # 2 horizontal
        pygame.draw.line(self.screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # 1 vertical
        pygame.draw.line(self.screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # 2 vertical
        pygame.draw.line(self.screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figures(self, state):
        self.screen.fill(BG_COLOR)
        self.draw_lines()
        for i in range(9):
            row = i // 3
            col = i % 3
            if state.board[i] == 1:
                # Draw X
                pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 50), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 25)
                pygame.draw.line(self.screen, CROSS_COLOR, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + SQUARE_SIZE - 50), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 50, row * SQUARE_SIZE + 50), 25)
            elif state.board[i] == 2:
                # Draw O
                pygame.draw.circle(self.screen, CIRCLE_COLOR, 
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), 
                                   SQUARE_SIZE//2 - 40, 15)
        pygame.display.update()

    def get_square_from_mouse(self, x, y):
        """Converts mouse pixels into an array index (0-8)"""
        clicked_row = y // SQUARE_SIZE
        clicked_col = x // SQUARE_SIZE
        return clicked_row * 3 + clicked_col
