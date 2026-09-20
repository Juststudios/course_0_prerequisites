# Module 12: Neural Game AI (Hybrid AI)

## What You Will Learn
You will learn how modern Game AI (like DeepMind's AlphaGo and AlphaZero) combines classical search algorithms with Deep Learning to create superhuman play.

## The Limits of Pure Search
* Minimax + Alpha-Beta is limited by the quality of the hand-written heuristic.
* MCTS is limited by the fact that pure random playouts are a very "noisy" way to evaluate a board.

## The Limits of Pure Machine Learning
* A pure Neural Network (like a CNN) trained via Reinforcement Learning can look at a board and instantly predict the best move. 
* However, Neural Networks can "hallucinate" or suffer from "blind spots". A neural network might make a move that looks strategically beautiful, but misses a simple 2-move tactical checkmate because it didn't explicitly calculate the future.

## The Hybrid Solution: AlphaZero Architecture

Modern engines combine both approaches:

1. **The Neural Network replaces the Heuristic:** Instead of a human writing `score = pawns*100 + knights*300`, a massive neural network takes the board array as input and outputs a single float: the probability of winning (Value). It also outputs probabilities for every legal move (Policy).
2. **MCTS replaces Random Playouts:** Instead of doing random playouts to evaluate a leaf node, MCTS simply passes the leaf node to the Neural Network. The Network instantly says "White has a 75% chance of winning from here." 

### How it plays:
1. MCTS begins searching the tree.
2. It uses the Neural Network's *Policy* to decide which branches to explore first (Move Ordering).
3. When it reaches a leaf node, it uses the Neural Network's *Value* to evaluate the board, rather than playing to the end.
4. MCTS backpropagates that value up the tree.

**Result:** The Neural Network gives the AI deep, grandmaster-level positional intuition. The MCTS search algorithm ensures the AI calculates exact tactics and doesn't blunder.

This hybrid approach defeated the world champions in Go, Chess, and Shogi, and is the current state-of-the-art in Game AI!
