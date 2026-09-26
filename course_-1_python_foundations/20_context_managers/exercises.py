"""
Module 20: Context Managers — Exercises
========================================

Practice the Context Manager Protocol (__enter__, __exit__) and @contextlib.contextmanager.
Complete the four progressive exercise levels below.
"""

import contextlib
from typing import Any, Dict, List, Optional, Tuple, Type


# =====================================================================
# Level 1: Recall
# =====================================================================
def trace_context_lifecycle() -> List[str]:
    """
    Recall Exercise:
    Consider the following class-based context manager:

        class TraceManager:
            def __init__(self):
                # Action A: "init"
            def __enter__(self):
                # Action B: "enter"
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                # Action C: "exit"
                return False

        with TraceManager() as tm:
            # Action D: "body"

    # TODO: In what exact sequence are actions A, B, C, D executed?
    # Return a list of four strings in chronological execution order.
    # Choices: ["init", "enter", "body", "exit"]
    """
    # TODO: Replace the line below with your execution order trace
    raise NotImplementedError("Level 1: Implement trace_context_lifecycle().")


# =====================================================================
# Level 2: Modify
# =====================================================================
class Indenter:
    """
    Modify / Adapt Exercise:
    Implement a context manager that tracks block indentation depth.

    Requirements:
    - Maintains a class-level variable `depth: int = 0`.
    - Upon entering the `with` block (`__enter__`), increments `depth` by 1 and returns `self`.
    - Upon exiting the `with` block (`__exit__`), decrements `depth` by 1.
    - Provides a helper method `format(text: str) -> str` that prefixes `text`
      with `2 * depth` spaces.
    - Supports multiple nested `with Indenter() as ind:` blocks.
    - Does not suppress exceptions.
    """
    depth: int = 0

    def __enter__(self) -> "Indenter":
        # TODO: Implement __enter__
        raise NotImplementedError("Level 2: Implement Indenter.__enter__().")

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # TODO: Implement __exit__
        raise NotImplementedError("Level 2: Implement Indenter.__exit__().")

    def format(self, text: str) -> str:
        return f"{'  ' * Indenter.depth}{text}"


# =====================================================================
# Level 3: Build
# =====================================================================
@contextlib.contextmanager
def safe_suppress(*exc_types: Type[BaseException]):
    """
    Build Exercise:
    Using the `@contextlib.contextmanager` decorator, create a context manager
    that catches and swallows any exception matching the provided `exc_types`.

    Requirements:
    - If an exception occurs inside the block and matches any of `exc_types`,
      catch it and exit silently without crashing the caller.
    - If an exception occurs that does NOT match `exc_types`, allow it to propagate.
    - If no exception occurs, complete cleanly.
    - Must use the generator `try...yield...except` structure.

    Example:
        with safe_suppress(FileNotFoundError, KeyError):
            d = {}
            val = d["nonexistent"]  # Swallowed cleanly
    """
    # TODO: Implement safe_suppress generator context manager
    raise NotImplementedError("Level 3: Implement safe_suppress context manager.")


# =====================================================================
# Level 4: Debug
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
    Debug Exercise:
    The following generator-based context manager is supposed to manage
    database transactions:
      1. Yield the connection `conn` so the caller can execute statements.
      2. If the block finishes without error, call `conn.commit()`.
      3. If an exception occurs in the block, call `conn.rollback()` and
         re-raise the exception so the caller is notified of transaction failure.

    However, the buggy implementation below contains critical defects:
      - It calls commit() inside the try block before yield!
      - It swallows the exception instead of re-raising it.
      - It does not yield the connection to the caller.

    Buggy implementation:
        @contextlib.contextmanager
        def db_transaction(conn):
            conn.commit()  # BUG: commits before any work is done!
            try:
                yield      # BUG: does not yield conn!
            except Exception:
                conn.rollback()
                # BUG: swallows error instead of re-raising!

    # TODO: Fix all bugs in db_transaction.
    """
    # TODO: Replace with corrected implementation
    raise NotImplementedError("Level 4: Fix bugs in db_transaction.")


if __name__ == "__main__":
    print("Module 20 Exercises loaded successfully.")
    print("Complete the TODOs and verify your work with solutions.py.")
