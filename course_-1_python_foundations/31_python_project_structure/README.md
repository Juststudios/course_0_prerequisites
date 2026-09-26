# Topic: Python Project Structure

Every Python developer starts by creating a single file named `script.py` or `main.py` and running it directly. But as your codebase expands—adding multiple modules, database models, agent tools, unit tests, configuration files, and external dependencies—a flat folder filled with miscellaneous scripts quickly becomes an unmaintainable disaster. Imports break mysteriously, tests accidentally import local development code rather than installed packages, and other developers cannot install or run your project.

In this module, you will learn how professional Python developers structure real-world repositories: the modern `src/` layout, `pyproject.toml` configuration according to modern standards (PEP 517/518/621), package exports with `__init__.py` and `__all__`, executable entry points with `__main__.py`, and testing directory conventions.

---

## What You Will Learn

- **Flat vs. `src/` Layouts**: Understand why the modern `src/` layout protects you from import traps and testing false positives.
- **The Modern Packaging Standard (`pyproject.toml`)**: How PEP 517, 518, and 621 replaced legacy `setup.py` and `requirements.txt` with a single, unified declarative configuration file.
- **Package Architecture with `__init__.py`**: How directories become importable Python packages and how to curate a clean public API using `__all__`.
- **Executable Modules with `__main__.py`**: How to enable command-line execution via `python -m my_package`.
- **Organizing Tests**: Why test suites belong in a dedicated `tests/` directory at the project root rather than inside your application package.
- **Console Script Entry Points**: How to configure CLI commands that users can execute directly in their terminal after installing your package.

---

## Prerequisites

Before starting this module, you should be familiar with:
- **Python Modules and Imports**: Using `import module` and `from package import member` (Module 12).
- **Files and Paths**: Working with file paths using `pathlib` (Module 11).
- **Basic Software Architecture**: Modularity and separation of concerns (Module 30).
- **Basic Command Line**: Navigating directories with `cd`, `ls`, and running `python script.py`.

---

## The Problem

Consider what happens when a beginner creates an AI agent project in a flat directory:

```text
my_agent/
├── agent.py
├── tools.py
├── memory.py
├── test_agent.py
├── math.py              <-- DANGER: Shadows Python's built-in 'math' library!
└── run.py
```

Three severe problems immediately arise:

1. **Namespace Shadowing**: The file `math.py` shadows the standard library `math` module. Any third-party library or standard module that attempts to `import math` will accidentally load your local file instead of CPython's math library, causing bizarre runtime crashes.
2. **Import Path Traps**: If you run `pytest` from inside `my_agent/`, Python automatically prepends the current working directory to `sys.path`. Your tests will import from the local folder, even if your package packaging is completely broken or uninstalled. You might deploy a broken package that passes tests on your machine but crashes for everyone else!
3. **Distribution Failure**: There is no standard metadata declaring what version of Python is required, which external packages (like `pydantic` or `httpx`) must be installed, or how to invoke the agent from the terminal.

---

## Key Terminology

- **Package**: A directory containing Python files and an `__init__.py` file (or a namespace package) that can be imported as a unified module.
- **`src/` Layout**: A repository structure where all installable application code is placed inside an isolated `src/` subfolder, keeping the root directory clean for build scripts, documentation, and tests.
- **`pyproject.toml`**: The standardized configuration file for Python projects defined in PEP 518 and PEP 621, consolidating metadata, dependencies, build tool settings, and linter configurations.
- **Build Backend**: A tool (such as `setuptools`, `hatchling`, `flit`, or `poetry`) that reads `pyproject.toml` and builds distributable `.tar.gz` source archives and `.whl` wheel packages.
- **`__init__.py`**: The package initialization file executed when a package or sub-package is imported.
- **`__all__`**: A special list of strings defined in a module or `__init__.py` that specifies exactly which symbols are exported when someone runs `from package import *`.
- **`__main__.py`**: A special file that allows a package or directory to be executed as a script using the `python -m <package_name>` flag.
- **Editable Install (`pip install -e .`)**: A development installation mode that links your live project source code into your Python environment so code changes take effect immediately without re-installing.

