"""
Module 17: Generators — Exercises
==================================

Practice lazy evaluation, generator functions, and streaming pipelines.
Complete the four progressive exercise levels below.
"""

from typing import Iterable, Iterator, Generator, List, Tuple, Any, Dict


# =====================================================================
# Level 1: Recall
# =====================================================================
def generator_lifecycle_trace() -> List[int]:
    """
    Recall Exercise:
    Consider the following generator function:

        def my_generator():
            val = 10
            yield val
            val += 5
            yield val * 2
            val -= 3
            yield val

    If someone creates `g = my_generator()` and calls `next(g)` three times:
      first = next(g)
      second = next(g)
      third = next(g)

    # TODO: Trace the execution values and return a list of the three yielded integers:
    #       [first, second, third]
    """
    # TODO: Replace the line below with your trace results
    raise NotImplementedError("Level 1: Implement generator_lifecycle_trace() with the 3 yielded values.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def batch_stream(items: Iterable[Any], batch_size: int) -> Generator[List[Any], None, None]:
    """
    Modify / Adapt Exercise:
    Given an input iterable and a batch size, yield consecutive chunks/batches
    of items as lists.
    The final batch may have fewer than `batch_size` elements if the stream ends.
    Must be lazily evaluated (do NOT convert the entire input `items` into a list upfront!).

    Example:
        list(batch_stream([1, 2, 3, 4, 5], batch_size=2))
        -> [[1, 2], [3, 4], [5]]

    # TODO: Implement the batching generator without buffering the entire input stream.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement batch_stream() generator.")


# =====================================================================
# Level 3: Build
# =====================================================================
def sliding_window_tokens(tokens: List[str], window_size: int, step: int) -> Generator[Tuple[str, ...], None, None]:
    """
    Build Exercise:
    In LLM and AI agent systems, long documents are split into overlapping
    sliding context windows.

    Build a generator that yields tuples of length `window_size`, advancing
    by `step` tokens each time.
    Iteration terminates when a window would extend past the end of `tokens`
    or when no more tokens remain. If `window_size` is larger than `len(tokens)`,
    no windows should be yielded.

    Parameters:
        tokens: List of token strings.
        window_size: Number of tokens per window.
        step: Offset to advance for the next window (e.g. step=1 for full overlap,
              step=window_size for non-overlapping).

    Example:
        tokens = ["Agent", "observes", "environment", "and", "acts"]
        list(sliding_window_tokens(tokens, window_size=3, step=2))
        -> [("Agent", "observes", "environment"), ("environment", "and", "acts")]

    # TODO: Build sliding_window_tokens() as a generator function.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement sliding_window_tokens() generator.")


# =====================================================================
# Level 4: Debug
# =====================================================================
def filter_and_format_agent_logs(
    raw_stream: Iterable[Dict[str, Any]],
    target_role: str
) -> Generator[str, None, None]:
    """
    Debug Exercise:
    An agent log pipeline is supposed to filter log records by `role`
    (e.g., 'planner', 'coder', 'auditor') and format them as:
        "[{role.upper()}]: {action} - success={success}"

    However, the buggy implementation below contains critical bugs:
      1. It tries to return a list instead of yielding each formatted string.
      2. It crashes with KeyError if a record is missing the 'success' key (default should be False).
      3. It consumes the generator incorrectly.

    Buggy code:
        # BUG: uses return instead of yield, misses default keys
        formatted = []
        for item in raw_stream:
            if item["role"] == target_role:
                formatted.append(f"[{item['role'].upper()}]: {item['action']} - success={item['success']}")
        return formatted

    # TODO: Fix the bugs so that this function is a genuine generator yielding
    # formatted strings lazily.
    """
    # TODO: Fix the implementation to yield properly
    raise NotImplementedError("Level 4: Fix bugs in filter_and_format_agent_logs().")


if __name__ == "__main__":
    print("Module 17 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
