"""
Module 7: Human vs Human Tic-Tac-Toe
Notice how clean the main loop is because logic and UI are separated!
"""

import pygame
import sys
from tic_tac_toe import TicTacToeState
from ui import TicTacToeUI

def main():
    state = TicTacToeState()
    ui = TicTacToeUI()
    
    ui.draw_figures(state)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not state.is_terminal:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                # Ask UI which square was clicked
                move_idx = ui.get_square_from_mouse(mouseX, mouseY)
                
                # Ask Engine if move is legal
                if move_idx in state.get_legal_moves():
                    # Tell Engine to update state
                    state = state.make_move(move_idx)
                    
                    # Tell UI to render new state
                    ui.draw_figures(state)
                    
                    if state.is_terminal:
                        if state.winner == 0:
                            print("Draw!")
                        else:
                            print(f"Player {state.winner} Wins!")

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