---

## Intuition

Think of structuring a Python project like organizing a physical manufacturing company:

- **The Factory Floor (`src/my_package/`)**: This is where the product is actually built. Only certified parts and finished sub-assemblies reside here.
- **The Blueprint & Company Registry (`pyproject.toml`)**: The legal documentation describing the company name, version, required raw materials (dependencies), and safety certificates.
- **The Quality Assurance Lab (`tests/`)**: Inspectors test the finished product rigorously. The QA lab is strictly separated from the manufacturing floor so that test gear is never shipped to customers.
- **The Loading Dock / Front Desk (`__init__.py` and `__all__`)**: When customers visit, they don't wander through the messy factory floor. They walk up to the reception desk, which hands them only the approved, public goods.
- **The Master Power Switch (`__main__.py`)**: The big button that turns on the facility for daily operations when someone issues a command.

---

## Concept

The modern gold standard for Python project architecture is the **`src/` layout**:

```text
my_awesome_project/
├── pyproject.toml              # Single source of truth for build & metadata
├── README.md                   # Human-readable project overview
├── LICENSE                     # Open-source or proprietary license
├── .gitignore                  # Files ignored by git (e.g., __pycache__, .venv)
├── src/
│   └── my_awesome_project/     # The actual importable package
│       ├── __init__.py         # Package initialization & public API exports
│       ├── __main__.py         # CLI entry point for `python -m my_awesome_project`
│       ├── core.py             # Internal domain logic
│       └── utils.py            # Helper routines
└── tests/                      # Dedicated test directory
    ├── conftest.py             # Pytest configuration and shared fixtures
    └── test_core.py            # Unit and integration tests
```

### Why the `src/` Layout Outperforms Flat Layouts

1. **Prevents Accidental Imports**: When you execute `python` from the root directory of a project with a flat layout (`my_awesome_project/` at root), Python places the current directory first on `sys.path`. Python can import your package even if it wasn't installed properly into your virtual environment. With `src/`, running from root prevents `import my_awesome_project` unless you have performed `pip install -e .`. This guarantees that your packaging works.
2. **Clean Root Directory**: Your top-level repository remains organized, containing only tooling configuration (`pyproject.toml`), documentation (`README.md`), and test suites.
3. **Prevents Packaging Pollutants**: Packaging tools won't accidentally bundle test files or scratch scripts into the production wheel distributed to users.

---

## Syntax

### Modern `pyproject.toml` (PEP 621 Standard)
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "hermes-agent"
version = "0.1.0"
description = "A lightweight autonomous tool-calling agent"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    { name = "Python Engineer", email = "engineer@example.com" }
]
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
hermes = "hermes_agent.__main__:cli_entry"
```

### Curating Exports with `__all__` in `src/hermes_agent/__init__.py`
```python
"""Hermes Agent Package."""

from hermes_agent.core import Agent, AgentConfig
from hermes_agent.tools import ToolRegistry

# Explicitly declare the public API:
__all__ = [
    "Agent",
    "AgentConfig",
    "ToolRegistry",
]

__version__ = "0.1.0"
```

### Enabling CLI Execution in `src/hermes_agent/__main__.py`
```python
"""Executed when running `python -m hermes_agent`."""
import sys

def cli_entry() -> None:
    print("Hermes Agent CLI is running!")
    # Parse CLI flags, instantiate agent, run loop

if __name__ == "__main__":
    cli_entry()
```

---

## Example

Here is a runnable simulation showing how Python's module resolution, `__all__` filtering, and project verification work under the hood:

```python
import sys
import tempfile
from pathlib import Path

