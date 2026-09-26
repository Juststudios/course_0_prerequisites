"""
Module 23 Solutions: Virtual Environments
=========================================

Reference solutions for all 4 exercise levels.
"""

from typing import Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

def is_in_virtual_environment(prefix: str, base_prefix: str) -> bool:
    """Checks if running within an isolated virtual environment."""
    return prefix != base_prefix


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

def parse_requirement(raw_line: str) -> Tuple[str, str, str]:
    """
    Parses a requirement specification line into (name, operator, version).
    """
    # 1. Strip inline comments and outer whitespace
    clean_line = raw_line.split("#")[0].strip()
    if not clean_line:
        return ("", "", "")
        
    # Supported comparison operators ordered by length descending to match multi-char first
    operators = ("==", ">=", "<=", "!=", "~=", ">", "<")
    
    for op in operators:
        if op in clean_line:
            parts = clean_line.split(op, 1)
            name = parts[0].strip().lower().replace("_", "-")
            version = parts[1].strip()
            return (name, op, version)
            
    # If no operator is found, the line is just a package name
    name = clean_line.strip().lower().replace("_", "-")
    return (name, "", "")


# ============================================================================
# Level 3: Build Solution
# ============================================================================

def find_conflicting_packages(
    reqs1: List[str], reqs2: List[str]
) -> Dict[str, Tuple[str, str]]:
    """
    Builds a conflict detector identifying exact-pinned version mismatches.
    """
    # Parse requirements from list 1
    pinned1: Dict[str, str] = {}
    for line in reqs1:
        name, op, ver = parse_requirement(line)
        if name and op == "==" and ver:
            pinned1[name] = ver
            
    # Parse requirements from list 2
    pinned2: Dict[str, str] = {}
    for line in reqs2:
        name, op, ver = parse_requirement(line)
        if name and op == "==" and ver:
            pinned2[name] = ver
            
    conflicts: Dict[str, Tuple[str, str]] = {}
    for pkg, ver1 in pinned1.items():
        if pkg in pinned2:
            ver2 = pinned2[pkg]
            if ver1 != ver2:
                conflicts[pkg] = (ver1, ver2)
                
    return conflicts


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

def generate_pyvenv_cfg(
    home_dir: str,
    python_version: str,
    include_system_site_packages: bool = False,
) -> str:
    """
    Generates standard pyvenv.cfg contents with correct keys and casing.
    """
    site_packages_str = "true" if include_system_site_packages else "false"
    lines = [
        f"home = {home_dir}",
        f"include-system-site-packages = {site_packages_str}",
        f"version = {python_version}",
    ]
    return "\n".join(lines)


# ============================================================================
# Verification Tests
# ============================================================================

def run_tests() -> None:
    print("Running Module 23 Verification Tests...")
    
    # Level 1 test
    assert not is_in_virtual_environment("/usr", "/usr"), "Failed L1: identical prefixes"
    assert is_in_virtual_environment("/path/to/.venv", "/usr"), "Failed L1: distinct prefixes"
    print("  [✓] Level 1 (Recall) passed.")
    
    # Level 2 test
    assert parse_requirement("Requests >= 2.28.0 # comment") == ("requests", ">=", "2.28.0")
    assert parse_requirement("click") == ("click", "", "")
    assert parse_requirement("# pure comment") == ("", "", "")
    assert parse_requirement("  my_tool_pkg == 1.5.0 ") == ("my-tool-pkg", "==", "1.5.0")
    print("  [✓] Level 2 (Modify) passed.")
    
    # Level 3 test
    r1 = ["requests==2.28.0", "pydantic==1.10.8", "urllib3>=1.26.0"]
    r2 = ["requests==2.31.0", "pydantic==1.10.8", "fastapi==0.100.0"]
    conflicts = find_conflicting_packages(r1, r2)
    assert conflicts == {"requests": ("2.28.0", "2.31.0")}, f"Unexpected conflicts: {conflicts}"
    print("  [✓] Level 3 (Build) passed.")
    
    # Level 4 test
    cfg = generate_pyvenv_cfg("/usr/bin", "3.12.3", False)
    assert "home = /usr/bin" in cfg
    assert "include-system-site-packages = false" in cfg
    assert "version = 3.12.3" in cfg
    print("  [✓] Level 4 (Debug) passed.")
    
    print("All Module 23 exercise solutions verified successfully!\n")


if __name__ == "__main__":
    run_tests()
