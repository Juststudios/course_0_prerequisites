"""
Module 15: Type Hints and Modern Python Typing — Exercises
===========================================================
Complete each of the four levels below to master type hints, container generics,
Optional/Union types, Callables, and runtime annotation introspection.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# =====================================================================
# Level 1: Recall
# =====================================================================
def format_agent_id(name: str, agent_number: int, is_active: bool) -> str:
    """
    Recall Exercise:
    Implement a function that formats an agent identifier into the string:
        f"AGENT[{name.upper()}#{agent_number:03d}]: ACTIVE" (if is_active is True)
        f"AGENT[{name.upper()}#{agent_number:03d}]: INACTIVE" (if is_active is False)

    # TODO: Implement format_agent_id with full type annotations.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement format_agent_id().")


def introspect_function_return_type(func: Callable[..., Any]) -> Any:
    """
    Recall Exercise:
    Python stores type annotations in the `__annotations__` dictionary attribute.
    Return the type annotation associated with the return value of `func`.
    If no return annotation is present, return None.

    # TODO: Inspect func.__annotations__ for the "return" key.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement introspect_function_return_type().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def extract_valid_responses(raw_responses: List[Optional[str]]) -> List[str]:
    """
    Modify Exercise:
    In an LLM multi-query batch, some queries return a string while failed ones return None.
    Implement a function that takes a list of `Optional[str]` (i.e. `str | None`):
    1. Filters out all `None` entries.
    2. Strips leading and trailing whitespace from each valid string.
    3. Excludes any strings that become empty after stripping.
    4. Returns a clean list of non-empty strings.

    # TODO: Implement extract_valid_responses immutably.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement extract_valid_responses().")


def lookup_agent_tool(
    registry: Dict[str, Callable[[str], str]],
    tool_name: str
) -> Optional[Callable[[str], str]]:
    """
    Modify Exercise:
    Look up a tool callable in an agent tool registry.
    Return the callable if present, or None if the tool does not exist.

    # TODO: Implement lookup_agent_tool with exact typing.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement lookup_agent_tool().")


# =====================================================================
# Level 3: Build
# =====================================================================
def execute_typed_pipeline(
    transforms: List[Callable[[int], int]],
    initial_value: int
) -> Tuple[int, List[int]]:
    """
    Build Exercise:
    Given a list of typed numeric transform functions `Callable[[int], int]`
    and a starting integer `initial_value`:
    1. Sequentially apply each transform to the running value.
    2. Record the intermediate result after each transformation in a history list.
    3. Return a tuple of: (final_value, history_list).
    If `transforms` is empty, return (initial_value, []).

    # TODO: Implement execute_typed_pipeline preserving type contracts.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement execute_typed_pipeline().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def safe_dispatch_callback(
    callback: Optional[Callable[[str], Any]],
    payload: str,
    fallback_value: Any
) -> Any:
    """
    Debugging Exercise:
    An agent orchestrator executes a user-provided completion callback.
    Requirements:
      1. If `callback` is None, immediately return `fallback_value`.
      2. If `callback` is provided, call it with `payload`.
      3. If the callback execution raises ANY exception, catch it and return `fallback_value`.
      4. Otherwise, return the callback's output.

    The buggy implementation below crashes:
        # BUG: Crashes with TypeError: 'NoneType' object is not callable if callback is None
        # BUG: Crashes with unhandled exception if callback fails
        # BUG: Ignores fallback_value
        result = callback(payload)
        return result

    # TODO: Fix the bugs so that safe_dispatch_callback handles None and exceptions safely.
    """
    # TODO: Replace the line below with your bug-free implementation
    raise NotImplementedError("Level 4: Fix bugs in safe_dispatch_callback().")


if __name__ == "__main__":
    print("Module 15 Exercises loaded successfully.")
    print("To test your solutions, implement the functions above or run solutions.py.")