# Programmatic demonstration of a verified src/ layout
def create_mock_project(root_path: Path) -> None:
    # 1. Create directory tree
    pkg_src = root_path / "src" / "sample_agent"
    pkg_tests = root_path / "tests"
    pkg_src.mkdir(parents=True, exist_ok=True)
    pkg_tests.mkdir(parents=True, exist_ok=True)

    # 2. Create pyproject.toml
    pyproject = root_path / "pyproject.toml"
    pyproject.write_text("""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "sample-agent"
version = "1.0.0"
dependencies = []
""", encoding="utf-8")

    # 3. Create package files
    init_file = pkg_src / "__init__.py"
    init_file.write_text("""\"\"\"Sample Agent Package.\"\"\"
__all__ = ["greet_agent"]

def greet_agent(name: str) -> str:
    return f"Hello, {name}! Welcome to Python Project Architecture."

def _private_helper():
    return "secret"
""", encoding="utf-8")

    main_file = pkg_src / "__main__.py"
    main_file.write_text("""from sample_agent import greet_agent
import sys

if __name__ == "__main__":
    print(greet_agent("CLI User"))
""", encoding="utf-8")

    test_file = pkg_tests / "test_agent.py"
    test_file.write_text("""from sample_agent import greet_agent

def test_greeting():
    assert "Hello" in greet_agent("Tester")
""", encoding="utf-8")

# Run verification
with tempfile.TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)
    create_mock_project(root)

    print("Created mock project structure at:", root)
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root)
            print(f"  {rel} ({p.stat().st_size} bytes)")

    # Simulate importing the package dynamically
    sys.path.insert(0, str(root / "src"))
    try:
        import sample_agent
        print("\nImported sample_agent successfully!")
        print("Exported public symbols:", sample_agent.__all__)
        print("Greeting output:", sample_agent.greet_agent("Ada"))
    finally:
        sys.path.remove(str(root / "src"))
```

---

## Line-by-Line Explanation

- **Lines 8–15 (`create_mock_project`)**: Uses Python's `pathlib.Path` to construct the standard directory structure: `src/sample_agent/` and `tests/`.
- **Lines 17–26 (`pyproject.toml`)**: Writes a PEP 621 compliant configuration defining the build backend and project metadata.
- **Lines 28–38 (`__init__.py`)**: Defines `__all__ = ["greet_agent"]`. Only `greet_agent` will be imported if a user writes `from sample_agent import *`. The internal `_private_helper` is properly encapsulated.
- **Lines 40–46 (`__main__.py`)**: Implements the module entry point so running `python -m sample_agent` executes this script.
- **Lines 48–53 (`test_agent.py`)**: Locates tests under `tests/`, ensuring test scripts are decoupled from package source code.
- **Lines 56–73 (`TemporaryDirectory` run)**: Demonstrates that appending `src/` to `sys.path` allows importing `sample_agent` cleanly, validating the complete architecture.

---

## What Python Is Doing

When you structure and run a Python project:

1. **Module Resolution (`sys.path`)**: When you invoke `import foo`, Python checks built-in modules first, then iterates through each directory in `sys.path` in order. The first directory containing a folder named `foo` with an `__init__.py` (or a `foo.py` file) wins.
2. **Namespace Creation**: When a directory with `__init__.py` is imported, Python executes the code inside `__init__.py` within a new module namespace. Any variables or functions defined in `__init__.py` become module attributes (accessible as `package.attribute`).
3. **Execution Mode (`__main__.py`)**: When you invoke `python -m my_pkg`, Python finds `my_pkg` on `sys.path`, loads it, and immediately looks for a top-level file named `__main__.py`. If found, it executes `__main__.py` with the special attribute `__name__` set to `"__main__"`.
4. **Editable Links**: When you run `pip install -e .`, pip creates a `.pth` file in your environment's `site-packages` that points directly to your project's `src/` directory. No code is copied, enabling instantaneous updates during active development.

---

## Common Mistakes

### 1. Using Legacy `setup.py` for New Projects
Do not write complex, executable `setup.py` scripts for basic packaging. Modern Python uses declarative `pyproject.toml` files, which are parsed safely without executing arbitrary Python code during installation.

### 2. Putting Tests Inside `src/`
```text
# BAD: Tests get packaged and distributed in production wheels
src/
└── my_pkg/
    ├── core.py
    └── test_core.py  <-- WRONG!

