"""
Module 15: Type Hints

TERM: Type Hint / Annotation
DEFINITION: An optional label on a variable or function parameter indicating
            what type of value is expected.
WHY IT EXISTS: Clarity, documentation, and static analysis (mypy, pyright).
NOTE: Python does NOT enforce type hints at runtime by default.
"""
from typing import Optional, Any, Callable

# ── Basic annotations ────────────────────────────────────────────────────────
name: str = "Alice"
age: int = 30
score: float = 9.5
active: bool = True

# ── Function annotations ─────────────────────────────────────────────────────
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# ── Collection types ─────────────────────────────────────────────────────────
def process_names(names: list[str]) -> dict[str, int]:
    return {name: len(name) for name in names}

print(process_names(["Alice", "Bob"]))

# ── Optional ─────────────────────────────────────────────────────────────────
def find_user(user_id: int) -> Optional[str]:
    """Returns the username, or None if not found."""
    db = {1: "alice", 2: "bob"}
    return db.get(user_id)   # returns None if not found

print(find_user(1))
print(find_user(99))

# ── Callable type hints ──────────────────────────────────────────────────────
# Callable[[arg_types], return_type]
# Example: a tool that takes a string and returns an int
def run_tool(tool: Callable[[str], int], input_text: str) -> int:
    return tool(input_text)

print(run_tool(len, "hello"))   # 5

# ── Breaking down Callable[[str], int] ──────────────────────────────────────
# Callable      → this is a callable object (function, method, __call__)
# [[str], int]  → takes one str argument, returns an int

# ── Why this matters in agents ───────────────────────────────────────────────
# Agent tool registries use Callable to describe what a tool looks like:
# tools: dict[str, Callable[..., Any]]
print("\nType hints lesson complete.")
