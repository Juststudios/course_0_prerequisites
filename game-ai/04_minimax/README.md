# Module 4: Minimax and Game Trees

## What You Will Learn
You will learn how computers "think ahead" using Game Trees and the Minimax algorithm. You will build an unbeatable Tic-Tac-Toe AI.

## The Problem
A random AI is terrible. A rule-based AI (like `if center is empty: take center`) is slightly better, but requires the programmer to hand-write hundreds of rules. What if we want the computer to simply *figure out* the best move on its own?

## Idea: The Game Tree
Since Tic-Tac-Toe is a small game, we can simulate every possible future.
From the empty board, there are 9 possible moves. For each of those 9 moves, there are 8 possible responses. Then 7, then 6...
This branching structure is called a **Game Tree**.

* **Node**: A specific board state.
* **Child Node**: A board state resulting from making one legal move.
* **Terminal Node**: A board state where the game is over (win, lose, or draw).

## Minimax Intuition
Imagine you are exploring this tree. You want to win, so you will pick the branch that leads to a win. 
But your opponent *also* gets to choose! 
If you pick a branch that has a win in 3 moves, but gives the opponent a chance to win in 1 move... they will take it, and you will lose.

Therefore, we assume **both players play perfectly**.

### The Mathematics of Minimax
We assign a "Utility" score to the end of the game:
* AI Wins: +10
* Human Wins: -10
* Draw: 0

The AI is the **Maximizer** (MAX). It wants the highest score.
The Human is the **Minimizer** (MIN). It wants the lowest score.

Let's look at a tiny tree, starting from the bottom up:
```text
              MAX (AI's Turn)
            /     \
          MIN     MIN  (Human's Turn)
         /  \     /  \
       +10   0  -10  +10
```
On the left side, it's MIN's turn. The choices are +10 (AI wins) or 0 (Draw). MIN wants the lowest score, so MIN chooses 0.
On the right side, the choices are -10 (Human wins) or +10. MIN chooses -10.

Now step back up to MAX. MAX is looking at the two branches. 
If MAX goes Left, MIN will force a score of 0.
If MAX goes Right, MIN will force a score of -10.
MAX wants the highest score, so MAX chooses Left.

`MAX chooses max(min(10, 0), min(-10, 10)) = max(0, -10) = 0.`

## Implementation
See `minimax.py` for the recursive implementation, and `play_minimax_ai.py` to play against it.
You will find that the AI is mathematically impossible to beat. The best you can do is force a draw.
