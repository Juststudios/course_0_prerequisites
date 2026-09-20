# Module 11: Reinforcement Learning (RL)

## What You Will Learn
- How Reinforcement Learning differs fundamentally from Classical Search (Minimax/Alpha-Beta) and Supervised Learning.
- The mathematical formulation of **Markov Decision Processes (MDPs)**: $(S, A, P, R, \gamma)$.
- The **Bellman Optimality Equations** for state-value functions $V(s)$ and action-value functions $Q(s, a)$.
- The **Tabular Q-Learning** algorithm: temporal-difference error updates and $\epsilon$-greedy exploration schedules.
- How to implement a discrete GridWorld environment with obstacles, traps, and goal rewards from scratch.
- How tabular RL scales to Deep Q-Networks (DQN) and hybrid systems like AlphaZero.

---

## 1. Classical Search vs Supervised Learning vs Reinforcement Learning

| Paradigm | How Decisions are Made | Strengths | Limitations |
|---|---|---|---|
| **Classical Search** (Minimax / $\alpha$-$\beta$) | Freezes game, looks ahead in tree, evaluates leaves with hand-written heuristic. | Exact play for small games; no training required. | Computationally prohibitive for large state spaces ($b^d$ explosion); requires manual heuristics. |
| **Supervised Learning** | Learns mapping $\text{State} \to \text{Action}$ by imitating expert human datasets. | Fast inference ($O(1)$ forward pass); leverages large data. | Cannot discover strategies superior to the demonstration dataset; suffers from distribution shift. |
| **Reinforcement Learning** | Agent interacts with environment via trial-and-error, guided purely by reward signals. | Discovers novel, superhuman policies without human demonstrations. | Sample inefficient; requires extensive exploration. |

---

## 2. Mathematical Foundations: Markov Decision Processes (MDPs)

An environment is formalized as a 5-tuple $(S, A, P, R, \gamma)$:

1. **State Space ($S$):** The set of all possible environment configurations (e.g., coordinates $(r, c)$).
2. **Action Space ($A$):** The discrete set of decisions available to the agent (e.g., $\{\text{UP}, \text{DOWN}, \text{LEFT}, \text{RIGHT}\}$).
3. **Transition Probability Function ($P$):**
   $$P(s' \mid s, a) = \mathbb{P}(S_{t+1} = s' \mid S_t = s, A_t = a)$$
4. **Reward Function ($R$):**
   $$R(s, a) = \mathbb{E}[R_{t+1} \mid S_t = s, A_t = a]$$
5. **Discount Factor ($\gamma \in [0, 1)$):** Balances immediate rewards against delayed long-term payoff:
   $$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

---

## 3. The Bellman Optimality Equation & Q-Learning

### The Action-Value Function $Q(s, a)$
The expected return of taking action $a$ in state $s$ and thereafter following optimal policy $\pi^*$:

$$Q^*(s, a) = R(s, a) + \gamma \sum_{s' \in S} P(s' \mid s, a) \max_{a'} Q^*(s', a')$$

### Model-Free Q-Learning Update Rule
Because the transition dynamics $P(s' \mid s, a)$ are unknown to the agent (model-free), Q-Learning updates its tabular estimates using sampled experience transitions $(s, a, r, s')$:

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ \underbrace{r + \gamma \max_{a'} Q(s', a')}_{\text{TD Target}} - Q(s, a) \right]$$

Where:
- $\alpha \in (0, 1]$: Learning rate.
- $\delta_t = \left( r + \gamma \max_{a'} Q(s', a') \right) - Q(s, a)$: Temporal Difference (TD) error.
- $\pi^*(s) = \arg\max_a Q(s, a)$: Deterministic greedy policy extracted from the converged Q-table.

### Exploration vs Exploitation: $\epsilon$-Greedy Schedule
At each decision step, the agent acts according to:

$$a_t = \begin{cases} \text{random action from } A & \text{with probability } \epsilon \\ \arg\max_a Q(s_t, a) & \text{with probability } 1 - \epsilon \end{cases}$$

$\epsilon$ decays multiplicatively over training: $\epsilon_{t+1} = \max(\epsilon_{\min}, \epsilon_t \cdot \lambda)$, transitioning from pure exploration to optimal exploitation.

---

## 4. Architecture of the Module

```text
game-ai/11_reinforcement_learning/
  ├── gridworld.py        # 4x5 MDP environment with start (0,0), goal (3,4), traps, and walls
  ├── q_learning.py       # Tabular QLearningAgent with Bellman update and policy extraction
  ├── train_rl.py         # 600-episode training loop, policy ASCII grid, and evaluation rollout
  ├── output/             # Visualization artifacts
  │     └── q_learning_training.png
  └── README.md           # Theoretical derivation and curriculum guide
```

---

## 5. Running the Training & Verification

Execute the complete training pipeline:

```bash
python3 game-ai/11_reinforcement_learning/train_rl.py
```

### Expected Output & Scorecard:
- **Reward Convergence:** Average episode reward transitions from negative ($\approx -24$) during initial random exploration to $+3.8$ upon discovering the shortest route.
- **Path Optimality:** Greedy evaluation rollout discovers the global optimal **7-step trajectory** to the goal:
  $$(0,0) \to (0,1) \to (0,2) \to (0,3) \to (0,4) \to (1,4) \to (2,4) \to (3,4)$$
  while safely avoiding traps at $(1,3)$ and $(2,1)$ and walls at $(1,1)$ and $(2,3)$.
- **Saved Figure:** Generates training diagnostic curves at `output/q_learning_training.png`.
