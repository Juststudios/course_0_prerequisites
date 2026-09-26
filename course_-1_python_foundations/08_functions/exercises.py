"""
Module 08 Exercises: Functions (Parameters, Return Values, and Functional Abstraction)
======================================================================================

Complete the exercises below across the four progressive tiers:
  Level 1: Recall  — Function signatures, variadic parameters, and keyword-only constraints
  Level 2: Modify  — Eliminating mutable default pitfalls and implementing higher-order callbacks
  Level 3: Build   — Designing an extensible tool dispatcher for an autonomous agent
  Level 4: Debug   — Diagnosing and repairing argument binding and state-leak bugs

Run your implementations against `solutions.py` to confirm correctness.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


# ==============================================================================
# Level 1: Recall
# ==============================================================================

def calculate_bounding_box(*points: Tuple[float, float]) -> Tuple[float, float, float, float]:
    """
    Accept an arbitrary number of 2D coordinates `(x, y)` via `*points`.
    Return a 4-tuple containing `(min_x, max_x, min_y, max_y)`.

    If no points are provided, raise ValueError("At least one point is required").

    Example:
        calculate_bounding_box((1.0, 2.0), (-3.0, 5.0), (4.0, -1.0))
        -> (-3.0, 4.0, -1.0, 5.0)
    """
    # TODO: Implement bounding box calculation using *points
    raise NotImplementedError("Exercise 1.1: calculate_bounding_box not implemented yet.")


def build_tool_config(
    tool_name: str,
    *,
    timeout_seconds: int = 30,
    max_retries: int = 3,
    debug_mode: bool = False
) -> Dict[str, Any]:
    """
    Return a configuration dictionary with keys:
      - 'tool_name': str
      - 'timeout': int (from timeout_seconds)
      - 'max_retries': int
      - 'debug': bool (from debug_mode)

    Notice: timeout_seconds, max_retries, and debug_mode MUST be keyword-only!

    Example:
        build_tool_config("web_search", timeout_seconds=60, debug_mode=True)
        -> {'tool_name': 'web_search', 'timeout': 60, 'max_retries': 3, 'debug': True}
    """
    # TODO: Build and return dictionary
    raise NotImplementedError("Exercise 1.2: build_tool_config not implemented yet.")


# ==============================================================================
# Level 2: Modify
# ==============================================================================

def append_to_agent_memory(
    message: str,
    memory_store: Optional[List[str]] = None
) -> List[str]:
    """
    Modify this function to correctly avoid the Python 'Mutable Default Argument' trap.
    
    If `memory_store` is omitted (None), create a new independent list.
    Append `message` to the memory store and return the list.
    """
    # TODO: Modify implementation to safely handle default argument without leaking state
    raise NotImplementedError("Exercise 2.1: append_to_agent_memory not implemented yet.")


def apply_pipeline(
    values: List[int],
    filter_fn: Callable[[int], bool],
    transform_fn: Callable[[int], int]
) -> List[int]:
    """
    A higher-order function:
      1. Iterate through `values`.
      2. Keep only elements where `filter_fn(element)` returns True.
      3. Apply `transform_fn(element)` to the retained elements.
      4. Return the new transformed list.

    Example:
        apply_pipeline([1, 2, 3, 4, 5], lambda x: x % 2 == 1, lambda x: x * 10)
        -> [10, 30, 50]
    """
    # TODO: Implement higher-order pipeline execution
    raise NotImplementedError("Exercise 2.2: apply_pipeline not implemented yet.")


# ==============================================================================
# Level 3: Build
# ==============================================================================

def create_tool_dispatcher(
    tool_map: Dict[str, Callable[..., Any]]
) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """
    Build and return a closure / dispatcher function `dispatch(tool_name, parameters)`:
    
    Requirements for returned `dispatch(tool_name: str, parameters: Dict[str, Any])`:
      1. If `tool_name` is not in `tool_map`:
         return {"status": "error", "message": f"Tool '{tool_name}' not found"}
      2. If `tool_name` is found, call the tool passing `**parameters`.
         - If execution succeeds:
           return {"status": "success", "result": result}
         - If execution raises an Exception:
           return {"status": "error", "message": str(exception)}

    Example:
        tools = {"add": lambda a, b: a + b}
        dispatcher = create_tool_dispatcher(tools)
        dispatcher("add", {"a": 2, "b": 3}) -> {"status": "success", "result": 5}
        dispatcher("unknown", {}) -> {"status": "error", "message": "Tool 'unknown' not found"}
    """
    # TODO: Build and return dispatcher function
    raise NotImplementedError("Exercise 3: create_tool_dispatcher not implemented yet.")


# ==============================================================================
# Level 4: Debug
# ==============================================================================

def buggy_merge_agent_options(base_options: Dict[str, Any], **custom_kwargs: Any) -> Dict[str, Any]:
    """
    BUGGED FUNCTION:
    Intended behavior:
      Return a NEW dictionary containing all keys from `base_options`, overridden
      or extended by any key-value pairs passed in `custom_kwargs`.
      Crucially: `base_options` MUST NOT be mutated!

    Bug in current code:
      Directly mutates `base_options` via `update()`, corrupting the caller's dictionary!
    """
    # --- BUGGED CODE BELOW (Modify to fix) ---
    # base_options.update(custom_kwargs)  # <-- Mutates original caller dict!
    # return base_options
    # TODO: Fix the bug so base_options is not mutated
    raise NotImplementedError("Exercise 4: buggy_merge_agent_options needs debugging.")
