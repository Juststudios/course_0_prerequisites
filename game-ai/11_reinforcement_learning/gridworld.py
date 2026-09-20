"""
GridWorld MDP Environment
=========================
A discrete 4x5 grid environment modeled as a Markov Decision Process (MDP):
  - State Space: S = {(r, c) | 0 <= r < 4, 0 <= c < 5, (r, c) not in walls}
  - Action Space: A = {0: UP, 1: DOWN, 2: LEFT, 3: RIGHT}
  - Start State: (0, 0)
  - Goal State: (3, 4) with terminal reward +10.0
  - Trap States: (1, 3), (2, 1) with terminal penalty -10.0
  - Obstacle Walls: (1, 1), (2, 3) impassable
  - Step Reward: -1.0 per transition to incentivize shortest path navigation
"""

import numpy as np

# Actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3

ACTION_NAMES = {
    ACTION_UP: "UP",
    ACTION_DOWN: "DOWN",
    ACTION_LEFT: "LEFT",
    ACTION_RIGHT: "RIGHT"
}

ACTION_DELTAS = {
    ACTION_UP: (-1, 0),
    ACTION_DOWN: (1, 0),
    ACTION_LEFT: (0, -1),
    ACTION_RIGHT: (0, 1)
}

ACTION_ARROWS = {
    ACTION_UP: "↑",
    ACTION_DOWN: "↓",
    ACTION_LEFT: "←",
    ACTION_RIGHT: "→"
}


class GridWorld:
    """
    4x5 GridWorld Environment with obstacles and terminal traps.
    """

    def __init__(self, rows=4, cols=5):
        self.rows = rows
        self.cols = cols
        self.start_state = (0, 0)
        self.goal_state = (3, 4)
        self.trap_states = {(1, 3), (2, 1)}
        self.wall_states = {(1, 1), (2, 3)}
        self.agent_pos = self.start_state
        self.action_space = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

    def reset(self):
        """Reset environment to start state and return initial position."""
        self.agent_pos = self.start_state
        return self.agent_pos

    def is_valid_state(self, r, c):
        """Return True if (r, c) is inside bounds and not a wall."""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if (r, c) in self.wall_states:
            return False
        return True

    def get_all_states(self):
        """Return list of all accessible states in the grid (excluding walls)."""
        states = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.wall_states:
                    states.append((r, c))
        return states

    def step(self, action):
        """
        Execute an action in the environment.
        
        Parameters
        ----------
        action : int in {0, 1, 2, 3}
        
        Returns
        -------
        next_state : tuple of (r, c)
        reward : float
        done : bool
        info : dict
        """
        if action not in self.action_space:
            raise ValueError(f"Invalid action {action}. Valid actions: {self.action_space}")

        dr, dc = ACTION_DELTAS[action]
        candidate_r = self.agent_pos[0] + dr
        candidate_c = self.agent_pos[1] + dc

        # Check bounds and walls
        if self.is_valid_state(candidate_r, candidate_c):
            self.agent_pos = (candidate_r, candidate_c)

        # Check outcomes at landing state
        if self.agent_pos == self.goal_state:
            reward = 10.0
            done = True
            info = {"event": "GOAL"}
        elif self.agent_pos in self.trap_states:
            reward = -10.0
            done = True
            info = {"event": "TRAP"}
        else:
            reward = -1.0
            done = False
            info = {"event": "STEP"}

        return self.agent_pos, reward, done, info

    def render(self):
        """Return formatted ASCII grid representation."""
        lines = ["  0 1 2 3 4"]
        for r in range(self.rows):
            row_str = f"{r} "
            for c in range(self.cols):
                pos = (r, c)
                if pos == self.agent_pos:
                    row_str += "A "
                elif pos == self.goal_state:
                    row_str += "G "
                elif pos in self.trap_states:
                    row_str += "T "
                elif pos in self.wall_states:
                    row_str += "# "
                else:
                    row_str += ". "
            lines.append(row_str)
        return "\n".join(lines)
