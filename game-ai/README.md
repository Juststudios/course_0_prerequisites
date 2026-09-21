# Game AI & Board-Game Algorithms

## Key Terminology
* **State:** The current condition of the game board.
* **Minimax:** An algorithm for finding the optimal move in a zero-sum game.
* **Heuristic:** A rule-of-thumb evaluation function.



Welcome to the **Game Programming and Artificial Intelligence** module!

## Where Are We in the Curriculum?

You have already completed foundational programming and advanced machine learning stages:

```text
Programming (Python)
        ↓
Data Tools (NumPy, Pandas, Matplotlib)
        ↓
Engineering Mathematics
        ↓
Machine Learning (Scikit-learn)
        ↓
Deep Learning & NEAT
        ↓
**Game AI & Board-Game Algorithms**
```

This course shifts our focus from pattern recognition and statistical modeling toward **logical reasoning, state spaces, and search algorithms**.

## Why Game AI?

A board game is a perfect sandbox for computer science. It forces us to ask:
1. **Representation:** How does a computer represent the rules of a complex world?
2. **Search:** How can a computer explore millions of possible futures to find the best move?
3. **Evaluation (Heuristics):** If a game is too large to fully simulate, how can the computer estimate who is winning?

You will learn that Game AI contains multiple distinct approaches:

```text
Classical Search
    ├── Minimax
    ├── Alpha-Beta Pruning
    └── Monte Carlo Tree Search (MCTS)

Machine Learning
    ├── Supervised Learning
    ├── Reinforcement Learning
    └── Neural Networks

Hybrid AI
    ├── Search + Neural Evaluation (e.g., AlphaZero)
```

## Course Structure

### Part 1: Pygame and Architecture
* **`01_pygame/`**: The basics of rendering, game loops, and input handling.
* **`02_game_state/`**: The crucial separation between game logic (rules/state) and rendering.

### Part 2: Search Algorithms
* **`03_tic_tac_toe/`**: Building your first game and introducing Random & Rule-based AI.
* **`04_minimax/`**: Teaching the computer to look ahead and assume optimal opponent play.
* **`05_alpha_beta/`**: Optimizing search by mathematically ignoring irrelevant branches.

### Part 3: Intermediate Games & Heuristics
* **`06_heuristics/`**: How to evaluate partial game states without searching to the end.
* **`07_connect_four/`**: Applying Minimax and Heuristics to a deeper game.
* **`08_checkers/`**: Complex movement, forced captures, and advanced evaluation.

### Part 4: Advanced AI
* **`09_chess/`**: Architecting search for a massive state space (using a library for move generation).
* **`10_mcts/`**: Monte Carlo Tree Search (Simulation-based search).
* **`11_reinforcement_learning/`**: How agents learn from rewards instead of search.
* **`12_neural_game_ai/`**: Combining Deep Learning with Classical Search.

### Practice & Assessment
* **`exercises/`**: Practice problems for debugging, coding, and theory.
* **`projects/`**: Progressive milestones.
* **`capstone/`**: Your final independent Game AI project.
* **`reference/`**: Algorithm cheat sheets.

## Architecture Rule: Separation of Concerns

Throughout this course, you must strictly separate:
1. **Game State / Logic:** The math, rules, and board representation.
2. **AI:** The search and evaluation algorithms.
3. **Rendering / UI:** The Pygame code that draws shapes on the screen.

An AI must be able to run millions of simulated games in memory *without ever drawing a single pixel*.

## Getting Started

Install the requirements:
```bash
pip install pygame numpy matplotlib python-chess
```

Head to **`01_pygame/README.md`** to begin!
