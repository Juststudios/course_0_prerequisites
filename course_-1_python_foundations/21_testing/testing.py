"""
Module 21: Automated Testing and Quality Assurance
==================================================

This lesson covers automated testing principles in Python, progressing from
basic assertions to structured test suites, boundary condition testing,
exception verification, test fixtures, and mock isolation for AI agents.

Topics covered:
  1. The Philosophy of Automated Testing & The AAA Pattern
  2. Pure Python Assertions and Custom Test Runner
  3. Boundary and Edge Case Testing (Happy vs Unhappy paths)
  4. Testing Expected Exceptions Cleanly
  5. Parametrized Data-Driven Testing
  6. Test Fixtures and State Isolation (Setup and Teardown)
  7. Mocking External Dependencies (Simulating AI Agent Tool Calls)
  8. Executing a Complete Test Suite with Failure Diagnostics
"""

import math
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# =====================================================================
# 1. The Philosophy of Automated Testing & The AAA Pattern
# =====================================================================
print("=" * 70)
print("1. THE PHILOSOPHY OF AUTOMATED TESTING & THE AAA PATTERN")
print("=" * 70)

# A unit test should follow the three-phase AAA pattern:
#   Arrange: Set up test inputs, dependencies, and expected outcomes.
#   Act:     Call the function or method under test.
#   Assert:  Verify that the actual result matches expected behavior.

def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model: str) -> float:
    """Calculates dollar cost for LLM usage."""
    rates = {
        "gpt-4o": {"prompt": 0.005 / 1000, "completion": 0.015 / 1000},
        "mini":   {"prompt": 0.00015 / 1000, "completion": 0.0006 / 1000},
    }
    if model not in rates:
        raise ValueError(f"Unknown model: {model}")
    if prompt_tokens < 0 or completion_tokens < 0:
        raise ValueError("Token counts cannot be negative")

    p_cost = prompt_tokens * rates[model]["prompt"]
    c_cost = completion_tokens * rates[model]["completion"]
    return round(p_cost + c_cost, 6)

# Test 1 following AAA pattern explicitly
def test_calculate_token_cost_happy_path():
    # 1. Arrange
    prompt_count = 1000
    completion_count = 500
    model_name = "gpt-4o"
    expected_cost = 0.0125  # (1000 * 0.000005) + (500 * 0.000015) = 0.005 + 0.0075 = 0.0125

    # 2. Act
    actual_cost = calculate_token_cost(prompt_count, completion_count, model_name)

    # 3. Assert
    assert actual_cost == expected_cost, f"Expected {expected_cost}, got {actual_cost}"
    print("  ✓ test_calculate_token_cost_happy_path passed")

test_calculate_token_cost_happy_path()


# =====================================================================
# 2. Building a Custom Micro-Test Harness
# =====================================================================
print("\n" + "=" * 70)
print("2. BUILDING A CUSTOM MICRO-TEST HARNESS")
print("=" * 70)

class MicroTestRunner:
    """
    A lightweight test runner that executes test functions,
    catches assertion errors, and records summary statistics.
    """
    def __init__(self):
        self.tests: List[Callable[[], None]] = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def add_test(self, test_func: Callable[[], None]) -> None:
        self.tests.append(test_func)

    def run(self) -> bool:
        print(f"Running {len(self.tests)} automated test cases...")
        for test_fn in self.tests:
            name = test_fn.__name__
            try:
                test_fn()
                print(f"  [PASS] {name}")
                self.passed += 1
            except AssertionError as err:
                print(f"  [FAIL] {name}: {err}")
                self.failed += 1
            except Exception as exc:
                print(f"  [ERROR] {name}: Uncaught {type(exc).__name__}: {exc}")
                self.errors += 1

        print(f"\nResults: {self.passed} passed, {self.failed} failed, {self.errors} errors.")
        return self.failed == 0 and self.errors == 0

runner = MicroTestRunner()


# =====================================================================
# 3. Boundary and Edge Case Testing
# =====================================================================
print("\n" + "=" * 70)
print("3. BOUNDARY AND EDGE CASE TESTING")
print("=" * 70)

def truncate_text(text: str, max_chars: int, suffix: str = "...") -> str:
    """Truncates text to max_chars including suffix if truncated."""
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative")
    if len(text) <= max_chars:
        return text
    if max_chars <= len(suffix):
        return suffix[:max_chars]
    return text[:max_chars - len(suffix)] + suffix

def test_truncate_shorter_than_limit():
    assert truncate_text("hello", 10) == "hello"

def test_truncate_exact_limit():
    assert truncate_text("hello", 5) == "hello"

def test_truncate_exceeds_limit():
    assert truncate_text("hello world", 8) == "hello..."

def test_truncate_empty_string():
    assert truncate_text("", 5) == ""

runner.add_test(test_truncate_shorter_than_limit)
runner.add_test(test_truncate_exact_limit)
runner.add_test(test_truncate_exceeds_limit)
runner.add_test(test_truncate_empty_string)


