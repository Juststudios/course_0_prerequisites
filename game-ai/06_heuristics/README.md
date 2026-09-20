# Module 6: Heuristic Evaluation

## What You Will Learn
You will learn what to do when a game is too large for Alpha-Beta pruning to reach the end of the game tree.

## The Problem with Terminal Search
Even with Alpha-Beta Pruning, games like Chess or Checkers are too big. If you ask a computer to look ahead until someone wins or loses, it will run for billions of years before making its first move.

We must **limit the search depth**. We might say: "Only look 4 moves ahead."

But Minimax requires a "Score" at the bottom of the tree.
* If a state is Terminal (Game Over), the score is easy: +10 (Win), -10 (Lose), 0 (Draw).
* If we stop searching at Depth 4, the game is *not over*. The state is just a regular board position in the middle of a game.

How do we give a "Score" to a game that isn't over?

## Idea: The Evaluation Function (Heuristics)
We create a function that takes a Game State, examines its features, and estimates how good it is. This is called a **Heuristic**.

```python
def heuristic_evaluation(state):
    score = 0
    # ... look at the board and add/subtract points
    return score
```

### Examples of Heuristics

**Tic-Tac-Toe** (If we stopped early)
* +1 point for every piece in a corner.
* +3 points for controlling the center.
* +5 points if you have 2-in-a-row with an empty third slot (a threat).

**Checkers**
* +10 points for every regular piece.
* +20 points for every King piece.
* +1 point for pieces on the edge (they can't be captured easily).

**Chess**
* Material: +1 for Pawns, +3 for Knights/Bishops, +5 for Rooks, +9 for Queens.
* Mobility: +0.1 points for every legal move available (more options = better position).
* King Safety: -1 point if the King is exposed.

## Integration into Minimax
The change to our algorithm is very small!

```python
def minimax(state, depth, is_maximizing, maximizing_player):
    # 1. Base Cases
    if state.is_terminal:
        return exact_score(state)
        
    if depth == MAX_DEPTH:  # <--- NEW
        return heuristic_evaluation(state) # <--- NEW
```

## The Catch
Heuristics are just guesses. If your heuristic thinks having all your pieces on the edge of the board in Checkers is a guaranteed win, your AI will play terribly. Designing good heuristics is what made IBM's Deep Blue able to defeat Garry Kasparov at Chess in 1997.

In modern times (post-2017), we often use Neural Networks to *learn* the heuristic evaluation function (e.g., AlphaZero), instead of handwriting it. We will cover that in Module 12!
