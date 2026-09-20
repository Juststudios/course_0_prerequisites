"""
The Minimax Algorithm
"""

def evaluate(state, maximizing_player):
    """
    Returns the utility (score) of a terminal state.
    Positive for Maximizer win, Negative for Minimizer win, 0 for draw.
    """
    if state.winner == maximizing_player:
        return 10
    elif state.winner == 0: # Draw
        return 0
    else: # Minimizer (opponent) won
        return -10

def minimax(state, depth, is_maximizing, maximizing_player):
    """
    Recursive Minimax search.
    Returns the optimal score for the current state.
    """
    # 1. Base Case: If the game is over, return the score
    if state.is_terminal:
        # We subtract depth so the AI prefers faster wins and slower losses
        score = evaluate(state, maximizing_player)
        if score > 0: score -= depth
        elif score < 0: score += depth
        return score

    # 2. Recursive Step for MAX (The AI)
    if is_maximizing:
        best_score = -float('inf')
        for move in state.get_legal_moves():
            # Simulate the move
            child_state = state.make_move(move)
            # Recursively call minimax for the opponent (MIN)
            score = minimax(child_state, depth + 1, False, maximizing_player)
            best_score = max(best_score, score)
        return best_score
        
    # 3. Recursive Step for MIN (The Opponent)
    else:
        best_score = float('inf')
        for move in state.get_legal_moves():
            # Simulate the move
            child_state = state.make_move(move)
            # Recursively call minimax for the AI (MAX)
            score = minimax(child_state, depth + 1, True, maximizing_player)
            best_score = min(best_score, score)
        return best_score

def get_best_move(state):
    """
    Acts as the entry point for Minimax.
    Instead of just returning the best score, it returns the actual move
    that leads to that best score.
    """
    best_score = -float('inf')
    best_move = None
    maximizing_player = state.current_player
    
    for move in state.get_legal_moves():
        child_state = state.make_move(move)
        # The child state is the opponent's turn, so is_maximizing is False
        score = minimax(child_state, 0, False, maximizing_player)
        
        if score > best_score:
            best_score = score
            best_move = move
            
    return best_move
