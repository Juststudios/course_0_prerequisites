"""
Module 20: Context Managers — Reference Solutions
==================================================

Complete, verified reference solutions for all four exercise tiers.
"""

import contextlib
from typing import Any, Dict, List, Optional, Tuple, Type


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def trace_context_lifecycle() -> List[str]:
    """
    Chronological lifecycle order:
      1. TraceManager() -> __init__ ("init")
      2. Entering with block -> __enter__ ("enter")
      3. Block body executes -> ("body")
      4. Leaving with block -> __exit__ ("exit")
    """
    return ["init", "enter", "body", "exit"]


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
class Indenter:
    """
    Context manager tracking indentation depth.
    """
    depth: int = 0

    def __enter__(self) -> "Indenter":
        Indenter.depth += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        Indenter.depth -= 1
        return False

    def format(self, text: str) -> str:
        return f"{'  ' * Indenter.depth}{text}"


# =====================================================================
# Level 3: Build Solution
# =====================================================================
@contextlib.contextmanager
def safe_suppress(*exc_types: Type[BaseException]):
    """
    Generator-based context manager suppressing specified exception types.
    """
    try:
        yield
    except exc_types:
        pass


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
class MockConnection:
    """Simulated database connection for Level 4."""
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


@contextlib.contextmanager
def db_transaction(conn: MockConnection):
    """
    Corrected transaction context manager:
      - Yields conn to the caller
      - Calls commit() only upon successful block completion
      - Calls rollback() and re-raises on exception
    """
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    t_res = trace_context_lifecycle()
    assert t_res == ["init", "enter", "body", "exit"], f"Level 1 failed: {t_res}"

    # Test Level 2
    assert Indenter.depth == 0
    with Indenter() as ind1:
        assert Indenter.depth == 1
        assert ind1.format("Hello") == "  Hello"
        with Indenter() as ind2:
            assert Indenter.depth == 2
            assert ind2.format("Nested") == "    Nested"
        assert Indenter.depth == 1
    assert Indenter.depth == 0

    # Test Level 3
    # A: Suppress matching exception
    suppressed = False
    with safe_suppress(KeyError, ValueError):
        d = {"a": 1}
        _ = d["nonexistent"]
        suppressed = True  # Should not reach here
    assert not suppressed, "Block should have raised KeyError which was suppressed"

    # B: Do not suppress non-matching exception
    unhandled_raised = False
    try:
        with safe_suppress(KeyError):
            _ = 10 / 0
    except ZeroDivisionError:
        unhandled_raised = True
    assert unhandled_raised, "ZeroDivisionError should not have been suppressed"

    # Test Level 4
    # A: Successful commit
    conn_success = MockConnection()
    with db_transaction(conn_success) as active_conn:
        assert active_conn is conn_success
    assert conn_success.committed is True
    assert conn_success.rolled_back is False

    # B: Rollback on exception
    conn_fail = MockConnection()
    threw_error = False
    try:
        with db_transaction(conn_fail) as active_conn:
            raise RuntimeError("Database constraint violation")
    except RuntimeError:
        threw_error = True

    assert threw_error is True
    assert conn_fail.committed is False
    assert conn_fail.rolled_back is True

    print("Module 20: All Level 1-4 solutions verified successfully!")
