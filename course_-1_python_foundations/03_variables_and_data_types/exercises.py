"""
Module 03: Variables and Data Types — Exercises
================================================
Complete each of the four levels below.
Each level exercises your understanding of primitive data types, type casting,
truthiness, and memory reference behavior.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def classify_primitive_types() -> Dict[str, str]:
    """
    Recall Exercise:
    Return a dictionary mapping each expression key to its exact type name
    as returned by `type(expr).__name__` (e.g., "int", "float", "str", "bool", "NoneType").

    Keys to classify:
        - "expr_int": result of `42`
        - "expr_float": result of `3.14159`
        - "expr_str": result of `"Agent 007"`
        - "expr_bool": result of `True`
        - "expr_none": result of `None`
        - "expr_truthy_zero": result of `bool(0)` (return the type name of bool(0), not its value)
        - "expr_cast_int": result of `int("99")`

    # TODO: Return the dictionary with correct type names for each key.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement classify_primitive_types() returning type name strings.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def sanitize_agent_config(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modify Exercise:
    Given a dictionary containing raw configuration parameters from an external API,
    sanitize and coerce values into strict Python types according to these rules:

    1. "agent_name": Ensure it is a non-empty string. If missing or falsy, set to "DefaultAgent".
       If it is a string with leading/trailing whitespace, strip it.
    2. "timeout": Convert to integer `int`. If conversion fails or value is <= 0, set to default 30.
    3. "temperature": Convert to `float`. Clamp the value so it is strictly between 0.0 and 1.0
       (if < 0.0 set to 0.0; if > 1.0 set to 1.0). If conversion fails, default to 0.7.
    4. "active": Convert to boolean `bool` using Python truthiness rules.
    5. "last_error": Always initialize to `None`.

    Returns a new cleaned dictionary with keys:
        {"agent_name": str, "timeout": int, "temperature": float, "active": bool, "last_error": None}

    # TODO: Implement sanitization and type coercion logic.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement sanitize_agent_config() with proper coercion.")


# =====================================================================
# Level 3: Build
# =====================================================================
def coerce_and_validate_payload(
    schema: Dict[str, type],
    data: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any]]:
    """
    Build Exercise:
    Build a type validation and coercion engine for AI tool payloads.

    Arguments:
        schema: A mapping of expected field names to target types (e.g. {"id": int, "rate": float, "flag": bool})
        data: A dictionary containing raw input data to validate and cast.

    Behavior:
        1. Check if all required keys in `schema` exist in `data`. If any key is missing,
           return (False, {}).
        2. For each key in `schema`, attempt to cast `data[key]` to the target type `schema[key]`:
           - If target type is `bool`:
             Special rule: If the input is the string "false", "0", or "no" (case-insensitive),
             cast to False. If "true", "1", or "yes", cast to True.
             Otherwise use standard bool(val).
           - For other target types (`int`, `float`, `str`):
             Call target_type(data[key]).
           - If any casting raises `(ValueError, TypeError)`, the payload is invalid;
             return (False, {}).
        3. If all fields are successfully coerced, return (True, coerced_dict).

    # TODO: Build the complete coercion and validation engine.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement coerce_and_validate_payload().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def calculate_normalized_metrics(scores: List[Any], baseline: Any) -> Dict[str, float]:
    """
    Debug Exercise:
    Calculates summary metrics normalized against a baseline:
    Each score should be divided by the baseline value.
    The returned dictionary must contain:
        {"mean": float, "min": float, "max": float}

    Buggy implementation details:
    - Input scores may contain strings (e.g. ["80", 90.0, 70]) or mixed types.
    - Baseline may be given as a string or float/int.
    - Baseline might be zero, which would cause ZeroDivisionError.
      If float(baseline) == 0.0, raise a ValueError("Baseline cannot be zero").
    - If scores list is empty, raise a ValueError("Scores list cannot be empty").
    - The buggy code below fails on string types and raises uncaught exceptions.

    # TODO: Fix the bugs and ensure all calculations produce exact floats.
    """
    # BUGGY CODE:
    # if baseline is 0:
    #     raise ValueError("Baseline cannot be zero")
    # norm_scores = [s / baseline for s in scores]
    # return {"mean": sum(norm_scores) / len(norm_scores), "min": min(norm_scores), "max": max(norm_scores)}

    # TODO: Replace the line below with your fixed implementation
    raise NotImplementedError("Level 4: Fix calculate_normalized_metrics().")


if __name__ == "__main__":
    print("Module 03 Exercises loaded successfully.")
    print("Implement the functions above or run solutions.py to verify.")
