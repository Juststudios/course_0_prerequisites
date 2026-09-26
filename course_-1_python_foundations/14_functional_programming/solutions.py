"""
Module 14: Functional Programming in Python — Reference Solutions
==================================================================
Clean, production-grade solutions for all four exercise tiers.
"""

from functools import partial, reduce
import re
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solutions
# =====================================================================
def filter_and_transform_tokens(tokens: List[str], min_length: int) -> List[str]:
    """
    Filters tokens by min_length and transforms to lowercase immutably.
    """
    return [token.lower() for token in tokens if len(token) >= min_length]


def recall_pure_function_rule() -> Dict[str, bool]:
    """
    Answers regarding pure function constraints:
      - Mutating a global variable is a side effect -> True (violates purity).
      - Deterministic output is required -> False (does NOT violate purity).
      - Printing to terminal is an I/O side effect -> True (violates purity).
    """
    return {
        "mutates_global_variable": True,
        "deterministic_output": False,
        "prints_to_terminal": True,
    }


# =====================================================================
# Level 2: Modify Solutions
# =====================================================================
def create_agent_prompt_styler(prefix: str, suffix: str) -> Callable[[str], str]:
    """
    Returns a formatter that wraps a message with prefix and suffix.
    """
    def styler(message: str) -> str:
        return f"{prefix} {message.strip()} {suffix}"
    return styler


def normalize_sensor_readings(
    readings: List[float],
    min_threshold: float,
    max_threshold: float
) -> List[float]:
    """
    Filters readings to [min_threshold, max_threshold] and normalizes to [0.0, 1.0].
    """
    span = max_threshold - min_threshold
    valid_readings = [r for r in readings if min_threshold <= r <= max_threshold]
    return [round((r - min_threshold) / span, 4) for r in valid_readings]


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def compose_pipeline(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Composes functions left-to-right using functools.reduce.
    """
    def pipeline(initial_value: Any) -> Any:
        return reduce(lambda val, fn: fn(val), functions, initial_value)
    return pipeline


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def sanitize_agent_telemetry(
    logs: List[Dict[str, Any]],
    blocked_roles: List[str]
) -> List[Dict[str, Any]]:
    """
    Pure functional transformation: filters blocked roles and masks secrets
    without mutating the input logs or dictionaries.
    """
    blocked_set = set(blocked_roles)
    sanitized: List[Dict[str, Any]] = []

    for item in logs:
        if item.get("role") in blocked_set:
            continue

        raw_content = str(item.get("content", ""))
        # Mask any password=... pattern safely
        masked_content = re.sub(r"password=[^\s;]+", "password=***", raw_content)

        # Create a fresh copy of the dictionary (immutable transformation)
        new_item = {**item, "content": masked_content}
        sanitized.append(new_item)

    return sanitized


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    sample_tokens = ["AI", "AGENT", "Python", "go", "Framework"]
    res1 = filter_and_transform_tokens(sample_tokens, min_length=3)
    assert res1 == ["agent", "python", "framework"], f"Level 1 failed: {res1}"
    assert sample_tokens[0] == "AI", "Level 1 mutated the input list!"

    rules = recall_pure_function_rule()
    assert rules["mutates_global_variable"] is True
    assert rules["deterministic_output"] is False
    assert rules["prints_to_terminal"] is True

    # Test Level 2
    styler = create_agent_prompt_styler(">>>", "<<<")
    formatted = styler("  Analyze system log  ")
    assert formatted == ">>> Analyze system log <<<", f"Level 2 styler failed: {formatted}"

    raw_data = [10.0, 5.0, 50.0, 100.0, 120.0, -5.0]
    # Filter between 0.0 and 100.0, scale
    normed = normalize_sensor_readings(raw_data, 0.0, 100.0)
    assert normed == [0.1, 0.05, 0.5, 1.0], f"Level 2 normalization failed: {normed}"

    # Test Level 3
    fn1 = lambda s: s.strip()
    fn2 = lambda s: s.lower()
    fn3 = lambda s: s.replace(" ", "_")
    pipe = compose_pipeline(fn1, fn2, fn3)
    piped_result = pipe("  Autonomous Agent Runtime  ")
    assert piped_result == "autonomous_agent_runtime", f"Level 3 pipeline failed: {piped_result}"

    empty_pipe = compose_pipeline()
    assert empty_pipe(42) == 42, "Level 3 empty pipeline failed"

    # Test Level 4
    original_logs = [
        {"role": "user", "content": "login with password=secret_pass_123"},
        {"role": "system", "content": "internal heartbeat"},
        {"role": "blocked_bot", "content": "spam spam spam"},
        {"role": "assistant", "content": "access granted with password=admin; done."},
    ]
    # Keep copy to verify immutability
    import copy
    original_copy = copy.deepcopy(original_logs)

    sanitized = sanitize_agent_telemetry(original_logs, blocked_roles=["blocked_bot", "system"])
    assert len(sanitized) == 2, f"Level 4 expected 2 logs, got {len(sanitized)}"
    assert sanitized[0]["content"] == "login with password=***", f"Level 4 masking failed: {sanitized[0]}"
    assert sanitized[1]["content"] == "access granted with password=***; done.", f"Level 4 masking failed: {sanitized[1]}"
    # Verify input was untouched:
    assert original_logs == original_copy, "Level 4 mutated the original input logs!"

    print("Module 14: All Level 1-4 solutions verified successfully!")
