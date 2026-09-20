"""Reference Solutions for Module 06 Exercises: Neural Network Phenotype & Activation."""

import math
from typing import Dict, List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "u",
        "q2": "overflow",
    }


# --- Tier 2: Understanding / Debugging ---
def fixed_kahns_sort(nodes: List[int], edges: List[Tuple[int, int]]) -> List[int]:
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
            # FIXED: decrement neighbor's in-degree
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order


# --- Tier 3: Application ---
def kahns_topological_sort(nodes: List[int], edges: List[Tuple[int, int]]) -> List[int]:
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
        for neighbor in adj.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order


# --- Tier 4: Challenge ---
def evaluate_dag(
    inputs: Dict[int, float],
    eval_order: List[int],
    in_edges: Dict[int, List[Tuple[int, float]]],
    biases: Dict[int, float],
    output_nodes: List[int],
) -> List[float]:
    values = dict(inputs)

    for node in eval_order:
        z = biases.get(node, 0.0)
        for in_node, weight in in_edges.get(node, []):
            z += values.get(in_node, 0.0) * weight
        z_clipped = max(-30.0, min(30.0, z))
        values[node] = 1.0 / (1.0 + math.exp(-z_clipped))

    return [values[o] for o in output_nodes]


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert ans["q1"].lower() == "u"
    assert "overflow" in ans["q2"].lower()

    # Tier 2 & 3
    nodes = [0, 1, 2, 3]
    edges = [(0, 2), (1, 2), (2, 3)]
    order = fixed_kahns_sort(nodes, edges)
    assert order.index(0) < order.index(2)
    assert order.index(1) < order.index(2)
    assert order.index(2) < order.index(3)

    # Tier 4
    inputs = {0: 1.0, 1: 0.0}
    eval_order = [2, 3]
    in_edges = {2: [(0, 1.0), (1, 1.0)], 3: [(2, 2.0)]}
    biases = {2: 0.0, 3: 0.0}
    outputs = evaluate_dag(inputs, eval_order, in_edges, biases, [3])
    # Node 2 = sigmoid(1.0*1.0 + 0.0) = sigmoid(1.0) ~ 0.731058
    # Node 3 = sigmoid(0.731058 * 2.0) = sigmoid(1.4621) ~ 0.8118
    assert len(outputs) == 1
    assert 0.80 < outputs[0] < 0.83

    print("[SUCCESS] All Module 06 solutions verified!")


if __name__ == "__main__":
    test_solutions()
