"""Train a NEAT neural network controller to balance the Cart-Pole dynamic system.

Evolves controllers capable of maintaining inverted pendulum balance for >= 500
consecutive time steps across multi-perturbation initial conditions.
"""

import os
import pickle
import sys
from typing import Optional, Tuple

# Ensure repository root is on sys.path
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.network import FeedForwardNetwork
from neat.neat_engine.population import Population
from neat.visualizations.visualizer import plot_fitness, plot_network

try:
    from cartpole_env import CartPoleEnv
except ImportError:
    import importlib
    _env_mod = importlib.import_module("neat.projects.02_cartpole.cartpole_env")
    CartPoleEnv = _env_mod.CartPoleEnv

EVAL_INITIAL_TILTS = [-0.05, 0.0, 0.05]


def eval_cartpole_genome(genome: Genome, env: CartPoleEnv) -> float:
    """Evaluate a candidate controller over multi-angle initial conditions."""
    net = FeedForwardNetwork.create(genome)
    total_steps = 0.0

    for init_theta in EVAL_INITIAL_TILTS:
        s = env.reset([0.0, 0.0, init_theta, 0.0])
        steps = 0
        while steps < env.max_steps:
            norm_s = env.normalize_state(s)
            action = net.activate(norm_s)[0]
            s, _, done, _ = env.step(action)
            steps += 1
            if done:
                break
        total_steps += steps

    return float(total_steps)


def train_cartpole(
    output_dir: Optional[str] = None,
    seed: int = 42,
    max_generations: int = 40,
    fitness_threshold: float = 1500.0,
) -> Tuple[Genome, dict]:
    """Execute NEAT evolution on Cart-Pole until controllers achieve >= 500 steps across trials."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    env = CartPoleEnv(max_steps=500)

    config = NEATConfig(
        num_inputs=4,
        num_outputs=1,
        has_bias=True,
        pop_size=100,
        add_node_rate=0.1,
        add_connection_rate=0.2,
        weight_mutate_rate=0.8,
        weight_mutate_power=0.5,
        compatibility_threshold=3.0,
        seed=seed,
    )

    print(f"--- Starting NEAT Cart-Pole Evolution (Seed={seed}) ---")
    population = Population(config)

    def fitness_fn(g: Genome) -> float:
        return eval_cartpole_genome(g, env)

    champion, history = population.run(
        fitness_func=fitness_fn,
        max_generations=max_generations,
        fitness_threshold=fitness_threshold,
    )

    print(f"Evolution terminated at generation {population.generation}.")
    print(f"Champion Fitness: {champion.fitness:.1f} / {fitness_threshold}")

    # Save champion
    champion_path = os.path.join(output_dir, "champion_cartpole.pkl")
    with open(champion_path, "wb") as f:
        pickle.dump(champion, f)
    print(f"\nChampion controller saved to: {champion_path}")

    # Generate plots
    fit_path = os.path.join(output_dir, "cartpole_fitness.png")
    plot_fitness(
        history,
        save_path=fit_path,
        title="NEAT Cart-Pole Fitness Convergence",
        threshold=fitness_threshold,
    )
    print(f"Saved: {fit_path}")

    net_path = os.path.join(output_dir, "cartpole_network.png")
    plot_network(
        champion,
        save_path=net_path,
        title="NEAT Cart-Pole Champion Controller Architecture",
    )
    print(f"Saved: {net_path}")

    return champion, history


if __name__ == "__main__":
    train_cartpole()
