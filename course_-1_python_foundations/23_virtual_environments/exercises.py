"""
Module 23 Exercises: Virtual Environments
=========================================

Practice understanding virtual environments, path resolution, dependency
manifests, and isolation mechanics.

Follow the instructions for each level. Replace `raise NotImplementedError`
with your solution.
"""

from typing import Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall
# ============================================================================

def is_in_virtual_environment(prefix: str, base_prefix: str) -> bool:
    """
    Recall how Python determines if it is running within a virtual environment.
    
    Given the path strings for `prefix` and `base_prefix`:
    - Returns True if they represent an active virtual environment (prefix != base_prefix).
    - Returns False if they are identical (global / base environment).
    
    Examples:
        is_in_virtual_environment("/usr", "/usr") -> False
        is_in_virtual_environment("/home/user/project/.venv", "/usr") -> True
    """
    # TODO: Compare prefix and base_prefix to determine if running in a venv.
    raise NotImplementedError("Level 1: Implement is_in_virtual_environment")


# ============================================================================
# Level 2: Modify
# ============================================================================

def parse_requirement(raw_line: str) -> Tuple[str, str, str]:
    """
    Modify and enhance a requirement string parser.
    
    Requirements:
    1. Strip any trailing inline comments starting with '#' and surrounding whitespace.
    2. Normalize package names to lowercase and replace underscores '_' with dashes '-'.
    3. Detect operators in: '==', '>=', '<=', '!=', '>', '<', '~='.
    4. Return a 3-element tuple: (package_name, operator, version_string).
       If no operator or version is specified, return (package_name, "", "").
       If the input is empty or just a comment, return ("", "", "").
       
    Examples:
        parse_requirement("Requests >= 2.28.0 # web client") -> ("requests", ">=", "2.28.0")
        parse_requirement("click") -> ("click", "", "")
        parse_requirement("# pure comment") -> ("", "", "")
    """
    # TODO: Strip comments, normalize package name, detect operator and version.
    raise NotImplementedError("Level 2: Implement parse_requirement")


# ============================================================================
# Level 3: Build
# ============================================================================

def find_conflicting_packages(
    reqs1: List[str], reqs2: List[str]
) -> Dict[str, Tuple[str, str]]:
    """
    Build a dependency conflict detector for two project requirement lists.
    
    A conflict occurs when the exact same package is pinned with '==' in both
    lists, but with different target versions.
    
    Returns:
        A dictionary mapping the normalized package name to a tuple of the two
        conflicting versions: {pkg_name: (version_from_reqs1, version_from_reqs2)}.
        
    Example:
        reqs1 = ["requests==2.28.0", "pydantic==1.10.8"]
        reqs2 = ["requests==2.31.0", "pydantic==1.10.8"]
        -> {"requests": ("2.28.0", "2.31.0")}
    """
    # TODO: Build conflict detector returning conflicting pinned versions.
    raise NotImplementedError("Level 3: Implement find_conflicting_packages")


# ============================================================================
# Level 4: Debug
# ============================================================================

def generate_pyvenv_cfg(
    home_dir: str,
    python_version: str,
    include_system_site_packages: bool = False,
) -> str:
    """
    DEBUG CHALLENGE:
    The function below was written to generate the standard contents of a `pyvenv.cfg`
    file, but it contains several bugs:
    1. Key names are malformed (e.g., 'home_dir' instead of standard 'home').
    2. The boolean value for 'include-system-site-packages' is printed in title-case
       ('True'/'False') instead of standard Python venv lowercase ('true'/'false').
    3. The version key is missing from the output.
    
    Expected format:
        home = <home_dir>
        include-system-site-packages = <true|false>
        version = <python_version>
        
    Fix the bugs so the output matches standard pyvenv.cfg format.
    """
    # BUGGY CODE:
    # return f"home_dir = {home_dir}\nsystem_site_packages = {include_system_site_packages}"
    
    # TODO: Fix the bugs and return the properly formatted pyvenv.cfg string.
    raise NotImplementedError("Level 4: Debug and fix generate_pyvenv_cfg")
