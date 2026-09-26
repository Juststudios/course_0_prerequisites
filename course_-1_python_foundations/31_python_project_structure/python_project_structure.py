"""
Module 31: Python Project Structure
===================================
A deep-dive tutorial demonstrating professional Python project organization,
modern packaging standards, and execution lifecycles:
  1. The Standard `src/` Layout Architecture
  2. PEP 621 Compliant `pyproject.toml` Generation & Validation
  3. Package Boundaries and Export Control via `__init__.py` and `__all__`
  4. Executable CLI Packages via `__main__.py` and Entry Points
  5. Dynamic Temporary Package Lifecycle Simulation & Verification

Modern Python packaging has moved away from executable `setup.py` scripts and
ad-hoc directory layouts. Today, reproducible, robust software uses declarative
configuration files and clean boundary separations.
"""

from typing import Any
from pathlib import Path
import sys
import tempfile
import importlib


# =====================================================================
# 1. THE STANDARD `src/` LAYOUT ARCHITECTURE
# =====================================================================
# Why src/ layout?
# In a flat layout, 'import my_pkg' can succeed from the repository root
# even if the package was never installed in the virtual environment.
# The src/ layout forces explicit installation (or explicit sys.path modification),
# preventing testing false positives where tests pass locally but fail in production.

SAMPLE_PROJECT_TREE = """
my_agent_system/
├── pyproject.toml              # Build & dependency metadata (PEP 517/518/621)
├── README.md                   # Human-readable documentation
├── LICENSE                     # Software license
├── .gitignore                  # Git exclusion rules
├── src/                        # Isolated application source directory
│   └── my_agent/               # The importable package folder
│       ├── __init__.py         # Marks package and defines public exports
│       ├── __main__.py         # CLI entry point for `python -m my_agent`
│       ├── core.py             # Agent orchestrator and state engine
│       ├── config.py           # Settings and environment loader
│       └── tools/              # Sub-package for agent tools
│           ├── __init__.py     # Tool registry and export list
│           ├── calculator.py   # Math operations
│           └── search.py       # Knowledge retrieval
└── tests/                      # Dedicated test suite (NOT shipped in wheel)
    ├── conftest.py             # Shared pytest fixtures
    ├── test_core.py            # Unit tests for core engine
    └── test_tools.py           # Unit tests for tools
"""


def render_project_tree() -> None:
    """Prints the pedagogical directory structure."""
    print("-" * 65)
    print("CANONICAL PYTHON PROJECT STRUCTURE (`src/` LAYOUT):")
    print(SAMPLE_PROJECT_TREE.strip())
    print("-" * 65)


# =====================================================================
# 2. DECLARATIVE PACKAGING WITH `pyproject.toml`
# =====================================================================
# PEP 518 introduced pyproject.toml for build-tool requirements.
# PEP 621 standardized project metadata (name, version, dependencies).

def generate_pyproject_toml(
    project_name: str,
    version: str,
    description: str,
    dependencies: list[str],
    cli_entry_point: str | None = None,
) -> str:
    """
    Generates a standardized, PEP 621 compliant pyproject.toml string.
    """
    dep_lines = ",\n    ".join(f'"{d}"' for d in dependencies)
    dep_section = f"[\n    {dep_lines}\n]" if dependencies else "[]"

    scripts_block = ""
    if cli_entry_point:
        # CLI command registration under [project.scripts]
        command_name = project_name.replace("-", "_")
        scripts_block = f"""
[project.scripts]
{command_name} = "{cli_entry_point}"
"""

    content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "{version}"
description = "{description}"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    {{ name = "Course -1 Engineer", email = "student@example.com" }}
]
dependencies = {dep_section}
{scripts_block}
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
"""
    return content.strip() + "\n"


def parse_metadata_summary(toml_content: str) -> dict[str, Any]:
    """
    Minimal parser extracting top-level project metadata for validation.
    """
    summary: dict[str, Any] = {}
    for line in toml_content.splitlines():
        line = line.strip()
        if line.startswith("name ="):
            summary["name"] = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("version ="):
            summary["version"] = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("requires-python ="):
            summary["requires_python"] = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("build-backend ="):
            summary["build_backend"] = line.split("=", 1)[1].strip().strip('"')
    return summary


# =====================================================================
# 3. PACKAGE EXPORT CONTROL: `__init__.py` AND `__all__`
# =====================================================================
# In Python, an __init__.py file signals that a directory is an importable package.
# Setting __all__ defines the public API of that package, preventing internal
# helper functions or third-party modules from leaking during wildcard imports.

INIT_PY_TEMPLATE = '''"""
Agent Core Package
==================
Public API for the agent runtime.
"""

from .core import Agent, AgentConfig
from .tools import CalculatorTool

# Explicitly define the symbols exported by this package
__all__ = [
    "Agent",
    "AgentConfig",
    "CalculatorTool",
]

__version__ = "1.0.0"
'''


# =====================================================================
# 4. EXECUTABLE MODULES: `__main__.py`
# =====================================================================
# When a user runs `python -m <package_name>`, Python locates <package_name>
# on sys.path and executes the code inside `__main__.py`.

MAIN_PY_TEMPLATE = '''"""
CLI Entry Point
================
Invoked when executing: python -m my_agent
"""
import sys

def main() -> int:
    print("[CLI] Welcome to My Agent CLI Runner!")
    print("[CLI] Agent successfully initialized from __main__.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


# =====================================================================
# 5. DYNAMIC EPHEMERAL PACKAGE LIFECYCLE SIMULATION
# =====================================================================
# To demonstrate project structure without polluting the user's filesystem,
# we construct a complete, valid Python project inside a temporary directory,
# add its src/ folder to sys.path, import it dynamically, verify its exports,
# and execute its components.

def run_project_structure_simulation() -> None:
    print("=" * 70)
    print("MODULE 31: PROJECT STRUCTURE & PACKAGING IN ACTION")
    print("=" * 70)

    # 1. Render layout reference
    render_project_tree()

    # 2. Generate pyproject.toml
    print("\n[Step 1] Generating Modern PEP 621 pyproject.toml...")
    pyproject_str = generate_pyproject_toml(
        project_name="nova-agent",
        version="0.2.0",
        description="Autonomous AI Agent Core Framework",
        dependencies=["pydantic>=2.0.0", "sqlite3"],
        cli_entry_point="nova_agent.__main__:main",
    )
    metadata = parse_metadata_summary(pyproject_str)
    print("    Parsed Metadata:")
    for k, v in metadata.items():
        print(f"      - {k:<18}: {v}")

    # 3. Create Ephemeral Project on Disk
    print("\n[Step 2] Creating Ephemeral `src/` Layout Package in Temp Directory...")
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        src_dir = temp_dir / "src" / "nova_agent"
        tests_dir = temp_dir / "tests"

        src_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        # Write pyproject.toml
        (temp_dir / "pyproject.toml").write_text(pyproject_str, encoding="utf-8")

        # Write README.md
        (temp_dir / "README.md").write_text("# Nova Agent Framework\nProduction-ready agent.", encoding="utf-8")

        # Write src/nova_agent/core.py
        core_py = """
