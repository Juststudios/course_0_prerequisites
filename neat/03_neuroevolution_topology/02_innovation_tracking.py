"""Demonstration of Global Historical Markings and Innovation Tracking.

Module 03: Neuroevolution & Topology Evolution.
"""

import os, sys
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from neat.neat_engine.innovation import InnovationTracker


def main():
    print("=== Innovation Tracking Demonstration ===")
    tracker = InnovationTracker(initial_node_count=3)
    print(f"Initial State: Current Innovation = {tracker.current_innovation}, Current Node ID = {tracker.current_node_id}")

    print("\n--- Generation 1 ---")
    # Genome A mutates: adds edge 1 -> 4
    inv_a = tracker.get_innovation(in_node=1, out_node=4)
    print(f"Genome A mutates connection (1 -> 4) => Assigned Innovation ID: {inv_a}")

    # Genome B mutates the same edge (1 -> 4) in the same generation
    inv_b = tracker.get_innovation(in_node=1, out_node=4)
    print(f"Genome B mutates connection (1 -> 4) => Assigned Innovation ID: {inv_b}")
    assert inv_a == inv_b, "Identical concurrent mutations must share innovation ID!"

    # Genome C mutates novel edge (2 -> 4)
    inv_c = tracker.get_innovation(in_node=2, out_node=4)
    print(f"Genome C mutates connection (2 -> 4) => Assigned Innovation ID: {inv_c}")
    assert inv_c == inv_a + 1

    # Genome D splits connection with innovation ID 1
    node_d1 = tracker.get_node_id(connection_innovation=inv_a)
    print(f"Genome D splits connection ID {inv_a} => Assigned New Node ID: {node_d1}")

    # Genome E also splits connection with innovation ID 1 in the same generation
    node_e1 = tracker.get_node_id(connection_innovation=inv_a)
    print(f"Genome E splits connection ID {inv_a} => Assigned New Node ID: {node_e1}")
    assert node_d1 == node_e1, "Splitting same connection in same generation must share Node ID!"

    print("\n--- Resetting for Generation 2 ---")
    tracker.reset_generation()
    print("Generation cache cleared. Monotonic counters preserved:")
    print(f"  Current Innovation Counter: {tracker.current_innovation}")
    print(f"  Current Node Counter      : {tracker.current_node_id}")

    # In generation 2, mutating (1 -> 4) receives a new innovation ID
    inv_next_gen = tracker.get_innovation(in_node=1, out_node=4)
    print(f"Generation 2: mutation (1 -> 4) => Assigned Innovation ID: {inv_next_gen}")
    assert inv_next_gen > inv_c, "New generation mutations must receive incremented innovation IDs!"

    print("\n[SUCCESS] InnovationTracker verification complete!")


if __name__ == "__main__":
    main()
