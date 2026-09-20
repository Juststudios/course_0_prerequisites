"""
Train Tabular Q-Learning on GridWorld
====================================
Runs an end-to-end Reinforcement Learning experiment:
  1. Initializes the 4x5 GridWorld MDP with obstacles and traps
  2. Trains a Tabular Q-Learning Agent over 600 episodes
  3. Visualizes epsilon decay, reward convergence, and step count reduction
  4. Renders the learned optimal policy in ASCII grid format
  5. Evaluates deterministic test rollouts to verify convergence to the optimal 7-step trajectory
  6. Saves training curves to `output/q_learning_training.png`
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

from gridworld import (
    GridWorld, ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
    ACTION_NAMES, ACTION_ARROWS
)
from q_learning import QLearningAgent

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def print_policy_grid(env, policy):
    """Render the learned policy grid in clean ASCII."""
    print("\nLearned Optimal Policy Grid (pi*):")
    header = "    " + "   ".join(str(c) for c in range(env.cols))
    print(header)
    print("  +" + "---+" * env.cols)

    for r in range(env.rows):
        row_cells = []
        for c in range(env.cols):
            pos = (r, c)
            if pos == env.goal_state:
                row_cells.append(" G ")
            elif pos in env.trap_states:
                row_cells.append(" T ")
            elif pos in env.wall_states:
                row_cells.append("###")
            else:
                best_act = policy.get(pos, None)
                arrow = ACTION_ARROWS.get(best_act, " ") if best_act is not None else " "
                row_cells.append(f" {arrow} ")
        print(f"{r} |" + "|".join(row_cells) + "|")
        print("  +" + "---+" * env.cols)


def print_value_grid(env, values):
    """Render state values V(s) in a formatted numeric grid."""
    print("\nState Values V(s) = max_a Q(s, a):")
    header = "    " + "       ".join(str(c) for c in range(env.cols))
    print(header)
    print("  +" + "-------+" * env.cols)

    for r in range(env.rows):
        row_cells = []
        for c in range(env.cols):
            pos = (r, c)
            if pos in env.wall_states:
                row_cells.append("  WALL ")
            elif pos == env.goal_state:
                row_cells.append(f"{values.get(pos, 10.0):6.2f} ")
            elif pos in env.trap_states:
                row_cells.append(f"{values.get(pos, -10.0):6.2f} ")
            else:
                row_cells.append(f"{values.get(pos, 0.0):6.2f} ")
        print(f"{r} |" + "|".join(row_cells) + "|")
        print("  +" + "-------+" * env.cols)


def train(num_episodes=600, max_steps_per_episode=60):
    """Execute training loop for Q-Learning agent."""
    print("=" * 65)
    print("REINFORCEMENT LEARNING: TABULAR Q-LEARNING TRAINING")
    print("=" * 65)

    env = GridWorld()
    agent = QLearningAgent(
        actions=env.action_space,
        alpha=0.15,
        gamma=0.95,
        epsilon=1.0,
        epsilon_decay=0.993,
        epsilon_min=0.01,
        random_state=42
    )

    episode_rewards = []
    episode_steps = []
    epsilons = []

    print(f"Environment: 4x5 GridWorld (Start: (0,0), Goal: (3,4))")
    print(f"Traps: {env.trap_states} | Walls: {env.wall_states}")
    print(f"Training for {num_episodes} episodes (max {max_steps_per_episode} steps/ep)...\n")

    for ep in range(1, num_episodes + 1):
        state = env.reset()
        total_reward = 0.0
        steps = 0

        for _ in range(max_steps_per_episode):
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.update(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps += 1
            if done:
                break

        agent.decay_epsilon()
        episode_rewards.append(total_reward)
        episode_steps.append(steps)
        epsilons.append(agent.epsilon)

        if ep % 100 == 0 or ep == 1:
            recent_avg_reward = np.mean(episode_rewards[-50:])
            recent_avg_steps = np.mean(episode_steps[-50:])
            print(f"Episode {ep:4d}/{num_episodes} | Epsilon: {agent.epsilon:.3f} | "
                  f"Avg Reward (last 50): {recent_avg_reward:6.2f} | Avg Steps: {recent_avg_steps:4.1f}")

    # Extract learned policy and values
    all_states = env.get_all_states()
    policy = agent.get_policy(all_states)
    values = agent.get_value_function(all_states)

    print_policy_grid(env, policy)
    print_value_grid(env, values)

    # Deterministic greedy evaluation
    agent.epsilon = 0.0
    eval_state = env.reset()
    eval_path = [eval_state]
    eval_done = False
    eval_reward = 0.0

    while not eval_done and len(eval_path) <= 20:
        act = agent.choose_action(eval_state)
        eval_state, r, eval_done, info = env.step(act)
        eval_reward += r
        eval_path.append(eval_state)

    print("\n" + "=" * 65)
    print("DETERMINISTIC EVALUATION ROLLOUT (Greedy Path):")
    print(f"  Path: {eval_path}")
    print(f"  Steps to Goal: {len(eval_path) - 1}")
    print(f"  Total Cumulative Reward: {eval_reward:.1f}")
    print(f"  Reached Goal Safely: {eval_state == env.goal_state}")
    print("=" * 65)

    assert eval_state == env.goal_state, "Agent failed to reach goal in greedy rollout!"
    assert len(eval_path) - 1 == 7, f"Agent did not discover the optimal 7-step path (took {len(eval_path)-1} steps)!"

    # Generate Visualization Plot
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    fig.suptitle("Tabular Q-Learning Convergence in GridWorld", fontsize=13, fontweight='bold')

    # Subplot 1: Episode Reward
    # Compute rolling window average
    window = 30
    rolling_reward = np.convolve(episode_rewards, np.ones(window)/window, mode='valid')
    axes[0].plot(episode_rewards, alpha=0.3, color='steelblue', label='Raw Episode Reward')
    axes[0].plot(range(window - 1, len(episode_rewards)), rolling_reward, color='navy', linewidth=2, label=f'{window}-Ep Moving Avg')
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Total Cumulative Reward")
    axes[0].set_title("Training Reward Convergence")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Subplot 2: Steps per Episode
    rolling_steps = np.convolve(episode_steps, np.ones(window)/window, mode='valid')
    axes[1].plot(episode_steps, alpha=0.3, color='coral', label='Steps')
    axes[1].plot(range(window - 1, len(episode_steps)), rolling_steps, color='crimson', linewidth=2, label=f'{window}-Ep Moving Avg')
    axes[1].axhline(7, color='green', linestyle='--', linewidth=1.5, label='Optimal Path (7 steps)')
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Steps Taken")
    axes[1].set_title("Convergence to Shortest Path")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Subplot 3: Epsilon Exploration Decay
    axes[2].plot(epsilons, color='purple', linewidth=2)
    axes[2].set_xlabel("Episode")
    axes[2].set_ylabel("Epsilon (Exploration Rate)")
    axes[2].set_title("Epsilon-Greedy Schedule")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plot_file = OUTPUT_DIR / "q_learning_training.png"
    plt.savefig(plot_file, dpi=120)
    plt.close()
    print(f"\nTraining curves saved to: {plot_file}")
    print("=" * 65)
    print("ALL Q-LEARNING VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    train(num_episodes=600)
