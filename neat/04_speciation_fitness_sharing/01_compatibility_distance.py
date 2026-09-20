"""Demonstration of Compatibility Distance Calculation between NEAT Genomes.

Module 04: Speciation & Fitness Sharing.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome


def build_test_genome(conn_specs):
    """Helper to build a test genome with specific connections (in, out, weight, enabled, inv)."""
    g = Genome()
    for in_n, out_n, w, enabled, inv in conn_specs:
        g.connections[inv] = ConnectionGene(in_node=in_n, out_node=out_n, weight=w, enabled=enabled, innovation=inv)
        for nid, ntype in [(in_n, 'input'), (out_n, 'output')]:
            if nid not in g.nodes:
                g.nodes[nid] = NodeGene(id=nid, node_type=ntype)
    return g


def main():
    print("=== Compatibility Distance Metric Demonstration ===")
    # Parent 1 has innovations: 1, 2, 3, 4, 5, 8
    g1 = build_test_genome([
        (1, 4, 1.0, True, 1),
        (2, 4, -1.5, True, 2),
        (3, 4, 0.5, True, 3),
        (2, 5, 0.8, True, 4),
        (5, 4, 1.2, True, 5),
        (1, 5, 0.4, True, 8),
    ])

    # Parent 2 has innovations: 1, 2, 3, 4, 6, 7, 9, 10
    g2 = build_test_genome([
        (1, 4, 1.2, True, 1),   # Matching (diff = 0.2)
        (2, 4, -1.0, True, 2),  # Matching (diff = 0.5)
        (3, 4, 0.5, True, 3),   # Matching (diff = 0.0)
        (2, 5, 0.4, True, 4),   # Matching (diff = 0.4)
        (5, 6, 0.9, True, 6),   # Disjoint in G2
        (6, 4, 0.7, True, 7),   # Disjoint in G2
        (3, 5, -0.6, True, 9),  # Excess in G2
        (4, 5, 0.2, True, 10),  # Excess in G2
    ])
    # Innovation 5 is Disjoint in G1.
    # Innovation 8 is Disjoint in G1 (since max in G2 is 10, 8 <= 10).

    c1, c2, c3 = 1.0, 1.0, 0.4
    dist = g1.compatibility_distance(g2, c1=c1, c2=c2, c3=c3)

    # Detailed breakdown
    invs1 = set(g1.connections.keys())
    invs2 = set(g2.connections.keys())
    matching = sorted(invs1 & invs2)
    max1, max2 = max(invs1), max(invs2)
    threshold = min(max1, max2)

    diff_invs = invs1 ^ invs2
    excess = sorted(i for i in diff_invs if i > threshold)
    disjoint = sorted(i for i in diff_invs if i <= threshold)
    weight_diffs = [abs(g1.connections[i].weight - g2.connections[i].weight) for i in matching]
    w_bar = sum(weight_diffs) / len(weight_diffs)

    print("Genome 1 Innovations:", sorted(invs1))
    print("Genome 2 Innovations:", sorted(invs2))
    print(f"\nGene Alignment Analysis:")
    print(f"  Matching Innovations (M={len(matching)}): {matching}")
    print(f"  Weight differences on matching : {[round(d, 2) for d in weight_diffs]} -> W_bar = {w_bar:.3f}")
    print(f"  Disjoint Innovations (D={len(disjoint)}): {disjoint}")
    print(f"  Excess Innovations   (E={len(excess)}): {excess}")
    print(f"  Genome Size Normalizer N       : {1.0} (size < 20)")
    print(f"\nCalculated Compatibility Distance:")
    print(f"  delta = ({c1} * {len(excess)} / 1.0) + ({c2} * {len(disjoint)} / 1.0) + ({c3} * {w_bar:.3f})")
    print(f"  delta = {dist:.4f}")

    threshold = 3.0
    is_compatible = dist <= threshold
    print(f"\nSpeciation Threshold delta_t = {threshold}")
    print(f"Are Genomes 1 & 2 in the same species? {'YES' if is_compatible else 'NO'}")


if __name__ == "__main__":
    main()
