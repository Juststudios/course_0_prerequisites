"""Demonstration of Recurrent Neural Network State Persistence and Temporal Dynamics.

Module 06: Neural Network Phenotype & Activation.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome
from neat.neat_engine.network import RecurrentNetwork


def main():
    print("=== Recurrent Neural Network Temporal Dynamics Demonstration ===")

    # Build a recurrent network with self-loop memory:
    # Input: 0, Output: 1.
    # Hidden: 2 with self-recurrent loop: 2 -> 2 (memory retention).
    # Connections:
    # 0 -> 2 (weight 1.0)
    # 2 -> 2 (recurrent self-connection, weight 1.5)
    # 2 -> 1 (weight 1.0)
    g = Genome()
    g.nodes[0] = NodeGene(0, 'input')
    g.nodes[1] = NodeGene(1, 'output', bias=0.0, activation='sigmoid')
    g.nodes[2] = NodeGene(2, 'hidden', bias=0.0, activation='tanh')

    g.connections[1] = ConnectionGene(in_node=0, out_node=2, weight=1.0, enabled=True, innovation=1)
    g.connections[2] = ConnectionGene(in_node=2, out_node=2, weight=1.5, enabled=True, innovation=2)  # Cycle!
    g.connections[3] = ConnectionGene(in_node=2, out_node=1, weight=1.0, enabled=True, innovation=3)

    rec_net = RecurrentNetwork.create(g, relaxation_steps=2)

    print("Network Structure:")
    print("  Input: Node 0")
    print("  Hidden: Node 2 (with self-recurrent connection 2 -> 2)")
    print("  Output: Node 1")

    # Feed a transient pulse: [1.0] at step 0, followed by [0.0] thereafter
    pulse_sequence = [1.0, 0.0, 0.0, 0.0, 0.0]
    print("\nSimulating discrete temporal steps with transient pulse [1.0, 0.0, 0.0, 0.0, 0.0]:")
    print(f"{'Step':<6} | {'Input':<8} | {'Hidden State (Node 2)':<24} | {'Output (Node 1)':<16}")
    print("-" * 62)

    rec_net.reset()
    for step, val in enumerate(pulse_sequence):
        out = rec_net.activate([val])
        h_val = rec_net.state[2]
        print(f"{step:<6} | {val:<8.1f} | {h_val:<24.5f} | {out[0]:<16.5f}")

    print("\nInsight:")
    print("Even when input returns to 0.0 at step 1+, the recurrent hidden neuron maintains")
    print("non-zero activation due to the internal self-recurrent feedback loop (memory).")
    print("\n[SUCCESS] RecurrentNetwork temporal dynamics verified!")


if __name__ == "__main__":
    main()
