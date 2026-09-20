"""
Connect Four: Core Game Logic and Heuristic AI
"""
import numpy as np
import copy
import random

ROWS = 6
COLS = 7

class ConnectFourState:
    def __init__(self, board=None, current_player=1):
        if board is None:
            self.board = np.zeros((ROWS, COLS), dtype=int)
        else:
            self.board = np.copy(board)
            
        self.current_player = current_player
        self.winner = None
        self.is_terminal = False

    def get_legal_moves(self):
        """Returns a list of valid columns (0-6) that are not full."""
        if self.is_terminal:
            return []
        valid_locations = []
        for col in range(COLS):
            if self.board[0][col] == 0: # If top row in this col is empty
                valid_locations.append(col)
        return valid_locations

    def make_move(self, col):
        """Drops a piece in the chosen column and returns new state."""
        new_board = np.copy(self.board)
        
        # Find lowest empty row in this col
        for row in range(ROWS-1, -1, -1):
            if new_board[row][col] == 0:
                new_board[row][col] = self.current_player
                break
                
        next_player = 2 if self.current_player == 1 else 1
        new_state = ConnectFourState(new_board, next_player)
        new_state._check_winner()
        return new_state

    def _check_winner(self):
        """Checks for 4 in a row. Sets self.winner and self.is_terminal."""
        # Horizontal
        for c in range(COLS-3):
            for r in range(ROWS):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3]:
                    self.winner = self.board[r][c]
                    self.is_terminal = True
                    return
        # Vertical
        for c in range(COLS):
            for r in range(ROWS-3):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c]:
                    self.winner = self.board[r][c]
                    self.is_terminal = True
                    return
        # Pos Diagonals
        for c in range(COLS-3):
            for r in range(ROWS-3):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3]:
                    self.winner = self.board[r][c]
                    self.is_terminal = True
                    return
        # Neg Diagonals
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if self.board[r][c] != 0 and self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3]:
                    self.winner = self.board[r][c]
                    self.is_terminal = True
                    return

        # Check for draw (top row is full)
        if 0 not in self.board[0]:
            self.winner = 0
            self.is_terminal = True

# --- HEURISTIC EVALUATION ---

def evaluate_window(window, player):
    """Scores a window of 4 slots."""
    score = 0
    opponent = 2 if player == 1 else 1
    
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
        
    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4 # Block the opponent!
        
    return score

def heuristic_score(state, maximizing_player):
    """Calculates heuristic score of board for the maximizing player."""
    score = 0
    # Prefer center column
    center_array = list(state.board[:, COLS//2])
    center_count = center_array.count(maximizing_player)
    score += center_count * 3

    # Score Horizontals
    for r in range(ROWS):
        row_array = list(state.board[r,:])
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, maximizing_player)

    # Score Verticals
    for c in range(COLS):
        col_array = list(state.board[:,c])
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, maximizing_player)

    # Score Pos Diags
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [state.board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, maximizing_player)

    # Score Neg Diags
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [state.board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, maximizing_player)
            
    return score

# --- MINIMAX WITH ALPHA-BETA AND DEPTH LIMIT ---

def minimax_ab_depth(state, depth, alpha, beta, is_maximizing, maximizing_player):
    if state.is_terminal:
        if state.winner == maximizing_player:
            return 1000000000 # Instant win is better than any heuristic
        elif state.winner == 0:
            return 0
        else:
            return -1000000000
            
    # DEPTH LIMIT - Call Heuristic
    if depth == 0:
        return heuristic_score(state, maximizing_player)

    if is_maximizing:
        best_score = -float('inf')
        for move in state.get_legal_moves():
            child_state = state.make_move(move)
            score = minimax_ab_depth(child_state, depth - 1, alpha, beta, False, maximizing_player)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha: break
        return best_score
    else:
        best_score = float('inf')
        for move in state.get_legal_moves():
            child_state = state.make_move(move)
            score = minimax_ab_depth(child_state, depth - 1, alpha, beta, True, maximizing_player)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha: break
        return best_score

def get_best_move(state, depth=4):
    best_score = -float('inf')
    best_move = random.choice(state.get_legal_moves()) # Fallback
    alpha = -float('inf')
    beta = float('inf')
    maximizing_player = state.current_player
    
    for move in state.get_legal_moves():
        child_state = state.make_move(move)
        score = minimax_ab_depth(child_state, depth - 1, alpha, beta, False, maximizing_player)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)
            
    return best_move
