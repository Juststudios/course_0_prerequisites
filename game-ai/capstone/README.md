# Game AI Capstone: Othello (Reversi) AI

## The Problem
Your final project is to build an AI for the board game Othello (also known as Reversi).
You must build this from scratch: the game logic, the rendering, and the AI.

Othello is played on an 8x8 grid. Players take turns placing a disc of their color.
Any opponent discs trapped in a straight line between the new disc and another disc of your color are flipped to your color.
The player with the most discs at the end wins.

## Milestones

### Milestone 1: The Engine (State & Rules)
Create a class `OthelloState` (similar to our Tic-Tac-Toe engine).
* Represent the 8x8 board.
* Write a `get_legal_moves()` function. This is tricky! You must scan in 8 directions from empty squares to see if placing a piece there would flip any opponent pieces.
* Write a `make_move(move)` function that copies the board, places the piece, flips the captured pieces, and returns the new state.

### Milestone 2: Pygame Rendering
Write a Pygame UI that imports your Engine and allows two humans to play Othello.
* Draw the 8x8 green grid.
* Draw the black and white circles.
* Highlight legal moves for the current player when they hover the mouse.

### Milestone 3: The AI & Heuristics
Implement Alpha-Beta pruning to create an AI opponent.
Because Othello is large, you must use a Depth Limit (e.g., depth 4 or 5) and a Heuristic.

**Heuristic Hint:** In Othello, having the most pieces in the middle of the game is often *bad*, because it gives your opponent more pieces to jump over! A good heuristic prioritizes **Corners** and **Edges** (since they cannot be flipped back).
Create a Piece-Square Table matrix that assigns high values (+100) to corners, and negative values (-50) to squares right next to corners.

## Deliverables
1. A fully playable Pygame Othello game (Human vs AI).
2. A Technical Report (Markdown or PDF).

## The Technical Report
Your report must include:
1. **Engine Architecture:** How did you represent the board? How does your legal move generator work?
2. **Heuristic Design:** Explain the heuristic you designed and *why* you chose those values.
3. **Experiment:** Pit your AI running at Depth 2 against your AI running at Depth 4. Who wins? Does Depth 4 take noticeably longer to think?
4. **Conclusion:** Based on the curriculum, if you had 6 months to make a world-champion Othello AI, would you stick with Minimax+Alpha-Beta, or would you use Reinforcement Learning? Why?

You can use `reversi_starter.py` to begin.
