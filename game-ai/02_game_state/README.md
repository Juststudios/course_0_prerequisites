# Module 2: Game Architecture & Board Representation

## What You Will Learn
In this module, you will learn the most important concept in Game AI: **Separation of Concerns**. You will learn how to represent a board game mathematically so an AI can understand it, completely separate from how it is drawn on the screen.

## The Architecture Problem
When beginners make their first game, they often mix everything together:
```python
# BAD ARCHITECTURE
if mouse_clicked_on_pixel(150, 300):
    draw_X_on_screen(150, 300)
    check_if_screen_has_three_Xs_in_a_row()
```

If you do this, **you cannot build an AI.**
An AI needs to simulate thousands of possible future moves. It cannot simulate moves by "clicking the mouse" and "drawing X on the screen" 10,000 times a second.

## The Solution: Layers

A well-architected game separates logic from presentation:

```text
  INPUT     -> Reads human intent (e.g. mouse click at pixel 150, 300)
    ↓
GAME LOGIC  -> Translates pixel to Board Coordinate (Row 1, Col 0).
               Checks if move is legal.
               Updates internal array (board[1][0] = 'X').
               Checks for a winner.
    ↓
  RENDER    -> Reads the internal array and draws it on the screen.
```

If you build the game this way, the **AI** can entirely bypass the Input and Render layers. It can just ask the Game Logic: *"If I set board[1][0] to 'O', do I win?"*

## Representing the Board

To let the AI reason about the game, we represent the board as a data structure (usually a 1D list, 2D list, or NumPy matrix).

**Tic-Tac-Toe (2D List):**
```python
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
# 0 = Empty, 1 = Player X, 2 = Player O
```

**Chess (1D List / Array):**
Often represented as a 64-element array where integers represent piece types (e.g., +1 for White Pawn, -1 for Black Pawn).

## The Game State

The "Game State" is the complete snapshot of everything needed to continue the game from this exact moment. 

For Tic-Tac-Toe, the Game State is:
1. The 3x3 board array.
2. Whose turn it is (Player 1 or Player 2).

For Chess, the Game State is:
1. The 8x8 board array.
2. Whose turn it is.
3. Castling rights (Has the king moved?).
4. En passant targets.
5. Halfmove clock (for the 50-move draw rule).

## Legal Moves

The AI must be able to ask the game state: "What are all the legal moves from here?"
The game state should return a list of coordinates or actions.

```python
def get_legal_moves(state):
    # Returns [(0,0), (0,1), (0,2)...] for all empty spots
```

## Summary
Before we build Tic-Tac-Toe, remember: **The AI does not know what a pixel or a screen is. The AI only knows arrays, numbers, and rules.**
