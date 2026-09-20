# Module 5: Alpha-Beta Pruning

## What You Will Learn
You will learn why standard Minimax fails on larger games, and how a mathematical optimization called "Alpha-Beta Pruning" speeds it up without changing the result.

## The Problem: The Branching Factor
In Tic-Tac-Toe, the first move has 9 options, the second has 8, etc. The total number of possible games is roughly 9! (9 factorial) = 362,880. A modern computer can search this in less than a second.

But what about **Chess**?
The average number of legal moves from any position (the **Branching Factor**) is 35. 
* Depth 1: 35 positions
* Depth 2: 1,225 positions
* Depth 3: 42,875 positions
* Depth 4: 1,500,000+ positions
* Depth 6: ~1.8 Billion positions.

Minimax grows **exponentially**. We cannot exhaustively search games like Connect Four, Checkers, or Chess.

## Idea: Pruning Unnecessary Branches
Look at this small game tree:
```text
              MAX
            /     \
          MIN     MIN
         /  \     /  \
        3    5   1    9
```

Let's evaluate it from left to right, exactly as the computer does.
1. MAX goes to the left MIN branch.
2. Left MIN evaluates 3 and 5. It wants the minimum, so it chooses **3**.
3. Now MAX knows that if it goes Left, it gets a guaranteed **3**.
4. MAX goes to the right MIN branch.
5. Right MIN evaluates the first option: **1**.

**STOP.**

Think about this logically. 
Right MIN is going to choose the minimum value. It has already found a 1. Therefore, the absolute *highest* value Right MIN will return is 1. (If the next number is 0, it returns 0. If the next number is 9, it still returns 1).

MAX knows:
* Go Left = get 3.
* Go Right = get 1 (or less).

MAX wants the maximum. Does MAX need to look at the '9'? **NO.**
MAX already knows it is *never* going to choose the Right branch, because the Left branch (3) is already better than the best-case scenario of the Right branch (1).

We can completely skip evaluating the '9'. We "prune" that branch.

## Alpha and Beta
* **Alpha**: The best (highest) score that MAX can guarantee so far. (In the example, Alpha becomes 3).
* **Beta**: The best (lowest) score that MIN can guarantee so far.

As we traverse the tree down, we pass Alpha and Beta along. If at any point a branch is worse than Alpha/Beta, we `break` out of the loop and skip the rest of the branch.

## Impact
Alpha-Beta Pruning **does not change the final move the AI chooses**. It is mathematically identical to standard Minimax. However, in the best case, it can evaluate twice as deep in the same amount of time.
