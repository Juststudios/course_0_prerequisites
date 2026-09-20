"""
Pytest configuration and shared fixtures for the Curriculum Completion E2E Test Suite.
"""

import os
import sys
import socket
import importlib.util
from pathlib import Path
import pytest
import matplotlib
matplotlib.use("Agg")

os.environ["MKL_SERVICE_FORCE_INTEL"] = "1"
os.environ["MKL_THREADING_LAYER"] = "GNU"

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def pytest_configure(config):
    """Register custom markers for the 4-tier test methodology."""
    config.addinivalue_line("markers", "tier1: Tier 1 - Feature nominal isolation tests")
    config.addinivalue_line("markers", "tier2: Tier 2 - Boundary and edge case tests")
    config.addinivalue_line("markers", "tier3: Tier 3 - Cross-feature combination tests")
    config.addinivalue_line("markers", "tier4: Tier 4 - Real-world application scenario tests")
    config.addinivalue_line("markers", "m1: Milestone 1 - Deep Learning tests")
    config.addinivalue_line("markers", "m2: Milestone 2 - Math & Game AI tests")
    config.addinivalue_line("markers", "m3: Milestone 3 - Networking & TensorFlow tests")
    config.addinivalue_line("markers", "m4: Milestone 4 - Capstones & Simulink tests")
    config.addinivalue_line("markers", "m5: Milestone 5 - Master runner & overall verification")


@pytest.fixture(scope="session")
def repo_root():
    """Return the absolute path to the repository root."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def load_module():
    """Dynamically load and return a Python module from an absolute or relative path."""
    def _loader(module_name: str, rel_path: str):
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            pytest.skip(f"Target module file not found at {rel_path}")
        parent_dir = str(full_path.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        spec = importlib.util.spec_from_file_location(module_name, str(full_path))
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create module spec for {full_path}")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
        return mod
    return _loader


@pytest.fixture
def get_free_port():
    """Return an available ephemeral port on localhost."""
    def _find_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    return _find_port
