"""
Solutions to Debugging Exercises
================================
"""

# ==========================================
# SOLUTION 1: The Infinite Loop
# ==========================================
# The bug: The student passed `state` into the recursive call instead of `child_state`.
# The algorithm just evaluated the same exact board position infinitely.
def fixed_minimax(state, depth, is_maximizing):
    if state.is_terminal:
        return state.score
        
    if is_maximizing:
        best_score = -999
        for move in state.get_legal_moves():
            child_state = state.make_move(move) # Create the child!
            # Pass the child_state to the recursion, not the current state.
            best_score = max(best_score, fixed_minimax(child_state, depth + 1, False))
        return best_score
    # ... (same for MIN)


# ==========================================
# SOLUTION 2: The Self-Sabotaging AI
# ==========================================
# The bug: A Maximizer wants the highest possible positive score. 
# The student added points for black pieces and subtracted points for white pieces.
# Therefore, losing pieces increased the score! The AI tried to maximize the score
# by getting all its pieces captured.
def fixed_heuristic(board):
    score = 0
    white_pieces = board.count("W")
    black_pieces = board.count("B")
    
    score += white_pieces * 10
    score -= black_pieces * 10
    return score


# ==========================================
# SOLUTION 3: The Broken Alpha-Beta
# ==========================================
# The bug: MAX updates Alpha, MIN updates Beta.
# The student had MAX updating Beta, and MIN updating Alpha. This breaks the math.
def fixed_alpha_beta(state, alpha, beta, is_maximizing):
    if state.is_terminal: return state.score
    
    if is_maximizing:
        best_score = -999
        for move in state.get_legal_moves():
            child = state.make_move(move)
            score = fixed_alpha_beta(child, alpha, beta, False)
            best_score = max(best_score, score)
            
            # FIXED: MAX updates Alpha
            alpha = max(alpha, best_score)
            
            if beta <= alpha: break
        return best_score
    else:
        best_score = 999
        for move in state.get_legal_moves():
            child = state.make_move(move)
            score = fixed_alpha_beta(child, alpha, beta, True)
            best_score = min(best_score, score)
            
            # FIXED: MIN updates Beta
            beta = min(beta, best_score)
            
            if beta <= alpha: break
        return best_score
