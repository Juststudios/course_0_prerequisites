"""Module 05 Exercises: Crossover & Mutation Operators in NEAT.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Homologous Crossover)
- Tier 4: Challenge (Add Node Mutation Splitting)
"""

import random
from typing import Dict, List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        # Q1: In NEAT crossover, which parent provides the disjoint and excess genes to the offspring?
        "q1": "FILL_ME_IN",  # 'fitter' or 'less-fit'
        # Q2: In an Add Node mutation, what weight is assigned to the new connection leading INTO the new node?
        "q2": "FILL_ME_IN",  # '1.0' or '0.0' or 'random'
    }


# --- Tier 2: Understanding / Debugging ---
def buggy_add_node(connections: Dict[int, dict], target_inv: int, new_node_id: int, new_inv1: int, new_inv2: int) -> Dict[int, dict]:
    """DEBUG CHALLENGE: This function splits an existing connection, but forgets to disable
    the old connection, causing redundant parallel transmission paths. Fix it!
    """
    updated = dict(connections)
    old = updated[target_inv]

    # BUG: old connection remains enabled: old['enabled'] is not set to False!

    updated[new_inv1] = {'in': old['in'], 'out': new_node_id, 'weight': 1.0, 'enabled': True}
    updated[new_inv2] = {'in': new_node_id, 'out': old['out'], 'weight': old['weight'], 'enabled': True}
    return updated


# --- Tier 3: Application ---
def neat_crossover_weights(
    fitter_connections: Dict[int, float],  # inv -> weight
    other_connections: Dict[int, float],   # inv -> weight
    rng: random.Random,
) -> Dict[int, float]:
    """Implement NEAT crossover weight inheritance:
    - For matching innovations: choose weight from fitter or other with 50% probability.
    - For disjoint/excess innovations: inherit only from fitter_connections.
    Return dictionary mapping innovation -> inherited weight.
    """
    # TODO: Implement neat_crossover_weights
    raise NotImplementedError


# --- Tier 4: Challenge ---
def apply_add_node_mutation(
    connections: Dict[int, dict],  # inv -> {'in': int, 'out': int, 'weight': float, 'enabled': bool}
    target_inv: int,
    new_node_id: int,
    inv_in: int,
    inv_out: int,
) -> Dict[int, dict]:
    """Split target connection:
    1. Mark target_inv as enabled = False.
    2. Add inv_in: in_node -> new_node_id, weight = 1.0, enabled = True.
    3. Add inv_out: new_node_id -> out_node, weight = old.weight, enabled = True.
    Return updated connections dictionary.
    """
    # TODO: Implement apply_add_node_mutation
    raise NotImplementedError


if __name__ == "__main__":
    print("Run solutions/module_05_solutions.py to test reference solutions.")
