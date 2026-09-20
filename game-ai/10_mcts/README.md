# Module 10: Monte Carlo Tree Search (MCTS)

## What You Will Learn
- Why classical Minimax and Alpha-Beta search fail when game trees have high branching factors (e.g. Go with $b \approx 250$, Connect Four with $b \approx 7$).
- How Monte Carlo simulation replaces hand-engineered heuristic evaluation functions with random playouts.
- The mathematical foundation of **UCB1** (Upper Confidence Bound 1 applied to trees) for balancing the exploration-exploitation dilemma.
- The 4-phase algorithm lifecycle: Selection, Expansion, Simulation (Rollout), and Backpropagation.
- How to apply domain-independent MCTS across multiple games (`TicTacToeState` and `ConnectFourState`).

---

## 1. The Problem with Minimax for High-Branching Games

In Minimax with Alpha-Beta pruning, the search tree expands exhaustively down to depth $d$.
The number of evaluated states scales as $O(b^d)$, where $b$ is the branching factor:

| Game | Branching Factor ($b$) | State Space | Minimax Feasibility |
|---|---|---|---|
| **Tic-Tac-Toe** | $\approx 4$ | $5 \times 10^3$ | Exhaustive search to completion ($< 1$ ms) |
| **Connect Four** | $\approx 7$ | $4.5 \times 10^{12}$ | Depth-limited (depth 6–8) with heuristic |
| **Chess** | $\approx 35$ | $10^{43}$ | Depth-limited (depth 6–10) with complex evaluation |
| **Go** | $\approx 250$ | $10^{170}$ | **Fails completely** ($250^4 \approx 3.9 \times 10^9$ states) |

Furthermore, designing a hand-crafted evaluation heuristic for games like Go is notoriously difficult. MCTS solves both problems:
1. It is **asymmetric**: focusing computing power almost entirely on promising branches.
2. It requires **no heuristic evaluation**: game positions are evaluated purely through self-play rollouts to game termination.

---

## 2. Mathematical Foundation: UCB1 Derivation

MCTS frames move selection at each tree node as a **Multi-Armed Bandit Problem**:
- Each available legal move $i$ is an arm with unknown win rate $\mu_i$.
- We wish to maximize our reward (exploitation) while gathering information about less-visited moves (exploration).

Using the Chernoff-Hoeffding inequality, Auer, Cesa-Bianchi, and Fischer (2002) proved that the regret is asymptotically bounded if we pick the arm maximizing:

$$\text{UCB1}_i = \bar{X}_i + c \sqrt{\frac{2 \ln N_{\text{parent}}}{N_i}}$$

Where:
- $\bar{X}_i = \frac{Q_i}{N_i}$: Empirical win rate of action $i$ (Exploitation term).
- $N_i$: Number of times action $i$ has been visited.
- $N_{\text{parent}}$: Total visits to the parent node ($\sum_j N_j$).
- $c = \sqrt{2} \approx 1.414$: Theoretical exploration constant balancing exploitation and exploration.

### Behavior of UCB1
- **Frequently visited moves ($N_i$ large):** The exploration term $c \sqrt{\dots}$ approaches 0; UCB1 is dominated by the empirical win rate $\frac{Q_i}{N_i}$.
- **Infrequently visited moves ($N_i$ small):** The exploration term blows up, forcing the search to revisit and verify uncertain branches.

---

## 3. The 4 Phases of MCTS

```text
       [Selection]                [Expansion]               [Simulation]             [Backpropagation]
            ( )                        ( )                       ( )                        (N+1)
           /   \                      /   \                     /   \                      /    \
         ( )   ( )                  ( )   ( )                 ( )   ( )                  ( )    (N+1)
               / \                        / \                       / \                         / \
             ( ) (★)                    ( ) ( )                   ( ) ( )                     ( ) (N+1)
                                             |                         |                           |
                                            [★]                       ( ) Rollout                 [Q+r, N+1]
                                                                       |  Terminal
                                                                      (★) Win/Loss
```

1. **Selection:**
   Starting at the root node, iteratively choose the child with the highest UCB1 score until reaching an unexpanded node or terminal state.

2. **Expansion:**
   If the selected node is non-terminal, select an untried legal move and add a new child node to the tree.

3. **Simulation (Rollout):**
   From the new child node, simulate moves according to a fast default rollout policy (e.g., uniform random selection) until the game reaches a terminal state ($s \in S_{\text{terminal}}$).

4. **Backpropagation:**
   Propagate the terminal outcome back up through all parent nodes along the selected trajectory to the root:
   - $N \leftarrow N + 1$
   - $Q \leftarrow Q + 1.0$ (if player won), $Q \leftarrow Q + 0.5$ (on draw), $Q \leftarrow Q + 0.0$ (on loss).

### Final Move Selection (Robust Child Rule)
When time or the simulation budget expires, the agent selects the move corresponding to the child with the **highest visit count ($N$)**, NOT the highest average reward ($\frac{Q}{N}$). In game theory, visit count is far more robust against stochastic noise from random rollouts.

---

## 4. Benchmark Execution & Validation

Run the automated test suite across Tic-Tac-Toe and Connect Four:

```bash
python3 game-ai/10_mcts/play_mcts.py
```

### Verified Performance Benchmarks:
1. **Tic-Tac-Toe vs Random Agent:**
   - Evaluated over 20 games (alternating first/second turn).
   - Expected Win + Draw rate: $\ge 95\%$.
2. **Tic-Tac-Toe vs Perfect Minimax Agent:**
   - Evaluated over 10 games against exhaustive Minimax.
   - Expected outcome: 100% Draws (demonstrating theoretical convergence to optimal game play).
3. **Connect Four vs Random Agent:**
   - Evaluated over 5 games on the 6x7 board grid ($4.5 \times 10^{12}$ states).
   - Expected Win rate: $\ge 80\%$.
