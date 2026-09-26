"""
Module 23: Virtual Environments in Python
=========================================

This comprehensive lesson covers the mechanics, internal structure, and
practical management of Python virtual environments.

A virtual environment is a self-contained directory tree that isolates a
specific Python interpreter, its standard library links, and a dedicated
`site-packages` directory for third-party dependencies.

Key Topics Explored:
--------------------
1. Inspecting the running Python environment (`sys.prefix`, `sys.base_prefix`).
2. Detecting whether Python is executing inside an active virtual environment.
3. Programmatically creating and configuring an isolated environment via `venv`.
4. Anatomy of `pyvenv.cfg` and environment layout.
5. Parsing and validating `requirements.txt` dependency specifications.
6. Dependency conflict detection (how package managers avoid dependency hell).
7. How AI agents utilize virtual environment sandboxing for tool execution.
"""

import os
import sys
import tempfile
import shutil
import venv
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============================================================================
# Section 1: Inspecting the Current Python Environment
# ============================================================================

def inspect_current_environment() -> Dict[str, object]:
    """
    Examines Python runtime variables to determine the active environment details.
    
    Returns a dictionary of key runtime diagnostic metrics.
    """
    # sys.prefix: The directory prefix where platform-independent Python files
    # are installed. In a virtual environment, this points to the virtualenv root.
    prefix = sys.prefix
    
    # sys.base_prefix: The directory prefix of the underlying base installation.
    # If not running in a virtualenv, base_prefix equals prefix.
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    
    # sys.executable: The absolute path to the binary interpreter currently running.
    executable = sys.executable
    
    # Check if the current interpreter is running inside a virtual environment.
    is_virtual = prefix != base_prefix
    
    # Search for pyvenv.cfg in prefix or its parent directories
    cfg_file = Path(prefix) / "pyvenv.cfg"
    has_cfg = cfg_file.is_file()
    
    info = {
        "executable": executable,
        "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "prefix": prefix,
        "base_prefix": base_prefix,
        "is_virtual_env": is_virtual,
        "has_pyvenv_cfg": has_cfg,
        "sys_path_entries_count": len(sys.path),
    }
    return info


def print_environment_report() -> None:
    """Prints a human-readable diagnostic report of the active environment."""
    info = inspect_current_environment()
    print("=" * 68)
    print("        PYTHON RUNTIME ENVIRONMENT DIAGNOSTIC REPORT")
    print("=" * 68)
    print(f"  Python Version     : {info['version']}")
    print(f"  Python Executable  : {info['executable']}")
    print(f"  Active Prefix      : {info['prefix']}")
    print(f"  Base Prefix        : {info['base_prefix']}")
    print(f"  Virtual Env Active : {info['is_virtual_env']}")
    print(f"  Found pyvenv.cfg   : {info['has_pyvenv_cfg']}")
    print(f"  Search Path Count  : {info['sys_path_entries_count']} directories")
    print("-" * 68)
    print("Sample sys.path directories (first 3 entries):")
    for i, path_entry in enumerate(sys.path[:3], start=1):
        print(f"    [{i}] {path_entry}")
    print("=" * 68 + "\n")


# ============================================================================
# Section 2: Programmatic Creation of a Virtual Environment
# ============================================================================

