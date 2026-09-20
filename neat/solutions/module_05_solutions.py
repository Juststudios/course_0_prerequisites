"""Reference Solutions for Module 05 Exercises: Crossover & Mutation Operators in NEAT."""

import random
from typing import Dict, List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "fitter",
        "q2": "1.0",
    }


# --- Tier 2: Understanding / Debugging ---
def fixed_add_node(connections: Dict[int, dict], target_inv: int, new_node_id: int, new_inv1: int, new_inv2: int) -> Dict[int, dict]:
    updated = {k: dict(v) for k, v in connections.items()}
    # FIXED: Disable original connection
    updated[target_inv]['enabled'] = False

    old = updated[target_inv]
    updated[new_inv1] = {'in': old['in'], 'out': new_node_id, 'weight': 1.0, 'enabled': True}
    updated[new_inv2] = {'in': new_node_id, 'out': old['out'], 'weight': old['weight'], 'enabled': True}
    return updated


# --- Tier 3: Application ---
def neat_crossover_weights(
    fitter_connections: Dict[int, float],
    other_connections: Dict[int, float],
    rng: random.Random,
) -> Dict[int, float]:
    child_weights = {}
    for inv, w_fit in fitter_connections.items():
        if inv in other_connections:
            # Matching: coin flip
            w_other = other_connections[inv]
            child_weights[inv] = w_fit if rng.random() < 0.5 else w_other
        else:
            # Disjoint / excess from fitter parent only
            child_weights[inv] = w_fit
    return child_weights


# --- Tier 4: Challenge ---
def apply_add_node_mutation(
    connections: Dict[int, dict],
    target_inv: int,
    new_node_id: int,
    inv_in: int,
    inv_out: int,
) -> Dict[int, dict]:
    updated = {k: dict(v) for k, v in connections.items()}
    target = updated[target_inv]
    target['enabled'] = False

    updated[inv_in] = {
        'in': target['in'],
        'out': new_node_id,
        'weight': 1.0,
        'enabled': True,
    }
    updated[inv_out] = {
        'in': new_node_id,
        'out': target['out'],
        'weight': target['weight'],
        'enabled': True,
    }
    return updated


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert ans["q1"].lower() == "fitter"
    assert "1" in ans["q2"]

    # Tier 2 & Tier 4
    conns = {1: {'in': 0, 'out': 2, 'weight': 0.85, 'enabled': True}}
    res = fixed_add_node(conns, target_inv=1, new_node_id=3, new_inv1=2, new_inv2=3)
    assert res[1]['enabled'] is False
    assert res[2]['weight'] == 1.0 and res[2]['out'] == 3
    assert res[3]['weight'] == 0.85 and res[3]['in'] == 3

    # Tier 3
    fitter = {1: 1.0, 2: 2.0, 3: 3.0}
    other = {1: 10.0, 2: 20.0, 4: 40.0}  # Inv 4 is disjoint in other
    rng = random.Random(42)
    child = neat_crossover_weights(fitter, other, rng)
    assert set(child.keys()) == {1, 2, 3}  # 4 from other must NOT be present
    assert child[3] == 3.0

    print("[SUCCESS] All Module 05 solutions verified!")


if __name__ == "__main__":
    test_solutions()
