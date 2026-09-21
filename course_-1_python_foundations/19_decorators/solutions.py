"""Module 19 Solutions"""
import functools

def broken_logger(func):
    @functools.wraps(func)   # FIX: add wraps
    def wrapper(*args, **kwargs):
        print("Calling")
        return func(*args, **kwargs)
    return wrapper

def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Expected positive, got {arg}")
        return func(*args, **kwargs)
    return wrapper

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
