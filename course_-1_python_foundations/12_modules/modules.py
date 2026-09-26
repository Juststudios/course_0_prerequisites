"""
Module 12: Modules, Packages, and Imports
==========================================
A comprehensive hands-on exploration of Python's modular code architecture:
namespaces, the import system, sys.path, sys.modules caching, the __name__ guard,
package hierarchies, and dynamic module loading for autonomous AI agents.

Run this script directly:
    python3 modules.py
"""

import importlib
import math
import os
import sys
import types
from pathlib import Path


def banner(title: str) -> None:
    """Helper to format section headers for clean terminal output."""
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


# =============================================================================
# Section 1: What is a Module? Namespaces and Module Objects
# =============================================================================
banner("Section 1: What is a Module? Namespaces and Module Objects")

# In Python, any file ending with .py is a module.
# When a module is loaded, Python creates an instance of types.ModuleType.
# This module object contains a dictionary (its namespace) storing all functions,
# classes, variables, and imported symbols defined inside that file.

print(f"Type of the 'math' module: {type(math)}")
print(f"Is 'math' an instance of types.ModuleType? {isinstance(math, types.ModuleType)}")
print(f"Module name attribute (__name__): {math.__name__}")
print(f"Module docstring attribute (__doc__): {math.__doc__[:45]}...")

# The dir() function inspects everything exposed inside a module namespace:
math_symbols = [s for s in dir(math) if not s.startswith("__")]
print(f"Sample symbols in 'math' ({len(math_symbols)} total): {math_symbols[:8]}")


# =============================================================================
# Section 2: Import Styles and Namespace Isolation
# =============================================================================
banner("Section 2: Import Styles and Namespace Isolation")

# Style A: Full module import (Preferred for clarity and avoiding name collisions)
# Keeps all symbols neatly inside the 'math' namespace.
radius = 5.0
area = math.pi * (radius ** 2)
print(f"Style A (import math): area = {area:.2f}")

# Style B: Selective import into the current local scope
# Brings specific symbols directly into the local namespace.
from math import sqrt, floor
val = 18.75
print(f"Style B (from math import sqrt, floor): sqrt = {sqrt(val):.2f}, floor = {floor(val)}")

# Style C: Aliasing with 'as'
# Renames a module or function to prevent collisions or shorten long names.
import datetime as dt
now = dt.datetime.now()
print(f"Style C (import datetime as dt): Current year = {now.year}")

# Anti-pattern: from module import *
# Wildcard imports pollute the local namespace, obscure where names come from,
# and risk silently overwriting existing variables or functions.


# =============================================================================
# Section 3: How Python Finds Modules — sys.path
# =============================================================================
banner("Section 3: The Module Search Path (sys.path)")

# When you run `import foo`, Python looks through a list of directory paths
# stored in `sys.path`. It searches sequentially:
#   1. The directory containing the input script (or current directory)
#   2. PYTHONPATH (environment variable, if set)
#   3. Standard library directories
#   4. Installed third-party packages (site-packages / virtualenv)

print("Directories currently searched by Python (first 4 entries of sys.path):")
for index, directory in enumerate(sys.path[:4]):
    print(f"  [{index}] {directory}")

# We can inspect where a specific module file was loaded from on disk:
print(f"\nLocation of 'os' module on disk: {os.__file__}")


# =============================================================================
# Section 4: Module Caching and the Singleton Pattern in sys.modules
# =============================================================================
banner("Section 4: sys.modules Caching (Modules are Singletons)")

# When a module is imported for the first time:
#   1. Python compiles and executes the file's top-level code.
#   2. The resulting module object is cached in sys.modules (a Python dictionary).
# Subsequent imports anywhere in your program DO NOT re-execute the file;
# they simply return the cached module reference from sys.modules!

print(f"Total modules currently cached in sys.modules: {len(sys.modules)}")
print(f"Is 'math' cached in sys.modules? {'math' in sys.modules}")
print(f"sys.modules['math'] is identical to math: {sys.modules['math'] is math}")

# If two different parts of an application import the same module and one modifies
# a module-level variable, that modification is visible to the other.


# =============================================================================
# Section 5: The __name__ == '__main__' Execution Guard
# =============================================================================
banner("Section 5: The __name__ == '__main__' Execution Guard")

# Every Python module has a built-in __name__ string variable.
# When a script is executed directly from the terminal (e.g. python3 modules.py),
# Python sets __name__ = "__main__".
# When the same file is imported by another script, Python sets __name__
# to the module's file name (e.g. "modules").

print(f"Current value of __name__ in this file: '{__name__}'")

if __name__ == "__main__":
    print("Execution check: This block executes ONLY when run directly!")
    print("If another script writes 'import modules', this block is skipped.")


# =============================================================================
# Section 6: Packages and Project Layout
# =============================================================================
banner("Section 6: Packages and Project Structure")

