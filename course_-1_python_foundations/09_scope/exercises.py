"""
Module 09 Exercises: Scope, Lifetimes, and Closures
===================================================

Complete the exercises below across the four progressive tiers:
  Level 1: Recall  — Basic closure creation and the LEGB lookup sequence
  Level 2: Modify  — Refactoring problematic global state into clean enclosing scopes
  Level 3: Build   — Constructing a stateful token-bucket rate limiter closure
  Level 4: Debug   — Diagnosing UnboundLocalError and the classic late-binding loop capture trap

Run your implementations against `solutions.py` to confirm correctness.
"""

from typing import Any, Callable, Dict, List, Tuple


# ==============================================================================
# Level 1: Recall
# ==============================================================================

def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """
    Create and return a closure function `increment() -> int`.
    
    Each time `increment()` is called, it should increase its internal
    counter by `step` and return the new value.
    The first call should return `start + step`.

    Example:
        c = make_counter(start=10, step=2)
        c() -> 12
        c() -> 14
    """
    # TODO: Implement closure using nonlocal
    raise NotImplementedError("Exercise 1.1: make_counter not implemented yet.")


def make_prefixer(prefix: str) -> Callable[[str], str]:
    """
    Create and return a closure function `add_prefix(text: str) -> str`.
    The returned function prepends `prefix + ": "` to `text`.

    Example:
        log_err = make_prefixer("ERROR")
        log_err("Database timed out") -> "ERROR: Database timed out"
    """
    # TODO: Implement prefixer closure
    raise NotImplementedError("Exercise 1.2: make_prefixer not implemented yet.")


# ==============================================================================
# Level 2: Modify
# ==============================================================================

def refactor_global_logger() -> Tuple[Callable[[str], None], Callable[[], List[str]]]:
    """
    Refactor an anti-pattern global logger into an encapsulated closure.

    Return a 2-tuple of functions: `(log_message, get_logs)`
      - `log_message(msg: str) -> None`: appends msg to an internal list.
      - `get_logs() -> List[str]`: returns a COPY of the logged messages list.

    Crucially: Multiple calls to `refactor_global_logger()` must return independent,
    isolated loggers that do NOT share state!
    """
    # TODO: Implement encapsulated logger closure
    raise NotImplementedError("Exercise 2: refactor_global_logger not implemented yet.")


# ==============================================================================
# Level 3: Build
# ==============================================================================

def make_token_bucket(capacity: int) -> Callable[[int], bool]:
    """
    Build a stateful token-bucket closure for an AI agent's request rate limiter.

    The bucket begins full with `capacity` tokens.
    The returned function `consume(tokens: int) -> bool`:
      - If `tokens <= current_tokens`:
          Deducts `tokens` from `current_tokens` and returns True.
      - If `tokens > current_tokens`:
          Leaves `current_tokens` unchanged and returns False.
      - If `tokens <= 0`:
          Raises ValueError("Requested tokens must be positive").

    Example:
        limiter = make_token_bucket(100)
        limiter(30) -> True  (70 remaining)
        limiter(80) -> False (still 70 remaining)
        limiter(70) -> True  (0 remaining)
    """
    # TODO: Build token bucket rate limiter using closures and nonlocal
    raise NotImplementedError("Exercise 3: make_token_bucket not implemented yet.")


# ==============================================================================
# Level 4: Debug
# ==============================================================================

def buggy_running_average() -> Callable[[float], float]:
    """
    BUGGED FUNCTION:
    Intended behavior:
      Return a closure `add_value(val: float) -> float` that computes the cumulative
      moving average of all numbers passed to it so far.

    Current buggy implementation raises UnboundLocalError or fails to maintain state!
    """
    # --- BUGGED CODE BELOW (Modify to fix) ---
    # count = 0
    # total = 0.0
    # def add_value(val: float) -> float:
    #     count += 1        # <-- UnboundLocalError without nonlocal!
    #     total += val
    #     return total / count
    # return add_value
    # TODO: Fix UnboundLocalError using nonlocal and return functioning closure
    raise NotImplementedError("Exercise 4.1: buggy_running_average needs debugging.")


def buggy_closure_multipliers(n: int) -> List[Callable[[int], int]]:
    """
    BUGGED FUNCTION:
    Intended behavior:
      Return a list of `n` functions where the i-th function (0 <= i < n)
      multiplies its input by `i`.

    Current buggy code:
      `return [lambda x: x * i for i in range(n)]`
      Because Python closures bind late, all lambdas reference the final value
      of `i` (which is `n - 1`), so every function multiplies by `n - 1`!

    Fix this so that the i-th function properly captures its own index `i`.
    """
    # --- BUGGED CODE BELOW (Modify to fix) ---
    # return [lambda x: x * i for i in range(n)]
    # TODO: Fix late-binding closure bug (e.g. using default argument capture `lambda x, i=i: ...`)
    raise NotImplementedError("Exercise 4.2: buggy_closure_multipliers needs debugging.")
