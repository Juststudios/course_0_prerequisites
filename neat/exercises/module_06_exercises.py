"""Module 06 Exercises: Neural Network Phenotype & Activation.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Kahn's Topological Sort)
- Tier 4: Challenge (Feedforward DAG Forward Pass)
"""

import math
from typing import Dict, List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        # Q1: In a DAG, if there is a directed edge from u to v, which node must be evaluated first?
        "q1": "FILL_ME_IN",  # 'u' or 'v'
        # Q2: What numerical issue does clipping inputs to [-30, 30] prevent in sigmoid activation?
        "q2": "FILL_ME_IN",  # 'overflow' or 'dead neuron'
    }


# --- Tier 2: Understanding / Debugging ---
def buggy_kahns_sort(nodes: List[int], edges: List[Tuple[int, int]]) -> List[int]:
    """DEBUG CHALLENGE: This implementation decrements the in-degree of the current node
    instead of its outgoing neighbors, causing the algorithm to stall. Fix it!
    """
    in_degree = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for u, v in edges:
        in_degree[v] += 1
        adj[u].append(v)

    queue = [n for n in nodes if in_degree[n] == 0]
    order = []
    while queue:
        curr = queue.pop(0)
        order.append(curr)
        for neighbor in adj[curr]:
            # BUG: in_degree[curr] -= 1 was written instead of in_degree[neighbor] -= 1!
            in_degree[curr] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order


# --- Tier 3: Application ---
def kahns_topological_sort(nodes: List[int], edges: List[Tuple[int, int]]) -> List[int]:
    """Implement Kahn's algorithm:
    1. Compute in-degree for each node in `nodes`.
    2. Initialize queue with nodes having in-degree 0.
    3. Pop from queue, append to order, decrement in-degree of neighbors.
    4. When neighbor in-degree hits 0, append to queue.
    Return topological order list.
    """
    # TODO: Implement kahns_topological_sort
    raise NotImplementedError


# --- Tier 4: Challenge ---
def evaluate_dag(
    inputs: Dict[int, float],  # node_id -> input_value
    eval_order: List[int],     # hidden and output node IDs in topological order
    in_edges: Dict[int, List[Tuple[int, float]]],  # node_id -> [(in_node, weight)]
    biases: Dict[int, float],
    output_nodes: List[int],
) -> List[float]:
    """Perform forward evaluation across the DAG in topological order using sigmoid activation:
    For each node in eval_order:
      z = biases.get(node, 0.0) + sum(values[in_node] * w)
      values[node] = 1.0 / (1.0 + exp(-clip(z, -30, 30)))
    Return output activations for output_nodes.
    """
    # TODO: Implement evaluate_dag
    raise NotImplementedError


if __name__ == "__main__":
    print("Run solutions/module_06_solutions.py to test reference solutions.")
