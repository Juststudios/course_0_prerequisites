"""
End-to-End Acceptance Test Suite: Course -1 Python Foundations (33 Modules)
=============================================================================

Strictly and comprehensively verifies all 33 modules of Course -1 Python Foundations
against the core pedagogical, structural, and execution requirements:

  - R1: README.md exists and contains all 18 exact required headers in order,
        with non-empty content in every section.
  - R2: Main .py lesson file exists, is at least 150 lines, and executes with exit code 0.
  - R3: exercises.py exists, has 4 distinct levels (Recall, Modify, Build, Debug),
        and contains NotImplementedError or # TODO.
  - R3: solutions.py exists, contains no NotImplementedError, and executes with exit code 0.
  - R4: Curriculum completeness across all 33 modules.

Usage:
  pytest tests/e2e/test_course_minus_1_acceptance.py -v
  pytest tests/e2e/test_course_minus_1_acceptance.py -k "01_what" -v
  pytest tests/e2e/test_course_minus_1_acceptance.py -m "m1" -v
  python3 tests/e2e/test_course_minus_1_acceptance.py
"""

import sys
from pathlib import Path
from typing import List, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify_course_minus_1 import (  # noqa: E402
    DEFAULT_COURSE_DIR,
    REQUIRED_README_HEADERS,
    CheckResult,
    ModuleVerification,
    verify_check_1_readme,
    verify_check_2_lesson,
    verify_check_3_exercises,
    verify_check_4_solutions,
    verify_module,
)

# Canonical 33 modules per PROJECT.md and directory structure
COURSE_MINUS_1_MODULES: List[Tuple[str, str, str]] = [
    ("01", "01_what_programming_is", "m1"),
    ("02", "02_first_python_programs", "m1"),
    ("03", "03_variables_and_data_types", "m1"),
    ("04", "04_operators", "m1"),
    ("05", "05_strings", "m1"),
    ("06", "06_collections", "m1"),
    ("07", "07_control_flow", "m2"),
    ("08", "08_functions", "m2"),
    ("09", "09_scope", "m2"),
    ("10", "10_errors_and_exceptions", "m2"),
    ("11", "11_files", "m2"),
    ("12", "12_modules", "m3"),
    ("13", "13_classes_and_oop", "m3"),
    ("14", "14_functional_programming", "m3"),
    ("15", "15_type_hints", "m3"),
    ("16", "16_dataclasses", "m3"),
    ("17", "17_generators", "m4"),
    ("18", "18_iterators", "m4"),
    ("19", "19_decorators", "m4"),
    ("20", "20_context_managers", "m4"),
    ("21", "21_testing", "m4"),
    ("22", "22_logging", "m4"),
    ("23", "23_virtual_environments", "m5"),
    ("24", "24_async_python_intro", "m5"),
    ("25", "25_async_concurrency", "m5"),
    ("26", "26_http_and_json_intro", "m5"),
    ("27", "27_environment_variables", "m5"),
    ("28", "28_subprocesses_intro", "m5"),
    ("29", "29_sqlite_intro", "m5"),
    ("30", "30_basic_software_architecture", "m6"),
    ("31", "31_python_project_structure", "m6"),
    ("32", "32_python_debugging", "m6"),
    ("33", "33_integrated_projects", "m6"),
]


# =====================================================================
# R1: PEDAGOGICAL README TESTS (18 Exact Headers, In Order, Non-Empty)
# =====================================================================

class TestR1PedagogicalReadme:
    """Verifies that each module README.md strictly conforms to R1."""

    @pytest.mark.parametrize(
        "mod_num,mod_name,milestone",
        COURSE_MINUS_1_MODULES,
        ids=[m[1] for m in COURSE_MINUS_1_MODULES],
    )
    def test_readme_18_headers_in_order_with_content(self, mod_num: str, mod_name: str, milestone: str):
        """
        Verify README.md exists, contains all 18 canonical headers in order,
        and every section has non-empty content.
        """
        mod_dir = DEFAULT_COURSE_DIR / mod_name
        assert mod_dir.exists() and mod_dir.is_dir(), (
            f"Module directory '{mod_name}' does not exist under {DEFAULT_COURSE_DIR}"
        )

        res: CheckResult = verify_check_1_readme(mod_dir)
        assert res.passed, (
            f"[{mod_name}] R1 README Verification Failed: {res.message}\n"
            f"  Details: {res.details}"
        )


# =====================================================================
# R2: DETAILED LESSON SCRIPT TESTS (>= 150 Lines & Clean Execution)
# =====================================================================

class TestR2DetailedLessonScript:
    """Verifies that each module main lesson .py file conforms to R2."""

    @pytest.mark.parametrize(
        "mod_num,mod_name,milestone",
        COURSE_MINUS_1_MODULES,
        ids=[m[1] for m in COURSE_MINUS_1_MODULES],
    )
    def test_main_lesson_script_length_and_execution(self, mod_num: str, mod_name: str, milestone: str):
        """
        Verify main lesson .py file exists, is at least 150 lines, and executes with exit code 0.
        """
        mod_dir = DEFAULT_COURSE_DIR / mod_name
        assert mod_dir.exists() and mod_dir.is_dir(), (
            f"Module directory '{mod_name}' does not exist under {DEFAULT_COURSE_DIR}"
        )

        res: CheckResult = verify_check_2_lesson(mod_dir, min_lines=150, timeout_sec=25)
        assert res.passed, (
            f"[{mod_name}] R2 Lesson Script Verification Failed: {res.message}\n"
            f"  Details: {res.details}"
        )


