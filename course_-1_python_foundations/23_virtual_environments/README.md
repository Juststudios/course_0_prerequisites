# Topic: Virtual Environments in Python

## What You Will Learn
In this module, you will learn:
- Why virtual environments are essential in modern Python development and agent engineering.
- The fundamental difference between global Python installations and isolated project environments.
- How Python locates installed libraries using `sys.path`, `sys.prefix`, and `sys.base_prefix`.
- The internal structure of a virtual environment: the `pyvenv.cfg` configuration file, the `bin` (or `Scripts`) directory, and the `site-packages` directory.
- How to create, activate, and manage virtual environments using the built-in `venv` module.
- How to capture, lock, and install project dependencies using `pip` and `requirements.txt`.
- How autonomous AI agents use virtual environments as execution sandboxes to safely run untrusted code and avoid dependency conflicts.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 11: File operations and directory paths in Python.
- Module 12: Modules, packages, and how `import` statements find libraries.
- Basic command-line interface (CLI) navigation (e.g., `cd`, `ls` or `dir`).

## The Problem
When you first learn Python, installing a third-party library seems simple: you open a terminal and run `pip install requests` or `pip install openai`. The package installs directly into your global, system-wide Python environment.

At first, this works. But as you build more projects, problems emerge:
1. **Conflicting Dependencies**: Project A requires `pydantic<2.0.0` because an older SDK hasn't been updated. Project B requires `pydantic>=2.5.0` for its modern validation speed. On a single global Python installation, only one version of `pydantic` can exist in `site-packages`. Upgrading for Project B instantly breaks Project A.
2. **Polluting System Python**: On Unix-like operating systems (Linux, macOS), system utilities (like package managers or desktop tools) depend on the system Python. Messing with system packages can break OS functionality.
3. **Inability to Replicate**: When you share your code with a colleague, deploy to a cloud server, or give an AI agent a sandbox, you cannot easily tell which of the 150 packages in your global environment are actually needed by your project.

## Key Terminology
- **Virtual Environment (`venv`)**: An isolated, self-contained directory tree that contains a specific Python interpreter and its own independent set of installed libraries.
- **Global / System Python**: The primary Python installation provided by your operating system or system installer, shared across all users and applications unless isolated.
- **`site-packages`**: The specific directory on the filesystem where Python stores third-party libraries installed via `pip`.
- **`sys.prefix`**: A built-in Python string variable pointing to the root directory of the currently active Python environment.
- **`sys.base_prefix`**: A built-in Python string variable pointing to the root directory of the base (original) Python installation from which the virtual environment was created.
- **`pyvenv.cfg`**: A small metadata configuration file located at the root of every virtual environment that tells the Python executable where the base installation lives.
- **Activation Script**: A shell script (such as `bin/activate` on Linux/macOS or `Scripts/activate.bat` on Windows) that temporarily alters your shell's `PATH` environment variable so that running `python` invokes the virtual environment's executable.
- **Dependency Pinning**: The practice of locking package versions in a manifest file (like `requirements.txt` or `pyproject.toml`) to guarantee reproducible behavior across machines.

## Intuition
Think of your computer as a professional shared kitchen.
- The **Global Python** is the common pantry. If Chef Alice puts a gallon of spicy hot sauce into the only communal soup pot, Chef Bob's delicate vanilla custard is ruined.
- A **Virtual Environment** is a private, dedicated prep station for a single recipe. Chef Alice gets her own workbench with her own hot sauce, and Chef Bob gets his own workbench with his own vanilla bean. Neither chef can contaminate the other's ingredients, and when a dish is finished, its entire workbench can be wiped clean or recreated instantly using the written recipe (`requirements.txt`).

## Concept
A Python virtual environment is **not a heavy virtual machine** like Docker or VirtualBox. It does not emulate hardware or duplicate the operating system.

