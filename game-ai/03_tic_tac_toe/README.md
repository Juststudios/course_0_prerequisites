# Module 3: Tic-Tac-Toe and Baselines

## What You Will Learn
In this module, you will see how separating the Game Logic from the UI allows us to easily build different types of AI. You will learn about "Baseline" AIs and why we need them.

## The Architecture in Action
Look at `tic_tac_toe.py`. This is the **Engine**. It has no Pygame imports. It only deals with arrays and rules.
Look at `ui.py`. This is the **Renderer**. It only knows how to draw circles and lines.

In `play_human.py`, the main loop just acts as a messenger between the Human (mouse clicks), the Engine (logic), and the UI (rendering).

## Building a Baseline (Random AI)
In `play_random_ai.py`, we introduce our first AI opponent.
It is extremely simple:
```python
def random_ai_move(state):
    moves = state.get_legal_moves()
    return random.choice(moves)
```

**Why do this?**
In Game AI research, a "Random Agent" is the universal baseline. If you write a complex Neural Network or Deep Search algorithm, and it cannot beat a Random Agent, you know your advanced algorithm has a bug.

## Next Steps
A Random AI is easily beaten. A "Rule-Based" AI might check if there's an immediate winning move, but writing out every single rule by hand is exhausting.

To create an unbeatable Tic-Tac-Toe AI, we need an algorithm that can look into the future: **Minimax**. Head to the next module.
