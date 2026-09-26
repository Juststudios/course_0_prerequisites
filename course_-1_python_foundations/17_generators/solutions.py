"""
Module 17: Generators — Reference Solutions
============================================

Complete, verified reference solutions for all four exercise tiers.
"""

from typing import Iterable, Iterator, Generator, List, Tuple, Any, Dict


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def generator_lifecycle_trace() -> List[int]:
    """
    Tracing step-by-step:
      1. val = 10 -> yield 10 (first = 10)
      2. val += 5 (15) -> yield val * 2 (15 * 2 = 30) (second = 30)
      3. val -= 3 (15 - 3 = 12) -> yield val (12) (third = 12)
    """
    return [10, 30, 12]


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def batch_stream(items: Iterable[Any], batch_size: int) -> Generator[List[Any], None, None]:
    """
    Batches an arbitrary iterable into chunks of size `batch_size`
    without buffering the entire stream into memory.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    current_batch = []
    for item in items:
        current_batch.append(item)
        if len(current_batch) == batch_size:
            yield current_batch
            current_batch = []

    if current_batch:
        yield current_batch


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def sliding_window_tokens(tokens: List[str], window_size: int, step: int) -> Generator[Tuple[str, ...], None, None]:
    """
    Yields consecutive sliding windows of tokens of length `window_size`,
    advancing by `step` each iteration.
    """
    if window_size <= 0 or step <= 0:
        raise ValueError("window_size and step must be positive integers")

    n = len(tokens)
    if window_size > n:
        return

    i = 0
    while i + window_size <= n:
        yield tuple(tokens[i : i + window_size])
        i += step


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def filter_and_format_agent_logs(
    raw_stream: Iterable[Dict[str, Any]],
    target_role: str
) -> Generator[str, None, None]:
    """
    Corrected generator:
    - Uses `yield` instead of accumulating a full list and returning.
    - Uses `.get()` to avoid KeyError on missing fields.
    - Yields formatted strings lazily.
    """
    for item in raw_stream:
        if item.get("role") == target_role:
            role_str = str(item.get("role", "")).upper()
            action_str = str(item.get("action", "unknown"))
            success_str = str(item.get("success", False))
            yield f"[{role_str}]: {action_str} - success={success_str}"


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    trace_res = generator_lifecycle_trace()
    assert trace_res == [10, 30, 12], f"Level 1 failed: {trace_res}"

    # Test Level 2
    data = iter([1, 2, 3, 4, 5, 6, 7])
    batches = list(batch_stream(data, batch_size=3))
    assert batches == [[1, 2, 3], [4, 5, 6], [7]], f"Level 2 failed: {batches}"

    # Test Level 3
    doc = ["Agent", "observes", "environment", "and", "acts"]
    windows = list(sliding_window_tokens(doc, window_size=3, step=2))
    assert windows == [
        ("Agent", "observes", "environment"),
        ("environment", "and", "acts"),
    ], f"Level 3 failed: {windows}"

    empty_windows = list(sliding_window_tokens(["short"], window_size=5, step=1))
    assert empty_windows == [], f"Level 3 empty window failed: {empty_windows}"

    # Test Level 4
    logs = [
        {"role": "planner", "action": "formulate_goals", "success": True},
        {"role": "coder", "action": "write_tests"},  # missing success, defaults False
        {"role": "planner", "action": "review_plan", "success": True},
    ]
    planner_logs = list(filter_and_format_agent_logs(logs, "planner"))
    assert planner_logs == [
        "[PLANNER]: formulate_goals - success=True",
        "[PLANNER]: review_plan - success=True",
    ], f"Level 4 failed: {planner_logs}"

    coder_logs = list(filter_and_format_agent_logs(logs, "coder"))
    assert coder_logs == [
        "[CODER]: write_tests - success=False",
    ], f"Level 4 coder log failed: {coder_logs}"

    print("Module 17: All Level 1-4 solutions verified successfully!")