# A package is a directory containing Python modules.
# In Python 3.3+, any directory on sys.path can be a namespace package,
# but adding an __init__.py file explicitly defines a regular package and
# allows initialization code or custom exports.
#
# A professional AI Agent package structure typically looks like:
#
#   agent_core/
#   ├── __init__.py         -> Defines package-level exports and version
#   ├── orchestrator.py     -> Main ReAct reasoning loop
#   ├── memory/
#   │   ├── __init__.py
#   │   ├── sqlite_store.py -> Short-term & long-term persistence
#   │   └── vector_cache.py -> Embedding similarity search
#   └── tools/
#       ├── __init__.py     -> Registry of available tools
#       ├── web_search.py   -> HTTP/API search tool
#       └── code_exec.py    -> Sandboxed Python executor

sample_package_structure = """
agent_project/
├── __init__.py           (makes directory an importable package)
├── config.py             (environment and model settings)
├── memory.py             (state management)
└── tools/
    ├── __init__.py       (exposes all tools)
    ├── calculator.py     (math tool)
    └── scraper.py        (web tool)
"""
print(sample_package_structure.strip())


# =============================================================================
# Section 7: Controlling Public Exports with __all__
# =============================================================================
banner("Section 7: Controlling Public Exports with __all__")

# In a module, defining __all__ specifies exactly which names are exported
# when a user does `from module import *`.
# Symbols prefixed with an underscore (e.g., _internal_state) are considered private
# by convention and will not be exported by wildcard imports.

__all__ = ["banner", "dynamic_tool_loader", "AgentToolRegistry"]

print(f"Symbols officially exported by this module's __all__: {__all__}")


# =============================================================================
# Section 8: Dynamic Module Loading for AI Agents (importlib)
# =============================================================================
banner("Section 8: Dynamic Tool Loading for AI Agent Systems")

# Modern autonomous agents do not hardcode every tool into their main script.
# Instead, the agent is given a tool name as a string (e.g. "json", "math", "csv")
# and dynamically loads the module and target function at runtime using importlib.

class AgentToolRegistry:
    """A registry that dynamically loads tool functions from module strings."""

    def __init__(self) -> None:
        self.tools: dict[str, types.FunctionType] = {}

    def register_dynamic_tool(self, tool_name: str, module_path: str, function_name: str) -> None:
        """Dynamically imports a module and registers a function as an agent tool."""
        print(f"  [Registry] Loading '{function_name}' from module '{module_path}'...")
        try:
            # importlib.import_module takes a string module name and returns the module object!
            mod = importlib.import_module(module_path)
            func = getattr(mod, function_name)
            self.tools[tool_name] = func
            print(f"  [Registry] Successfully registered tool: '{tool_name}' -> {module_path}.{function_name}")
        except (ImportError, AttributeError) as err:
            print(f"  [Registry] ERROR: Could not load tool '{tool_name}': {err}")

    def execute_tool(self, tool_name: str, *args, **kwargs):
        """Executes a registered tool by string identifier."""
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' is not registered in agent registry.")
        return self.tools[tool_name](*args, **kwargs)


def dynamic_tool_loader() -> None:
    """Demonstrates dynamic tool registration and invocation."""
    registry = AgentToolRegistry()

    # The agent dynamically registers standard library functions as tools:
    registry.register_dynamic_tool("calc_sqrt", "math", "sqrt")
    registry.register_dynamic_tool("calc_factorial", "math", "factorial")

    # Agent invokes the tools dynamically based on user prompts:
    print("\nExecuting agent tools via dynamic registry:")
    sqrt_res = registry.execute_tool("calc_sqrt", 144)
    fact_res = registry.execute_tool("calc_factorial", 6)
    print(f"  Tool result: calc_sqrt(144) = {sqrt_res}")
    print(f"  Tool result: calc_factorial(6) = {fact_res}")


dynamic_tool_loader()


# =============================================================================
# Section 9: Circular Imports & Safe Architectural Patterns
# =============================================================================
banner("Section 9: Circular Imports and Best Practices")

# A circular import occurs when Module A imports Module B, and Module B imports Module A.
# Why it breaks:
#   1. Python begins executing Module A from top to bottom.
#   2. At line 2, Module A hits 'import B'.
#   3. Python pauses Module A and starts executing Module B.
#   4. Module B hits 'from A import func_a'.
#   5. But Module A hasn't finished loading yet! 'func_a' doesn't exist yet!
#   6. Python raises: ImportError: cannot import name 'func_a' from partially initialized module.
#
# Three Solutions:
#   1. Dependency Inversion: Move shared classes/functions into a shared 'types.py' or 'common.py'.
#   2. Function-level import: Move the import inside the specific function that uses it.
#   3. Redesign architecture: Ensure dependencies flow in one direction (A -> B, never A <-> B).

print("Best practices for Python modules:")
print("  1. Keep module dependencies acyclic (Directed Acyclic Graph).")
print("  2. Never use wildcard imports ('from module import *').")
print("  3. Always place the `if __name__ == '__main__':` guard on executable files.")
print("  4. Group related modules in packages with meaningful names.")
print("  5. Use `importlib` for flexible runtime tool plugins in AI agent architectures.")

banner("Module 12 Lesson Complete")
