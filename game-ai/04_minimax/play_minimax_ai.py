"""
Module 15: Tic-Tac-Toe with Minimax AI
"""

import pygame
import sys
import sys
import os

# Add the 03_tic_tac_toe directory to the path so we can import the Engine and UI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '03_tic_tac_toe')))

from tic_tac_toe import TicTacToeState
from ui import TicTacToeUI
from minimax import get_best_move

def main():
    state = TicTacToeState()
    ui = TicTacToeUI()
    ui.draw_figures(state)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Human Turn (Player 1)
            if event.type == pygame.MOUSEBUTTONDOWN and state.current_player == 1 and not state.is_terminal:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                move_idx = ui.get_square_from_mouse(mouseX, mouseY)
                if move_idx in state.get_legal_moves():
                    state = state.make_move(move_idx)
                    ui.draw_figures(state)
                    
                    if state.is_terminal:
                        print(f"Game Over! Winner: {state.winner}")
        
        # AI Turn (Player 2)
        if state.current_player == 2 and not state.is_terminal:
            print("AI is thinking...")
            
            # Ask the Minimax algorithm for the best move
            ai_move = get_best_move(state)
            
            state = state.make_move(ai_move)
            ui.draw_figures(state)
            
            if state.is_terminal:
                print(f"Game Over! Winner: {state.winner}")

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