# =====================================================================
# 4. Testing Expected Exceptions Cleanly
# =====================================================================
print("\n" + "=" * 70)
print("4. TESTING EXPECTED EXCEPTIONS CLEANLY")
print("=" * 70)

# How to verify defensive programming without false passes:
def test_calculate_token_cost_negative_tokens():
    try:
        calculate_token_cost(-10, 50, "mini")
        assert False, "Should have raised ValueError for negative tokens!"
    except ValueError as err:
        assert "Token counts cannot be negative" in str(err)

def test_calculate_token_cost_unknown_model():
    try:
        calculate_token_cost(100, 100, "nonexistent-model-xyz")
        assert False, "Should have raised ValueError for unknown model!"
    except ValueError as err:
        assert "Unknown model" in str(err)

runner.add_test(test_calculate_token_cost_negative_tokens)
runner.add_test(test_calculate_token_cost_unknown_model)


# =====================================================================
# 5. Parametrized Data-Driven Testing
# =====================================================================
print("\n" + "=" * 70)
print("5. PARAMETRIZED DATA-DRIVEN TESTING")
print("=" * 70)

def parse_agent_action_tag(tag: str) -> Optional[Tuple[str, str]]:
    """Parses '<action:name>payload</action:name>' tags."""
    if not (tag.startswith("<action:") and tag.endswith(">")):
        return None
    closing_idx = tag.find(">")
    action_name = tag[8:closing_idx]
    close_tag = f"</action:{action_name}>"
    if not tag.endswith(close_tag):
        return None
    payload = tag[closing_idx + 1 : len(tag) - len(close_tag)]
    return (action_name, payload)

def test_parse_agent_action_parametrized():
    # Table of (input, expected_output) test vectors
    test_cases = [
        ("<action:search>python docs</action:search>", ("search", "python docs")),
        ("<action:eval>1 + 1</action:eval>", ("eval", "1 + 1")),
        ("<action:bash></action:bash>", ("bash", "")),
        ("Plain text response without tags", None),
        ("<action:incomplete>tag with no close", None),
    ]

    for raw_input, expected in test_cases:
        actual = parse_agent_action_tag(raw_input)
        assert actual == expected, f"For input '{raw_input}', expected {expected}, got {actual}"

runner.add_test(test_parse_agent_action_parametrized)


# =====================================================================
# 6. Test Fixtures and State Isolation (Setup and Teardown)
# =====================================================================
print("\n" + "=" * 70)
print("6. TEST FIXTURES AND STATE ISOLATION")
print("=" * 70)

class AgentKVStore:
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

# Setup fixture pattern: create fresh isolated instance per test
def test_kv_store_set_and_get():
    # Arrange (fresh instance prevents state leakage)
    store = AgentKVStore()
    store.set("session_id", "sess_12345")

    # Act & Assert
    assert store.get("session_id") == "sess_12345"
    assert store.get("nonexistent") is None

def test_kv_store_delete():
    store = AgentKVStore()
    store.set("temp_token", "abc")
    assert store.delete("temp_token") is True
    assert store.delete("temp_token") is False  # Already deleted
    assert store.get("temp_token") is None

runner.add_test(test_kv_store_set_and_get)
runner.add_test(test_kv_store_delete)


# =====================================================================
# 7. Mocking External Dependencies (Simulating AI Agent Tool Calls)
# =====================================================================
print("\n" + "=" * 70)
print("7. MOCKING EXTERNAL DEPENDENCIES (AGENT TOOL EXECUTION)")
print("=" * 70)

class MockLLMClient:
    """Mock simulating external API client without making network requests."""
    def __init__(self, responses: List[str]):
        self.responses = list(responses)
        self.calls: List[str] = []

    def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        if not self.responses:
            return "Default simulated response"
        return self.responses.pop(0)

def test_agent_decision_loop_with_mock():
    # Arrange mock responses
    mock_api = MockLLMClient(responses=["Plan: Inspect files", "Plan: Run tests"])

    # Act: Simulate agent queries
    turn1 = mock_api.generate("User request: Fix bug")
    turn2 = mock_api.generate("System: Continue execution")

    # Assert
    assert turn1 == "Plan: Inspect files"
    assert turn2 == "Plan: Run tests"
    assert len(mock_api.calls) == 2
    assert mock_api.calls[0] == "User request: Fix bug"

runner.add_test(test_agent_decision_loop_with_mock)


# =====================================================================
# 8. Executing the Complete Test Suite
# =====================================================================
print("\n" + "=" * 70)
print("8. EXECUTING COMPLETE TEST SUITE")
print("=" * 70)

suite_passed = runner.run()
assert suite_passed, "All test cases in suite must pass!"

print("\n" + "=" * 70)
print("Module 21 lesson completed successfully!")
print("=" * 70)
