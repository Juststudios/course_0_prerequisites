"""
Module 10 Solutions: Errors and Exceptions in Python
====================================================

Reference solutions for all progressive exercises in Module 10.
Includes complete self-verification test suite under `if __name__ == "__main__":`.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Type


# ==============================================================================
# Level 1: Recall Solutions
# ==============================================================================

def safe_parse_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int, catching ValueError and TypeError."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def validate_positive_budget(amount: Any) -> float:
    """Validate numeric type and strictly positive range."""
    # Note: in Python, bool is a subclass of int, so isinstance(True, int) is True!
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Budget must be numeric")
    if amount <= 0:
        raise ValueError("Budget must be positive")
    return float(amount)


# ==============================================================================
# Level 2: Modify Solutions
# ==============================================================================

def safe_extract_nested_field(payload: Dict[str, Any], path: List[str], fallback: Any = None) -> Any:
    """Traverse nested dictionary using idiomatic EAFP style."""
    current = payload
    try:
        for key in path:
            current = current[key]
        return current
    except (KeyError, TypeError, IndexError):
        return fallback


def compute_operation_ratio(
    total: float,
    count: int,
    audit_log: List[str]
) -> Optional[float]:
    """Execute complete 4-part try/except/else/finally with audit trail."""
    ratio: Optional[float] = None
    try:
        ratio = total / count
    except ZeroDivisionError:
        audit_log.append("Error: Division by zero")
        ratio = None
    else:
        audit_log.append(f"Success: Ratio is {ratio:.2f}")
    finally:
        audit_log.append("Audit record finalized")
    return ratio


# ==============================================================================
# Level 3: Build Solutions
# ==============================================================================

class ToolError(Exception):
    """Base exception for all agent tool errors."""
    def __init__(self, message: str, tool_name: str):
        super().__init__(message)
        self.tool_name = tool_name


class ToolNotFoundError(ToolError):
    """Raised when a requested tool name is not in the registry."""
    pass


class ToolParameterError(ToolError):
    """Raised when the parameters passed to a tool are invalid."""
    pass


class ToolExecutionFailure(ToolError):
    """Raised when the tool execution itself encounters a runtime crash."""
    pass


def execute_agent_tool(
    tool_name: str,
    registry: Dict[str, Callable[..., Any]],
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute an agent tool with defensive exception handling and translation."""
    try:
        if tool_name not in registry:
            raise ToolNotFoundError(f"Unknown tool: {tool_name}", tool_name)

        tool_fn = registry[tool_name]
        try:
            result = tool_fn(**params)
        except TypeError as type_err:
            raise ToolParameterError(f"Bad arguments for {tool_name}", tool_name) from type_err
        except ToolError:
            # Re-raise already specialized ToolError
            raise
        except Exception as generic_err:
            raise ToolExecutionFailure(f"Crash during {tool_name}", tool_name) from generic_err

    except ToolError as tool_err:
        return {
            "status": "error",
            "tool": tool_name,
            "error_type": type(tool_err).__name__,
            "message": str(tool_err)
        }

    return {
        "status": "success",
        "tool": tool_name,
        "result": result
    }


# ==============================================================================
# Level 4: Debug Solution
# ==============================================================================

def execute_with_retry_fixed(
    action_fn: Callable[[], Any],
    max_attempts: int = 3
) -> Any:
    """
    Repaired retry handler:
      - Catches only (ConnectionError, TimeoutError, OSError)
      - Propagates un-retryable errors immediately
      - Avoids return/break inside finally
      - Chains original cause on retry exhaustion
    """
    last_error: Optional[Exception] = None

    for _ in range(max_attempts):
        try:
            return action_fn()
        except (ConnectionError, TimeoutError, OSError) as retryable:
            last_error = retryable

    # If all attempts exhausted
    raise RuntimeError("Max retry attempts exceeded") from last_error


# ==============================================================================
# Self-Verification Test Suite
# ==============================================================================

