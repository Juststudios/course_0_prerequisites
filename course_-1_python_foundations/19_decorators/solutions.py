"""
Module 19: Decorators — Reference Solutions
============================================

Complete, verified reference solutions for all four exercise tiers.
"""

import functools
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def trace_decorator_output() -> List[str]:
    """
    Tracing definition and execution:
      1. Definition time: @dec_b wraps first (inner), then @dec_a wraps outer.
         So definition inner decorator is "dec_b".
      2. Execution time: dec_a's wrapper executes first (outer), which calls dec_b's wrapper.
         So execution outer decorator is "dec_a".
      3. Returned string:
         dec_b wrapper produces: "[B HELLO B]"
         dec_a wrapper wraps that: "[A [B HELLO B] A]"
    """
    return ["dec_b", "dec_a", "[A [B HELLO B] A]"]


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def validate_positive(func: Callable) -> Callable:
    """
    Decorator that checks all numeric arguments are strictly > 0.
    Preserves original function identity via @functools.wraps.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, (int, float)) and not isinstance(arg, bool):
                if arg <= 0:
                    raise ValueError(f"Argument {arg} must be positive")
        return func(*args, **kwargs)
    return wrapper


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def memoize_with_stats(func: Callable) -> Callable:
    """
    Caching decorator with cache hits/misses tracking.
    """
    cache: Dict[Tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args):
        # args is a tuple, which is hashable if all elements are hashable
        if args in cache:
            wrapper.hits += 1
            return cache[args]
        else:
            wrapper.misses += 1
            result = func(*args)
            cache[args] = result
            return result

    # Initialize stats attributes on wrapper
    wrapper.hits = 0
    wrapper.misses = 0
    return wrapper


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def agent_retry(max_retries: int = 3, fallback: Any = "FAILED"):
    """
    Corrected parameterized decorator factory:
      - Uses @functools.wraps(func) to preserve metadata
      - Catches Exception inside attempt loop
      - Retries up to max_retries times
      - Returns fallback value if all retries fail
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_retries:
                        return fallback
            return fallback
        return wrapper
    return decorator


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    t_res = trace_decorator_output()
    assert t_res == ["dec_b", "dec_a", "[A [B HELLO B] A]"], f"Level 1 failed: {t_res}"

    # Test Level 2
    @validate_positive
    def multiply_dimensions(length: float, width: float) -> float:
        """Calculates area."""
        return length * width

    assert multiply_dimensions.__name__ == "multiply_dimensions"
    assert multiply_dimensions.__doc__ == "Calculates area."
    assert multiply_dimensions(5, 10) == 50.0

    try:
        multiply_dimensions(5, -2)
        assert False, "Should have raised ValueError for -2"
    except ValueError as e:
        assert "Argument -2 must be positive" in str(e)

    # Test Level 3
    @memoize_with_stats
    def compute_heavy_hash(n: int) -> int:
        return n * 42

    assert compute_heavy_hash.hits == 0
    assert compute_heavy_hash.misses == 0

    res1 = compute_heavy_hash(10)
    assert res1 == 420
    assert compute_heavy_hash.misses == 1
    assert compute_heavy_hash.hits == 0

    res2 = compute_heavy_hash(10)
    assert res2 == 420
    assert compute_heavy_hash.misses == 1
    assert compute_heavy_hash.hits == 1

    res3 = compute_heavy_hash(20)
    assert res3 == 840
    assert compute_heavy_hash.misses == 2
    assert compute_heavy_hash.hits == 1

    # Test Level 4
    call_counts = {"count": 0}

    @agent_retry(max_retries=3, fallback="RECOVERY_FALLBACK")
    def flaky_agent_call():
        """Simulated unreliable API."""
        call_counts["count"] += 1
        raise ConnectionError("Network dropped")

    assert flaky_agent_call.__name__ == "flaky_agent_call"
    fallback_res = flaky_agent_call()
    assert fallback_res == "RECOVERY_FALLBACK", f"Level 4 fallback failed: {fallback_res}"
    assert call_counts["count"] == 3, f"Expected 3 retries, got {call_counts['count']}"

    # Verify success on intermediate attempt
    success_tracker = {"tries": 0}

    @agent_retry(max_retries=3, fallback="FAILED")
    def eventually_succeeds():
        success_tracker["tries"] += 1
        if success_tracker["tries"] < 2:
            raise TimeoutError("Temporary timeout")
        return "SUCCESS_DATA"

    res_success = eventually_succeeds()
    assert res_success == "SUCCESS_DATA"
    assert success_tracker["tries"] == 2

    print("Module 19: All Level 1-4 solutions verified successfully!")
