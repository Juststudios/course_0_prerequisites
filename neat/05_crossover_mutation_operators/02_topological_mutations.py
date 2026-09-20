"""Demonstration of Structural Mutations: Add Connection and Add Node.

Module 05: Crossover & Mutation Operators in NEAT.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import random
from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker


def main():
    print("=== NEAT Structural Topological Mutations Demonstration ===")
    rng = random.Random(42)
    cfg = NEATConfig(num_inputs=2, num_outputs=1, has_bias=True)
    tracker = InnovationTracker(initial_node_count=3)

    # 1. Start with minimal genome
    genome = Genome.create_minimal(cfg, tracker, genome_id=1, rng=rng)
    print("Initial Minimal Genome (0 Hidden Nodes):")
    print(f"  Nodes: {list(genome.nodes.keys())}")
    print(f"  Connections ({len(genome.connections)}):")
    for inv, c in sorted(genome.connections.items()):
        print(f"    Inv {inv}: ({c.in_node} -> {c.out_node}), Weight = {c.weight:+.4f}, Enabled = {c.enabled}")

    # 2. Add Node Mutation (split an enabled connection)
    print("\n--- Applying 'Add Node Mutation' ---")
    success_node = genome.mutate_add_node(cfg, tracker, rng=rng)
    assert success_node

    hidden_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'hidden']
    print(f"  Discovered Hidden Node IDs: {hidden_nodes}")
    print(f"  Updated Connections ({len(genome.connections)}):")
    for inv, c in sorted(genome.connections.items()):
        status = "ENABLED " if c.enabled else "DISABLED"
        print(f"    Inv {inv}: ({c.in_node} -> {c.out_node}), Weight = {c.weight:+.4f}, {status}")

    # 3. Add Connection Mutation (connect previously unconnected nodes)
    print("\n--- Applying 'Add Connection Mutation' ---")
    initial_conn_count = len(genome.connections)
    success_conn = genome.mutate_add_connection(cfg, tracker, rng=rng)
    print(f"  New Connection Added: {success_conn}")
    assert len(genome.connections) == initial_conn_count + 1

    latest_inv = max(genome.connections.keys())
    new_c = genome.connections[latest_inv]
    print(f"  Added Edge: ({new_c.in_node} -> {new_c.out_node}) with Innovation ID {new_c.innovation}")

    print("\n[SUCCESS] Structural mutations verified!")


if __name__ == "__main__":
    main()