Instead, a virtual environment is an ingenious directory structure containing:
1. A small `pyvenv.cfg` file pointing back to the real system Python binary.
2. Symbolic links (or small copy shims) to the system Python binary in a `bin/` (or `Scripts/`) directory.
3. A private `lib/pythonX.Y/site-packages/` folder.

When you run Python from within this directory, Python initializes its runtime by checking for the existence of `pyvenv.cfg` in its parent directory. If found:
- `sys.prefix` is set to the virtual environment directory.
- `sys.base_prefix` remains set to the underlying global Python directory.
- Python prepends the virtual environment's `site-packages` directory to `sys.path`.
- Third-party packages installed via `pip install` are written directly into this private folder!

## Syntax
Creating and managing virtual environments from your terminal:

```bash
# 1. Create a virtual environment named '.venv'
python3 -m venv .venv

# 2. Activate the virtual environment:
# On Linux / macOS:
source .venv/bin/activate

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 3. Verify which Python interpreter is active:
which python    # Linux/macOS
where python    # Windows

# 4. Install dependencies inside the isolated environment:
pip install requests==2.31.0

# 5. Export installed dependencies:
pip freeze > requirements.txt

# 6. Install dependencies from a requirements file:
pip install -r requirements.txt

# 7. Deactivate and return to your system shell:
deactivate
```

In Python code, you can inspect environment isolation programmatically:
```python
import sys

# Detect if currently running inside a virtual environment
in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
print(f"Inside virtual environment: {in_venv}")
print(f"Current Environment Prefix: {sys.prefix}")
print(f"Base System Prefix:         {sys.base_prefix}")
```

## Example
Here is a complete Python script demonstrating how to inspect the current environment's configuration and programmatically simulate dependency version checks:

```python
import sys
import os
from pathlib import Path

def inspect_environment():
    """Inspect and report on Python runtime environment isolation."""
    is_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    
    print("=== Python Environment Inspection ===")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version:    {sys.version.split()[0]}")
    print(f"sys.prefix:        {sys.prefix}")
    print(f"sys.base_prefix:   {sys.base_prefix}")
    print(f"Isolated venv:     {is_venv}")
    
    if is_venv:
        cfg_path = Path(sys.prefix) / "pyvenv.cfg"
        print(f"Config file exists ({cfg_path}): {cfg_path.is_file()}")
        if cfg_path.is_file():
            print("--- pyvenv.cfg contents ---")
            with open(cfg_path, "r", encoding="utf-8") as f:
                for line in f:
                    print("  " + line.strip())

if __name__ == "__main__":
    inspect_environment()
```

## Line-by-Line Explanation
1. `import sys, os, Path`: Imports standard library modules for system inspection and path operations.
2. `def inspect_environment()`: Declares a diagnostic function to audit environment isolation.
3. `is_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)`: In a global Python environment, `sys.prefix` and `sys.base_prefix` are identical. In a virtual environment, `sys.prefix` is replaced with the local environment folder path, while `sys.base_prefix` retains the original installation path.
4. `sys.executable`: Points to the exact binary being executed (e.g., `/myproject/.venv/bin/python`).
5. `cfg_path = Path(sys.prefix) / "pyvenv.cfg"`: Locates the configuration file generated by the `venv` module.
6. `cfg_path.is_file()`: Verifies that the configuration metadata exists on disk.
7. Reading and printing lines from `pyvenv.cfg`: Demonstrates the underlying key-value pairs (like `home = /usr/bin` and `include-system-site-packages = false`).

## What Python Is Doing
When Python starts up, its C runtime executes an initialization sequence known as site initialization:
1. It determines the directory of the running binary (`sys.executable`).
2. It walks up directory trees looking for a file named `pyvenv.cfg` or milestone landmark files (like standard library directories).
3. If `pyvenv.cfg` is found, Python parses its keys. If `include-system-site-packages = false` (the default), Python sets `sys.prefix` to the directory containing `pyvenv.cfg` and deliberately excludes the global `site-packages` directory from `sys.path`.
4. The `site` module is automatically imported unless `-S` is passed. The `site` module adds the virtual environment's `lib/pythonX.Y/site-packages` to `sys.path`.
5. Now, whenever an `import` statement executes, Python searches the virtual environment's private package folder first!

