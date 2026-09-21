"""Module 14 Solutions"""
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return f"Point({self.x}, {self.y})"

class RateLimiter:
    def __init__(self, max_calls):
        self.max_calls = max_calls
        self._calls = 0
    def __call__(self, func, *args, **kwargs):
        if self._calls >= self.max_calls:
            raise RuntimeError("Rate limit exceeded")
        self._calls += 1
        return func(*args, **kwargs)

class Memoizer:
    def __init__(self, func):
        self._func = func
        self._cache = {}
    def __call__(self, *args):
        if args not in self._cache:
            self._cache[args] = self._func(*args)
        return self._cache[args]
