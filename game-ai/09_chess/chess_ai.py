"""
Module 24, 25, 26, 27: Chess AI Engine
Using python-chess for board representation, and Alpha-Beta + PST for the AI.
"""

import chess
import math

# --- EVALUATION FUNCTION (HEURISTICS) ---

# Piece values
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-Square Tables (PST) - encourage pieces to move to good squares
# (Simplified example for Knights: encourage center squares)
knight_pst = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

def evaluate_board(board):
    """
    Evaluates the board from WHITE's perspective.
    Positive score = White is winning. Negative score = Black is winning.
    """
    if board.is_checkmate():
        if board.turn:
            return -99999 # Black wins
        else:
            return 99999  # White wins
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Material value
            val = piece_values[piece.piece_type]
            
            # Positional value (example for Knights only)
            if piece.piece_type == chess.KNIGHT:
                # If black, flip the board vertically for the PST
                sq_idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
                val += knight_pst[sq_idx]

            if piece.color == chess.WHITE:
                score += val
            else:
                score -= val
                
    return score

# --- MINIMAX SEARCH ---

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    # Move Ordering Optimization: Search captures first to trigger Alpha-Beta faster
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)

    if is_maximizing:
        best_score = -float('inf')
        for move in legal_moves:
            board.push(move) # Make move
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()      # Undo move
            
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def get_best_move(board, depth=3):
    best_move = None
    is_maximizing = board.turn == chess.WHITE
    
    alpha = -float('inf')
    beta = float('inf')
    
    best_score = -float('inf') if is_maximizing else float('inf')
    
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)
    
    for move in legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta, not is_maximizing)
        board.pop()
        
        if is_maximizing:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            
    return best_move

# --- SIMPLE PLAY LOOP ---
if __name__ == '__main__':
    board = chess.Board()
    
    print("Welcome to Terminal Chess!")
    print(board)
    
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nYour turn (White).")
            user_move = input("Enter move (e.g. e2e4): ")
            try:
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move!")
            except:
                print("Invalid format!")
        else:
            print("\nAI is thinking...")
            ai_move = get_best_move(board, depth=3) # Depth 3 is fast enough for Python
            board.push(ai_move)
            print(f"AI plays: {ai_move}")
            
        print("\n" + str(board))
        
    print("Game Over!")
