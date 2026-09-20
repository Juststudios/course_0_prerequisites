"""
Tic-Tac-Toe: Core Game Logic (The Engine)
This file contains NO Pygame code. It is purely the mathematical
representation of the game state and rules.
"""

class TicTacToeState:
    def __init__(self, board=None, current_player=1):
        # Board is a 1D list of 9 elements. 0=Empty, 1=X, 2=O
        if board is None:
            self.board = [0] * 9
        else:
            self.board = list(board)
        self.current_player = current_player
        self.winner = None
        self.is_terminal = False

    def get_legal_moves(self):
        """Returns a list of indices (0-8) that are empty."""
        if self.is_terminal:
            return []
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, move_index):
        """
        Returns a NEW game state after the move is made.
        We do NOT modify the current state (this is crucial for AI searching).
        """
        if self.board[move_index] != 0 or self.is_terminal:
            raise ValueError("Illegal move")

        new_board = list(self.board)
        new_board[move_index] = self.current_player
        
        next_player = 2 if self.current_player == 1 else 1
        
        new_state = TicTacToeState(new_board, next_player)
        new_state._check_winner()
        return new_state

    def _check_winner(self):
        """Checks if the game is over and updates self.winner and self.is_terminal."""
        win_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        for a, b, c in win_lines:
            if self.board[a] != 0 and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                self.is_terminal = True
                return
        
        if 0 not in self.board:
            # Draw
            self.winner = 0
            self.is_terminal = True
