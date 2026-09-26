"""
Module 18: Iterators — Exercises
=================================

Practice the Iterator Protocol, custom iterator classes, and itertools.
Complete the four progressive exercise levels below.
"""

from typing import Any, Iterable, Iterator, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def trace_iterator_sequence() -> List[Any]:
    """
    Recall Exercise:
    Predict the exact sequence of return values from the following operations:

        data = [10, 20, 30]
        it = iter(data)
        v1 = next(it)
        v2 = next(it)
        v3 = next(it)
        v4 = next(it, -1)
        v5 = next(it, "STOP")

    # TODO: Return a list containing [v1, v2, v3, v4, v5].
    """
    # TODO: Replace the line below with your answer
    raise NotImplementedError("Level 1: Implement trace_iterator_sequence() with the 5 retrieved values.")


# =====================================================================
# Level 2: Modify
# =====================================================================
class BoundedTake:
    """
    Modify / Adapt Exercise:
    Implement an iterator class that wraps an arbitrary iterable and produces
    at most `limit` items from it.

    Requirements:
    - Must implement both `__iter__()` and `__next__()` following the Iterator Protocol.
    - If `limit <= 0`, it should immediately raise `StopIteration` on the first `next()`.
    - If the underlying iterable has fewer than `limit` items, it terminates cleanly
      when the underlying iterable is exhausted.

    Example:
        list(BoundedTake([1, 2, 3, 4, 5], limit=3)) -> [1, 2, 3]
        list(BoundedTake([10, 20], limit=5)) -> [10, 20]
    """
    def __init__(self, iterable: Iterable[Any], limit: int):
        self.iterator = iter(iterable)
        self.limit = max(0, limit)
        self.count = 0

    def __iter__(self) -> "BoundedTake":
        # TODO: Implement __iter__
        raise NotImplementedError("Level 2: Implement __iter__() on BoundedTake.")

    def __next__(self) -> Any:
        # TODO: Implement __next__ respecting self.limit and StopIteration
        raise NotImplementedError("Level 2: Implement __next__() on BoundedTake.")


# =====================================================================
# Level 3: Build
# =====================================================================
class Interleave:
    """
    Build Exercise:
    Build an iterator class that takes two iterables (`iterable_a` and `iterable_b`)
    and yields elements from them alternately: a0, b0, a1, b1, a2, b2, ...

    If one iterable is shorter than the other, the remaining elements of the
    longer iterable should continue to be yielded until both are completely exhausted.

    Requirements:
    - Must implement `__iter__()` returning `self`.
    - Must implement `__next__()` advancing between the two streams.
    - Once both underlying iterators are exhausted, raise `StopIteration`.

    Example:
        list(Interleave([1, 2, 3], ["a", "b"])) -> [1, "a", 2, "b", 3]
    """
    def __init__(self, iterable_a: Iterable[Any], iterable_b: Iterable[Any]):
        self.it_a = iter(iterable_a)
        self.it_b = iter(iterable_b)
        self.turn_a = True

    def __iter__(self) -> "Interleave":
        # TODO: Implement __iter__
        raise NotImplementedError("Level 3: Implement __iter__() on Interleave.")

    def __next__(self) -> Any:
        # TODO: Implement alternating retrieval logic in __next__()
        raise NotImplementedError("Level 3: Implement __next__() on Interleave.")


# =====================================================================
# Level 4: Debug
# =====================================================================
class AgentMemoryStream:
    """
    Debug Exercise:
    The following class represents an AI Agent's memory stream iterator.
    It is intended to wrap a list of memory events and yield each event formatted as:
        "EVENT #{index}: {content}"

    However, the buggy implementation below suffers from multiple critical bugs:
      1. It forgets to implement `__iter__()` returning `self`, breaking the Iterator Protocol.
      2. It forgets to increment its cursor, leading to an infinite loop.
      3. It does not raise `StopIteration` when the index exceeds the list length.

    Buggy implementation:
        class AgentMemoryStream:
            def __init__(self, events: List[str]):
                self.events = events
                self.cursor = 0

            def __next__(self) -> str:
                if self.cursor >= len(self.events):
                    return None  # BUG: Returns None instead of raising StopIteration
                item = f"EVENT #{self.cursor}: {self.events[self.cursor]}"
                # BUG: Forgot to increment self.cursor!
                return item

    # TODO: Fix all bugs so that AgentMemoryStream complies fully with the Iterator Protocol.
    """
    def __init__(self, events: List[str]):
        self.events = list(events)
        self.cursor = 0

    def __iter__(self) -> "AgentMemoryStream":
        # TODO: Fix and implement __iter__
        raise NotImplementedError("Level 4: Fix __iter__ in AgentMemoryStream.")

    def __next__(self) -> str:
        # TODO: Fix and implement __next__
        raise NotImplementedError("Level 4: Fix __next__ in AgentMemoryStream.")


if __name__ == "__main__":
    print("Module 18 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
