# Game AI Cheat Sheet

## Terminology

* **State Space:** All mathematically possible configurations of the game board.
* **Branching Factor:** The average number of legal moves available on a turn. (Tic-Tac-Toe ~4, Chess ~35, Go ~250).
* **Game Tree:** A directed graph where nodes are Game States and edges are Moves.
* **Terminal State:** A state where the game is mathematically over (Win, Lose, Draw).
* **Heuristic:** A function that estimates the value of a non-terminal state.

## Algorithm Matrix

| Algorithm | Type | Description | When to Use |
|---|---|---|---|
| **Minimax** | Search | Explores all futures assuming optimal opponent play. | Tiny games (Tic-Tac-Toe) |
| **Alpha-Beta Pruning** | Search Opt. | Minimax, but mathematically ignores branches that cannot improve the result. | Medium games (Connect Four) |
| **Depth-Limited Search** | Search | Stops searching after N moves and uses a Heuristic to guess the score. | Large games (Chess, Checkers) |
| **Monte Carlo Tree Search** | Search | Plays thousands of random games to the end to find statistically good moves. | Massive branching factors (Go) |
| **Supervised Learning** | Machine Learning | Trains a neural network to mimic human Grandmaster moves from a dataset. | When massive human datasets exist |
| **Reinforcement Learning** | Machine Learning | Agent plays itself millions of times, adjusting its neural net based on win/loss rewards. | When creating novel strategies (AlphaZero) |

## The Standard Minimax + Alpha-Beta Pattern (Python)

```python
def minimax(state, depth, alpha, beta, is_maximizing):
    # 1. Terminal condition
    if state.is_terminal: return get_exact_score(state)
    
    # 2. Depth limit condition (if game too big)
    if depth == 0: return heuristic_guess(state)
    
    # 3. Recursive Search
    if is_maximizing:
        best_val = -infinity
        for move in state.get_legal_moves():
            child = state.make_move(move)
            val = minimax(child, depth-1, alpha, beta, False)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha: break # Prune
        return best_val
    else:
        # Same logic, but minimize and update beta
        ...
```

## Architecture Rule of Thumb
**Never import `pygame` into your game logic or AI files.**
Your Game State class should only import standard math/list modules (or numpy). Your AI should only import your Game State. Only your `main.py` should import Pygame, the Engine, and the AI to wire them together.
