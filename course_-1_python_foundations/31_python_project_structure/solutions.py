"""
Module 31 Solutions: Python Project Structure
=============================================
Reference implementations for all 4 levels of Module 31 exercises.
"""

from typing import Any
from pathlib import PurePath, Path
import re


# =====================================================================
# LEVEL 1: RECALL — Project Layout Validation Solution
# =====================================================================

def validate_project_layout(file_paths: list[str]) -> dict[str, bool]:
    """Validates whether a file list complies with standard modern Python structure."""
    normalized = [PurePath(p).as_posix().lstrip("./") for p in file_paths]

    has_pyproject = "pyproject.toml" in normalized
    has_readme = "README.md" in normalized
    has_src = any(p.startswith("src/") and len(p) > 4 for p in normalized)
    has_tests = any(p.startswith("tests/") and len(p) > 6 for p in normalized)

    # Check for src/<package_name>/__init__.py
    has_package_init = False
    for p in normalized:
        parts = p.split("/")
        if len(parts) >= 3 and parts[0] == "src" and parts[-1] == "__init__.py":
            has_package_init = True
            break

    return {
        "has_pyproject": has_pyproject,
        "has_readme": has_readme,
        "has_src": has_src,
        "has_tests": has_tests,
        "has_package_init": has_package_init,
    }


# =====================================================================
# LEVEL 2: MODIFY — Extending pyproject.toml Configuration Solution
# =====================================================================

def generate_pyproject_config(
    name: str,
    version: str,
    dependencies: list[str],
    cli_command: str | None = None,
    entry_point: str | None = None,
) -> str:
    """Generates pyproject.toml content with validation and CLI entry point support."""
    # Validate semantic versioning (e.g., '1.0.0' or '0.1.2')
    semver_pattern = r"^\d+\.\d+\.\d+$"
    if not re.match(semver_pattern, version.strip()):
        raise ValueError(f"Invalid semantic version: {version!r}. Must follow 'major.minor.patch'.")

    dep_formatted = ", ".join(f'"{d}"' for d in dependencies)

    lines = [
        "[build-system]",
        'requires = ["setuptools>=61.0"]',
        'build-backend = "setuptools.build_meta"',
        "",
        "[project]",
        f'name = "{name}"',
        f'version = "{version}"',
        'requires-python = ">=3.10"',
        f"dependencies = [{dep_formatted}]",
    ]

    if cli_command and entry_point:
        lines.extend([
            "",
            "[project.scripts]",
            f'{cli_command} = "{entry_point}"',
        ])

    return "\n".join(lines) + "\n"


# =====================================================================
# LEVEL 3: BUILD — Public API & __all__ Export Inspector Solution
# =====================================================================

class PackageExportInspector:
    """Inspects and validates public API exports defined by __all__."""
    def __init__(self, module_dict: dict[str, Any]) -> None:
        self._module_dict = module_dict

    def get_public_exports(self) -> dict[str, Any]:
        """Returns public symbols respecting __all__ or non-underscore default."""
        if "__all__" in self._module_dict:
            all_symbols = self._module_dict["__all__"]
            exports: dict[str, Any] = {}
            for name in all_symbols:
                if name not in self._module_dict:
                    raise AttributeError(
                        f"Export symbol {name!r} listed in __all__ does not exist in module namespace"
                    )
                exports[name] = self._module_dict[name]
            return exports

        # Default fallback: export all names that don't begin with an underscore
        return {
            k: v for k, v in self._module_dict.items()
            if not k.startswith("_")
        }

    def has_leaked_privates(self) -> bool:
        """Returns True if __all__ contains any name starting with an underscore '_'."""
        if "__all__" not in self._module_dict:
            return False
        return any(name.startswith("_") for name in self._module_dict["__all__"])


# =====================================================================
# LEVEL 4: DEBUG — Repaired Path to Dot-Import Solution
# =====================================================================

