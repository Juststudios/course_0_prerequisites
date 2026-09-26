"""
Module 07 Exercises: Control Flow (Conditionals, Loops, and Decision Logic)
==========================================================================

Complete the exercises below across the four progressive tiers:
  Level 1: Recall  — Basic understanding of conditionals, truthiness, and ternary syntax
  Level 2: Modify  — Updating existing loops to add guards and filtering logic
  Level 3: Build   — Writing complete decision and iteration algorithms from scratch
  Level 4: Debug   — Identifying and fixing logic bugs (infinite loops, off-by-one errors)

Run your solutions against `solutions.py` to verify your implementations.
"""

from typing import Any, List, Dict, Optional


# ==============================================================================
# Level 1: Recall
# ==============================================================================

def classify_truthiness(val: Any) -> str:
    """
    Return 'truthy' if `val` evaluates to True in a boolean context,
    or 'falsy' if `val` evaluates to False.

    Examples:
        classify_truthiness(0) -> 'falsy'
        classify_truthiness([]) -> 'falsy'
        classify_truthiness("hello") -> 'truthy'
        classify_truthiness([1, 2]) -> 'truthy'
    """
    # TODO: Implement truthiness check using `if val:` or `bool(val)`
    raise NotImplementedError("Exercise 1.1: classify_truthiness not implemented yet.")


def format_status_ternary(is_active: bool, token_count: int) -> str:
    """
    Use a single conditional expression (ternary operator) to return:
      - "ACTIVE (<token_count> tokens)" if is_active is True
      - "OFFLINE" if is_active is False

    Example:
        format_status_ternary(True, 150) -> "ACTIVE (150 tokens)"
        format_status_ternary(False, 0)   -> "OFFLINE"
    """
    # TODO: Return formatted status using a ternary expression
    raise NotImplementedError("Exercise 1.2: format_status_ternary not implemented yet.")


# ==============================================================================
# Level 2: Modify
# ==============================================================================

def filter_prompt_tokens(tokens: List[str], max_chars: int) -> List[str]:
    """
    Given a list of token strings, return a new list containing tokens such that:
      1. Empty tokens ('') or whitespace-only tokens are skipped (use `continue`).
      2. If adding the next token would cause the total character length of accepted
         tokens to exceed `max_chars`, stop accepting tokens immediately (use `break`).
      3. Return the accepted list of tokens.

    Example:
        tokens = ["Hello", "", "world", " ", "this", "is", "a", "long", "prompt"]
        filter_prompt_tokens(tokens, max_chars=12)
        -> ["Hello", "world"]  (len: 5 + 5 = 10 <= 12; "this" would make it 14 > 12)
    """
    accepted: List[str] = []
    total_chars = 0

    # TODO: Modify the loop below to skip whitespace/empty tokens and break before exceeding max_chars
    for token in tokens:
        # Step 1: Check if token is empty or only whitespace
        # Step 2: Check if adding token exceeds max_chars
        # Step 3: Append to accepted and update total_chars
        raise NotImplementedError("Exercise 2: filter_prompt_tokens not implemented yet.")

    return accepted


# ==============================================================================
# Level 3: Build
# ==============================================================================

def run_agent_retry_loop(max_retries: int, success_on_attempt: int) -> Dict[str, Any]:
    """
    Simulate an agent API call with retry logic and exponential backoff tracking.
    
    Requirements:
      - Use a loop (for or while) that attempts up to `max_retries` times (1-indexed).
      - On each iteration:
          - If the current attempt equals `success_on_attempt`, return immediately:
            {"status": "SUCCESS", "attempts": attempt, "total_backoff_seconds": accumulated_backoff}
          - Otherwise, add backoff delay `2 ** (attempt - 1)` to accumulated_backoff.
      - If the loop finishes without success (e.g. success_on_attempt > max_retries), return:
        {"status": "FAILED", "attempts": max_retries, "total_backoff_seconds": accumulated_backoff}

    Example:
        run_agent_retry_loop(max_retries=3, success_on_attempt=2)
        -> attempt 1 fails (backoff +1s)
        -> attempt 2 succeeds
        -> {"status": "SUCCESS", "attempts": 2, "total_backoff_seconds": 1}
    """
    # TODO: Build the complete retry loop with backoff calculation
    raise NotImplementedError("Exercise 3.1: run_agent_retry_loop not implemented yet.")


def dispatch_tool_calls(
    calls: List[Dict[str, Any]], 
    available_tools: Dict[str, Any]
) -> List[str]:
    """
    Given a list of tool call specifications:
        [{"call_id": 1, "tool": "search"}, {"call_id": 2, "tool": "unknown"}]
    and a dictionary of available tools:
        {"search": <handler>, "calculator": <handler>}

    Use `enumerate()` to iterate through `calls` and construct an audit log list:
      - If call["tool"] is in available_tools:
        Log: "Step {idx}: Executed {tool_name} (call_id: {call_id})"
      - If call["tool"] is NOT in available_tools:
        Log: "Step {idx}: REJECTED unknown tool '{tool_name}' (call_id: {call_id})"
    
    Indices in log should be 1-based (start=1).
    """
    # TODO: Build tool dispatch auditor using enumerate()
    raise NotImplementedError("Exercise 3.2: dispatch_tool_calls not implemented yet.")


# ==============================================================================
# Level 4: Debug
# ==============================================================================

def buggy_countdown(start: int) -> List[int]:
    """
    BUGGED FUNCTION:
    Intended behavior:
      Count down from `start` to 1 inclusive, returning the list of integers.
      If start <= 0, return an empty list.

    Current buggy code either loops indefinitely or misses the final 1.
    Find and fix the bug(s).
    """
    # --- BUGGED CODE BELOW (Modify to fix) ---
    result = []
    current = start
    # Bug: While condition and decrement logic are flawed
    while current > 0:
        result.append(current)
        # Missing decrement! Causes infinite loop in original
        current -= 1
    return result


def buggy_find_first_match(items: List[str], target: str) -> int:
    """
    BUGGED FUNCTION:
    Intended behavior:
      Search for `target` in `items`.
      Return the 0-based index of the first occurrence of `target`.
      If `target` is not found, return -1.

    The buggy implementation uses a broken flag or bad break logic.
    """
    # --- BUGGED CODE BELOW (Modify to fix) ---
    # TODO: Fix the bug so that target index is returned, or -1 if not found
    raise NotImplementedError("Exercise 4: buggy_find_first_match needs debugging.")
