"""Module 03 Exercises: Neuroevolution & Topology Evolution.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Innovation Tracker)
- Tier 4: Challenge (Node Split Innovation Caching)
"""

from typing import Dict, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        # Q1: What problem describes topologically identical networks with permuted hidden neurons?
        "q1": "FILL_ME_IN",  # 'competing conventions' or 'vanishing gradient'
        # Q2: In NEAT, what data structure acts as an evolutionary birth certificate for connection genes?
        "q2": "FILL_ME_IN",  # 'innovation number' or 'layer index'
    }


# --- Tier 2: Understanding / Debugging ---
class BuggyInnovationTracker:
    """DEBUG CHALLENGE: This tracker fails to cache mutations within a generation,
    so two identical concurrent mutations get different innovation numbers. Fix it!
    """
    def __init__(self):
        self.counter = 0

    def get_innovation(self, in_node: int, out_node: int) -> int:
        # BUG: Doesn't check if (in_node, out_node) was already mutated this generation!
        self.counter += 1
        return self.counter


# --- Tier 3: Application ---
class SimpleInnovationTracker:
    """Implement an Innovation Tracker:
    - `get_innovation(in_node, out_node)` returns same ID if already mutated this generation,
      otherwise increments counter and records it.
    - `reset_generation()` clears generation cache while preserving counter.
    """
    def __init__(self):
        # TODO: Initialize
        pass

    def get_innovation(self, in_node: int, out_node: int) -> int:
        # TODO: Implement
        raise NotImplementedError

    def reset_generation(self) -> None:
        # TODO: Implement
        raise NotImplementedError


# --- Tier 4: Challenge ---
class AdvancedInnovationTracker(SimpleInnovationTracker):
    """Extend the tracker to also manage node splitting:
    `get_node_id(connection_innovation: int) -> int`:
    If connection_innovation was already split this generation, return the existing node ID.
    Otherwise increment node counter and record it.
    """
    def __init__(self, initial_nodes: int = 3):
        # TODO: Implement
        super().__init__()

    def get_node_id(self, connection_innovation: int) -> int:
        # TODO: Implement
        raise NotImplementedError


if __name__ == "__main__":
    print("Run solutions/module_03_solutions.py to test reference solutions.")
