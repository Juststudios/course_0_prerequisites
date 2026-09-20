"""Reference Solutions for Module 03 Exercises: Neuroevolution & Topology Evolution."""

from typing import Dict, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "competing conventions",
        "q2": "innovation number",
    }


# --- Tier 2: Understanding / Debugging ---
class FixedInnovationTracker:
    def __init__(self):
        self.counter = 0
        self.cache: Dict[Tuple[int, int], int] = {}

    def get_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key in self.cache:
            return self.cache[key]
        self.counter += 1
        self.cache[key] = self.counter
        return self.counter


# --- Tier 3: Application ---
class SimpleInnovationTracker:
    def __init__(self):
        self.current_innovation = 0
        self.generation_innovations: Dict[Tuple[int, int], int] = {}

    def get_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key in self.generation_innovations:
            return self.generation_innovations[key]
        self.current_innovation += 1
        self.generation_innovations[key] = self.current_innovation
        return self.current_innovation

    def reset_generation(self) -> None:
        self.generation_innovations.clear()


# --- Tier 4: Challenge ---
class AdvancedInnovationTracker(SimpleInnovationTracker):
    def __init__(self, initial_nodes: int = 3):
        super().__init__()
        self.current_node_id = initial_nodes
        self.node_innovations: Dict[int, int] = {}

    def get_node_id(self, connection_innovation: int) -> int:
        if connection_innovation in self.node_innovations:
            return self.node_innovations[connection_innovation]
        self.current_node_id += 1
        self.node_innovations[connection_innovation] = self.current_node_id
        return self.current_node_id

    def reset_generation(self) -> None:
        super().reset_generation()
        self.node_innovations.clear()


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert "competing" in ans["q1"].lower()
    assert "innovation" in ans["q2"].lower()

    # Tier 2
    fit = FixedInnovationTracker()
    assert fit.get_innovation(1, 2) == 1
    assert fit.get_innovation(1, 2) == 1
    assert fit.get_innovation(2, 3) == 2

    # Tier 3
    tracker = SimpleInnovationTracker()
    assert tracker.get_innovation(0, 3) == 1
    assert tracker.get_innovation(0, 3) == 1
    assert tracker.get_innovation(1, 3) == 2
    tracker.reset_generation()
    assert tracker.get_innovation(0, 3) == 3

    # Tier 4
    adv = AdvancedInnovationTracker(initial_nodes=3)
    assert adv.get_node_id(1) == 4
    assert adv.get_node_id(1) == 4
    assert adv.get_node_id(2) == 5
    adv.reset_generation()
    assert adv.get_node_id(1) == 6

    print("[SUCCESS] All Module 03 solutions verified!")


if __name__ == "__main__":
    test_solutions()