# =====================================================================
# R3: AUTHENTIC EXERCISES TESTS (4 Distinct Levels & Scaffolding)
# =====================================================================

class TestR3ExercisesScaffolding:
    """Verifies that exercises.py in each module conforms to R3."""

    @pytest.mark.parametrize(
        "mod_num,mod_name,milestone",
        COURSE_MINUS_1_MODULES,
        ids=[m[1] for m in COURSE_MINUS_1_MODULES],
    )
    def test_exercises_four_levels_and_scaffolding(self, mod_num: str, mod_name: str, milestone: str):
        """
        Verify exercises.py exists, has 4 distinct levels (Recall, Modify, Build, Debug),
        and contains NotImplementedError or # TODO scaffolding.
        """
        mod_dir = DEFAULT_COURSE_DIR / mod_name
        assert mod_dir.exists() and mod_dir.is_dir(), (
            f"Module directory '{mod_name}' does not exist under {DEFAULT_COURSE_DIR}"
        )

        res: CheckResult = verify_check_3_exercises(mod_dir)
        assert res.passed, (
            f"[{mod_name}] R3 Exercises Verification Failed: {res.message}\n"
            f"  Details: {res.details}"
        )


# =====================================================================
# R3: SOLUTIONS EXECUTION TESTS (No NotImplementedError & Clean Exec)
# =====================================================================

class TestR3SolutionsExecution:
    """Verifies that solutions.py in each module conforms to R3."""

    @pytest.mark.parametrize(
        "mod_num,mod_name,milestone",
        COURSE_MINUS_1_MODULES,
        ids=[m[1] for m in COURSE_MINUS_1_MODULES],
    )
    def test_solutions_no_not_implemented_and_executes_cleanly(self, mod_num: str, mod_name: str, milestone: str):
        """
        Verify solutions.py exists, contains no NotImplementedError, and executes with exit code 0.
        """
        mod_dir = DEFAULT_COURSE_DIR / mod_name
        assert mod_dir.exists() and mod_dir.is_dir(), (
            f"Module directory '{mod_name}' does not exist under {DEFAULT_COURSE_DIR}"
        )

        res: CheckResult = verify_check_4_solutions(mod_dir, timeout_sec=25)
        assert res.passed, (
            f"[{mod_name}] R3 Solutions Verification Failed: {res.message}\n"
            f"  Details: {res.details}"
        )


# =====================================================================
# R4: COMPREHENSIVE PER-MODULE ACCEPTANCE
# =====================================================================

class TestR4ModuleAcceptance:
    """Aggregate per-module gate acceptance testing all 4 checks simultaneously."""

    @pytest.mark.parametrize(
        "mod_num,mod_name,milestone",
        COURSE_MINUS_1_MODULES,
        ids=[m[1] for m in COURSE_MINUS_1_MODULES],
    )
    def test_single_module_full_acceptance(self, mod_num: str, mod_name: str, milestone: str):
        """
        Runs all 4 verification checks for a single module.
        Reports exact failing checks with descriptive diagnostic output.
        """
        mod_dir = DEFAULT_COURSE_DIR / mod_name
        verification: ModuleVerification = verify_module(mod_dir)

        failures = [
            f"Check {cid} ({cr.name}): {cr.message}"
            for cid, cr in verification.check_results.items()
            if not cr.passed
        ]

        assert verification.passed, (
            f"Module {mod_name} failed {len(failures)}/4 acceptance criteria:\n"
            + "\n".join(f"  - {f}" for f in failures)
        )


# =====================================================================
# ADVERSARIAL VERIFICATION: HARNESS INTEGRITY TESTS
# =====================================================================

