"""Multi-trial evaluation and trajectory logging for the NEAT Cart-Pole controller.

Simulates the champion controller across multiple perturbation angles, verifies
>= 500 step stabilization, logs physical telemetry, and generates trajectory plots.
"""

import os
import pickle
import sys
from typing import List, Optional, Tuple

# Ensure repository root is on sys.path
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from neat.neat_engine.network import FeedForwardNetwork

try:
    from cartpole_env import CartPoleEnv
    from train_cartpole import train_cartpole
except ImportError:
    import importlib
    _env_mod = importlib.import_module("neat.projects.02_cartpole.cartpole_env")
    CartPoleEnv = _env_mod.CartPoleEnv
    _train_mod = importlib.import_module("neat.projects.02_cartpole.train_cartpole")
    train_cartpole = _train_mod.train_cartpole


def evaluate_controller(output_dir: Optional[str] = None) -> None:
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    champion_path = os.path.join(output_dir, "champion_cartpole.pkl")

    if not os.path.exists(champion_path):
        print("No champion found. Running training first...")
        champion, _ = train_cartpole(output_dir=output_dir)
    else:
        with open(champion_path, "rb") as f:
            champion = pickle.load(f)

    net = FeedForwardNetwork.create(champion)
    env = CartPoleEnv(max_steps=500)

    test_angles = [-0.08, -0.05, -0.02, 0.0, 0.03, 0.06, 0.08]
    print("\n--- Multi-Trial Cart-Pole Controller Validation ---")

    all_survived = True
    logged_trajectory: List[Tuple[float, float, float, float, float, float]] = []

    for i, angle in enumerate(test_angles):
        s = env.reset([0.0, 0.0, angle, 0.0])
        steps = 0
        traj = []
        while steps < env.max_steps:
            norm_s = env.normalize_state(s)
            action = net.activate(norm_s)[0]
            force = env.force_mag if action > 0.5 else -env.force_mag
            traj.append((steps * env.tau, s[0], s[1], s[2], s[3], force))
            s, _, done, _ = env.step(action)
            steps += 1
            if done:
                break

        print(f"  Trial {i+1} (Init Angle = {angle:+.3f} rad): Survived {steps} / {env.max_steps} steps")
        assert steps >= 500, f"Controller failed early on initial angle {angle} (survived {steps} steps)"

        # Save trajectory from the largest perturbation for plotting
        if abs(angle - 0.06) < 1e-4 or not logged_trajectory:
            logged_trajectory = traj

    print("\n[SUCCESS] Controller successfully balanced >= 500 steps across all test trials!")

    # Plot telemetry trajectory
    times = [t[0] for t in logged_trajectory]
    pos_x = [t[1] for t in logged_trajectory]
    vel_x = [t[2] for t in logged_trajectory]
    angle_deg = [np.degrees(t[3]) for t in logged_trajectory]
    vel_theta = [t[4] for t in logged_trajectory]
    forces = [t[5] for t in logged_trajectory]

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), dpi=200, sharex=True)

    # Subplot 1: Cart Position
    axes[0].plot(times, pos_x, color='#2980b9', linewidth=1.5, label='Cart Position x(t)')
    axes[0].axhline(y=2.4, color='#c0392b', linestyle=':', label='Track Boundary (+/- 2.4 m)')
    axes[0].axhline(y=-2.4, color='#c0392b', linestyle=':')
    axes[0].set_ylabel('Position (m)', fontsize=10)
    axes[0].set_title('Cart-Pole 500-Step Balancing Telemetry', fontsize=12, fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)
    axes[0].legend(loc='upper right', fontsize=8)

    # Subplot 2: Pole Angle
    axes[1].plot(times, angle_deg, color='#27ae60', linewidth=1.5, label='Pole Angle theta(t)')
    axes[1].axhline(y=12.0, color='#c0392b', linestyle=':', label='Failure Threshold (+/- 12 deg)')
    axes[1].axhline(y=-12.0, color='#c0392b', linestyle=':')
    axes[1].set_ylabel('Angle (deg)', fontsize=10)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].legend(loc='upper right', fontsize=8)

    # Subplot 3: Control Force
    axes[2].step(times, forces, color='#8e44ad', linewidth=1.2, where='post', label='Control Force F(t)')
    axes[2].set_xlabel('Time (s)', fontsize=10)
    axes[2].set_ylabel('Force (N)', fontsize=10)
    axes[2].grid(True, linestyle='--', alpha=0.5)
    axes[2].legend(loc='upper right', fontsize=8)

    traj_path = os.path.join(output_dir, "cartpole_trajectory.png")
    plt.tight_layout()
    plt.savefig(traj_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {traj_path}")


if __name__ == "__main__":
    evaluate_controller()
