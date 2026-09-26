"""
Module 08 Solutions: Functions (Parameters, Return Values, and Functional Abstraction)
======================================================================================

Reference solutions for all progressive exercises in Module 08.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


# ==============================================================================
# Level 1: Recall Solutions
# ==============================================================================

def calculate_bounding_box(*points: Tuple[float, float]) -> Tuple[float, float, float, float]:
    """Calculate (min_x, max_x, min_y, max_y) from arbitrary (x, y) tuples."""
    if not points:
        raise ValueError("At least one point is required")
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def build_tool_config(
    tool_name: str,
    *,
    timeout_seconds: int = 30,
    max_retries: int = 3,
    debug_mode: bool = False
) -> Dict[str, Any]:
    """Return dictionary with keyword-only enforced configuration."""
    return {
        "tool_name": tool_name,
        "timeout": timeout_seconds,
        "max_retries": max_retries,
        "debug": debug_mode
    }


# ==============================================================================
# Level 2: Modify Solutions
# ==============================================================================

def append_to_agent_memory(
    message: str,
    memory_store: Optional[List[str]] = None
) -> List[str]:
    """Safely append without mutable default state leakage."""
    if memory_store is None:
        memory_store = []
    memory_store.append(message)
    return memory_store


def apply_pipeline(
    values: List[int],
    filter_fn: Callable[[int], bool],
    transform_fn: Callable[[int], int]
) -> List[int]:
    """Filter and transform values using provided callbacks."""
    return [transform_fn(x) for x in values if filter_fn(x)]


# ==============================================================================
# Level 3: Build Solution
# ==============================================================================

def create_tool_dispatcher(
    tool_map: Dict[str, Callable[..., Any]]
) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """Build a closure that safely dispatches tool invocations."""
    def dispatch(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in tool_map:
            return {"status": "error", "message": f"Tool '{tool_name}' not found"}
        
        func = tool_map[tool_name]
        try:
            res = func(**parameters)
            return {"status": "success", "result": res}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}
            
    return dispatch


# ==============================================================================
# Level 4: Debug Solution
# ==============================================================================

def buggy_merge_agent_options(base_options: Dict[str, Any], **custom_kwargs: Any) -> Dict[str, Any]:
    """Fixed merge: creates a new dictionary copy rather than mutating base_options."""
    merged = dict(base_options)
    merged.update(custom_kwargs)
    return merged


# ==============================================================================
# Verification Self-Test Block
# ==============================================================================

if __name__ == "__main__":
    print("Testing Module 08 Solutions...")

    # Level 1 Tests
    bbox = calculate_bounding_box((1.0, 2.0), (-3.0, 5.0), (4.0, -1.0))
    assert bbox == (-3.0, 4.0, -1.0, 5.0)

    try:
        calculate_bounding_box()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    cfg = build_tool_config("search", timeout_seconds=45, debug_mode=True)
    assert cfg == {"tool_name": "search", "timeout": 45, "max_retries": 3, "debug": True}

    # Level 2 Tests
    mem1 = append_to_agent_memory("hello")
    mem2 = append_to_agent_memory("world")
    assert mem1 == ["hello"]
    assert mem2 == ["world"]
    assert mem1 is not mem2

    piped = apply_pipeline([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0, lambda x: x * 10)
    assert piped == [20, 40, 60]

    # Level 3 Tests
    tools = {
        "multiply": lambda a, b: a * b,
        "fail_tool": lambda: 1 / 0
    }
    dispatcher = create_tool_dispatcher(tools)
    r1 = dispatcher("multiply", {"a": 6, "b": 7})
    assert r1 == {"status": "success", "result": 42}

    r2 = dispatcher("unknown", {})
    assert r2["status"] == "error"
    assert "not found" in r2["message"]

    r3 = dispatcher("fail_tool", {})
    assert r3["status"] == "error"
    assert "division by zero" in r3["message"]

    # Level 4 Tests
    original_dict = {"env": "prod", "retries": 2}
    merged_dict = buggy_merge_agent_options(original_dict, retries=5, model="gpt-4o")
    assert original_dict == {"env": "prod", "retries": 2}  # NOT mutated!
    assert merged_dict == {"env": "prod", "retries": 5, "model": "gpt-4o"}

    print("All Module 08 solutions verified successfully!")
