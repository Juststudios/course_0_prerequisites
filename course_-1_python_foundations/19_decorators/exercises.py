"""
Module 19: Decorators — Exercises
==================================

Practice function closures, the @ syntax, functools.wraps, and parameterized decorators.
Complete the four progressive exercise levels below.
"""

import functools
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def trace_decorator_output() -> List[str]:
    """
    Recall Exercise:
    Consider the following decorators and decorated function:

        def dec_a(func):
            def wrapper():
                return f"[A {func()} A]"
            return wrapper

        def dec_b(func):
            def wrapper():
                return f"[B {func()} B]"
            return wrapper

        @dec_a
        @dec_b
        def greet():
            return "HELLO"

    When `greet()` is called:
    1. Which decorator wraps first during definition? ("dec_b" or "dec_a")
    2. Which wrapper runs first during execution? ("dec_b" or "dec_a")
    3. What is the exact string returned by `greet()`?

    # TODO: Return a list containing [definition_inner_decorator, execution_outer_decorator, returned_string].
    """
    # TODO: Replace the line below with your trace results
    raise NotImplementedError("Level 1: Implement trace_decorator_output().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def validate_positive(func: Callable) -> Callable:
    """
    Modify / Adapt Exercise:
    Implement a decorator `validate_positive` that checks all positional
    and keyword arguments passed to the target function.

    If any argument is an integer or float and is <= 0, raise a `ValueError`
    with the message: f"Argument {val} must be positive".
    Otherwise, execute the function and return its result.

    Requirements:
    - Must preserve original function metadata via `@functools.wraps(func)`.
    - Must support arbitrary `*args` and `**kwargs`.
    """
    # TODO: Implement the validate_positive decorator
    raise NotImplementedError("Level 2: Implement validate_positive decorator.")


# =====================================================================
# Level 3: Build
# =====================================================================
def memoize_with_stats(func: Callable) -> Callable:
    """
    Build Exercise:
    Build a caching decorator that caches the return values of `func`
    based on its positional arguments `args`.

    Requirements:
    - Must preserve original function metadata via `@functools.wraps(func)`.
    - Must store cached values in an internal dictionary.
    - Must attach two attributes to the returned wrapper function:
        `wrapper.hits`: int (number of times a cached result was returned)
        `wrapper.misses`: int (number of times func was actually executed)
    - If `args` is in the cache, increment `hits` and return the cached value.
    - If `args` is not in cache, increment `misses`, compute result, store in cache, and return it.

    Example:
        @memoize_with_stats
        def square(x): return x * x
        square(4)  # miss (misses=1, hits=0)
        square(4)  # hit  (misses=1, hits=1)
    """
    # TODO: Implement memoize_with_stats decorator
    raise NotImplementedError("Level 3: Implement memoize_with_stats decorator.")


# =====================================================================
# Level 4: Debug
# =====================================================================
def agent_retry(max_retries: int = 3, fallback: Any = "FAILED"):
    """
    Debug Exercise:
    The following parameterized decorator is intended to retry a flaky function
    up to `max_retries` times. If all attempts fail, it should return the `fallback` value
    instead of crashing the program.

    However, the buggy code below contains several critical bugs:
      1. It does not use `@functools.wraps`, losing the target function's identity.
      2. It fails to catch exceptions during execution.
      3. It has incorrect nesting and variable references.

    Buggy implementation:
        def agent_retry(max_retries=3, fallback="FAILED"):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    for attempt in range(max_retries):
                        res = func(*args, **kwargs) # BUG: unhandled exception crashes loop!
                        return res
                    return fallback
                return wrapper
            return decorator

    # TODO: Fix all bugs in agent_retry so it properly catches exceptions,
    # preserves metadata, retries up to max_retries, and returns fallback on complete failure.
    """
    # TODO: Replace the line below with your corrected implementation
    raise NotImplementedError("Level 4: Fix bugs in agent_retry decorator factory.")


if __name__ == "__main__":
    print("Module 19 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
