"""Comparison of Fixed Topology vs Variable Topology Neuroevolution.

Demonstrates how linear fixed topologies fail on non-linear problems (XOR)
whereas structural topology growth discovers non-linear feature extractors.
Module 03: Neuroevolution & Topology Evolution.
"""

import math
import random
from typing import List, Tuple

# Ensure repository root is on sys.path
import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.neat_engine.network import FeedForwardNetwork

XOR_DATA = [
    ([0.0, 0.0], 0.0),
    ([0.0, 1.0], 1.0),
    ([1.0, 0.0], 1.0),
    ([1.0, 1.0], 0.0),
]


def evaluate_network(net: FeedForwardNetwork) -> Tuple[float, List[float]]:
    loss = 0.0
    preds = []
    for x, y in XOR_DATA:
        p = net.activate(x)[0]
        preds.append(p)
        loss += (y - p) ** 2
    return 4.0 - loss, preds


def simulate_fixed_topology_search(trials: int = 500) -> Tuple[float, Genome]:
    """Optimizes weights only on a strictly linear fixed topology (0 hidden nodes)."""
    cfg = NEATConfig(num_inputs=2, num_outputs=1, has_bias=True)
    tracker = InnovationTracker(initial_node_count=3)
    best_genome = Genome.create_minimal(cfg, tracker, genome_id=0)
    best_fit = -float('inf')

    rng = random.Random(42)
    current = best_genome.copy()

    for _ in range(trials):
        candidate = current.copy()
        candidate.mutate_weights(cfg, rng=rng)
        net = FeedForwardNetwork.create(candidate)
        fit, _ = evaluate_network(net)
        if fit > best_fit:
            best_fit = fit
            best_genome = candidate.copy()
            current = candidate.copy()

    return best_fit, best_genome


def simulate_variable_topology_search(trials: int = 500) -> Tuple[float, Genome]:
    """Allows structural mutations (adding nodes and connections) to expand topology."""
    cfg = NEATConfig(num_inputs=2, num_outputs=1, has_bias=True)
    tracker = InnovationTracker(initial_node_count=3)
    best_genome = Genome.create_minimal(cfg, tracker, genome_id=0)
    best_fit = -float('inf')

    rng = random.Random(42)
    current = best_genome.copy()

    for i in range(trials):
        candidate = current.copy()
        candidate.mutate_weights(cfg, rng=rng)
        # Periodically attempt structural mutations
        if rng.random() < 0.2:
            candidate.mutate_add_node(cfg, tracker, rng=rng)
        if rng.random() < 0.3:
            candidate.mutate_add_connection(cfg, tracker, rng=rng)

        net = FeedForwardNetwork.create(candidate)
        fit, _ = evaluate_network(net)
        if fit > best_fit:
            best_fit = fit
            best_genome = candidate.copy()
            current = candidate.copy()

    return best_fit, best_genome


def main():
    print("=== Fixed vs Variable Topology Comparison on XOR ===")

    fixed_fit, fixed_genome = simulate_fixed_topology_search(trials=1000)
    fixed_net = FeedForwardNetwork.create(fixed_genome)
    _, fixed_preds = evaluate_network(fixed_net)

    print(f"Fixed Topology (Linear Model, 0 Hidden Neurons):")
    print(f"  Best Fitness Achieved: {fixed_fit:.4f} / 4.0 (Theoretical Upper Bound: 3.0)")
    print(f"  Predictions:")
    for (x, y), p in zip(XOR_DATA, fixed_preds):
        print(f"    Input {x} -> Pred: {p:.4f} (Target: {y})")
    print(f"  Active Nodes: {len(fixed_genome.nodes)}, Connections: {len(fixed_genome.connections)}")

    print("\n-----------------------------------------------------\n")

    var_fit, var_genome = simulate_variable_topology_search(trials=1000)
    var_net = FeedForwardNetwork.create(var_genome)
    _, var_preds = evaluate_network(var_net)

    print(f"Variable Topology (Augmenting Topologies with Discovered Neurons):")
    print(f"  Best Fitness Achieved: {var_fit:.4f} / 4.0")
    print(f"  Predictions:")
    for (x, y), p in zip(XOR_DATA, var_preds):
        print(f"    Input {x} -> Pred: {p:.4f} (Target: {y})")
    hidden_nodes = [nid for nid, n in var_genome.nodes.items() if n.node_type == 'hidden']
    print(f"  Active Nodes: {len(var_genome.nodes)} (Discovered Hidden: {len(hidden_nodes)}), Connections: {len(var_genome.connections)}")


if __name__ == "__main__":
    main()
