"""
test_networking_structure.py
============================
Static and structural validation tests for Level 6 Networking curriculum.
Verifies file existence, directory conventions, non-zero file sizes,
clean Python compilation, and 0 remaining TODOs in reference solutions.
"""

import os
import py_compile
import re
from pathlib import Path
import pytest

NETWORKING_ROOT = Path(__file__).resolve().parent.parent


def test_networking_root_files():
    """Verify presence of master README and requirements.txt."""
    readme = NETWORKING_ROOT / "README.md"
    reqs = NETWORKING_ROOT / "requirements.txt"
    assert readme.exists(), "networking/README.md is missing"
    assert reqs.exists(), "networking/requirements.txt is missing"
    assert readme.stat().st_size > 1000, "networking/README.md appears truncated"
    assert reqs.stat().st_size > 10, "networking/requirements.txt appears truncated"


def test_module_01_tcp_ip_files():
    """Verify Module 1 files and scripts exist and are non-empty."""
    mod1 = NETWORKING_ROOT / "01_tcp_ip"
    required = [
        "README.md",
        "01_tcp_server.py",
        "02_tcp_client.py",
        "03_udp_sockets.py",
        "04_concurrent_server.py",
        "exercises.py",
    ]
    for filename in required:
        file_path = mod1 / filename
        assert file_path.exists(), f"Missing {file_path}"
        assert file_path.stat().st_size > 100, f"File {file_path} is too small / empty"


def test_module_02_http_files():
    """Verify Module 2 files and scripts exist and are non-empty."""
    mod2 = NETWORKING_ROOT / "02_http_protocols"
    required = [
        "README.md",
        "01_raw_http_client.py",
        "02_python_http_server.py",
        "03_requests_and_httpx.py",
        "exercises.py",
    ]
    for filename in required:
        file_path = mod2 / filename
        assert file_path.exists(), f"Missing {file_path}"
        assert file_path.stat().st_size > 100, f"File {file_path} is too small / empty"


def test_module_03_rest_files():
    """Verify Module 3 files and scripts exist and are non-empty."""
    mod3 = NETWORKING_ROOT / "03_rest_apis"
    required = [
        "README.md",
        "01_rest_principles.py",
        "02_fastapi_endpoints.py",
        "03_ml_model_serving.py",
        "exercises.py",
    ]
    for filename in required:
        file_path = mod3 / filename
        assert file_path.exists(), f"Missing {file_path}"
        assert file_path.stat().st_size > 100, f"File {file_path} is too small / empty"


def test_solutions_files():
    """Verify solutions exist and have zero TODO markers."""
    sol_dir = NETWORKING_ROOT / "solutions"
    required = [
        "tcp_ip_solutions.py",
        "http_solutions.py",
        "rest_api_solutions.py",
    ]
    for filename in required:
        sol_path = sol_dir / filename
        assert sol_path.exists(), f"Missing solution: {sol_path}"
        content = sol_path.read_text(encoding="utf-8")
        assert len(content) > 500, f"Solution {sol_path} is too short"

        # Check for any TODO markers in solution files
        todos = re.findall(r"(?:#|%)\s*TODO", content, flags=re.IGNORECASE)
        assert len(todos) == 0, f"Found {len(todos)} remaining TODOs in {filename}: {todos}"


def test_all_python_files_compile():
    """Verify that every single python file in networking compiles without syntax errors."""
    for root, _, files in os.walk(NETWORKING_ROOT):
        for f in files:
            if f.endswith(".py"):
                path = Path(root) / f
                try:
                    py_compile.compile(str(path), doraise=True)
                except py_compile.PyCompileError as e:
                    pytest.fail(f"Compilation failed for {path}: {e}")
