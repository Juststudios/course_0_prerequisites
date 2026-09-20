"""
Checkers AI: Depth-Limited Alpha-Beta Search & Heuristics
=========================================================
Implements an intelligent Checkers agent combining:
  1. Material Advantage: Men = 10 pts, Kings = 20 pts
  2. Positional Valuation:
     - Center control (rows 3-4, cols 2-5): strategic pivot points
     - Advancement towards promotion (rewarding forward rank progress)
     - Back-row home defense (protecting baseline against opponent crowning)
  3. Mobility: Rewarding board flexibility and penalizing blocked pieces
  4. Depth-limited Minimax with Alpha-Beta Pruning
"""

import math
from checkers import (
    CheckersState, EMPTY, RED_MAN, BLACK_MAN, RED_KING, BLACK_KING,
    PLAYER_RED, PLAYER_BLACK
)

# Heuristic Weights
MATERIAL_MAN = 100
MATERIAL_KING = 180
CENTER_BONUS = 15
BACK_ROW_DEFENSE = 20
ADVANCEMENT_BONUS = 8
MOBILITY_BONUS = 5

CENTER_SQUARES = {
    (3, 2), (3, 4), (4, 1), (4, 3), (4, 5), (3, 6)
}


def evaluate_checkers(state, player):
    """
    Evaluate the board state from the perspective of `player`.
    
    Returns
    -------
    float
        Higher values favor `player`. Large positive/negative values for terminals.
    """
    if state.is_terminal:
        if state.winner == player:
            return 100000.0
        elif state.winner == 0:
            return 0.0
        else:
            return -100000.0

    opponent = PLAYER_BLACK if player == PLAYER_RED else PLAYER_RED
    score = 0.0

    # 1. Material and Positional Evaluation
    for r in range(8):
        for c in range(8):
            piece = state.board[r, c]
            if piece == EMPTY:
                continue

            # Base material
            if piece == RED_MAN:
                val = MATERIAL_MAN + (7 - r) * ADVANCEMENT_BONUS
                if r == 7:
                    val += BACK_ROW_DEFENSE
                if (r, c) in CENTER_SQUARES:
                    val += CENTER_BONUS
                score += val if player == PLAYER_RED else -val

            elif piece == BLACK_MAN:
                val = MATERIAL_MAN + r * ADVANCEMENT_BONUS
                if r == 0:
                    val += BACK_ROW_DEFENSE
                if (r, c) in CENTER_SQUARES:
                    val += CENTER_BONUS
                score += val if player == PLAYER_BLACK else -val

            elif piece == RED_KING:
                val = MATERIAL_KING
                if (r, c) in CENTER_SQUARES:
                    val += CENTER_BONUS
                score += val if player == PLAYER_RED else -val

            elif piece == BLACK_KING:
                val = MATERIAL_KING
                if (r, c) in CENTER_SQUARES:
                    val += CENTER_BONUS
                score += val if player == PLAYER_BLACK else -val

    # 2. Mobility Evaluation
    # How many legal options does each player have?
    if state.current_player == player:
        own_moves = len(state.get_legal_moves())
        score += own_moves * MOBILITY_BONUS
    else:
        opp_moves = len(state.get_legal_moves())
        score -= opp_moves * MOBILITY_BONUS

    return score


def minimax_ab(state, depth, alpha, beta, is_maximizing, player):
    """
    Depth-limited Minimax search with Alpha-Beta pruning.
    
    Parameters
    ----------
    state : CheckersState
    depth : int
        Remaining depth to search.
    alpha : float
        Best score the maximizer can guarantee so far.
    beta : float
        Best score the minimizer can guarantee so far.
    is_maximizing : bool
    player : int (PLAYER_RED or PLAYER_BLACK)
    
    Returns
    -------
    tuple of (best_eval, best_move)
    """
    if depth == 0 or state.is_terminal:
        return evaluate_checkers(state, player), None

    legal_moves = state.get_legal_moves()
    if not legal_moves:
        return evaluate_checkers(state, player), None

    # Move ordering heuristic: search jump moves first (they drastically alter material)
    ordered_moves = sorted(legal_moves, key=lambda m: len(m), reverse=True)

    best_move = ordered_moves[0]

    if is_maximizing:
        max_eval = -math.inf
        for move in ordered_moves:
            next_state = state.make_move(move)
            # If next turn is opponent's, next level is minimizing
            next_is_max = (next_state.current_player == player)
            eval_score, _ = minimax_ab(next_state, depth - 1, alpha, beta, next_is_max, player)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in ordered_moves:
            next_state = state.make_move(move)
            next_is_max = (next_state.current_player == player)
            eval_score, _ = minimax_ab(next_state, depth - 1, alpha, beta, next_is_max, player)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move


def get_best_move(state, depth=4):
    """
    Select the optimal checkers move for state.current_player.
    
    Parameters
    ----------
    state : CheckersState
    depth : int, default=4
    
    Returns
    -------
    tuple of (r, c) coordinates
    """
    legal_moves = state.get_legal_moves()
    if not legal_moves:
        return None
    if len(legal_moves) == 1:
        # Only one legal move (forced) — no need to search tree!
        return legal_moves[0]

    _, best_move = minimax_ab(
        state=state,
        depth=depth,
        alpha=-math.inf,
        beta=math.inf,
        is_maximizing=True,
        player=state.current_player
    )
    return best_move if best_move is not None else legal_moves[0]
