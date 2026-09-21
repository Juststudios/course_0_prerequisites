"""Module 17 Exercises"""

# Level 1: What does this print?
it = iter(range(3))
print(next(it), next(it))

# Level 2: TODO — fix the bug (StopIteration crashes the program)
it2 = iter([1, 2])
# print(next(it2), next(it2), next(it2))   # crashes

# Level 3: TODO — implement a `Take` class that wraps an iterable
# and only yields the first n items.
class Take:
    def __init__(self, iterable, n: int):
        raise NotImplementedError

# Level 4: TODO — write a function `interleave(a, b)` that yields
# elements from two lists alternately: [a0, b0, a1, b1, ...]
def interleave(a, b):
    raise NotImplementedError
