"""Pure-Python dynamical simulation of the inverted pendulum (Cart-Pole) system.

Implements non-linear Lagrangian equations of motion integrated via the
symplectic Euler-Cromer numerical method, with zero external dependencies (no Gym/PyBullet).
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union


class CartPoleEnv:
    """Dynamical simulation environment for cart-pole inverted pendulum balance."""

    def __init__(self, max_steps: int = 500):
        # Physical constants
        self.gravity: float = 9.8  # m/s^2
        self.masscart: float = 1.0  # kg
        self.masspole: float = 0.1  # kg
        self.total_mass: float = self.masscart + self.masspole
        self.length: float = 0.5  # Half-length of pole (m)
        self.polemass_length: float = self.masspole * self.length
        self.force_mag: float = 10.0  # N
        self.tau: float = 0.02  # Integration step size (seconds)

        # Operational failure boundaries
        self.theta_threshold_radians: float = 12.0 * 2.0 * math.pi / 360.0  # ~0.2094 rad (12 deg)
        self.x_threshold: float = 2.4  # Track limit (m)
        self.max_steps: int = max_steps

        self.state: List[float] = [0.0, 0.0, 0.0, 0.0]
        self.steps: int = 0

    def reset(self, initial_state: Optional[List[float]] = None) -> List[float]:
        """Reset the environment to a starting state [x, x_dot, theta, theta_dot]."""
        if initial_state is not None:
            self.state = [float(v) for v in initial_state]
        else:
            # Small random initial perturbation
            self.state = [
                random.uniform(-0.05, 0.05),
                random.uniform(-0.05, 0.05),
                random.uniform(-0.05, 0.05),
                random.uniform(-0.05, 0.05),
            ]
        self.steps = 0
        return list(self.state)

    def normalize_state(self, state: Optional[List[float]] = None) -> List[float]:
        """Normalize state components to approximately [-1.0, 1.0] for neural network inputs."""
        s = self.state if state is None else state
        return [
            s[0] / self.x_threshold,
            s[1] / 3.0,
            s[2] / self.theta_threshold_radians,
            s[3] / 3.0,
        ]

    def step(self, action: Union[int, float]) -> Tuple[List[float], float, bool, Dict[str, Any]]:
        """Simulate one discrete time-step of cart-pole dynamics using Euler-Cromer integration."""
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action > 0.5 else -self.force_mag

        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # Non-linear equations of motion derived from Euler-Lagrange equations
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        theta_acc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta * costheta / self.total_mass)
        )
        x_acc = temp - self.polemass_length * theta_acc * costheta / self.total_mass

        # Symplectic Euler-Cromer numerical integration
        x_dot = x_dot + self.tau * x_acc
        x = x + self.tau * x_dot
        theta_dot = theta_dot + self.tau * theta_acc
        theta = theta + self.tau * theta_dot

        self.state = [x, x_dot, theta, theta_dot]
        self.steps += 1

        failed = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )
        done = failed or (self.steps >= self.max_steps)
        reward = 1.0 if not failed else 0.0

        info = {'steps': self.steps, 'failed': failed}
        return list(self.state), reward, done, info