def repaired_path_to_import_string(filepath: str) -> str:
    """The corrected, cross-platform path to dot-import converter."""
    # Convert to pure path for cross-platform normalization (handles backslashes)
    path_obj = PurePath(filepath)

    # Check extension
    if path_obj.suffix != ".py":
        raise ValueError(f"File {filepath!r} is not a Python source file (missing .py extension)")

    parts = list(path_obj.parts)

    # Remove root '/' or drive letters on Windows
    if parts and (parts[0] == "/" or parts[0].endswith(":\\") or parts[0].endswith(":")):
        parts = parts[1:]

    # Remove leading 'src' directory if present
    if parts and parts[0] == "src":
        parts = parts[1:]

    if not parts:
        raise ValueError("Invalid path: no module components found")

    # If the target file is __init__.py, drop it so the package name itself is the import path
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        # Strip .py suffix from filename
        parts[-1] = PurePath(parts[-1]).stem

    return ".".join(parts)


# =====================================================================
# VERIFICATION RUNNER
# =====================================================================

def verify_module_31() -> None:
    print("Verifying Module 31 Solutions...")

    # Test Level 1: validate_project_layout
    valid_tree = [
        "pyproject.toml",
        "README.md",
        "src/agent/__init__.py",
        "src/agent/core.py",
        "tests/test_agent.py",
    ]
    check = validate_project_layout(valid_tree)
    assert check["has_pyproject"] is True
    assert check["has_readme"] is True
    assert check["has_src"] is True
    assert check["has_tests"] is True
    assert check["has_package_init"] is True

    # Incomplete tree
    incomplete = ["README.md", "main.py"]
    check2 = validate_project_layout(incomplete)
    assert check2["has_pyproject"] is False
    assert check2["has_package_init"] is False
    print("  [✓] Level 1 (Recall) passed!")

    # Test Level 2: generate_pyproject_config
    cfg = generate_pyproject_config(
        name="test-agent",
        version="1.2.3",
        dependencies=["pytest>=7.0"],
        cli_command="test-cli",
        entry_point="test_agent.cli:run",
    )
    assert "[project.scripts]" in cfg
    assert 'test-cli = "test_agent.cli:run"' in cfg
    assert 'requires-python = ">=3.10"' in cfg

    # Semver error test
    try:
        generate_pyproject_config("bad", "1.0", [])
        assert False, "Should have raised ValueError on invalid semver"
    except ValueError:
        pass
    print("  [✓] Level 2 (Modify) passed!")

    # Test Level 3: PackageExportInspector
    # Case A: Valid __all__
    sample_ns = {
        "__all__": ["PublicClass", "public_func"],
        "PublicClass": 1,
        "public_func": 2,
        "_internal_secret": 3,
        "unlisted_var": 4,
    }
    inspector = PackageExportInspector(sample_ns)
    exports = inspector.get_public_exports()
    assert set(exports.keys()) == {"PublicClass", "public_func"}
    assert inspector.has_leaked_privates() is False

    # Case B: Leaked private in __all__
    leak_ns = {
        "__all__": ["public", "_private"],
        "public": 1,
        "_private": 2,
    }
    leak_inspector = PackageExportInspector(leak_ns)
    assert leak_inspector.has_leaked_privates() is True

    # Case C: Missing symbol in __all__
    missing_ns = {
        "__all__": ["phantom_symbol"],
    }
    try:
        PackageExportInspector(missing_ns).get_public_exports()
        assert False, "Should have raised AttributeError for missing export"
    except AttributeError:
        pass
    print("  [✓] Level 3 (Build) passed!")

    # Test Level 4: repaired_path_to_import_string
    assert repaired_path_to_import_string("src/my_agent/tools/calc.py") == "my_agent.tools.calc"
    assert repaired_path_to_import_string("src/my_agent/__init__.py") == "my_agent"
    assert repaired_path_to_import_string("my_agent/core.py") == "my_agent.core"
    assert repaired_path_to_import_string("src/my_agent/subpkg/__init__.py") == "my_agent.subpkg"

    # Non-.py exception test
    try:
        repaired_path_to_import_string("src/my_agent/config.json")
        assert False, "Should have raised ValueError on non-.py file"
    except ValueError:
        pass
    print("  [✓] Level 4 (Debug) passed!")

    print("All Module 31 solutions verified successfully!\n")


if __name__ == "__main__":
    verify_module_31()
