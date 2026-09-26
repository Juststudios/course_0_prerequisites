"""
Module 14: Functional Programming in Python — Exercises
========================================================
Complete each of the four levels below to master first-class functions,
pure functions, higher-order functions, and functional pipelines.
"""

from functools import partial, reduce
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def filter_and_transform_tokens(tokens: List[str], min_length: int) -> List[str]:
    """
    Recall Exercise:
    Given a list of raw token strings and a minimum character length:
    1. Filter out all tokens whose length is strictly less than `min_length`.
    2. Transform all remaining tokens to lowercase.
    3. Return the new list of transformed tokens.
    (Do NOT mutate the input list).

    # TODO: Implement using map/filter or a list comprehension.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement filter_and_transform_tokens().")


def recall_pure_function_rule() -> Dict[str, bool]:
    """
    Recall Exercise:
    Return a dictionary answering whether each behavior violates the definition of a pure function:
      - "mutates_global_variable": True (violates) or False (does not violate)
      - "deterministic_output": True or False (does it violate purity?)
      - "prints_to_terminal": True or False (does side-effect I/O violate purity?)

    # TODO: Return {"mutates_global_variable": ..., "deterministic_output": ..., "prints_to_terminal": ...}
    """
    # TODO: Replace the line below with your answer
    raise NotImplementedError("Level 1: Answer pure function rules dictionary.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def create_agent_prompt_styler(prefix: str, suffix: str) -> Callable[[str], str]:
    """
    Modify / Higher-Order Factory Exercise:
    Create and return a function that formats an incoming message prompt.
    The returned function should accept a single `message: str` argument and return:
        f"{prefix} {message.strip()} {suffix}"

    Use `functools.partial` or a closure to achieve this.

    # TODO: Implement create_agent_prompt_styler returning the specialized formatter callable.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement create_agent_prompt_styler().")


def normalize_sensor_readings(
    readings: List[float],
    min_threshold: float,
    max_threshold: float
) -> List[float]:
    """
    Modify Exercise:
    Given a list of raw sensor float readings:
    1. Discard any readings strictly outside the valid range [min_threshold, max_threshold].
    2. For valid readings, scale each value into [0.0, 1.0] using formula:
           (val - min_threshold) / (max_threshold - min_threshold)
       (Assume max_threshold > min_threshold).
    3. Return the resulting list of scaled floats (rounded to 4 decimal places).

    # TODO: Implement normalize_sensor_readings immutably.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement normalize_sensor_readings().")


# =====================================================================
# Level 3: Build
# =====================================================================
def compose_pipeline(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Build Exercise:
    Implement a function composition pipeline utility `compose_pipeline`.
    It takes an arbitrary number of single-argument functions: f1, f2, f3...
    and returns a single callable `pipeline(initial_value)` that passes the data
    sequentially left-to-right through each function:
        result = f3(f2(f1(initial_value)))

    If no functions are passed, the pipeline should simply return the initial value unchanged.
    Use `functools.reduce` to perform the sequential folding.

    # TODO: Implement compose_pipeline using reduce.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement compose_pipeline() using functools.reduce.")


# =====================================================================
# Level 4: Debug
# =====================================================================
def sanitize_agent_telemetry(
    logs: List[Dict[str, Any]],
    blocked_roles: List[str]
) -> List[Dict[str, Any]]:
    """
    Debugging Exercise:
    An AI agent processes telemetry dictionaries before saving them to disk.
    Requirements:
      1. Exclude logs whose "role" is in `blocked_roles`.
      2. Mask any log's "content" string by replacing occurrences of "password=..." with "password=***".
      3. CRITICAL: The function MUST NOT mutate the input `logs` list or the original dictionaries!
         It must return a brand new list containing new dictionary copies.

    The buggy implementation below violates functional immutability:
        # BUG: It mutates the caller's dictionaries in-place!
        # BUG: It modifies the list during iteration, dropping items!
        for item in logs:
            if item["role"] in blocked_roles:
                logs.remove(item)  # BUG: mutates input list during iteration
            else:
                item["content"] = item["content"].replace("password=secret", "password=***") # BUG: mutates dict
        return logs

    # TODO: Fix the bugs by implementing a pure functional transformation that returns
    # fresh dictionary copies without mutating the inputs.
    """
    # TODO: Replace the line below with your pure bug-free implementation
    raise NotImplementedError("Level 4: Fix bugs in sanitize_agent_telemetry().")


if __name__ == "__main__":
    print("Module 14 Exercises loaded successfully.")
    print("To test your solutions, implement the functions above or run solutions.py.")
