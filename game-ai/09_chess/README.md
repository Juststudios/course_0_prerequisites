# Module 9: Chess

## What You Will Learn
You will learn how to architect a Game AI for a highly complex board game by leveraging an external library for legal move generation, and combining Minimax, Alpha-Beta, Depth Limits, and a sophisticated Heuristic Evaluation.

## Chess Representation
Chess rules are massive. En passant, castling rights, promotion, 50-move rules, checking if a move puts your own king in check... writing all of this from scratch is an engineering project on its own.

In the real world, AI developers use highly optimized libraries (often written in C or C++) to handle the board representation. We will use `python-chess`.

`python-chess` gives us:
* `board.legal_moves`: A generator of all strictly legal moves.
* `board.push(move)`: Make a move.
* `board.pop()`: Undo the last move (much faster than copying the whole board state!).
* `board.is_game_over()`: Checks for checkmate, stalemate, etc.

## The Chess Evaluation Function (Module 26)
Because Chess is so complex, a simple heuristic (like counting material) is not enough to play well. 

A standard simple chess heuristic includes:
1. **Material:** Pawn=100, Knight=300, Bishop=300, Rook=500, Queen=900.
2. **Piece Square Tables (PST):** A Knight in the center of the board is worth more than a Knight in the corner. We use a matrix to add bonus points based on where a piece is standing.
3. **Mobility:** Having more legal moves available is generally good.

## Optimization: Move Ordering (Module 27)
Alpha-Beta Pruning works best when it finds a "good" move early, because that creates a strong Alpha/Beta bound which prunes the rest of the tree.
If we search terrible moves first, we won't prune anything!

Therefore, we **Sort the legal moves** before searching them. We evaluate captures (`board.is_capture(move)`) and promotions first. This drastically speeds up the search.

## Running the Code
We have provided `chess_ai.py` which contains the AI and a simple text-based loop. (Pygame chess is complex to draw, but you can build a UI as a challenge!).

Run it:
```bash
python chess_ai.py
```
