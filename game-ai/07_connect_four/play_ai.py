"""
Module 21: Play Connect Four vs AI
"""

import pygame
import sys
import math
from connect_four import ConnectFourState, get_best_move, ROWS, COLS

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)

def draw_board(screen, board):
    # Pygame y=0 is top, our internal board row 0 is top
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLS):
        for r in range(ROWS):		
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    
    state = ConnectFourState()
    draw_board(screen, state.board)
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 75)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if state.current_player == 1 and not state.is_terminal:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            # Human turn
            if event.type == pygame.MOUSEBUTTONDOWN and state.current_player == 1 and not state.is_terminal:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if col in state.get_legal_moves():
                    state = state.make_move(col)
                    draw_board(screen, state.board)
                    
                    if state.is_terminal:
                        label = myfont.render(f"Player {state.winner} wins!", 1, RED if state.winner == 1 else YELLOW)
                        screen.blit(label, (40, 10))
                        pygame.display.update()
        
        # AI Turn
        if state.current_player == 2 and not state.is_terminal:
            print("AI thinking...")
            col = get_best_move(state, depth=4)
            
            state = state.make_move(col)
            draw_board(screen, state.board)
            
            if state.is_terminal:
                label = myfont.render(f"Player {state.winner} wins!", 1, RED if state.winner == 1 else YELLOW)
                screen.blit(label, (40, 10))
                pygame.display.update()

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