# GOOD: Tests live in a root-level tests/ folder
src/
└── my_pkg/
    └── core.py
tests/
└── test_core.py
```

### 3. Missing `__init__.py` in Sub-packages
While Python 3.3+ supports implicit namespace packages without `__init__.py`, regular packages should always include an `__init__.py` file to explicitly define package boundaries, declare version strings, and control public API exports.

### 4. Forgetting to Specify `requires-python`
Always declare `requires-python = ">=3.10"` in `pyproject.toml`. If a user attempts to install your project on an obsolete Python version (like 3.7) that lacks modern type syntax, pip will abort early with a helpful error message instead of failing during execution.

---

## Real-World Uses

- **Requests, FastAPI, Pytest, Pydantic**: Every major modern open-source Python library utilizes the `src/` layout and `pyproject.toml` packaging architecture.
- **Microservices and Monorepos**: Production enterprise backends organize dozens of microservices, each with its own clean `pyproject.toml` and independent virtual environment.
- **CLI Development Tools**: Tools like `ruff`, `black`, and `mypy` use `[project.scripts]` in `pyproject.toml` so users can simply type `ruff check .` in their shell.

---

## Connection to AI Agents

AI Agent development requires rock-solid project structure for four key reasons:

1. **Tool Modularization**: As an agent acquires 20+ specialized tools (SQL execution, web search, code compilation), tools should be organized into a sub-package like `src/agent/tools/` with an `__init__.py` registering and exporting them.
2. **CLI & Headless Agent Runners**: Running an agent daemon in Docker or cloud containers typically uses `python -m my_agent --config prod.json`, which depends directly on `__main__.py`.
3. **Packaging Agents for Team Collaboration**: When building agentic workflows in a company, team members install the agent core via `pip install -e .` so they can build custom agents on top of shared primitives.
4. **Isolated Test Harnesses**: Testing agent decision loops requires mocking LLM API calls and testing against deterministic fixtures in `tests/conftest.py`.

---

## Practice

1. Write a Python function `inspect_package_tree(root_dir: Path) -> dict` that recursively crawls a directory and categorizes files into `source_files`, `test_files`, and `config_files`.
2. Create a minimal `pyproject.toml` string template containing placeholders for `{project_name}`, `{version}`, and `{author_email}`.
3. Write a small package containing two modules (`calculator.py` and `formatter.py`). In `__init__.py`, export only the `calculate` function, hiding all formatting functions from wildcard imports.

---

## Challenge

Build an **Automated Project Structure Validator**:
1. Implement a class `ProjectStructureValidator` that accepts a project root directory path.
2. Verify that:
   - `pyproject.toml` exists and contains required sections (`[build-system]` and `[project]`).
   - `src/` directory exists and contains at least one package folder with an `__init__.py`.
   - `tests/` directory exists at the root level and contains at least one file starting with `test_`.
   - No `.pyc` files or `__pycache__` directories are committed directly in the source tree.
3. Return a detailed validation report indicating whether the repository passes the modern Python packaging standard.

---

## Summary

- **`src/` layout is standard**: It separates your installable package from testing, tooling, and documentation, preventing import path bugs.
- **`pyproject.toml` is the single source of truth**: It unifies build backend declaration, dependencies, and metadata.
- **`__init__.py` defines the public surface**: Use `__all__` to make your public API clear and deliberate.
- **`__main__.py` powers command-line invocation**: Enables `python -m your_package` for seamless CLI execution.
- **Separation of tests**: Keep tests in a dedicated root-level `tests/` folder.

---

## What You Should Know Before Moving On

Before proceeding to Module 32, make sure you can:
- Explain why the `src/` layout prevents importing uninstalled local code during testing.
- Write a basic PEP 621 compliant `pyproject.toml` from memory.
- Explain the role of `__init__.py` and the `__all__` list in controlling what gets exported from a package.
- Describe how `__main__.py` enables running a package with `python -m`.