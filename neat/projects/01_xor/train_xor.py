"""Train NEAT to solve the non-linear XOR classification problem.

Evolves minimal neural network topologies from scratch until reaching
fitness > 3.9, outputting visualization plots and champion genome state.
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
from neat.visualizations.visualizer import plot_fitness, plot_network, plot_species

XOR_DATA = [
    ([0.0, 0.0], 0.0),
    ([0.0, 1.0], 1.0),
    ([1.0, 0.0], 1.0),
    ([1.0, 1.0], 0.0),
]


def eval_xor(genome: Genome) -> float:
    """Fitness function computing 4.0 - sum of squared prediction errors."""
    net = FeedForwardNetwork.create(genome)
    total_loss = 0.0
    for inputs, target in XOR_DATA:
        pred = net.activate(inputs)[0]
        total_loss += (target - pred) ** 2
    return 4.0 - total_loss


def train_xor(
    output_dir: Optional[str] = None,
    seed: int = 3,
    max_generations: int = 80,
    fitness_threshold: float = 3.9,
) -> Tuple[Genome, dict]:
    """Execute NEAT evolution on XOR until fitness threshold is exceeded."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    config = NEATConfig(
        num_inputs=2,
        num_outputs=1,
        has_bias=True,
        pop_size=150,
        add_node_rate=0.2,
        add_connection_rate=0.4,
        weight_mutate_rate=0.8,
        weight_mutate_power=0.7,
        compatibility_threshold=2.5,
        seed=seed,
    )

    print(f"--- Starting NEAT XOR Evolution (Seed={seed}) ---")
    population = Population(config)
    champion, history = population.run(
        fitness_func=eval_xor,
        max_generations=max_generations,
        fitness_threshold=fitness_threshold,
    )

    print(f"Evolution terminated at generation {population.generation}.")
    print(f"Champion Fitness: {champion.fitness:.4f} / 4.0 (Threshold: {fitness_threshold})")

    # Evaluate champion network
    net = FeedForwardNetwork.create(champion)
    print("\nTruth Table Predictions:")
    for inputs, target in XOR_DATA:
        pred = net.activate(inputs)[0]
        print(f"  Input: {inputs} -> Pred: {pred:.4f} (Target: {target})")

    # Save champion model
    champion_path = os.path.join(output_dir, "champion_xor.pkl")
    with open(champion_path, "wb") as f:
        pickle.dump(champion, f)
    print(f"\nChampion model saved to: {champion_path}")

    # Generate Matplotlib visualizations
    fit_path = os.path.join(output_dir, "xor_fitness_curve.png")
    plot_fitness(
        history,
        save_path=fit_path,
        title="NEAT XOR Fitness Convergence",
        threshold=fitness_threshold,
    )
    print(f"Saved: {fit_path}")

    spec_path = os.path.join(output_dir, "xor_species_tracking.png")
    plot_species(
        history['species_history'],
        save_path=spec_path,
        title="NEAT XOR Speciation Dynamics",
    )
    print(f"Saved: {spec_path}")

    net_path = os.path.join(output_dir, "xor_best_network.png")
    plot_network(
        champion,
        save_path=net_path,
        title="NEAT XOR Evolved Champion Network",
    )
    print(f"Saved: {net_path}")

    return champion, history


if __name__ == "__main__":
    train_xor()