class TestAdversarialHarnessIntegrity:
    """
    Validates that the verification harness itself correctly detects defects,
    out-of-order headers, facade implementations, empty sections, and stubs.
    """

    def test_adversarial_readme_missing_header_detected(self, tmp_path: Path):
        """Harness must fail when a required header is omitted."""
        test_dir = tmp_path / "mod_missing_header"
        test_dir.mkdir()
        readme = test_dir / "README.md"
        # 17 headers only (omit 'Syntax')
        content = "\n\n".join(
            f"## {name}\nSome valid substantive text for this section."
            for _, name, _ in REQUIRED_README_HEADERS
            if name != "Syntax"
        )
        readme.write_text(content, encoding="utf-8")
        res = verify_check_1_readme(test_dir)
        assert not res.passed, "Harness falsely passed a README missing the 'Syntax' header"
        assert "Syntax" in res.details["missing_headers"]

    def test_adversarial_readme_out_of_order_detected(self, tmp_path: Path):
        """Harness must fail when headers appear out of sequential order."""
        test_dir = tmp_path / "mod_out_of_order"
        test_dir.mkdir()
        readme = test_dir / "README.md"
        # Swap 'Syntax' and 'Concept'
        headers = []
        for hid, name, _ in REQUIRED_README_HEADERS:
            headers.append(name)
        # Swap items
        idx_concept = headers.index("Concept")
        idx_syntax = headers.index("Syntax")
        headers[idx_concept], headers[idx_syntax] = headers[idx_syntax], headers[idx_concept]

        content = "\n\n".join(
            (f"# {name}: Title" if name == "Topic" else f"## {name}\nValid substantive content.")
            for name in headers
        )
        readme.write_text(content, encoding="utf-8")
        res = verify_check_1_readme(test_dir)
        assert not res.passed, "Harness falsely passed a README with out-of-order headers"
        assert len(res.details.get("out_of_order", [])) > 0

    def test_adversarial_readme_empty_section_detected(self, tmp_path: Path):
        """Harness must fail when a section has no body content."""
        test_dir = tmp_path / "mod_empty_sec"
        test_dir.mkdir()
        readme = test_dir / "README.md"
        lines = []
        for hid, name, _ in REQUIRED_README_HEADERS:
            if hid == 1:
                lines.append("# Topic: Something")
            elif name == "Intuition":
                # Header immediately followed by next header without content
                lines.append(f"## {name}")
            else:
                lines.append(f"## {name}")
                lines.append("Substantive body text.")
            lines.append("")
        readme.write_text("\n".join(lines), encoding="utf-8")
        res = verify_check_1_readme(test_dir)
        assert not res.passed, "Harness falsely passed a README with an empty section"
        assert "Intuition" in res.details.get("empty_sections", [])

    def test_adversarial_lesson_short_file_rejected(self, tmp_path: Path):
        """Harness must fail lesson script with fewer than 150 lines."""
        test_dir = tmp_path / "mod_short_lesson"
        test_dir.mkdir()
        lesson = test_dir / "lesson.py"
        lesson.write_text("print('hello world')\n" * 50, encoding="utf-8")
        res = verify_check_2_lesson(test_dir, min_lines=150)
        assert not res.passed, "Harness falsely passed a lesson with only 50 lines"

    def test_adversarial_lesson_runtime_error_rejected(self, tmp_path: Path):
        """Harness must fail lesson script that exits non-zero."""
        test_dir = tmp_path / "mod_crashing_lesson"
        test_dir.mkdir()
        lesson = test_dir / "lesson.py"
        lines = ["print('line')\n"] * 160 + ["raise RuntimeError('Fatal boom!')\n"]
        lesson.write_text("".join(lines), encoding="utf-8")
        res = verify_check_2_lesson(test_dir, min_lines=150)
        assert not res.passed, "Harness falsely passed a lesson that raised a RuntimeError"

    def test_adversarial_exercises_missing_levels_rejected(self, tmp_path: Path):
        """Harness must fail exercises missing any of the 4 required tiers."""
        test_dir = tmp_path / "mod_partial_exercises"
        test_dir.mkdir()
        ex = test_dir / "exercises.py"
        # Has Recall and Modify, but missing Build and Debug
        ex.write_text(
            "# Level 1: Recall\n# TODO: do it\n# Level 2: Modify\nraise NotImplementedError()\n",
            encoding="utf-8",
        )
        res = verify_check_3_exercises(test_dir)
        assert not res.passed, "Harness falsely passed exercises missing Build and Debug"
        assert "Build" in res.details["missing_levels"]
        assert "Debug" in res.details["missing_levels"]

    def test_adversarial_exercises_missing_scaffolding_rejected(self, tmp_path: Path):
        """Harness must fail exercises without TODO comments or NotImplementedError."""
        test_dir = tmp_path / "mod_no_scaffolding"
        test_dir.mkdir()
        ex = test_dir / "exercises.py"
        ex.write_text(
            "# Level 1: Recall\ndef f(): return 1\n"
            "# Level 2: Modify\ndef g(): return 2\n"
            "# Level 3: Build\ndef h(): return 3\n"
            "# Level 4: Debug\ndef i(): return 4\n",
            encoding="utf-8",
        )
        res = verify_check_3_exercises(test_dir)
        assert not res.passed, "Harness falsely passed exercises lacking # TODO or NotImplementedError"

    def test_adversarial_solutions_with_not_implemented_rejected(self, tmp_path: Path):
        """Harness must fail solutions that leave NotImplementedError unresolved."""
        test_dir = tmp_path / "mod_incomplete_solutions"
        test_dir.mkdir()
        sol = test_dir / "solutions.py"
        lines = ["# Valid solution lines\n"] * 20 + ["def uncompleted(): raise NotImplementedError()\n"]
        sol.write_text("".join(lines), encoding="utf-8")
        res = verify_check_4_solutions(test_dir)
        assert not res.passed, "Harness falsely passed solutions containing NotImplementedError"
        assert res.details.get("has_not_implemented") is True


if __name__ == "__main__":
    pytest.main(["-v", str(Path(__file__).resolve())])
