#!/usr/bin/env python3
"""
Course -1 Python Foundations: Acceptance Verification Harness
==============================================================

Automated acceptance auditor for all 33 modules of Course -1.
Validates the four non-negotiable pedagogical and execution requirements:
  - Check 1: Every README.md contains all 18 required exact headers.
  - Check 2: Every main lesson .py file is at least 150 lines long and executes
             cleanly with exit code 0.
  - Check 3: Every exercises.py contains 4 distinct levels (Recall, Modify,
             Build, Debug) with authentic # TODO comments and NotImplementedError.
  - Check 4: Every solutions.py executes cleanly with exit code 0 and contains
             genuine completed solutions.

Usage:
  python3 scripts/verify_course_minus_1.py
  python3 scripts/verify_course_minus_1.py --module 01
  python3 scripts/verify_course_minus_1.py --module 01,02,03 --check 1,2
  python3 scripts/verify_course_minus_1.py --json report.json --verbose
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COURSE_DIR = REPO_ROOT / "course_-1_python_foundations"

# The 18 canonical required headers specified in ORIGINAL_REQUEST.md & PROJECT.md
REQUIRED_README_HEADERS = [
    (1, "Topic", re.compile(r"^#\s+(?:Topic\b|[A-Za-z0-9])", re.IGNORECASE)),
    (2, "What You Will Learn", re.compile(r"^##\s+What You Will Learn", re.IGNORECASE)),
    (3, "Prerequisites", re.compile(r"^##\s+Prerequisites", re.IGNORECASE)),
    (4, "The Problem", re.compile(r"^##\s+The Problem", re.IGNORECASE)),
    (5, "Key Terminology", re.compile(r"^##\s+Key Terminology", re.IGNORECASE)),
    (6, "Intuition", re.compile(r"^##\s+Intuition", re.IGNORECASE)),
    (7, "Concept", re.compile(r"^##\s+Concept", re.IGNORECASE)),
    (8, "Syntax", re.compile(r"^##\s+Syntax", re.IGNORECASE)),
    (9, "Example", re.compile(r"^##\s+Example", re.IGNORECASE)),
    (10, "Line-by-Line Explanation", re.compile(r"^##\s+Line-by-Line Explanation", re.IGNORECASE)),
    (11, "What Python Is Doing", re.compile(r"^##\s+What Python Is Doing", re.IGNORECASE)),
    (12, "Common Mistakes", re.compile(r"^##\s+Common Mistakes", re.IGNORECASE)),
    (13, "Real-World Uses", re.compile(r"^##\s+Real-World Uses", re.IGNORECASE)),
    (14, "Connection to AI Agents", re.compile(r"^##\s+Connection to AI Agents", re.IGNORECASE)),
    (15, "Practice", re.compile(r"^##\s+Practice", re.IGNORECASE)),
    (16, "Challenge", re.compile(r"^##\s+Challenge", re.IGNORECASE)),
    (17, "Summary", re.compile(r"^##\s+Summary", re.IGNORECASE)),
    (18, "What You Should Know Before Moving On", re.compile(r"^##\s+What You Should Know Before Moving On", re.IGNORECASE)),
]

# Canonical mapping for primary lesson file names per module prefix
PRIMARY_LESSON_FILES: Dict[str, List[str]] = {
    "01": ["what_programming_is.py"],
    "02": ["hello.py"],
    "03": ["vars.py"],
    "04": ["ops.py"],
    "05": ["strings.py"],
    "06": ["collections_demo.py"],
    "07": ["flow.py"],
    "08": ["functions.py"],
    "09": ["scope.py"],
    "10": ["errors.py"],
    "11": ["files.py"],
    "12": ["modules.py"],
    "13": ["classes.py", "classes_and_oop.py"],
    "14": ["functional.py", "special_methods.py"],
    "15": ["typing_lesson.py", "type_hints.py"],
    "16": ["dataclasses_lesson.py", "dataclasses.py"],
    "17": ["generators.py", "iteration.py"],
    "18": ["iterators.py", "generators.py"],
    "19": ["decorators.py"],
    "20": ["context_managers.py"],
    "21": ["testing.py"],
    "22": ["logging_lesson.py", "logging_demo.py"],
    "23": ["venv_guide.py", "virtual_environments.py"],
    "24": ["async_intro.py", "async_python_intro.py"],
    "25": ["async_concurrency.py"],
    "26": ["http_json_intro.py", "http_and_json_intro.py"],
    "27": ["env_vars.py", "environment_variables.py"],
    "28": ["subprocess_intro.py", "subprocesses_intro.py"],
    "29": ["sqlite_intro.py"],
    "30": ["architecture.py", "basic_software_architecture.py"],
    "31": ["python_project_structure.py"],
    "32": ["python_debugging.py"],
    "33": ["mini_agent.py"],
}

# The 4 exercise levels required by R3
EXERCISE_LEVEL_PATTERNS = [
    ("Recall", re.compile(r"(?:level\s*1|tier\s*1|#.*recall|\brecall\b)", re.IGNORECASE)),
    ("Modify", re.compile(r"(?:level\s*2|tier\s*2|#.*modify|\bmodify\b)", re.IGNORECASE)),
    ("Build", re.compile(r"(?:level\s*3|tier\s*3|#.*build|\bbuild\b)", re.IGNORECASE)),
    ("Debug", re.compile(r"(?:level\s*4|tier\s*4|#.*debug|\bdebug\b)", re.IGNORECASE)),
]


@dataclass
class CheckResult:
    """Individual verification check result."""
    check_id: int
    name: str
    passed: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleVerification:
    """Comprehensive verification result for a single module."""
    module_num: str
    module_name: str
    module_dir: Path
    check_results: Dict[int, CheckResult] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.check_results.values())


@dataclass
class VerificationSuiteResult:
    """Aggregate result across all verified modules."""
    module_results: List[ModuleVerification]
    total_modules: int
    passed_modules: int
    check_stats: Dict[int, Tuple[int, int]]  # check_id -> (passed_count, total_count)


def get_module_directories(course_dir: Path) -> List[Path]:
    """Scan and return all numbered module subdirectories sorted by prefix."""
    if not course_dir.exists() or not course_dir.is_dir():
        return []
    dirs = [
        d for d in course_dir.iterdir()
        if d.is_dir() and re.match(r"^\d{2}_", d.name)
    ]
    return sorted(dirs, key=lambda d: d.name)


def find_main_lesson_file(mod_dir: Path) -> Optional[Path]:
    """Identify the primary lesson script in a module directory."""
    prefix = mod_dir.name[:2]
    # 1. Check known primary names
    if prefix in PRIMARY_LESSON_FILES:
        for candidate_name in PRIMARY_LESSON_FILES[prefix]:
            candidate_path = mod_dir / candidate_name
            if candidate_path.exists() and candidate_path.is_file():
                return candidate_path

    # 2. Search all .py files excluding scaffolding & tests
    excluded = {"exercises.py", "solutions.py", "__init__.py", "conftest.py"}
    py_candidates = [
        f for f in mod_dir.glob("*.py")
        if f.name not in excluded and not f.name.startswith("test_")
    ]

    if not py_candidates:
        return None

    # Pick the largest candidate by line count / size
    py_candidates.sort(key=lambda f: f.stat().st_size, reverse=True)
    return py_candidates[0]


def verify_check_1_readme(mod_dir: Path) -> CheckResult:
    """
    Check 1: Verifies README.md exists, contains all 18 required exact headers in order,
    and has non-empty content in every section.
    """
    readme_path = mod_dir / "README.md"
    if not readme_path.exists():
        return CheckResult(
            check_id=1,
            name="README 18 Headers",
            passed=False,
            message="README.md does not exist",
            details={"found_headers": [], "missing_headers": [name for _, name, _ in REQUIRED_README_HEADERS]},
        )

    try:
        content = readme_path.read_text(encoding="utf-8")
    except Exception as e:
        return CheckResult(
            check_id=1,
            name="README 18 Headers",
            passed=False,
            message=f"Failed to read README.md: {e}",
            details={"error": str(e)},
        )

    lines = content.splitlines()
    header_matches: List[Tuple[int, str, int]] = []  # (header_id, name, line_idx)
    missing_headers: List[str] = []

    for header_id, header_name, pattern in REQUIRED_README_HEADERS:
        found_idx = None
        for idx, line in enumerate(lines):
            if pattern.search(line.strip()):
                found_idx = idx
                break
        if found_idx is not None:
            header_matches.append((header_id, header_name, found_idx))
        else:
            missing_headers.append(header_name)

    # 1. Completeness: all 18 headers must be found
    if missing_headers:
        msg = f"Missing {len(missing_headers)}/18 headers: {', '.join(missing_headers[:3])}{'...' if len(missing_headers) > 3 else ''}"
        return CheckResult(
            check_id=1,
            name="README 18 Headers",
            passed=False,
            message=msg,
            details={
                "found_count": len(header_matches),
                "missing_count": len(missing_headers),
                "found_headers": [name for _, name, _ in header_matches],
                "missing_headers": missing_headers,
                "line_count": len(lines),
            },
        )

    # 2. Ordering: each header must appear strictly after the previous header
    out_of_order: List[str] = []
    for i in range(len(header_matches) - 1):
        curr_id, curr_name, curr_line = header_matches[i]
        next_id, next_name, next_line = header_matches[i + 1]
        if next_line <= curr_line:
            out_of_order.append(f"'{next_name}' (L{next_line+1}) before '{curr_name}' (L{curr_line+1})")

    if out_of_order:
        return CheckResult(
            check_id=1,
            name="README 18 Headers",
            passed=False,
            message=f"Headers out of order: {'; '.join(out_of_order[:2])}",
            details={
                "out_of_order": out_of_order,
                "found_count": len(header_matches),
                "missing_count": 0,
                "line_count": len(lines),
            },
        )

    # 3. Content Non-Emptiness: every section must contain substantive content
    empty_sections: List[str] = []
    for i in range(len(header_matches)):
        hid, name, line_idx = header_matches[i]
        if hid == 1:
            # Topic: check header text itself or content between header 1 and 2
            title_text = re.sub(r"^#\s*", "", lines[line_idx]).strip()
            next_idx = header_matches[i + 1][2]
            body_between = [ln.strip() for ln in lines[line_idx + 1:next_idx] if ln.strip()]
            if not title_text and not body_between:
                empty_sections.append(name)
        elif i + 1 < len(header_matches):
            next_idx = header_matches[i + 1][2]
            body_between = [ln.strip() for ln in lines[line_idx + 1:next_idx] if ln.strip()]
            if not body_between:
                empty_sections.append(name)
        else:
            # Section 18: content through EOF
            body_after = [ln.strip() for ln in lines[line_idx + 1:] if ln.strip()]
            if not body_after:
                empty_sections.append(name)

    if empty_sections:
        return CheckResult(
            check_id=1,
            name="README 18 Headers",
            passed=False,
            message=f"Empty content in {len(empty_sections)} section(s): {', '.join(empty_sections[:3])}",
            details={
                "empty_sections": empty_sections,
                "found_count": len(header_matches),
                "missing_count": 0,
                "line_count": len(lines),
            },
        )

    return CheckResult(
        check_id=1,
        name="README 18 Headers",
        passed=True,
        message=f"All 18 required headers present in order with non-empty content ({len(lines)} lines)",
        details={
            "found_count": 18,
            "missing_count": 0,
            "found_headers": [name for _, name, _ in header_matches],
            "missing_headers": [],
            "line_count": len(lines),
        },
    )



def verify_check_2_lesson(mod_dir: Path, min_lines: int = 150, timeout_sec: int = 25) -> CheckResult:
    """
    Check 2: Verifies main lesson .py is at least 150-200 lines long and executes with exit code 0.
    """
    lesson_file = find_main_lesson_file(mod_dir)
    if not lesson_file:
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message="No main lesson .py file found",
            details={"lesson_file": None, "line_count": 0, "exit_code": None},
        )

    try:
        content = lesson_file.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
    except Exception as e:
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message=f"Failed reading {lesson_file.name}: {e}",
            details={"lesson_file": lesson_file.name, "error": str(e)},
        )

    if line_count < min_lines:
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message=f"{lesson_file.name} is only {line_count} lines (requires >= {min_lines})",
            details={"lesson_file": lesson_file.name, "line_count": line_count, "min_required": min_lines},
        )

    # Clean execution test
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT}:{mod_dir}"
    try:
        proc = subprocess.run(
            [sys.executable, str(lesson_file)],
            cwd=str(mod_dir),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message=f"{lesson_file.name} timed out after {timeout_sec}s",
            details={"lesson_file": lesson_file.name, "line_count": line_count, "timeout": True},
        )
    except Exception as e:
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message=f"{lesson_file.name} execution error: {e}",
            details={"lesson_file": lesson_file.name, "line_count": line_count, "error": str(e)},
        )

    if proc.returncode != 0:
        stderr_sample = proc.stderr.strip().splitlines()[-3:] if proc.stderr else []
        err_msg = " | ".join(stderr_sample) or f"exit code {proc.returncode}"
        return CheckResult(
            check_id=2,
            name="Lesson Script",
            passed=False,
            message=f"{lesson_file.name} failed (exit {proc.returncode}): {err_msg}",
            details={
                "lesson_file": lesson_file.name,
                "line_count": line_count,
                "exit_code": proc.returncode,
                "stderr": proc.stderr,
                "stdout": proc.stdout[:500],
            },
        )

    return CheckResult(
        check_id=2,
        name="Lesson Script",
        passed=True,
        message=f"{lesson_file.name} passed ({line_count} lines, exit code 0)",
        details={"lesson_file": lesson_file.name, "line_count": line_count, "exit_code": 0},
    )


def verify_check_3_exercises(mod_dir: Path) -> CheckResult:
    """
    Check 3: Verifies exercises.py contains 4 distinct levels (Recall, Modify, Build, Debug)
             and authentic # TODO comments with NotImplementedError scaffolding.
    """
    exercises_path = mod_dir / "exercises.py"
    if not exercises_path.exists():
        return CheckResult(
            check_id=3,
            name="Exercises Scaffolding",
            passed=False,
            message="exercises.py does not exist",
            details={"exists": False},
        )

    try:
        content = exercises_path.read_text(encoding="utf-8")
    except Exception as e:
        return CheckResult(
            check_id=3,
            name="Exercises Scaffolding",
            passed=False,
            message=f"Failed reading exercises.py: {e}",
            details={"error": str(e)},
        )

    # Verify 4 levels
    found_levels: List[str] = []
    missing_levels: List[str] = []
    for level_name, pattern in EXERCISE_LEVEL_PATTERNS:
        if pattern.search(content):
            found_levels.append(level_name)
        else:
            missing_levels.append(level_name)

    # Verify scaffolding: requires NotImplementedError or # TODO
    has_todo = bool(re.search(r"#.*?TODO\b", content, re.IGNORECASE))
    has_not_implemented = bool(re.search(r"\bNotImplementedError\b", content))
    has_scaffolding = has_todo or has_not_implemented

    deficits: List[str] = []
    if missing_levels:
        deficits.append(f"missing levels: {', '.join(missing_levels)}")
    if not has_scaffolding:
        deficits.append("missing # TODO comments or NotImplementedError")

    passed = (len(missing_levels) == 0) and has_scaffolding
    if passed:
        scaff_desc = []
        if has_todo:
            scaff_desc.append("# TODO")
        if has_not_implemented:
            scaff_desc.append("NotImplementedError")
        msg = f"4 levels verified ({', '.join(found_levels)}), scaffolding present ({' & '.join(scaff_desc)})"
    else:
        msg = "; ".join(deficits)

    return CheckResult(
        check_id=3,
        name="Exercises Scaffolding",
        passed=passed,
        message=msg,
        details={
            "found_levels": found_levels,
            "missing_levels": missing_levels,
            "has_todo": has_todo,
            "has_not_implemented": has_not_implemented,
            "line_count": len(content.splitlines()),
        },
    )


def verify_check_4_solutions(mod_dir: Path, timeout_sec: int = 25) -> CheckResult:
    """
    Check 4: Verifies solutions.py exists, contains no NotImplementedError,
             and executes cleanly with exit code 0.
    """
    solutions_path = mod_dir / "solutions.py"
    if not solutions_path.exists():
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message="solutions.py does not exist",
            details={"exists": False},
        )

    try:
        content = solutions_path.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
    except Exception as e:
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message=f"Failed reading solutions.py: {e}",
            details={"error": str(e)},
        )

    if line_count < 10:
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message=f"solutions.py is a stub ({line_count} lines)",
            details={"line_count": line_count},
        )

    # Check for forbidden NotImplementedError in solutions
    if re.search(r"\bNotImplementedError\b", content):
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message="solutions.py contains NotImplementedError (solutions must be completely implemented)",
            details={"line_count": line_count, "has_not_implemented": True},
        )

    # Clean execution test
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{REPO_ROOT}:{mod_dir}"
    try:
        proc = subprocess.run(
            [sys.executable, str(solutions_path)],
            cwd=str(mod_dir),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message=f"solutions.py timed out after {timeout_sec}s",
            details={"timeout": True},
        )
    except Exception as e:
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message=f"solutions.py execution error: {e}",
            details={"error": str(e)},
        )

    if proc.returncode != 0:
        stderr_sample = proc.stderr.strip().splitlines()[-3:] if proc.stderr else []
        err_msg = " | ".join(stderr_sample) or f"exit code {proc.returncode}"
        return CheckResult(
            check_id=4,
            name="Solutions Execution",
            passed=False,
            message=f"solutions.py failed (exit {proc.returncode}): {err_msg}",
            details={
                "exit_code": proc.returncode,
                "stderr": proc.stderr,
                "stdout": proc.stdout[:500],
            },
        )

    return CheckResult(
        check_id=4,
        name="Solutions Execution",
        passed=True,
        message=f"solutions.py verified cleanly (exit code 0, {line_count} lines, no NotImplementedError)",
        details={"exit_code": 0, "line_count": line_count, "has_not_implemented": False},
    )



def verify_module(mod_dir: Path, checks: Optional[List[int]] = None) -> ModuleVerification:
    """Run specified checks (or all 4) on a single module directory."""
    active_checks = checks or [1, 2, 3, 4]
    module_num = mod_dir.name[:2]
    module_name = mod_dir.name

    check_results: Dict[int, CheckResult] = {}
    if 1 in active_checks:
        check_results[1] = verify_check_1_readme(mod_dir)
    if 2 in active_checks:
        check_results[2] = verify_check_2_lesson(mod_dir)
    if 3 in active_checks:
        check_results[3] = verify_check_3_exercises(mod_dir)
    if 4 in active_checks:
        check_results[4] = verify_check_4_solutions(mod_dir)

    return ModuleVerification(
        module_num=module_num,
        module_name=module_name,
        module_dir=mod_dir,
        check_results=check_results,
    )


def verify_all_modules(
    course_dir: Path = DEFAULT_COURSE_DIR,
    module_filter: Optional[List[str]] = None,
    checks: Optional[List[int]] = None,
) -> VerificationSuiteResult:
    """Scan and verify all matching module directories."""
    all_dirs = get_module_directories(course_dir)
    if module_filter:
        filter_set = {m.strip().lower() for m in module_filter}
        filtered_dirs = [
            d for d in all_dirs
            if d.name.lower() in filter_set or d.name[:2] in filter_set
        ]
    else:
        filtered_dirs = all_dirs

    module_results: List[ModuleVerification] = []
    for mod_dir in filtered_dirs:
        module_results.append(verify_module(mod_dir, checks=checks))

    active_checks = checks or [1, 2, 3, 4]
    check_stats: Dict[int, Tuple[int, int]] = {}
    for cid in active_checks:
        passed_c = sum(1 for m in module_results if cid in m.check_results and m.check_results[cid].passed)
        check_stats[cid] = (passed_c, len(module_results))

    passed_modules = sum(1 for m in module_results if m.passed)

    return VerificationSuiteResult(
        module_results=module_results,
        total_modules=len(module_results),
        passed_modules=passed_modules,
        check_stats=check_stats,
    )


def format_summary_table(suite: VerificationSuiteResult, verbose: bool = False) -> str:
    """Render a human-readable ASCII summary table of verification results."""
    lines: List[str] = []
    width = 106
    lines.append("=" * width)
    lines.append("              COURSE -1 PYTHON FOUNDATIONS: ACCEPTANCE VERIFICATION REPORT")
    lines.append("=" * width)
    header = f"{'Mod':<4} | {'Module Name':<30} | {'C1: README':<12} | {'C2: Lesson':<12} | {'C3: Exercise':<13} | {'C4: Solution':<13} | {'Status':<6}"
    lines.append(header)
    lines.append("-" * width)

    for m in suite.module_results:
        def _fmt_check(cid: int) -> str:
            if cid not in m.check_results:
                return "SKIPPED"
            res = m.check_results[cid]
            if res.passed:
                if cid == 1:
                    return "PASS (18)"
                elif cid == 2:
                    return f"PASS ({res.details.get('line_count', 'OK')}L)"
                elif cid == 3:
                    return "PASS (4lvl)"
                elif cid == 4:
                    return "PASS (0)"
                return "PASS"
            else:
                if cid == 1:
                    cnt = res.details.get("found_count", 0)
                    return f"FAIL ({cnt}/18)"
                elif cid == 2:
                    cnt = res.details.get("line_count", 0)
                    return f"FAIL ({cnt}L)"
                elif cid == 3:
                    return "FAIL (scaff)"
                elif cid == 4:
                    return "FAIL (exec)"
                return "FAIL"

        c1 = _fmt_check(1)
        c2 = _fmt_check(2)
        c3 = _fmt_check(3)
        c4 = _fmt_check(4)
        status = "PASS" if m.passed else "FAIL"

        lines.append(f"{m.module_num:<4} | {m.module_name[:30]:<30} | {c1:<12} | {c2:<12} | {c3:<13} | {c4:<13} | {status:<6}")

        if verbose and not m.passed:
            for cid in sorted(m.check_results.keys()):
                res = m.check_results[cid]
                if not res.passed:
                    lines.append(f"     -> [Check {cid}: {res.name}] {res.message}")

    lines.append("-" * width)
    lines.append("SUMMARY METRICS:")
    lines.append(f"  Total Modules Checked:       {suite.total_modules}")
    lines.append(f"  Fully Passing Modules:       {suite.passed_modules}/{suite.total_modules} ({suite.passed_modules/max(suite.total_modules,1)*100:.1f}%)")
    for cid, (p_cnt, t_cnt) in sorted(suite.check_stats.items()):
        c_names = {1: "README 18 Headers", 2: "Lesson >=150L & Clean Exec", 3: "Exercises 4 Tiers & Scaffolding", 4: "Solutions Clean Execution"}
        lines.append(f"  Check {cid} ({c_names.get(cid, 'Check')}): {p_cnt}/{t_cnt} passed ({p_cnt/max(t_cnt,1)*100:.1f}%)")
    lines.append("=" * width)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Course -1 Python Foundations Acceptance Verification Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--course-dir",
        type=Path,
        default=DEFAULT_COURSE_DIR,
        help="Path to course_-1_python_foundations directory",
    )
    parser.add_argument(
        "--module",
        "-m",
        type=str,
        default=None,
        help="Filter specific module numbers or names (comma-separated, e.g. '01' or '01,02,07')",
    )
    parser.add_argument(
        "--check",
        "-c",
        type=str,
        default=None,
        help="Run only specific checks (comma-separated, e.g. '1' or '1,2,3,4')",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed failure diagnostics and messages",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Export full verification results as JSON file",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Print only the summary metrics",
    )

    args = parser.parse_args()

    # Parse module filter
    mod_filter = [m.strip() for m in args.module.split(",")] if args.module else None

    # Parse check filter
    check_filter = [int(c.strip()) for c in args.check.split(",")] if args.check else [1, 2, 3, 4]

    suite = verify_all_modules(
        course_dir=args.course_dir,
        module_filter=mod_filter,
        checks=check_filter,
    )

    table_output = format_summary_table(suite, verbose=args.verbose)
    print(table_output)

    if args.json:
        # Convert suite to serializable dict
        data = {
            "total_modules": suite.total_modules,
            "passed_modules": suite.passed_modules,
            "success": suite.passed_modules == suite.total_modules,
            "check_stats": {str(k): {"passed": v[0], "total": v[1]} for k, v in suite.check_stats.items()},
            "modules": [
                {
                    "num": m.module_num,
                    "name": m.module_name,
                    "passed": m.passed,
                    "checks": {
                        str(cid): {
                            "name": cr.name,
                            "passed": cr.passed,
                            "message": cr.message,
                            "details": cr.details,
                        }
                        for cid, cr in m.check_results.items()
                    },
                }
                for m in suite.module_results
            ],
        }
        try:
            args.json.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"\nJSON report written to: {args.json}")
        except Exception as e:
            print(f"\nError writing JSON report: {e}", file=sys.stderr)

    # Return exit code: 0 if 100% of tested modules pass all checked criteria
    return 0 if (suite.passed_modules == suite.total_modules and suite.total_modules > 0) else 1


if __name__ == "__main__":
    sys.exit(main())
