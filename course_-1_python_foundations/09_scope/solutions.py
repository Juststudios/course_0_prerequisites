"""
Module 09 Solutions: Scope, Lifetimes, and Closures
===================================================

Reference solutions for all progressive exercises in Module 09.
"""

from typing import Any, Callable, Dict, List, Tuple


# ==============================================================================
# Level 1: Recall Solutions
# ==============================================================================

def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Create a stateful counter closure using nonlocal."""
    current = start

    def increment() -> int:
        nonlocal current
        current += step
        return current

    return increment


def make_prefixer(prefix: str) -> Callable[[str], str]:
    """Create a prefixing closure capturing prefix in enclosing scope."""
    def add_prefix(text: str) -> str:
        return f"{prefix}: {text}"

    return add_prefix


# ==============================================================================
# Level 2: Modify Solution
# ==============================================================================

def refactor_global_logger() -> Tuple[Callable[[str], None], Callable[[], List[str]]]:
    """Encapsulate log messages in a private closure scope."""
    messages: List[str] = []

    def log_message(msg: str) -> None:
        messages.append(msg)

    def get_logs() -> List[str]:
        return list(messages)  # Return shallow copy to prevent outside tampering

    return log_message, get_logs


# ==============================================================================
# Level 3: Build Solution
# ==============================================================================

def make_token_bucket(capacity: int) -> Callable[[int], bool]:
    """Construct a stateful token-bucket rate limiter closure."""
    if capacity <= 0:
        raise ValueError("Capacity must be positive")
    
    current_tokens = capacity

    def consume(tokens: int) -> bool:
        nonlocal current_tokens
        if tokens <= 0:
            raise ValueError("Requested tokens must be positive")
        
        if tokens <= current_tokens:
            current_tokens -= tokens
            return True
        return False

    return consume


# ==============================================================================
# Level 4: Debug Solutions
# ==============================================================================

def buggy_running_average() -> Callable[[float], float]:
    """Fixed running average: uses nonlocal to track count and total across calls."""
    count = 0
    total = 0.0

    def add_value(val: float) -> float:
        nonlocal count, total
        count += 1
        total += val
        return total / count

    return add_value


def buggy_closure_multipliers(n: int) -> List[Callable[[int], int]]:
    """Fixed multipliers: uses default argument binding `i=i` to defeat late-binding."""
    return [lambda x, factor=i: x * factor for i in range(n)]


# ==============================================================================
# Verification Self-Test Block
# ==============================================================================

if __name__ == "__main__":
    print("Testing Module 09 Solutions...")

    # Level 1 Tests
    c = make_counter(start=10, step=2)
    assert c() == 12
    assert c() == 14
    assert c() == 16

    c2 = make_counter(start=0, step=5)
    assert c2() == 5
    assert c() == 18  # c is independent of c2!

    pref = make_prefixer("DEBUG")
    assert pref("cache hit") == "DEBUG: cache hit"

    # Level 2 Tests
    log1, get1 = refactor_global_logger()
    log2, get2 = refactor_global_logger()

    log1("First event")
    log1("Second event")
    log2("Other logger event")

    assert get1() == ["First event", "Second event"]
    assert get2() == ["Other logger event"]

    # Verify immutability of returned list
    retrieved = get1()
    retrieved.append("Hacked event")
    assert get1() == ["First event", "Second event"]

    # Level 3 Tests
    bucket = make_token_bucket(100)
    assert bucket(30) is True
    assert bucket(80) is False  # 70 remaining, cannot take 80
    assert bucket(70) is True   # 0 remaining
    assert bucket(1) is False

    try:
        bucket(-5)
        assert False, "Should raise ValueError for non-positive request"
    except ValueError:
        pass

    # Level 4 Tests
    avg_calc = buggy_running_average()
    assert avg_calc(10.0) == 10.0
    assert avg_calc(20.0) == 15.0
    assert avg_calc(30.0) == 20.0

    multipliers = buggy_closure_multipliers(4)
    # Each multiplier should capture its own index
    assert [m(10) for m in multipliers] == [0, 10, 20, 30]

    print("All Module 09 solutions verified successfully!")
