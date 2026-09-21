"""
Module 21: Testing

TERM: Test
DEFINITION: Code that verifies other code behaves as expected.
TERM: Unit Test
DEFINITION: A test that checks a single, isolated function or class.
WHY IT EXISTS: Without tests, you only discover bugs when users do.
"""
import math

# ── Simple assertion-based tests ─────────────────────────────────────────────
def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5, "2+3 should equal 5"

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 0) == 0

# Run all tests
for test_fn in [test_add_positive, test_add_negative, test_add_zero]:
    test_fn()
    print(f"  ✓ {test_fn.__name__}")

# ── Testing exceptions ────────────────────────────────────────────────────────
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    try:
        divide(5, 0)
        assert False, "Should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass   # expected

test_divide_by_zero()
print("  ✓ test_divide_by_zero")

# ── Running with pytest ───────────────────────────────────────────────────────
# Save tests to test_add.py (with test_ prefix) and run:
#   pytest test_add.py -v
# pytest automatically discovers and runs all test_ functions.
print("\nTesting lesson complete. See test_example.py for pytest usage.")
