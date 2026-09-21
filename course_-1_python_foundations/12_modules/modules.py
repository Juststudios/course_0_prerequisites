"""
Module 12: Modules and Imports

TERM: Module
DEFINITION: A Python file containing functions, classes, and variables that
            other files can reuse.
INTUITION: Like chapters in a book — you don't reread every chapter every time;
           you open the relevant one.
WHY IT EXISTS: To split large programs into manageable, reusable pieces.
"""

# ── Importing the standard library ──────────────────────────────────────────
import math
print(f"pi = {math.pi:.4f}")
print(f"sqrt(16) = {math.sqrt(16)}")

import os
print(f"\nCurrent directory: {os.getcwd()}")

from pathlib import Path
print(f"Home directory: {Path.home()}")

# ── The __name__ == "__main__" guard ─────────────────────────────────────────
# When Python runs a file directly, __name__ is "__main__".
# When a file is imported by another module, __name__ is the module's filename.
# This guard prevents "side-effect" code from running on import.
print(f"\n__name__ = {__name__!r}")

if __name__ == "__main__":
    print("Running as main script, not as imported module.")

# ── How a project grows ──────────────────────────────────────────────────────
# One file:   agent.py  (everything crammed together)
#
# Better:
# my_agent/
# ├── __init__.py    (makes this a package)
# ├── tools.py       (tool functions)
# ├── memory.py      (SQLite persistence)
# └── agent.py       (orchestration)
#
# This is exactly how real agent runtimes like Hermes are structured.
print("\nModule lesson complete.")