## Common Mistakes
1. **Checking `.venv` into Git**: Beginners frequently commit the entire virtual environment directory (hundreds of megabytes of binary files and symlinks) into version control. **Never commit `.venv`!** Always add `.venv/` and `venv/` to `.gitignore`. Instead, commit `requirements.txt` or `pyproject.toml`.
2. **Moving or Renaming a Virtual Environment Folder**: Virtual environments contain hardcoded absolute paths inside their activation scripts and `pyvenv.cfg`. If you rename or move the parent folder, the environment will break. If you move your project, delete the old `.venv` and create a fresh one.
3. **Forgetting to Activate the Environment**: Running `pip install <package>` in a terminal where the environment is not activated installs the package into the global environment or throws permission errors (`PEP 668: externally-managed-environment`).
4. **Hardcoding `python` vs `python3`**: On different platforms, `python` might point to Python 2 (legacy) or not exist at all. Using `python3 -m venv .venv` ensures the correct interpreter version is invoked.

## Real-World Uses
- **Local Multi-Project Development**: Every professional software engineer maintains dozens of client or research projects on their workstation, each with its own isolated `.venv`.
- **Continuous Integration (CI/CD)**: Automated test runners (GitHub Actions, GitLab CI) spin up a pristine virtual environment for every test run to ensure tests do not pass merely because of leftover local packages.
- **Microservices and Container Builds**: Docker images create minimal virtual environments to keep container image sizes small and strictly reproduce target dependencies.

## Connection to AI Agents
Modern AI agents frequently act as autonomous software engineers. When an agent is tasked with writing code, installing dependencies, or running third-party tools:
- **Sandbox Safety**: An agent must never run `pip install` directly on the host system. Agents create transient, isolated virtual environments to test generated code.
- **Tool Dependency Isolation**: Different agent skills (e.g., a data analysis tool using Pandas vs a web scraper using Playwright) can run inside separate virtual environments to prevent version conflicts.
- **Dynamic Dependency Resolution**: Agents read project dependency manifests (`pyproject.toml`, `requirements.txt`) and programmatically construct virtual environments using the `venv` module and `subprocess`.

## Practice
Try these quick checks:
1. Open your terminal and run `python3 -m venv /tmp/test_env`.
2. List the contents of `/tmp/test_env` using `ls -la /tmp/test_env`. Locate `pyvenv.cfg` and examine what directories exist.
3. Clean up by deleting `/tmp/test_env`.

## Challenge
Can you write a Python function that parses a `requirements.txt` file, extracts package names and version constraints (e.g., `requests>=2.28.0`), and identifies whether two different requirement files have conflicting exact-version requirements (e.g., `pkg==1.0` vs `pkg==2.0`)? (We will build this in the exercises!)

## Summary
- Virtual environments create an isolated sandbox for your Python projects, solving the "dependency hell" problem.
- The built-in `venv` module provides lightweight environments by modifying `sys.prefix` and managing a dedicated `site-packages` directory.
- `pyvenv.cfg` is the core metadata file that configures environment isolation.
- Dependencies should be tracked in manifest files (`requirements.txt`) rather than committing `.venv` directories to version control.

## What You Should Know Before Moving On
- How to create and activate a virtual environment using `python3 -m venv .venv`.
- How Python distinguishes an isolated virtual environment from the base system using `sys.prefix` and `sys.base_prefix`.
- How to export and install dependencies with `pip freeze` and `pip install -r requirements.txt`.
- Why AI agents require virtual environment sandboxing when executing autonomous coding tasks.
