"""
Module 07 Solutions: Control Flow (Conditionals, Loops, and Decision Logic)
==========================================================================

Reference solutions for all progressive exercises in Module 07.
"""

from typing import Any, List, Dict, Optional


# ==============================================================================
# Level 1: Recall Solutions
# ==============================================================================

def classify_truthiness(val: Any) -> str:
    """Return 'truthy' if val evaluates to True, else 'falsy'."""
    return "truthy" if val else "falsy"


def format_status_ternary(is_active: bool, token_count: int) -> str:
    """Return formatted status using a ternary expression."""
    return f"ACTIVE ({token_count} tokens)" if is_active else "OFFLINE"


# ==============================================================================
# Level 2: Modify Solution
# ==============================================================================

def filter_prompt_tokens(tokens: List[str], max_chars: int) -> List[str]:
    """Filter out empty/whitespace tokens and cap by max_chars limit."""
    accepted: List[str] = []
    total_chars = 0

    for token in tokens:
        # Skip empty or whitespace-only strings
        if not token or token.isspace():
            continue

        token_len = len(token)
        # Check if adding this token breaches budget
        if total_chars + token_len > max_chars:
            break

        accepted.append(token)
        total_chars += token_len

    return accepted


# ==============================================================================
# Level 3: Build Solutions
# ==============================================================================

def run_agent_retry_loop(max_retries: int, success_on_attempt: int) -> Dict[str, Any]:
    """Simulate retry loop with exponential backoff accumulation."""
    accumulated_backoff = 0

    for attempt in range(1, max_retries + 1):
        if attempt == success_on_attempt:
            return {
                "status": "SUCCESS",
                "attempts": attempt,
                "total_backoff_seconds": accumulated_backoff,
            }
        # Add backoff for failed attempt
        accumulated_backoff += 2 ** (attempt - 1)

    return {
        "status": "FAILED",
        "attempts": max_retries,
        "total_backoff_seconds": accumulated_backoff,
    }


def dispatch_tool_calls(
    calls: List[Dict[str, Any]], 
    available_tools: Dict[str, Any]
) -> List[str]:
    """Audit and dispatch tool calls using enumerate()."""
    logs: List[str] = []

    for idx, call in enumerate(calls, start=1):
        tool_name = call.get("tool", "")
        call_id = call.get("call_id")
        if tool_name in available_tools:
            logs.append(f"Step {idx}: Executed {tool_name} (call_id: {call_id})")
        else:
            logs.append(f"Step {idx}: REJECTED unknown tool '{tool_name}' (call_id: {call_id})")

    return logs


# ==============================================================================
# Level 4: Debug Solutions
# ==============================================================================

def buggy_countdown(start: int) -> List[int]:
    """Fixed countdown: iterates from start down to 1 cleanly."""
    if start <= 0:
        return []
    result = []
    current = start
    while current > 0:
        result.append(current)
        current -= 1
    return result


def buggy_find_first_match(items: List[str], target: str) -> int:
    """Fixed match search: returns 0-based index or -1 if not found using for...else."""
    for idx, item in enumerate(items):
        if item == target:
            return idx
    return -1


# ==============================================================================
# Verification Self-Test Block
# ==============================================================================

if __name__ == "__main__":
    print("Testing Module 07 Solutions...")

    # Level 1 Tests
    assert classify_truthiness(0) == "falsy"
    assert classify_truthiness([]) == "falsy"
    assert classify_truthiness(None) == "falsy"
    assert classify_truthiness("hello") == "truthy"
    assert classify_truthiness([1]) == "truthy"

    assert format_status_ternary(True, 120) == "ACTIVE (120 tokens)"
    assert format_status_ternary(False, 0) == "OFFLINE"

    # Level 2 Tests
    toks = ["Hello", "", "world", "  ", "agent", "system"]
    assert filter_prompt_tokens(toks, max_chars=10) == ["Hello", "world"]
    assert filter_prompt_tokens(toks, max_chars=4) == []
    assert filter_prompt_tokens(toks, max_chars=100) == ["Hello", "world", "agent", "system"]

    # Level 3 Tests
    retry_succ = run_agent_retry_loop(max_retries=4, success_on_attempt=3)
    assert retry_succ == {"status": "SUCCESS", "attempts": 3, "total_backoff_seconds": 1 + 2}

    retry_fail = run_agent_retry_loop(max_retries=3, success_on_attempt=5)
    assert retry_fail == {"status": "FAILED", "attempts": 3, "total_backoff_seconds": 1 + 2 + 4}

    tools = {"web_search": None, "calculator": None}
    calls = [
        {"call_id": "c1", "tool": "web_search"},
        {"call_id": "c2", "tool": "terminal_exec"},
        {"call_id": "c3", "tool": "calculator"},
    ]
    logs = dispatch_tool_calls(calls, tools)
    assert logs[0] == "Step 1: Executed web_search (call_id: c1)"
    assert logs[1] == "Step 2: REJECTED unknown tool 'terminal_exec' (call_id: c2)"
    assert logs[2] == "Step 3: Executed calculator (call_id: c3)"

    # Level 4 Tests
    assert buggy_countdown(5) == [5, 4, 3, 2, 1]
    assert buggy_countdown(0) == []
    assert buggy_countdown(-3) == []

    fruits = ["apple", "banana", "orange", "apple"]
    assert buggy_find_first_match(fruits, "banana") == 1
    assert buggy_find_first_match(fruits, "apple") == 0
    assert buggy_find_first_match(fruits, "grape") == -1

    print("All Module 07 solutions verified successfully!")
