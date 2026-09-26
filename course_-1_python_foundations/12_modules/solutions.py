"""
Module 12: Modules, Packages, and Imports — Reference Solutions
================================================================
Clean, production-grade solutions for all four exercise tiers.
"""

from typing import Any, Dict, List, Optional
import importlib
import sys


# =====================================================================
# Level 1: Recall Solutions
# =====================================================================
def is_module_loaded(module_name: str) -> bool:
    """
    Checks if a given module is currently present in sys.modules.
    """
    return module_name in sys.modules


def recall_main_guard_value() -> str:
    """
    When a script is run directly, Python sets __name__ to '__main__'.
    """
    return "__main__"


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def prioritize_search_path(directory_path: str) -> List[str]:
    """
    Modifies sys.path in-place to place directory_path at index 0.
    """
    if directory_path in sys.path:
        sys.path.remove(directory_path)
    sys.path.insert(0, directory_path)
    return list(sys.path)


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def dynamic_agent_tool_runner(
    module_name: str,
    function_name: str,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    Dynamically loads and executes a tool function from a module by string name.
    """
    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError as err:
        raise ValueError(f"Module '{module_name}' not found") from err

    if not hasattr(mod, function_name):
        raise AttributeError(f"Function '{function_name}' not found in '{module_name}'")

    func = getattr(mod, function_name)
    if not callable(func):
        raise AttributeError(f"Attribute '{function_name}' in '{module_name}' is not callable")

    return func(*args, **kwargs)


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def audit_agent_dependencies(required_modules: List[str]) -> Dict[str, bool]:
    """
    Audits availability of modules, correctly handling whitespace and missing modules.
    """
    results: Dict[str, bool] = {}
    for raw_name in required_modules:
        clean_name = raw_name.strip()
        if not clean_name:
            continue
        try:
            importlib.import_module(clean_name)
            results[clean_name] = True
        except (ModuleNotFoundError, ImportError, ValueError):
            results[clean_name] = False
    return results


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    assert recall_main_guard_value() == "__main__", "Level 1 guard value failed"
    import math
    assert is_module_loaded("math") is True, "Level 1 is_module_loaded(math) failed"
    assert is_module_loaded("non_existent_fake_module_xyz_123") is False, "Level 1 negative check failed"

    # Test Level 2
    original_len = len(sys.path)
    test_dir = "/tmp/agent_custom_tools_path_test"
    new_path = prioritize_search_path(test_dir)
    assert new_path[0] == test_dir, "Level 2 prioritization failed"
    # Clean up sys.path after test
    if test_dir in sys.path:
        sys.path.remove(test_dir)

    # Test Level 3
    # Dynamically call math.sqrt(81) -> 9.0
    res = dynamic_agent_tool_runner("math", "sqrt", 81)
    assert res == 9.0, f"Level 3 dynamic sqrt failed: {res}"

    # Test error handling on missing module
    try:
        dynamic_agent_tool_runner("completely_fictional_agent_plugin_xyz", "run")
        assert False, "Level 3 did not raise ValueError on missing module"
    except ValueError as e:
        assert "not found" in str(e)

    # Test error handling on missing function
    try:
        dynamic_agent_tool_runner("math", "imaginary_tool_function_xyz")
        assert False, "Level 3 did not raise AttributeError on missing function"
    except AttributeError as e:
        assert "not found in 'math'" in str(e)

    # Test Level 4
    audit = audit_agent_dependencies(["math", "sys", "  os  ", "non_existent_pkg_abc"])
    assert audit.get("math") is True, "Level 4 audit math failed"
    assert audit.get("sys") is True, "Level 4 audit sys failed"
    assert audit.get("os") is True, "Level 4 audit os with whitespace failed"
    assert audit.get("non_existent_pkg_abc") is False, "Level 4 audit non-existent failed"

    print("Module 12: All Level 1-4 solutions verified successfully!")
