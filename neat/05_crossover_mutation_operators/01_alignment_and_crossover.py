"""Demonstration of NEAT Innovation Alignment and Recombination.

Module 05: Crossover & Mutation Operators in NEAT.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import random
from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome


def build_parent(fitness: float, conn_tuples):
    """Build genome with fitness and connections: [(in, out, weight, enabled, inv), ...]."""
    g = Genome()
    g.fitness = fitness
    for in_n, out_n, w, enabled, inv in conn_tuples:
        g.connections[inv] = ConnectionGene(in_node=in_n, out_node=out_n, weight=w, enabled=enabled, innovation=inv)
        for nid, ntype in [(in_n, 'input'), (out_n, 'output')]:
            if nid not in g.nodes:
                g.nodes[nid] = NodeGene(id=nid, node_type=ntype)
    return g


def main():
    print("=== NEAT Gene Alignment & Crossover Demonstration ===")
    rng = random.Random(42)

    # Parent 1: Fitter Parent (Fitness = 3.8)
    p1 = build_parent(3.8, [
        (1, 4, +0.8, True, 1),
        (2, 4, -0.5, True, 2),
        (3, 4, +0.3, True, 3),
        (2, 5, +0.7, True, 4),
        (5, 4, +1.0, True, 5),
        (1, 5, -0.2, True, 8),  # Disjoint
    ])

    # Parent 2: Less-Fit Parent (Fitness = 2.1)
    p2 = build_parent(2.1, [
        (1, 4, +0.1, True, 1),
        (2, 4, -0.9, False, 2),  # Disabled in P2
        (3, 4, +0.4, True, 3),
        (2, 5, +0.2, True, 4),
        (5, 6, +0.5, True, 6),   # Disjoint in P2
        (6, 4, +0.6, True, 7),   # Disjoint in P2
        (3, 5, -0.1, True, 9),   # Excess in P2
        (4, 5, +0.3, True, 10),  # Excess in P2
    ])

    print("Parent 1 (FITTER, Fitness = 3.8):")
    for inv, c in sorted(p1.connections.items()):
        status = "ENABLED" if c.enabled else "DISABLED"
        print(f"  Inv {inv:>2}: ({c.in_node} -> {c.out_node}), Weight={c.weight:+.2f}, {status}")

    print("\nParent 2 (LESS FIT, Fitness = 2.1):")
    for inv, c in sorted(p2.connections.items()):
        status = "ENABLED" if c.enabled else "DISABLED"
        print(f"  Inv {inv:>2}: ({c.in_node} -> {c.out_node}), Weight={c.weight:+.2f}, {status}")

    # Perform Crossover
    child = p1.crossover(p2, rng=rng)

    print("\nOffspring Result (Child Genome):")
    print(f"  Total Connections Inherited: {len(child.connections)}")
    for inv, c in sorted(child.connections.items()):
        source = "Parent 1 & 2 (Matching)" if inv in p1.connections and inv in p2.connections else "Parent 1 Only (Fitter Disjoint/Excess)"
        status = "ENABLED" if c.enabled else "DISABLED"
        print(f"  Inv {inv:>2}: ({c.in_node} -> {c.out_node}), Weight={c.weight:+.2f}, {status:<8} [{source}]")

    # Verify that no disjoint or excess genes from Parent 2 leaked into child
    p2_only = set(p2.connections.keys()) - set(p1.connections.keys())
    leaked = p2_only & set(child.connections.keys())
    assert not leaked, f"Error: Disjoint genes from less-fit parent leaked: {leaked}"
    print(f"\n[SUCCESS] Crossover verified: 0 of {len(p2_only)} disjoint/excess genes from less-fit parent inherited.")


if __name__ == "__main__":
    main()
