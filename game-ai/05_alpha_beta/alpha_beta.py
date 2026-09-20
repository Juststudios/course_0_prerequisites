"""
Minimax with Alpha-Beta Pruning
"""

def evaluate(state, maximizing_player):
    """Returns the utility (score) of a terminal state."""
    if state.winner == maximizing_player:
        return 10
    elif state.winner == 0:
        return 0
    else:
        return -10

def minimax_alpha_beta(state, depth, alpha, beta, is_maximizing, maximizing_player):
    if state.is_terminal:
        score = evaluate(state, maximizing_player)
        if score > 0: score -= depth
        elif score < 0: score += depth
        return score

    if is_maximizing:
        best_score = -float('inf')
        for move in state.get_legal_moves():
            child_state = state.make_move(move)
            score = minimax_alpha_beta(child_state, depth + 1, alpha, beta, False, maximizing_player)
            best_score = max(best_score, score)
            
            # Update Alpha
            alpha = max(alpha, best_score)
            
            # PRUNING: If beta is less than or equal to alpha, MIN will never allow this branch
            if beta <= alpha:
                break # Stop searching other moves for this state!
                
        return best_score
        
    else:
        best_score = float('inf')
        for move in state.get_legal_moves():
            child_state = state.make_move(move)
            score = minimax_alpha_beta(child_state, depth + 1, alpha, beta, True, maximizing_player)
            best_score = min(best_score, score)
            
            # Update Beta
            beta = min(beta, best_score)
            
            # PRUNING: If beta is less than or equal to alpha, MAX will never choose this branch
            if beta <= alpha:
                break # Stop searching other moves for this state!
                
        return best_score

def get_best_move_ab(state):
    best_score = -float('inf')
    best_move = None
    maximizing_player = state.current_player
    
    alpha = -float('inf')
    beta = float('inf')
    
    for move in state.get_legal_moves():
        child_state = state.make_move(move)
        score = minimax_alpha_beta(child_state, 0, alpha, beta, False, maximizing_player)
        
        if score > best_score:
            best_score = score
            best_move = move
            
        alpha = max(alpha, best_score)
            
    return best_move