def run_all_tests() -> None:
    print("Testing Module 10 Solutions...")

    # Level 1 Tests
    assert safe_parse_int("42") == 42
    assert safe_parse_int("not_a_number", default=-1) == -1
    assert safe_parse_int(None, default=10) == 10
    assert safe_parse_int(3.14) == 3

    assert validate_positive_budget(100) == 100.0
    assert validate_positive_budget(50.5) == 50.5
    try:
        validate_positive_budget(-10)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "positive" in str(e)

    try:
        validate_positive_budget("50")
        assert False, "Should have raised TypeError"
    except TypeError as e:
        assert "numeric" in str(e)

    try:
        validate_positive_budget(True)
        assert False, "Bool should have raised TypeError"
    except TypeError:
        pass

    # Level 2 Tests
    sample_tree = {"agent": {"config": {"model": "claude-3-5-sonnet", "temperature": 0.7}}}
    assert safe_extract_nested_field(sample_tree, ["agent", "config", "model"]) == "claude-3-5-sonnet"
    assert safe_extract_nested_field(sample_tree, ["agent", "config", "temperature"]) == 0.7
    assert safe_extract_nested_field(sample_tree, ["agent", "missing"], fallback="default") == "default"
    assert safe_extract_nested_field(sample_tree, ["agent", "config", "model", "child"], fallback="fb") == "fb"

    log_success: List[str] = []
    r_success = compute_operation_ratio(100.0, 4, log_success)
    assert r_success == 25.0
    assert log_success == ["Success: Ratio is 25.00", "Audit record finalized"]

    log_zero: List[str] = []
    r_zero = compute_operation_ratio(50.0, 0, log_zero)
    assert r_zero is None
    assert log_zero == ["Error: Division by zero", "Audit record finalized"]

    # Level 3 Tests
    tools = {
        "add": lambda x, y: x + y,
        "crash": lambda: 1 / 0
    }
    # Success
    res_ok = execute_agent_tool("add", tools, {"x": 10, "y": 20})
    assert res_ok == {"status": "success", "tool": "add", "result": 30}

    # Unknown tool
    res_unknown = execute_agent_tool("multiply", tools, {"x": 2, "y": 3})
    assert res_unknown["status"] == "error"
    assert res_unknown["error_type"] == "ToolNotFoundError"

    # Bad parameter
    res_bad_param = execute_agent_tool("add", tools, {"invalid_arg": 1})
    assert res_bad_param["status"] == "error"
    assert res_bad_param["error_type"] == "ToolParameterError"

    # Runtime crash in tool
    res_crash = execute_agent_tool("crash", tools, {})
    assert res_crash["status"] == "error"
    assert res_crash["error_type"] == "ToolExecutionFailure"

    # Level 4 Tests
    # 1. Un-retryable error must raise immediately
    def raise_value_error():
        raise ValueError("Non-retryable parameter error")

    try:
        execute_with_retry_fixed(raise_value_error, max_attempts=3)
        assert False, "Should have raised ValueError immediately"
    except ValueError as ve:
        assert "Non-retryable" in str(ve)

    # 2. Transient error eventually succeeds
    attempt_count = 0
    def flaky_network():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ConnectionError(f"Temporary outage {attempt_count}")
        return "Success!"

    result = execute_with_retry_fixed(flaky_network, max_attempts=5)
    assert result == "Success!"
    assert attempt_count == 3

    # 3. Exhausted retries raises RuntimeError chained from ConnectionError
    def persistent_failure():
        raise TimeoutError("Endpoint unreachable")

    try:
        execute_with_retry_fixed(persistent_failure, max_attempts=2)
        assert False, "Should have raised RuntimeError on exhausted retries"
    except RuntimeError as re:
        assert "Max retry attempts exceeded" in str(re)
        assert isinstance(re.__cause__, TimeoutError)

    print("All Module 10 solutions verified successfully!")


if __name__ == "__main__":
    run_all_tests()
