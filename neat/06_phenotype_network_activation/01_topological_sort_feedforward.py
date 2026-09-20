"""Demonstration of Kahn's Topological Sorting and Feedforward DAG Activation.

Module 06: Neural Network Phenotype & Activation.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome
from neat.neat_engine.network import FeedForwardNetwork


def main():
    print("=== Kahn's Topological Sort & Feedforward Activation ===")

    # Construct an irregular DAG with skip connections:
    # Inputs: 0, 1. Bias: 2. Hidden: 4, 5. Output: 3.
    # Connections:
    # 0 -> 4, 1 -> 4
    # 4 -> 5
    # 0 -> 3 (skip connection direct from input to output)
    # 5 -> 3
    # 2 -> 3 (bias)
    g = Genome()
    g.nodes[0] = NodeGene(0, 'input')
    g.nodes[1] = NodeGene(1, 'input')
    g.nodes[2] = NodeGene(2, 'bias', bias=1.0)
    g.nodes[3] = NodeGene(3, 'output', bias=-0.5, activation='sigmoid')
    g.nodes[4] = NodeGene(4, 'hidden', bias=0.2, activation='relu')
    g.nodes[5] = NodeGene(5, 'hidden', bias=-0.1, activation='tanh')

    conns = [
        (0, 4, 1.5, 1),
        (1, 4, -0.8, 2),
        (4, 5, 2.0, 3),
        (0, 3, 0.7, 4),  # Skip connection
        (5, 3, 1.2, 5),
        (2, 3, -1.0, 6), # Bias edge
    ]
    for u, v, w, inv in conns:
        g.connections[inv] = ConnectionGene(u, v, w, True, inv)

    print("Genome Topology:")
    print("  Inputs  : [0, 1], Bias: [2]")
    print("  Hidden  : [4 (ReLU), 5 (Tanh)]")
    print("  Outputs : [3 (Sigmoid)]")
    print("  Edges   :", [(c.in_node, c.out_node, c.weight) for c in g.connections.values()])

    net = FeedForwardNetwork.create(g)

    print("\nDecoded Computational Graph:")
    print(f"  Inputs Node IDs       : {net.inputs}")
    print(f"  Outputs Node IDs      : {net.outputs}")
    print(f"  Evaluation Order (DAG): {net.eval_order}")
    assert net.eval_order.index(4) < net.eval_order.index(5) < net.eval_order.index(3)
    print("  Topological constraint verified: Node 4 evaluated before 5, Node 5 before 3!")

    # Test forward activations
    test_inputs = [
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
    ]
    print("\nFeedforward Inference Outputs:")
    for inp in test_inputs:
        out = net.activate(inp)
        print(f"  Input: {inp} -> Output: [{out[0]:.5f}]")

    print("\n[SUCCESS] FeedForwardNetwork Kahn's sort verification passed!")


if __name__ == "__main__":
    main()
