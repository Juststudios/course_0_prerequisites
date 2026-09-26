"""
Module 15: Type Hints and Modern Python Typing — Reference Solutions
=====================================================================
Clean, production-grade solutions for all four exercise tiers.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# =====================================================================
# Level 1: Recall Solutions
# =====================================================================
def format_agent_id(name: str, agent_number: int, is_active: bool) -> str:
    """
    Formats agent identifier string with status.
    """
    status_str = "ACTIVE" if is_active else "INACTIVE"
    return f"AGENT[{name.upper()}#{agent_number:03d}]: {status_str}"


def introspect_function_return_type(func: Callable[..., Any]) -> Any:
    """
    Inspects and returns the 'return' annotation from func.__annotations__.
    """
    annotations = getattr(func, "__annotations__", {})
    return annotations.get("return", None)


# =====================================================================
# Level 2: Modify Solutions
# =====================================================================
def extract_valid_responses(raw_responses: List[Optional[str]]) -> List[str]:
    """
    Filters None and empty strings from raw responses list.
    """
    valid: List[str] = []
    for item in raw_responses:
        if item is not None:
            cleaned = item.strip()
            if cleaned:
                valid.append(cleaned)
    return valid


def lookup_agent_tool(
    registry: Dict[str, Callable[[str], str]],
    tool_name: str
) -> Optional[Callable[[str], str]]:
    """
    Retrieves tool from registry or returns None.
    """
    return registry.get(tool_name, None)


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def execute_typed_pipeline(
    transforms: List[Callable[[int], int]],
    initial_value: int
) -> Tuple[int, List[int]]:
    """
    Sequentially applies integer transforms and returns final value and history.
    """
    history: List[int] = []
    current_val = initial_value

    for fn in transforms:
        current_val = fn(current_val)
        history.append(current_val)

    return (current_val, history)


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def safe_dispatch_callback(
    callback: Optional[Callable[[str], Any]],
    payload: str,
    fallback_value: Any
) -> Any:
    """
    Safely executes callback with exception and None guarding.
    """
    if callback is None:
        return fallback_value

    try:
        return callback(payload)
    except Exception:
        return fallback_value


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    id1 = format_agent_id("hermes", 7, True)
    assert id1 == "AGENT[HERMES#007]: ACTIVE", f"Level 1 active failed: {id1}"
    id2 = format_agent_id("apollo", 42, False)
    assert id2 == "AGENT[APOLLO#042]: INACTIVE", f"Level 1 inactive failed: {id2}"

    def dummy_func(x: int) -> float:
        return float(x)
    ret_type = introspect_function_return_type(dummy_func)
    assert ret_type is float, f"Level 1 return introspection failed: {ret_type}"

    # Test Level 2
    raw = ["  Hello ", None, "", "   ", "Agent World", None]
    extracted = extract_valid_responses(raw)
    assert extracted == ["Hello", "Agent World"], f"Level 2 extraction failed: {extracted}"

    mock_registry: Dict[str, Callable[[str], str]] = {
        "echo": lambda s: s,
        "upper": lambda s: s.upper(),
    }
    tool = lookup_agent_tool(mock_registry, "upper")
    assert tool is not None and tool("test") == "TEST", "Level 2 lookup hit failed"
    missing = lookup_agent_tool(mock_registry, "non_existent")
    assert missing is None, "Level 2 lookup miss failed"

    # Test Level 3
    fns: List[Callable[[int], int]] = [
        lambda x: x + 5,
        lambda x: x * 2,
        lambda x: x - 3,
    ]
    final_val, hist = execute_typed_pipeline(fns, 10)
    # 10 + 5 = 15; 15 * 2 = 30; 30 - 3 = 27
    assert final_val == 27, f"Level 3 final value failed: {final_val}"
    assert hist == [15, 30, 27], f"Level 3 history failed: {hist}"

    empty_final, empty_hist = execute_typed_pipeline([], 100)
    assert empty_final == 100 and empty_hist == [], "Level 3 empty pipeline failed"

    # Test Level 4
    # Case A: callback is None
    res_none = safe_dispatch_callback(None, "data", "FALLBACK")
    assert res_none == "FALLBACK", "Level 4 None callback failed"

    # Case B: callback succeeds
    res_ok = safe_dispatch_callback(lambda s: f"PROCESSED: {s}", "data", "FALLBACK")
    assert res_ok == "PROCESSED: data", "Level 4 success callback failed"

    # Case C: callback crashes
    def failing_cb(s: str) -> str:
        raise RuntimeError("Network failure!")

    res_fail = safe_dispatch_callback(failing_cb, "data", "DEFAULT_SAFE")
    assert res_fail == "DEFAULT_SAFE", "Level 4 exception fallback failed"

    print("Module 15: All Level 1-4 solutions verified successfully!")
