"""Module 14 Exercises"""
# Level 1: What does print(obj) call?  __str__ or __repr__?
# Level 2: TODO — add __str__ to this class so print(p) shows "Point(3, 4)"
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    # TODO: add __str__

# Level 3: TODO — make RateLimiter callable. It should count calls and
# raise RuntimeError after max_calls invocations.
class RateLimiter:
    def __init__(self, max_calls: int):
        raise NotImplementedError

# Level 4: TODO — build a Memoizer class whose __call__ caches results.
