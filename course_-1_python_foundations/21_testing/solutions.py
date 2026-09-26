"""
Module 21: Testing — Reference Solutions
=========================================

Complete, verified reference solutions for all four exercise tiers.
"""

import math
from typing import Any, List, Optional


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def count_words(text: str) -> int:
    return len(text.split())

def test_count_words_suite() -> None:
    # 1. Empty string
    assert count_words("") == 0, "Empty string should have 0 words"

    # 2. Single word
    assert count_words("Python") == 1, "Single word should have 1 word"

    # 3. Multiple words
    assert count_words("AI agents write code") == 4, "Sentence should have 4 words"

    # 4. Irregular whitespace
    assert count_words("  hello   world  ") == 2, "Padded words should have 2 words"


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    return numerator / denominator

def test_safe_divide_unbroken() -> None:
    # 1. Strict assertion on happy path without vacuous shortcuts
    res = safe_divide(10, 2)
    assert res == 5.0, f"Expected 5.0, got {res}"

    # 2. Defensive exception check with assert False guard
    try:
        safe_divide(5, 0)
        assert False, "Expected ZeroDivisionError was not raised!"
    except ZeroDivisionError as err:
        assert "Denominator cannot be zero" in str(err)


# =====================================================================
# Level 3: Build Solution
# =====================================================================
class LifoStack:
    def __init__(self):
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


def test_lifo_stack_complete_suite() -> None:
    # 1. Initial empty state
    stack = LifoStack()
    assert stack.is_empty() is True
    assert len(stack) == 0

    # 2. Push elements
    stack.push("a")
    stack.push("b")
    assert len(stack) == 2
    assert stack.is_empty() is False

    # 3. Peek element
    top = stack.peek()
    assert top == "b"
    assert len(stack) == 2  # peek does not remove

    # 4. Pop elements in LIFO order
    assert stack.pop() == "b"
    assert stack.pop() == "a"
    assert stack.is_empty() is True
    assert len(stack) == 0

    # 5. Empty pop raises IndexError
    try:
        stack.pop()
        assert False, "Calling pop() on empty stack should raise IndexError"
    except IndexError:
        pass

    # 6. Empty peek raises IndexError
    try:
        stack.peek()
        assert False, "Calling peek() on empty stack should raise IndexError"
    except IndexError:
        pass


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def normalize_agent_probabilities(weights: List[float]) -> List[float]:
    total = sum(weights)
    if total <= 0:
        raise ValueError("Sum of weights must be positive")
    return [round(w / total, 4) for w in weights]


def test_normalize_agent_probabilities_robust() -> None:
    # 1. Check length and individual normalized probabilities
    probs = normalize_agent_probabilities([1.0, 1.0, 1.0])
    assert len(probs) == 3, f"Expected 3 probabilities, got {len(probs)}"
    for p in probs:
        assert math.isclose(p, 0.3333, abs_tol=1e-3), f"Expected ~0.3333, got {p}"

    # 2. Check total sum with tolerance
    total_prob = sum(probs)
    assert math.isclose(total_prob, 1.0, abs_tol=1e-3), f"Expected sum ~1.0, got {total_prob}"

    # 3. Check invalid non-positive sum weights raise ValueError
    try:
        normalize_agent_probabilities([-1.0, 0.5])
        assert False, "Should raise ValueError when sum is non-positive"
    except ValueError as err:
        assert "Sum of weights must be positive" in str(err)

    try:
        normalize_agent_probabilities([0.0, 0.0])
        assert False, "Should raise ValueError when sum is zero"
    except ValueError:
        pass


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    print("Running Module 21 Test Suite...")
    test_count_words_suite()
    test_safe_divide_unbroken()
    test_lifo_stack_complete_suite()
    test_normalize_agent_probabilities_robust()
    print("Module 21: All Level 1-4 solutions verified successfully!")
