"""Demonstration script for NEAT visualizations.

Generates sample fitness curves, speciation stackplots, and network topology diagrams.
"""

import os
import sys
from typing import Optional

# Ensure repository root is on sys.path
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import random

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.visualizations.visualizer import plot_fitness, plot_network, plot_species


def run_demo(output_dir: Optional[str] = None) -> None:
    if output_dir is None:
        output_dir = os.path.join(_REPO_ROOT, "neat/visualizations/output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating NEAT visualizer demonstrations in: {output_dir}")

    # 1. Synthetic fitness history
    generations = 30
    best_fitness = [1.0 + (3.95 - 1.0) / (1.0 + 2.718 ** (-0.3 * (g - 12))) for g in range(generations)]
    mean_fitness = [0.5 + 0.08 * g + 0.1 * random.uniform(-0.5, 0.5) for g in range(generations)]

    fit_path = os.path.join(output_dir, "demo_fitness_curve.png")
    plot_fitness(
        history={'best_fitness': best_fitness, 'mean_fitness': mean_fitness},
        save_path=fit_path,
        title="Demo: NEAT Fitness Convergence Curve",
        threshold=3.9,
    )
    print(f"Saved: {fit_path} ({os.path.getsize(fit_path)} bytes)")

    # 2. Synthetic speciation history
    species_history = {
        1: [100 - min(80, g * 3) for g in range(generations)],
        2: [0] * 5 + [min(40, (g - 5) * 4) for g in range(5, generations)],
        3: [0] * 12 + [min(50, (g - 12) * 5) for g in range(12, generations)],
        4: [0] * 18 + [min(30, (g - 18) * 3) for g in range(18, generations)],
    }
    spec_path = os.path.join(output_dir, "demo_species_dynamics.png")
    plot_species(species_history, spec_path, title="Demo: Speciation Dynamics Stackplot")
    print(f"Saved: {spec_path} ({os.path.getsize(spec_path)} bytes)")

    # 3. Sample evolved genome
    cfg = NEATConfig(num_inputs=2, num_outputs=1, has_bias=True)
    tracker = InnovationTracker(initial_node_count=3)
    genome = Genome.create_minimal(cfg, tracker, genome_id=1)
    # Add hidden node
    genome.mutate_add_node(cfg, tracker)
    # Add a second hidden node
    genome.mutate_add_node(cfg, tracker)
    genome.mutate_weights(cfg)

    net_path = os.path.join(output_dir, "demo_network_topology.png")
    plot_network(genome, net_path, title="Demo: Evolved Topology with Discovered Neurons")
    print(f"Saved: {net_path} ({os.path.getsize(net_path)} bytes)")


if __name__ == "__main__":
    run_demo()
