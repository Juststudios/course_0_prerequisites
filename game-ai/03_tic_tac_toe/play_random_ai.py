"""
Module 8: Random AI Tic-Tac-Toe
Human plays as Player 1 (X), Random AI plays as Player 2 (O).
"""

import pygame
import sys
import random
import time
from tic_tac_toe import TicTacToeState
from ui import TicTacToeUI

def random_ai_move(state):
    """Returns a random legal move."""
    moves = state.get_legal_moves()
    return random.choice(moves)

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
            # Small delay so the AI doesn't move instantly (feels more natural)
            time.sleep(0.5) 
            
            # The AI asks the engine for legal moves, then picks one randomly
            ai_move = random_ai_move(state)
            state = state.make_move(ai_move)
            ui.draw_figures(state)
            
            if state.is_terminal:
                print(f"Game Over! Winner: {state.winner}")

if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
