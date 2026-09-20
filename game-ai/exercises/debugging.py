"""
Game AI Debugging Exercises
===========================
Below are three common bugs found when writing Game AI.
Diagnose and fix them. Do not check the solutions directory until you try!
"""

# ==========================================
# EXERCISE 1: The Infinite Loop
# ==========================================
# A student wrote a Minimax algorithm for Tic-Tac-Toe.
# When they run it, Python crashes with a "RecursionError: maximum recursion depth exceeded".
# Look at the code below. Why doesn't it stop? Fix the bug.

def bad_minimax(state, depth, is_maximizing):
    # Base case?
    if state.is_terminal:
        return state.score
        
    if is_maximizing:
        best_score = -999
        for move in state.get_legal_moves():
            # BUG: Look closely at what is passed into the recursive call!
            best_score = max(best_score, bad_minimax(state, depth + 1, False))
        return best_score
    else:
        best_score = 999
        for move in state.get_legal_moves():
            best_score = min(best_score, bad_minimax(state, depth + 1, True))
        return best_score


# ==========================================
# EXERCISE 2: The Self-Sabotaging AI
# ==========================================
# A student wrote this heuristic for Checkers.
# They are playing as White (Maximizer). 
# But the AI is making terrible moves and constantly sacrificing its own pieces!
# Look at the heuristic function. Why is it doing this? Fix the bug.

def bad_heuristic(board):
    score = 0
    
    white_pieces = board.count("W")
    black_pieces = board.count("B")
    
    # We want White to win, so more white pieces should be good.
    # The student wrote:
    score += black_pieces * 10
    score -= white_pieces * 10
    
    return score


# ==========================================
# EXERCISE 3: The Broken Alpha-Beta
# ==========================================
# A student implemented Alpha-Beta pruning.
# It returns a score, but it's returning the WRONG score compared to normal Minimax.
# The bug is in how they update alpha and beta. Fix it.

def broken_alpha_beta(state, alpha, beta, is_maximizing):
    if state.is_terminal: return state.score
    
    if is_maximizing:
        best_score = -999
        for move in state.get_legal_moves():
            child = state.make_move(move)
            score = broken_alpha_beta(child, alpha, beta, False)
            best_score = max(best_score, score)
            
            # BUG IS HERE
            beta = max(beta, best_score)
            
            if beta <= alpha: break
        return best_score
    else:
        best_score = 999
        for move in state.get_legal_moves():
            child = state.make_move(move)
            score = broken_alpha_beta(child, alpha, beta, True)
            best_score = min(best_score, score)
            
            # BUG IS HERE
            alpha = min(alpha, best_score)
            
            if beta <= alpha: break
        return best_score