def create_transient_virtualenv(target_dir: Path) -> Dict[str, str]:
    """
    Demonstrates creating a virtual environment programmatically using Python's
    built-in `venv.EnvBuilder`.
    
    This is the exact technique autonomous AI agents use to build ephemeral
    sandboxes for testing user code or executing isolated tools.
    """
    print(f"[*] Building isolated virtual environment at: {target_dir}")
    
    # EnvBuilder allows customized environment construction:
    # - system_site_packages: False ensures no leakage from host global packages.
    # - clear: True cleans the target directory if it already exists.
    # - with_pip: False here for lightning-fast lightweight sandbox creation.
    builder = venv.EnvBuilder(
        system_site_packages=False,
        clear=True,
        symlinks=(os.name != "nt"),  # Use symlinks on Unix for speed and disk savings
        with_pip=False,
    )
    
    builder.create(str(target_dir))
    
    # Read the generated pyvenv.cfg
    cfg_path = target_dir / "pyvenv.cfg"
    config_data: Dict[str, str] = {}
    if cfg_path.is_file():
        with open(cfg_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    config_data[key.strip()] = val.strip()
                    
    return config_data


def audit_virtualenv_structure(venv_path: Path) -> None:
    """
    Walks the directory structure of a created virtual environment to inspect
    its architectural layout.
    """
    print("\n--- Virtual Environment Directory Layout ---")
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    expected_dirs = [bin_dir, "include", "lib"]
    
    for d in expected_dirs:
        sub = venv_path / d
        exists = sub.is_dir()
        print(f"  [Directory] {d:<12} : {'Present' if exists else 'Missing'} ({sub})")
        
    cfg = venv_path / "pyvenv.cfg"
    print(f"  [File]      pyvenv.cfg   : {'Present' if cfg.is_file() else 'Missing'}")


# ============================================================================
# Section 3: Dependency Specification & Version Parsing
# ============================================================================

class Requirement:
    """
    Represents a parsed package requirement specification, such as:
      - 'requests==2.31.0'
      - 'numpy>=1.24.0'
      - 'pydantic<2.0.0'
      - 'click'
    """
    SUPPORTED_OPERATORS = ("==", ">=", "<=", ">", "<", "!=", "~=")
    
    def __init__(self, raw_line: str):
        self.raw_line = raw_line.strip()
        self.name: str = ""
        self.operator: Optional[str] = None
        self.version: Optional[str] = None
        self._parse()

    def _parse(self) -> None:
        # Strip comments like: requests>=2.0 # for network calls
        line = self.raw_line.split("#")[0].strip()
        if not line:
            return
            
        # Find if any operator is present
        matched_op = None
        for op in self.SUPPORTED_OPERATORS:
            if op in line:
                matched_op = op
                break
                
        if matched_op:
            parts = line.split(matched_op, 1)
            self.name = parts[0].strip().lower().replace("_", "-")
            self.operator = matched_op
            self.version = parts[1].strip()
        else:
            # Unconstrained package, e.g. "click"
            self.name = line.strip().lower().replace("_", "-")
            self.operator = None
            self.version = None

    def __repr__(self) -> str:
        if self.operator and self.version:
            return f"Requirement({self.name} {self.operator} {self.version})"
        return f"Requirement({self.name} [any version])"


def parse_version_tuple(ver_str: str) -> Tuple[int, ...]:
    """Converts a semantic version string like '2.31.0' to a numeric tuple (2, 31, 0)."""
    parts = []
    for part in ver_str.split("."):
        clean_part = "".join(filter(str.isdigit, part))
        if clean_part:
            parts.append(int(clean_part))
    return tuple(parts)


def check_version_satisfaction(installed_version: str, req: Requirement) -> bool:
    """
    Evaluates whether an installed package version satisfies a requirement constraint.
    """
    if not req.operator or not req.version:
        return True
        
    inst_v = parse_version_tuple(installed_version)
    req_v = parse_version_tuple(req.version)
    
    if req.operator == "==":
        return inst_v == req_v
    elif req.operator == ">=":
        return inst_v >= req_v
    elif req.operator == "<=":
        return inst_v <= req_v
    elif req.operator == ">":
        return inst_v > req_v
    elif req.operator == "<":
        return inst_v < req_v
    elif req.operator == "!=":
        return inst_v != req_v
    return True


# ============================================================================
# Section 4: Conflict Resolution in Virtual Environments
# ============================================================================

def detect_dependency_conflicts(
    project_a_requirements: List[str],
    project_b_requirements: List[str],
) -> List[str]:
    """
    Detects packages where two projects have incompatible exact version pins (==),
    illustrating why each project requires its own independent virtual environment.
    """
    conflicts = []
    reqs_a = {r.name: r for r in [Requirement(line) for line in project_a_requirements] if r.name}
    reqs_b = {r.name: r for r in [Requirement(line) for line in project_b_requirements] if r.name}
    
    common_packages = set(reqs_a.keys()) & set(reqs_b.keys())
    
    for pkg in sorted(common_packages):
        ra = reqs_a[pkg]
        rb = reqs_b[pkg]
        if ra.operator == "==" and rb.operator == "==" and ra.version != rb.version:
            conflicts.append(
                f"Conflict on '{pkg}': Project A pins {ra.version}, but Project B pins {rb.version}"
            )
            
    return conflicts


# ============================================================================
# Section 5: Demonstration & Interactive Walkthrough
# ============================================================================

def main() -> None:
    """Executes the full pedagogical demonstration of virtual environments."""
    print("Starting Module 23 Virtual Environments Demonstration...\n")
    
    # 1. Inspect the host environment
    print_environment_report()
    
    # 2. Programmatically create a temporary sandbox virtual environment
    temp_dir = Path(tempfile.mkdtemp(prefix="agent_venv_sandbox_"))
    try:
        cfg = create_transient_virtualenv(temp_dir)
        audit_virtualenv_structure(temp_dir)
        print("\n--- Parsed pyvenv.cfg Settings ---")
        for k, v in cfg.items():
            print(f"  {k} = {v}")
    finally:
        # Cleanup transient sandbox
        print(f"\n[*] Cleaning up transient sandbox at: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("[+] Cleanup complete.")

    # 3. Simulate dependency isolation and conflict detection
    print("\n" + "=" * 68)
    print("      DEPENDENCY CONFLICT SIMULATION (THE 'WHY VENV' PROOF)")
    print("=" * 68)
    
    proj_agent_v1 = [
        "requests==2.28.1",
        "pydantic==1.10.8",
        "aiohttp>=3.8.0",
    ]
    
    proj_agent_v2 = [
        "requests==2.31.0",
        "pydantic==2.5.2",
        "aiohttp>=3.8.0",
    ]
    
    print("Project A Requirements (Legacy Agent):")
    for r in proj_agent_v1:
        print(f"  - {r}")
        
    print("\nProject B Requirements (Modern Agent):")
    for r in proj_agent_v2:
        print(f"  - {r}")
        
    conflicts = detect_dependency_conflicts(proj_agent_v1, proj_agent_v2)
    print("\nDetected Conflicts if installed into the same global environment:")
    for c in conflicts:
        print(f"  [!] {c}")
        
    print("\nSolution: Each project must have its own dedicated virtual environment:")
    print("  -> Project A:  python3 -m venv .venv_agent_v1")
    print("  -> Project B:  python3 -m venv .venv_agent_v2")
    print("=" * 68)
    print("Module 23 demonstration completed successfully!\n")


if __name__ == "__main__":
    main()
