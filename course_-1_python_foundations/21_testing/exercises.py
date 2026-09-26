"""
Module 21: Testing — Exercises
===============================

Practice unit testing, assertion mechanics, test fixtures, and edge cases.
Complete the four progressive exercise levels below.
"""

from typing import Any, List, Optional


# =====================================================================
# Level 1: Recall
# =====================================================================
def count_words(text: str) -> int:
    """Helper function under test for Level 1."""
    return len(text.split())

def test_count_words_suite() -> None:
    """
    Recall Exercise:
    Write four distinct assertions testing `count_words()`:
      1. Empty string "" should return 0.
      2. Single word "Python" should return 1.
      3. Multiple words "AI agents write code" should return 4.
      4. String with irregular whitespace "  hello   world  " should return 2.

    # TODO: Implement the four assertions.
    """
    # TODO: Replace the line below with your 4 assertions
    raise NotImplementedError("Level 1: Implement test_count_words_suite().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def safe_divide(numerator: float, denominator: float) -> float:
    """Helper function under test for Level 2."""
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    return numerator / denominator

def test_safe_divide_unbroken() -> None:
    """
    Modify / Adapt Exercise:
    The following test is broken because it contains two severe anti-patterns:
      1. A vacuous assertion that always evaluates to True (`or True`).
      2. An exception test that catches ZeroDivisionError but lacks `assert False`,
         meaning it passes even if no exception is raised!

    Original broken code:
        def test_broken():
            res = safe_divide(10, 2)
            assert res == 5 or True  # BUG: Vacuous assertion!

            try:
                safe_divide(5, 0)
                # BUG: If safe_divide doesn't raise, test still passes!
            except ZeroDivisionError:
                pass

    # TODO: Re-write test_safe_divide_unbroken() so that:
    #   1. It strictly asserts safe_divide(10, 2) == 5.0 without vacuous shortcuts.
    #   2. It strictly verifies safe_divide(5, 0) raises ZeroDivisionError using assert False.
    """
    # TODO: Implement the corrected test function
    raise NotImplementedError("Level 2: Implement test_safe_divide_unbroken().")


# =====================================================================
# Level 3: Build
# =====================================================================
class LifoStack:
    """The component under test for Level 3."""
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
    """
    Build Exercise:
    Write a comprehensive test suite that validates `LifoStack`:
      1. New stack is empty: is_empty() is True, len() is 0.
      2. Push items: push("a"), push("b") -> len() is 2, is_empty() is False.
      3. Peek item: peek() returns "b", but does not remove it (len remains 2).
      4. Pop items: pop() returns "b", then next pop() returns "a" (LIFO order).
      5. Exception on empty pop: Calling pop() on an empty stack raises IndexError.
      6. Exception on empty peek: Calling peek() on an empty stack raises IndexError.

    # TODO: Implement all 6 verification checks using assertions.
    """
    # TODO: Replace the line below with the complete stack test suite
    raise NotImplementedError("Level 3: Implement test_lifo_stack_complete_suite().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def normalize_agent_probabilities(weights: List[float]) -> List[float]:
    """Helper function under test for Level 4."""
    total = sum(weights)
    if total <= 0:
        raise ValueError("Sum of weights must be positive")
    return [round(w / total, 4) for w in weights]


def test_normalize_agent_probabilities_robust() -> None:
    """
    Debug Exercise:
    The test author wrote the following flawed test case:

    Buggy test:
        def test_flawed():
            probs = normalize_agent_probabilities([1.0, 1.0, 1.0])
            # Flaw 1: Checks exact sum to 1.0 using float equality without rounding tolerance
            # Flaw 2: Assumes output length is 4 instead of 3
            # Flaw 3: Does not test that weights with sum <= 0 raise ValueError
            assert sum(probs) == 1.0 and len(probs) == 4

    # TODO: Write a robust, bug-free test function that:
      1. Tests [1.0, 1.0, 1.0] and asserts len(probs) == 3.
      2. Asserts that each probability is approximately 0.3333.
      3. Asserts that sum of probabilities is within 0.001 of 1.0.
      4. Asserts that passing [-1.0, 0.5] or [0.0, 0.0] raises ValueError.
    """
    # TODO: Implement robust test
    raise NotImplementedError("Level 4: Implement test_normalize_agent_probabilities_robust().")


if __name__ == "__main__":
    print("Module 21 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