class AgentConfig:
    def __init__(self, name: str = 'Nova'):
        self.name = name

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config

    def status(self) -> str:
        return f"Agent {self.config.name!r} is healthy and active."

def _secret_helper():
    return "This should NEVER be in __all__"
"""
        (src_dir / "core.py").write_text(core_py.strip(), encoding="utf-8")

        # Write src/nova_agent/__init__.py with curated __all__
        init_py = """\"\"\"Nova Agent Package.\"\"\"
from .core import Agent, AgentConfig

__all__ = ["Agent", "AgentConfig"]
__version__ = "0.2.0"
"""
        (src_dir / "__init__.py").write_text(init_py.strip(), encoding="utf-8")

        # Write src/nova_agent/__main__.py
        (src_dir / "__main__.py").write_text(MAIN_PY_TEMPLATE.strip(), encoding="utf-8")

        # Write tests/test_agent.py
        test_py = """
from nova_agent import Agent, AgentConfig

def test_agent_status():
    cfg = AgentConfig("TestBot")
    bot = Agent(cfg)
    assert bot.status() == "Agent 'TestBot' is healthy and active."
"""
        (tests_dir / "test_agent.py").write_text(test_py.strip(), encoding="utf-8")

        print(f"    Constructed directory tree at: {temp_dir.name}")
        for p in sorted(temp_dir.rglob("*")):
            if p.is_file():
                rel = p.relative_to(temp_dir)
                print(f"      └── {str(rel):<35} ({p.stat().st_size} bytes)")

        # 4. Dynamic Import & Verification
        print("\n[Step 3] Dynamically Importing Package via sys.path...")
        sys_src_path = str(temp_dir / "src")
        sys.path.insert(0, sys_src_path)

        try:
            # Import newly created package
            nova_pkg = importlib.import_module("nova_agent")
            print(f"    Successfully imported module: {nova_pkg.__name__}")
            print(f"    Package version: {getattr(nova_pkg, '__version__', 'N/A')}")
            print(f"    Public __all__ exports: {getattr(nova_pkg, '__all__', [])}")

            # Instantiate exported class
            AgentClass = getattr(nova_pkg, "Agent")
            ConfigClass = getattr(nova_pkg, "AgentConfig")

            cfg = ConfigClass(name="Sentinel-9")
            agent = AgentClass(cfg)
            print(f"    Agent instance call: {agent.status()}")

            # 5. Verify Encapsulation (__all__ isolation)
            print("\n[Step 4] Verifying Encapsulation Boundaries...")
            assert "Agent" in nova_pkg.__all__
            assert "AgentConfig" in nova_pkg.__all__
            assert "_secret_helper" not in nova_pkg.__all__
            print("    [✓] Internal helper correctly excluded from public API (__all__).")

            # 6. Verify CLI Entry Point execution
            print("\n[Step 5] Simulating CLI Entry Point (__main__.py)...")
            main_module = importlib.import_module("nova_agent.__main__")
            exit_code = main_module.main()
            assert exit_code == 0
            print(f"    [✓] CLI main() executed successfully with returncode {exit_code}.")

        finally:
            # Clean up sys.path and sys.modules to keep global state pristine
            if sys_src_path in sys.path:
                sys.path.remove(sys_src_path)
            for mod_name in list(sys.modules.keys()):
                if mod_name.startswith("nova_agent"):
                    del sys.modules[mod_name]

    print("\n" + "=" * 70)
    print("PROJECT STRUCTURE SUMMARY:")
    print("  - The `src/` layout isolated production code from tests and tools.")
    print("  - `pyproject.toml` standardized build-system and dependencies.")
    print("  - `__init__.py` and `__all__` cleanly defined the public boundary.")
    print("  - `__main__.py` enabled seamless `python -m` execution.")
    print("=" * 70)


def main() -> None:
    run_project_structure_simulation()


if __name__ == "__main__":
    main()
