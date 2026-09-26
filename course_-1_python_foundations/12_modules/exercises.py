"""
Module 12: Modules, Packages, and Imports — Exercises
======================================================
Complete each of the four tiers below to master Python's module architecture,
search paths, dynamic importing, and namespace isolation.
"""

from typing import Any, Dict, List, Optional
import importlib
import sys


# =====================================================================
# Level 1: Recall
# =====================================================================
def is_module_loaded(module_name: str) -> bool:
    """
    Recall Exercise:
    Python caches all currently loaded modules in the global dictionary `sys.modules`.
    Given a module name as a string (e.g., 'math' or 'sys'), return True if the module
    is currently loaded in `sys.modules`, and False otherwise.

    # TODO: Check sys.modules for the presence of module_name.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement is_module_loaded() using sys.modules.")


def recall_main_guard_value() -> str:
    """
    Recall Exercise:
    When a Python script is executed directly from the terminal (e.g. `python3 script.py`),
    what exact string value does Python assign to the special global variable `__name__`?

    # TODO: Return the exact string value assigned to __name__ when executed directly.
    """
    # TODO: Replace the line below with your answer
    raise NotImplementedError("Level 1: Return the string value of __name__ for direct execution.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def prioritize_search_path(directory_path: str) -> List[str]:
    """
    Modify Exercise:
    Python searches directories listed in `sys.path` in sequential order.
    In autonomous agent development, developers often need to prioritize a local
    custom plugin directory so that local tools override system defaults.

    Modify the `sys.path` list in-place:
    1. If `directory_path` is already in `sys.path`, remove it from its current position.
    2. Insert `directory_path` at index 0 (highest priority).
    3. Return a shallow copy of `sys.path`.

    # TODO: Modify sys.path in-place to prioritize directory_path at index 0.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement prioritize_search_path() modifying sys.path.")


# =====================================================================
# Level 3: Build
# =====================================================================
def dynamic_agent_tool_runner(
    module_name: str,
    function_name: str,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    Build Exercise:
    Autonomous AI agents receive tool requests as text names from LLMs.
    Implement a dynamic tool runner that:
    1. Dynamically imports the module specified by `module_name` using `importlib.import_module()`.
       If `ModuleNotFoundError` is raised, catch it and raise `ValueError(f"Module '{module_name}' not found")`.
    2. Retrieves the function named `function_name` from the module using `getattr()`.
       If the attribute does not exist or is not callable, raise `AttributeError(f"Function '{function_name}' not found in '{module_name}'")`.
    3. Calls the function with `*args` and `**kwargs`, and returns its result.

    # TODO: Build dynamic tool resolution and execution using importlib.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement dynamic_agent_tool_runner() with error handling.")


# =====================================================================
# Level 4: Debug
# =====================================================================
def audit_agent_dependencies(required_modules: List[str]) -> Dict[str, bool]:
    """
    Debugging Exercise:
    An agent orchestrator must verify that all required third-party tools/modules
    are installed in the current environment before starting a task.

    The buggy implementation below fails because:
      1. It attempts to use `__import__(mod)` but catches `Exception`, masking other errors.
      2. It crashes if `required_modules` contains empty strings or whitespace.
      3. It modifies a dictionary while iterating or returns wrong boolean values.

    Buggy code snippet:
        results = {}
        for mod in required_modules:
            # BUG: does not strip whitespace, fails on empty strings
            # BUG: uses eval or incorrect import mechanism
            try:
                import mod  # BUG: tries to import the literal name 'mod'!
                results[mod] = True
            except:
                results[mod] = False
        return results

    # TODO: Fix the bugs using importlib.util or importlib.import_module to correctly
    # audit module availability, stripping whitespace and returning {module_name: bool}.
    """
    # TODO: Replace the line below with your bug-free implementation
    raise NotImplementedError("Level 4: Fix bugs in audit_agent_dependencies().")


if __name__ == "__main__":
    print("Module 12 Exercises loaded successfully.")
    print("To verify your solutions, implement the functions above and run solutions.py.")
