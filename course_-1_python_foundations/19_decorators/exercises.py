"""Module 19 Exercises"""
import functools

# Level 1: What does @timer do to a function?

# Level 2: TODO — fix the decorator so it preserves __name__:
def broken_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling")
        return func(*args, **kwargs)
    return wrapper   # BUG: __name__ is lost

# Level 3: TODO — write a `validate_positive` decorator that raises
# ValueError if any argument is <= 0.
def validate_positive(func):
    raise NotImplementedError

# Level 4: TODO — write a `memoize` decorator that caches function results.
def memoize(func):
    raise NotImplementedError
