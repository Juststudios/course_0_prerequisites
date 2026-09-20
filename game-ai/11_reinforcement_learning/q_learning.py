"""
Tabular Q-Learning Agent
========================
Implements the model-free, off-policy Temporal Difference control algorithm:
  - Q-Table: Maps (state, action) pairs to expected discounted returns
  - Epsilon-Greedy Exploration: Balances exploration with exploitation
  - Bellman Optimality Update:
      Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_a' Q(s', a') - Q(s, a) ]
  - Greedy Policy Extraction:
      pi*(s) = argmax_a Q(s, a)
"""

import random
from collections import defaultdict
import numpy as np


class QLearningAgent:
    """
    Tabular Q-Learning Agent.
    
    Parameters
    ----------
    actions : list of int
        Available discrete action identifiers.
    alpha : float, default=0.1
        Learning rate.
    gamma : float, default=0.95
        Discount factor for future rewards.
    epsilon : float, default=1.0
        Initial exploration probability.
    epsilon_decay : float, default=0.995
        Multiplicative decay factor per episode.
    epsilon_min : float, default=0.01
        Minimum exploration threshold floor.
    random_state : int, default=42
    """

    def __init__(
        self,
        actions,
        alpha=0.1,
        gamma=0.95,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.01,
        random_state=42
    ):
        self.actions = list(actions)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.rng = random.Random(random_state)
        # Default Q value is 0.0 for any unvisited (state, action) pair
        self.q_table = defaultdict(float)

    def get_q(self, state, action):
        """Retrieve Q(s, a) value."""
        return self.q_table[(state, action)]

    def choose_action(self, state):
        """
        Select an action using the epsilon-greedy policy.
        
        Parameters
        ----------
        state : tuple
        
        Returns
        -------
        action : int
        """
        # Exploration: pick uniform random action
        if self.rng.random() < self.epsilon:
            return self.rng.choice(self.actions)

        # Exploitation: pick action with maximum Q-value
        # Break ties randomly to encourage symmetric exploration
        q_vals = [self.get_q(state, a) for a in self.actions]
        max_q = max(q_vals)
        best_actions = [a for a, q in zip(self.actions, q_vals) if abs(q - max_q) < 1e-9]
        return self.rng.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        """
        Perform Bellman equation temporal-difference update.
        
        Q(s, a) <- Q(s, a) + alpha * (TD_target - Q(s, a))
        where TD_target = reward if done else reward + gamma * max_a' Q(s', a')
        """
        current_q = self.get_q(state, action)

        if done:
            target = reward
        else:
            max_future_q = max(self.get_q(next_state, a) for a in self.actions)
            target = reward + self.gamma * max_future_q

        # Temporal difference error
        td_error = target - current_q
        self.q_table[(state, action)] = current_q + self.alpha * td_error

    def decay_epsilon(self):
        """Decay exploration rate after an episode completes."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def get_policy(self, states):
        """
        Extract the greedy deterministic policy for a list of states.
        
        Returns
        -------
        dict mapping state -> optimal_action
        """
        policy = {}
        for s in states:
            q_vals = [self.get_q(s, a) for a in self.actions]
            max_q = max(q_vals)
            best_actions = [a for a, q in zip(self.actions, q_vals) if abs(q - max_q) < 1e-9]
            policy[s] = best_actions[0]
        return policy

    def get_value_function(self, states):
        """
        Extract the state-value function V(s) = max_a Q(s, a).
        
        Returns
        -------
        dict mapping state -> max_q_value
        """
        values = {}
        for s in states:
            values[s] = max(self.get_q(s, a) for a in self.actions)
        return values
