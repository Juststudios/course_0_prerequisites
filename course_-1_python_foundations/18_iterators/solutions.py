"""
Module 18: Iterators — Reference Solutions
===========================================

Complete, verified reference solutions for all four exercise tiers.
"""

from typing import Any, Iterable, Iterator, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def trace_iterator_sequence() -> List[Any]:
    """
    Step-by-step trace:
      v1 = next(it)     -> 10
      v2 = next(it)     -> 20
      v3 = next(it)     -> 30
      v4 = next(it, -1) -> it is exhausted; returns default -1
      v5 = next(it, "STOP") -> it is exhausted; returns default "STOP"
    """
    return [10, 20, 30, -1, "STOP"]


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
class BoundedTake:
    """
    Wraps an iterable and yields at most `limit` items, terminating cleanly
    via StopIteration when the limit is reached or the stream is exhausted.
    """
    def __init__(self, iterable: Iterable[Any], limit: int):
        self.iterator = iter(iterable)
        self.limit = max(0, limit)
        self.count = 0

    def __iter__(self) -> "BoundedTake":
        return self

    def __next__(self) -> Any:
        if self.count >= self.limit:
            raise StopIteration
        val = next(self.iterator)
        self.count += 1
        return val


# =====================================================================
# Level 3: Build Solution
# =====================================================================
class Interleave:
    """
    Alternates yielding items between two iterators until both are exhausted.
    """
    def __init__(self, iterable_a: Iterable[Any], iterable_b: Iterable[Any]):
        self.it_a = iter(iterable_a)
        self.it_b = iter(iterable_b)
        self.exhausted_a = False
        self.exhausted_b = False
        self.turn_a = True

    def __iter__(self) -> "Interleave":
        return self

    def __next__(self) -> Any:
        if self.exhausted_a and self.exhausted_b:
            raise StopIteration

        # Try yielding from stream A if it's A's turn and A is not exhausted
        if self.turn_a:
            self.turn_a = False
            if not self.exhausted_a:
                try:
                    return next(self.it_a)
                except StopIteration:
                    self.exhausted_a = True

            # If A was already exhausted or just became exhausted, try B
            if not self.exhausted_b:
                try:
                    return next(self.it_b)
                except StopIteration:
                    self.exhausted_b = True

            raise StopIteration
        else:
            self.turn_a = True
            if not self.exhausted_b:
                try:
                    return next(self.it_b)
                except StopIteration:
                    self.exhausted_b = True

            # If B was already exhausted or just became exhausted, try A
            if not self.exhausted_a:
                try:
                    return next(self.it_a)
                except StopIteration:
                    self.exhausted_a = True

            raise StopIteration


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
class AgentMemoryStream:
    """
    Corrected AgentMemoryStream adhering strictly to the Iterator Protocol:
      - Implements __iter__() returning self
      - Correctly increments cursor on every step
      - Raises StopIteration when exhausted instead of returning None
    """
    def __init__(self, events: List[str]):
        self.events = list(events)
        self.cursor = 0

    def __iter__(self) -> "AgentMemoryStream":
        return self

    def __next__(self) -> str:
        if self.cursor >= len(self.events):
            raise StopIteration
        item = f"EVENT #{self.cursor}: {self.events[self.cursor]}"
        self.cursor += 1
        return item


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    t_res = trace_iterator_sequence()
    assert t_res == [10, 20, 30, -1, "STOP"], f"Level 1 failed: {t_res}"

    # Test Level 2
    take_3 = list(BoundedTake([1, 2, 3, 4, 5], limit=3))
    assert take_3 == [1, 2, 3], f"Level 2 take 3 failed: {take_3}"

    take_all = list(BoundedTake([10, 20], limit=5))
    assert take_all == [10, 20], f"Level 2 take all failed: {take_all}"

    take_zero = list(BoundedTake([1, 2, 3], limit=0))
    assert take_zero == [], f"Level 2 take zero failed: {take_zero}"

    # Test Level 3
    inter = list(Interleave([1, 2, 3], ["a", "b"]))
    assert inter == [1, "a", 2, "b", 3], f"Level 3 failed: {inter}"

    inter_rev = list(Interleave(["x"], [10, 20, 30]))
    assert inter_rev == ["x", 10, 20, 30], f"Level 3 rev failed: {inter_rev}"

    inter_empty = list(Interleave([], []))
    assert inter_empty == [], f"Level 3 empty failed: {inter_empty}"

    # Test Level 4
    stream = AgentMemoryStream(["User asked question", "Agent searched tool", "Agent replied"])
    stream_output = list(stream)
    assert stream_output == [
        "EVENT #0: User asked question",
        "EVENT #1: Agent searched tool",
        "EVENT #2: Agent replied",
    ], f"Level 4 stream failed: {stream_output}"

    # Verify that stream complies with iter() protocol
    assert iter(stream) is stream, "Level 4 iter(stream) must return self"

    print("Module 18: All Level 1-4 solutions verified successfully!")
