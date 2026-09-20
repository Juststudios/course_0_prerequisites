# Game AI Final Assessment

## Part 1: Concepts

1. **Architecture:** Why must the Game Logic be completely separate from the Pygame rendering code if you want to build an AI?
2. **Game Tree:** What does a "Node" represent in a Game Tree? What does an "Edge" (a line between nodes) represent?
3. **Minimax:** Why does the Minimax algorithm alternate between trying to maximize the score and minimize the score?
4. **Alpha-Beta Pruning:** Does Alpha-Beta pruning ever cause the AI to choose a *different* move than standard Minimax would have chosen? Explain why or why not.
5. **Heuristics:** What is the purpose of a Heuristic Evaluation function? When is it used?

## Part 2: Math and Logic

**Scenario:** You are running Minimax (without pruning) on a tiny game tree. 
You are MAX.
From the root node, you have two legal moves (Left and Right).
* If you go Left, the opponent (MIN) has two moves. Move A results in a terminal score of +5. Move B results in +10.
* If you go Right, the opponent (MIN) has two moves. Move C results in a terminal score of +2. Move D results in -100.

1. What score will MIN force if you go Left?
2. What score will MIN force if you go Right?
3. Which move (Left or Right) will MAX choose at the root?

## Part 3: Architecture Identification

Match the AI approach to the problem:
**Approaches:** `[Random AI, Minimax, Depth-Limited Alpha-Beta, MCTS, Supervised Learning, Reinforcement Learning]`

1. You are building an AI for a game with a branching factor of 300, making Alpha-Beta impossible, and the game is too complex for human heuristics. What classical search algorithm do you use?
2. You want to build a Tic-Tac-Toe AI that never loses, and you want it to run as fast as possible.
3. You have a database of 5 million human chess games and want to train a Neural Network to predict the human's next move.
4. You are building an AI for Connect Four. The game is too big to search to the end, but you know exactly what a "good" board position looks like.

## Part 4: Code Reading

Explain what this bug does to an Alpha-Beta search tree:

```python
        for move in legal_moves:
            child = state.make_move(move)
            score = minimax(child, depth-1, alpha, beta, False)
            best_score = max(best_score, score)
            
            # THE BUG:
            alpha = min(alpha, best_score) 
            
            if beta <= alpha:
                break
```
*(Hint: Think about what alpha represents and whether it should be shrinking or growing for the maximizing player).*
