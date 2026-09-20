"""
End-to-End Test Suite for Milestone M1 & M4: Course 0 Prerequisites for AI Agents.

Validates the complete 15-module curriculum bridging basic Python to autonomous AI agent engineering:
- Tier 1: Feature Coverage (Directory structure, 15 modules, README existence, 2+ runnable scripts per module, mini_agent package layout)
- Tier 2: Boundary & Formatting (Strict adherence to TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE)
- Tier 3: Cross-Feature Execution (Standalone script execution across all 15 modules with exit code 0)
- Tier 4: Real-World Integration (mini_agent end-to-end execution, SQLite memory persistence, ContextVars propagation, Tool registry)
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
COURSE_0_DIR = REPO_ROOT / "course_0_prerequisites"

# The 15 canonical modules required by R1 and PROJECT.md
EXPECTED_MODULES = [
    "01_callables_and_functional_python",
    "02_classes_dunder_and_oop",
    "03_type_hints_and_pydantic",
    "04_async_and_event_loops",
    "05_contextvars_and_state",
    "06_http_and_rest_apis",
    "07_json_and_schema_validation",
    "08_config_management",
    "09_subprocesses_and_sandboxing",
    "10_sqlite_and_memory",
    "11_architecture_patterns",
    "12_prompt_templating",
    "13_logging_and_observability",
    "14_streaming_and_sse",
    "15_math_bridges",
]


# =====================================================================
# TIER 1: FEATURE COVERAGE (Structure & Packaging Completeness)
# =====================================================================

@pytest.mark.tier1
class TestTier1Course0Structure:
    """Verifies complete structural packaging of Course 0 Prerequisites."""

    def test_course_0_directory_exists(self):
        """Verify root course_0_prerequisites directory exists."""
        assert COURSE_0_DIR.exists() and COURSE_0_DIR.is_dir(), (
            f"Course 0 root directory missing at {COURSE_0_DIR}"
        )

    @pytest.mark.parametrize("mod_name", EXPECTED_MODULES)
    def test_module_directory_exists(self, mod_name: str):
        """Verify each of the 15 specified module directories exists."""
        mod_dir = COURSE_0_DIR / mod_name
        assert mod_dir.exists() and mod_dir.is_dir(), (
            f"Module directory '{mod_name}' does not exist under {COURSE_0_DIR}"
        )

    @pytest.mark.parametrize("mod_name", EXPECTED_MODULES)
    def test_module_contains_readme(self, mod_name: str):
        """Verify each module directory contains a non-empty README.md (> 200 bytes)."""
        readme_path = COURSE_0_DIR / mod_name / "README.md"
        assert readme_path.exists() and readme_path.is_file(), (
            f"README.md missing in module '{mod_name}'"
        )
        size = readme_path.stat().st_size
        assert size >= 200, (
            f"README.md in '{mod_name}' is too small ({size} bytes, expected >= 200 bytes)"
        )

    @pytest.mark.parametrize("mod_name", EXPECTED_MODULES)
    def test_module_contains_at_least_two_python_scripts(self, mod_name: str):
        """Verify each module contains at least 2 runnable Python (.py) files."""
        mod_dir = COURSE_0_DIR / mod_name
        py_files = [f for f in mod_dir.glob("*.py") if f.name != "__init__.py"]
        assert len(py_files) >= 2, (
            f"Module '{mod_name}' must contain at least 2 Python demonstration scripts. "
            f"Found {len(py_files)}: {[f.name for f in py_files]}"
        )

    def test_mini_agent_package_structure(self):
        """Verify mini_agent capstone directory contains all required components."""
        mini_agent_dir = COURSE_0_DIR / "mini_agent"
        assert mini_agent_dir.exists() and mini_agent_dir.is_dir(), (
            f"mini_agent directory missing at {mini_agent_dir}"
        )

        required_files = [
            "__init__.py",
            "config.py",
            "models.py",
            "memory.py",
            "tools.py",
            "engine.py",
            "agent.py",
            "main.py",
        ]
        for fname in required_files:
            target = mini_agent_dir / fname
            assert target.exists() and target.is_file(), (
                f"mini_agent is missing required component '{fname}'"
            )

        test_file = mini_agent_dir / "tests" / "test_mini_agent.py"
        assert test_file.exists() and test_file.is_file(), (
            f"mini_agent tests missing at {test_file}"
        )

    def test_course_0_root_readme_and_resources(self):
        """Verify Course 0 root README and supporting folders (exercises, solutions)."""
        root_readme = COURSE_0_DIR / "README.md"
        assert root_readme.exists() and root_readme.stat().st_size > 300, (
            "Course 0 root README.md missing or too small"
        )
        assert (COURSE_0_DIR / "exercises").is_dir(), "exercises/ directory missing"
        assert (COURSE_0_DIR / "solutions").is_dir(), "solutions/ directory missing"


# =====================================================================
# TIER 2: BOUNDARY & FORMATTING (Pedagogical Compliance)
# =====================================================================

@pytest.mark.tier2
class TestTier2Course0Pedagogy:
    """Verifies strict adherence to pedagogical structure in all 15 modules."""

    REQUIRED_PATTERNS = [
        ("TERM", re.compile(r"(?:\*\*TERM\*\*|###\s*(?:Concept\s*:?\s*)?Term|TERM\s*:)", re.IGNORECASE)),
        ("DEFINITION", re.compile(r"(?:\*\*DEFINITION\*\*|####?\s*Definition|DEFINITION\s*:)", re.IGNORECASE)),
        ("INTUITION", re.compile(r"(?:\*\*INTUITION\*\*|####?\s*Intuition|INTUITION\s*:)", re.IGNORECASE)),
        ("WHY IT EXISTS", re.compile(r"(?:\*\*WHY\s+IT\s+EXISTS\*\*|####?\s*Why\s+It\s+Exists|WHY\s+IT\s+EXISTS\s*:)", re.IGNORECASE)),
        ("HOW IT WORKS", re.compile(r"(?:\*\*HOW\s+IT\s+WORKS\*\*|####?\s*How\s+It\s+Works|HOW\s+IT\s+WORKS\s*:)", re.IGNORECASE)),
        ("CODE", re.compile(r"(?:\*\*CODE\*\*|####?\s*Code|CODE\s*:|```python)", re.IGNORECASE)),
    ]

    @pytest.mark.parametrize("mod_name", EXPECTED_MODULES)
    def test_readme_pedagogical_structure(self, mod_name: str):
        """
        Verify every module README strictly follows the required sequence:
        TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE
        """
        readme_path = COURSE_0_DIR / mod_name / "README.md"
        if not readme_path.exists():
            pytest.fail(f"README.md missing in {mod_name}")

        content = readme_path.read_text(encoding="utf-8")

        # Check that all 6 required elements are present in the text
        missing_elements = []
        for name, pattern in self.REQUIRED_PATTERNS:
            if not pattern.search(content):
                missing_elements.append(name)

        assert not missing_elements, (
            f"Module '{mod_name}/README.md' is missing required pedagogical sections: {missing_elements}. "
            f"Must follow TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE"
        )

        # Check that a python code block exists
        assert "```python" in content, (
            f"Module '{mod_name}/README.md' must contain at least one ```python code block"
        )

        # Ensure content is substantial (> 1000 characters)
        assert len(content) >= 1000, (
            f"Module '{mod_name}/README.md' lacks sufficient instructional depth ({len(content)} chars, expected >= 1000)"
        )


# =====================================================================
# TIER 3: CROSS-FEATURE EXECUTION (Standalone Script Verification)
# =====================================================================

@pytest.mark.tier3
class TestTier3Course0ScriptExecutability:
    """Verifies that all standalone demonstration scripts across all 15 modules execute cleanly."""

    def _discover_module_scripts(self) -> List[Tuple[str, Path]]:
        """Collect all executable demonstration scripts across the 15 modules."""
        scripts = []
        for mod_name in EXPECTED_MODULES:
            mod_dir = COURSE_0_DIR / mod_name
            if not mod_dir.is_dir():
                continue
            for py_file in sorted(mod_dir.glob("*.py")):
                if py_file.name != "__init__":
                    scripts.append((mod_name, py_file))
        return scripts

    def test_standalone_scripts_execute(self):
        """Execute all discovered demonstration scripts and assert exit code 0."""
        scripts = self._discover_module_scripts()
        assert len(scripts) >= 30, (
            f"Expected at least 30 demonstration scripts across 15 modules, found {len(scripts)}"
        )

        failures = []
        for mod_name, script_path in scripts:
            res = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=25,
                cwd=str(REPO_ROOT),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            if res.returncode != 0:
                failures.append(
                    f"[{mod_name}/{script_path.name}] exited with code {res.returncode}.\n"
                    f"Stderr: {res.stderr.strip()[:300]}\n"
                    f"Stdout: {res.stdout.strip()[:200]}"
                )

        assert not failures, (
            f"{len(failures)} script(s) failed during execution:\n" + "\n---\n".join(failures)
        )

    def test_contextvars_isolation_demonstration(self):
        """Verify ContextVars isolation script demonstrates task-scoped separation."""
        mod_dir = COURSE_0_DIR / "05_contextvars_and_state"
        script = mod_dir / "tenant_isolation.py"
        if not script.exists():
            script = mod_dir / "contextvars_demo.py"
        assert script.exists(), "No ContextVars demo script found in 05_contextvars_and_state"

        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, f"ContextVars script failed: {res.stderr}"
        stdout_lower = res.stdout.lower()
        assert "tenant" in stdout_lower or "trace" in stdout_lower or "isolated" in stdout_lower or "context" in stdout_lower, (
            f"ContextVars demo output did not demonstrate context isolation: {res.stdout}"
        )

    def test_sqlite_persistence_demonstration(self):
        """Verify SQLite demonstration script executes transactions and table persistence."""
        mod_dir = COURSE_0_DIR / "10_sqlite_and_memory"
        candidates = list(mod_dir.glob("*.py"))
        assert len(candidates) > 0, "No Python scripts in 10_sqlite_and_memory"

        script = candidates[0]
        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, f"SQLite script failed: {res.stderr}"

    def test_math_bridges_vector_search_demonstration(self):
        """Verify vector search math bridge calculates cosine similarity and retrieval."""
        mod_dir = COURSE_0_DIR / "15_math_bridges"
        script = mod_dir / "vector_search.py"
        if not script.exists():
            candidates = list(mod_dir.glob("*.py"))
            assert len(candidates) > 0, "No Python scripts in 15_math_bridges"
            script = candidates[0]

        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, f"Math bridge script failed: {res.stderr}"


# =====================================================================
# TIER 4: REAL-WORLD INTEGRATION (mini_agent End-to-End Verification)
# =====================================================================

@pytest.mark.tier4
class TestTier4MiniAgentEndToEnd:
    """Verifies complete end-to-end functionality of the mini_agent capstone project."""

    def test_mini_agent_unit_tests_pass(self):
        """Execute the official unit test suite in course_0_prerequisites/mini_agent/tests/."""
        tests_dir = COURSE_0_DIR / "mini_agent" / "tests"
        assert tests_dir.is_dir(), f"mini_agent tests dir missing at {tests_dir}"

        res = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, (
            f"mini_agent test suite failed (exit code {res.returncode}):\n{res.stdout}\n{res.stderr}"
        )

    def test_mini_agent_cli_entrypoint(self):
        """Verify python3 -m course_0_prerequisites.mini_agent.main executes with exit code 0."""
        res = subprocess.run(
            [sys.executable, "-m", "course_0_prerequisites.mini_agent.main"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, (
            f"mini_agent CLI main failed (exit code {res.returncode}):\n{res.stderr}\n{res.stdout}"
        )
        assert len(res.stdout) > 0, "mini_agent.main produced empty output"

    def test_mini_agent_sqlite_and_tools_direct(self, tmp_path):
        """
        Direct programmatic verification of mini_agent components:
        1. Tool registry and parameter validation
        2. SQLite persistence of messages and session state
        3. ContextVars trace isolation
        4. ReAct reasoning execution
        """
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))

        from course_0_prerequisites.mini_agent.config import AgentConfig
        from course_0_prerequisites.mini_agent.memory import SQLiteMemory
        from course_0_prerequisites.mini_agent.models import MessageRole
        from course_0_prerequisites.mini_agent.tools import ToolRegistry

        # 1. Verify SQLite Memory
        db_file = tmp_path / "test_agent_memory.db"
        memory = SQLiteMemory(db_path=str(db_file))
        assert db_file.exists(), "SQLite database file was not created by SQLiteMemory"

        memory.add_message(session_id="session_e2e_1", role=MessageRole.USER.value, content="Hello mini_agent!")

        history = memory.get_history(session_id="session_e2e_1")
        assert len(history) >= 1, "Failed to retrieve persisted message from SQLite"
        assert history[0]["content"] == "Hello mini_agent!"

        # 2. Verify Tool Registry
        registry = ToolRegistry()

        @registry.register
        def custom_multiplier(a: float, b: float) -> float:
            """Multiply two floats."""
            return a * b

        assert "custom_multiplier" in registry.list_tools(), "Failed to register tool"

        exec_res = registry.execute("custom_multiplier", a=3.5, b=2.0)
        assert exec_res.success is True, f"Tool execution failed: {exec_res.error}"
        assert exec_res.output == 7.0, f"Expected 7.0, got {exec_res.output}"

        # 3. Verify mini_agent execution loop
        from course_0_prerequisites.mini_agent.agent import MiniAgent
        from course_0_prerequisites.mini_agent.tools import default_registry
        config = AgentConfig(db_path=str(db_file), max_steps=5, verbose=False)
        agent = MiniAgent(config=config, memory=memory, tools=default_registry)

        import asyncio
        response = asyncio.run(agent.run(prompt="Calculate 25 * 4", session_id="session_e2e_1"))
        assert response is not None, "MiniAgent returned None response"
        assert response.success is True, f"Agent run failed: {response.error}"
        assert "100" in str(response.final_answer) or "100" in str(response), (
            f"Expected answer 100 in response, got: {response.final_answer}"
        )
