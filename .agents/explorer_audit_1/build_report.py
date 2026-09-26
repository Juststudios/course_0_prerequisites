#!/usr/bin/env python3
"""
Generate comprehensive audit_report.md from detailed_audit.json.
"""

import json
from pathlib import Path

def generate_report():
    data_path = Path("/home/settings/Documents/pearl/.agents/explorer_audit_1/detailed_audit.json")
    report_path = Path("/home/settings/Documents/pearl/.agents/explorer_audit_1/audit_report.md")
    
    with open(data_path, "r", encoding="utf-8") as f:
        modules = json.load(f)

    total_modules = len(modules)
    passing_modules = [m for m in modules if m["overall_status"] == "PASS"]
    failing_modules = [m for m in modules if m["overall_status"] != "PASS"]

    # Check stats
    r1_pass = [m for m in modules if m["readme"].get("passed")]
    r2_pass = [m for m in modules if m["lesson"].get("passed")]
    r3_ex_pass = [m for m in modules if m["exercises"].get("passed")]
    r3_sol_pass = [m for m in modules if m["solutions"].get("passed")]

    # Milestone breakdown
    by_ms = {}
    for m in modules:
        by_ms.setdefault(m["milestone"], []).append(m)

    lines = []
    lines.append("# Comprehensive Audit Report: Course -1 Python Foundations")
    lines.append("")
    lines.append("**Auditor**: Explorer Audit 1 (`teamwork_preview_explorer`)  ")
    lines.append("**Date**: 2026-09-21T15:20:00Z  ")
    lines.append("**Target Directory**: `/home/settings/Documents/pearl/course_-1_python_foundations/`  ")
    lines.append("**Audited Scope**: 33 modules (`01_what_programming_is` through `33_integrated_projects`)  ")
    lines.append("**Governing Requirements**: R1 (18-section README), R2 (150-200+ line lesson script), R3 (4-tier exercises with TODOs & clean solutions), R4 (100% curriculum completeness), E2E Test Track  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"A rigorous, automated, and structural audit was conducted across all **{total_modules} module directories** in Course -1 (`course_-1_python_foundations/`).")
    lines.append("")
    lines.append("### Key Audit Metrics")
    lines.append(f"- **Overall Curriculum Pass Rate**: **{len(passing_modules)}/{total_modules}** ({len(passing_modules)/total_modules*100:.1f}%) fully compliant")
    lines.append(f"- **Failing / Remediation Required**: **{len(failing_modules)}/{total_modules}** ({len(failing_modules)/total_modules*100:.1f}%)")
    lines.append(f"- **R1 — Pedagogical README (18 exact headers in order)**: **{len(r1_pass)}/{total_modules}** ({len(r1_pass)/total_modules*100:.1f}%)")
    lines.append(f"- **R2 — Main Lesson Script (>=150 lines, commented, clean run)**: **{len(r2_pass)}/{total_modules}** ({len(r2_pass)/total_modules*100:.1f}%)")
    lines.append(f"- **R3 — Progressive Exercises (4 distinct tiers, TODOs, NotImplementedError)**: **{len(r3_ex_pass)}/{total_modules}** ({len(r3_ex_pass)/total_modules*100:.1f}%)")
    lines.append(f"- **R3 — Reference Solutions (clean execution, exit code 0, full answers)**: **{len(r3_sol_pass)}/{total_modules}** ({len(r3_sol_pass)/total_modules*100:.1f}%)")
    lines.append(f"- **E2E Test Track**: `scripts/verify_course_minus_1.py` is **ACTIVE & OPERATIONAL** (697 lines); `tests/e2e/test_course_minus_1_acceptance.py` is **MISSING**.")
    lines.append("")
    lines.append("### Core Findings at a Glance")
    lines.append("1. **Gold Standard Modules (9 modules)**: Modules `01`, `02`, `07`, `08`, `17`, `23`, `24`, `30`, and `31` have been completed to exceptional pedagogical depth, featuring 135-356 line READMEs with all 18 headers in exact sequence, 193-331 line executable lesson scripts, authentic 4-tier exercises with TODOs, and verified clean solutions.")
    lines.append("2. **Partially Completed / Near-Pass Modules (2 modules)**:")
    lines.append("   - `09_scope`: Lesson (`scope.py`, 313 lines), `exercises.py` (139 lines), and `solutions.py` (158 lines) ALL PASS cleanly. Only `README.md` (6 lines, stub) failed.")
    lines.append("   - `25_async_concurrency`: `README.md` (187 lines, 18 headers) PASSES. Only code files (`async_concurrency.py` 27L, `exercises.py` 3L, `solutions.py` 1L) are stubs.")
    lines.append("3. **Missing Module (1 module)**: Module `14_functional_programming` directory exists but is **completely empty** (0 files).")
    lines.append("4. **Broken Solution Dependency (1 module)**: `21_testing/solutions.py` crashes on execution with `ModuleNotFoundError: No module named 'pytest'` because pytest is not installed in the workspace Python environment.")
    lines.append("5. **Stub / Template Modules (20 modules)**: The remaining 20 modules contain initial stub code generated from early scaffolding (`generate_course_minus_1.py`), featuring 1-50 line scripts, missing or stub exercises, and incomplete READMEs.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Comprehensive 33-Module Audit Matrix")
    lines.append("")
    lines.append("| Mod | Directory Name | Milestone | R1: README (18 Hdr) | R2: Lesson (>=150L) | R3: Exercises (4-Tier) | R3: Solutions (Exit 0) | Status |")
    lines.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")

    for m in modules:
        prefix = m["prefix"]
        name = m["name"]
        ms = m["milestone"]
        r = m["readme"]
        l = m["lesson"]
        e = m["exercises"]
        s = m["solutions"]

        # R1 format
        if r.get("passed"):
            r_str = f"PASS ({r.get('lines')}L)"
        elif not r.get("exists"):
            r_str = "FAIL (Missing)"
        else:
            r_str = f"FAIL ({r.get('headers_present')}/18)"

        # R2 format
        if l.get("passed"):
            l_str = f"PASS ({l.get('lines')}L)"
        elif not l.get("exists"):
            l_str = "FAIL (Missing)"
        else:
            l_str = f"FAIL ({l.get('lines')}L)"

        # R3 Ex format
        if e.get("passed"):
            e_str = f"PASS ({e.get('lines')}L, {e.get('todo_count')}T)"
        elif not e.get("exists"):
            e_str = "FAIL (Missing)"
        else:
            e_str = f"FAIL ({e.get('lines')}L, scaff)"

        # R3 Sol format
        if s.get("passed"):
            s_str = f"PASS ({s.get('lines')}L)"
        elif not s.get("exists"):
            s_str = "FAIL (Missing)"
        elif s.get("exit_code") not in (None, 0):
            s_str = f"FAIL (Exit {s.get('exit_code')})"
        else:
            s_str = f"FAIL ({s.get('lines')}L, stub)"

        status_str = "**PASS**" if m["overall_status"] == "PASS" else "FAIL"
        lines.append(f"| `{prefix}` | `{name}` | {ms} | {r_str} | {l_str} | {e_str} | {s_str} | {status_str} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Milestone-by-Milestone Diagnostic Analysis")
    lines.append("")

    for ms_name, ms_mods in sorted(by_ms.items()):
        ms_pass = [m for m in ms_mods if m["overall_status"] == "PASS"]
        ms_fail = [m for m in ms_mods if m["overall_status"] != "PASS"]
        lines.append(f"### Milestone {ms_name} ({len(ms_pass)}/{len(ms_mods)} passing)")
        lines.append("")
        
        for m in ms_mods:
            status_icon = "✅ PASS" if m["overall_status"] == "PASS" else "❌ FAIL"
            lines.append(f"#### Module {m['prefix']}: `{m['name']}` — {status_icon}")
            lines.append(f"- **Directory**: `/home/settings/Documents/pearl/course_-1_python_foundations/{m['name']}`")
            
            # README diagnosis
            r = m["readme"]
            if r.get("passed"):
                lines.append(f"- **R1 README.md**: ✅ PASS ({r.get('lines')} lines, {r.get('words')} words, all 18 headers in exact order).")
            elif not r.get("exists"):
                lines.append(f"- **R1 README.md**: ❌ MISSING file entirely.")
            else:
                lines.append(f"- **R1 README.md**: ❌ FAIL — {r.get('headers_present')}/18 headers present ({r.get('lines')} lines). Missing headers: `{', '.join(r.get('missing_headers', [])[:4])}`...")

            # Lesson diagnosis
            l = m["lesson"]
            if l.get("passed"):
                lines.append(f"- **R2 Lesson (`{l.get('filename')}`)**: ✅ PASS ({l.get('lines')} lines >= 150, {l.get('comments')} comments, {l.get('prints')} print statements, exit code 0).")
            elif not l.get("exists"):
                lines.append(f"- **R2 Lesson**: ❌ MISSING main lesson script.")
            else:
                err_detail = f" (Exit {l.get('exit_code')})" if l.get("exit_code") not in (None, 0) else ""
                lines.append(f"- **R2 Lesson (`{l.get('filename')}`)**: ❌ FAIL — {l.get('lines')} lines (requires >= 150){err_detail}, {l.get('comments')} comments, {l.get('prints')} prints.")

            # Exercises diagnosis
            e = m["exercises"]
            if e.get("passed"):
                lines.append(f"- **R3 Exercises (`exercises.py`)**: ✅ PASS ({e.get('lines')} lines, 4 tiers present, {e.get('todo_count')} `# TODO`s, {e.get('not_implemented_count')} `NotImplementedError`s).")
            elif not e.get("exists"):
                lines.append(f"- **R3 Exercises**: ❌ MISSING `exercises.py`.")
            else:
                missing_lvls = f", missing tiers: {e.get('missing_levels')}" if e.get("missing_levels") else ""
                scaff = []
                if e.get("todo_count") == 0: scaff.append("no # TODO")
                if e.get("not_implemented_count") == 0: scaff.append("no NotImplementedError")
                scaff_str = f", scaffolding defect: {', '.join(scaff)}" if scaff else ""
                lines.append(f"- **R3 Exercises (`exercises.py`)**: ❌ FAIL — {e.get('lines')} lines{missing_lvls}{scaff_str}.")

            # Solutions diagnosis
            s = m["solutions"]
            if s.get("passed"):
                lines.append(f"- **R3 Solutions (`solutions.py`)**: ✅ PASS ({s.get('lines')} lines, exit code 0).")
            elif not s.get("exists"):
                lines.append(f"- **R3 Solutions**: ❌ MISSING `solutions.py`.")
            elif s.get("exit_code") not in (None, 0):
                lines.append(f"- **R3 Solutions (`solutions.py`)**: ❌ RUNTIME ERROR (exit {s.get('exit_code')}): `{s.get('stderr', '').strip().replace(chr(10), ' | ')}`")
            else:
                lines.append(f"- **R3 Solutions (`solutions.py`)**: ❌ FAIL — stub file ({s.get('lines')} lines < 10).")

            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 4. Test Track & Acceptance Infrastructure")
    lines.append("")
    lines.append("### Status of Test Artifacts")
    lines.append("1. **`scripts/verify_course_minus_1.py`**: **EXISTS & OPERATIONAL**  ")
    lines.append("   - Path: `/home/settings/Documents/pearl/scripts/verify_course_minus_1.py`  ")
    lines.append("   - Total Lines: 697 lines  ")
    lines.append("   - Capabilities: Implements Check 1 (18 exact headers), Check 2 (lesson >= 150 lines and exit code 0), Check 3 (exercises 4 levels and authentic TODO/NotImplementedError), Check 4 (solutions exit code 0 and non-stub). Supports CLI flags `--module`, `--check`, `--json`, `--verbose`. Returns exit code 0 only when 100% of checked modules pass.  ")
    lines.append("")
    lines.append("2. **`tests/e2e/test_course_minus_1_acceptance.py`**: **MISSING**  ")
    lines.append("   - Path: `/home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py`  ")
    lines.append("   - Requirement: As documented in `PROJECT.md` line 100, the Test Writer agent has exclusive ownership to author this acceptance test file.  ")
    lines.append("   - Recommendation: The test file should wrap `verify_all_modules` from `scripts.verify_course_minus_1` into parametrized `pytest` test cases so that standard project CI/CD `pytest tests/e2e/test_course_minus_1_acceptance.py` reports each module and each check cleanly.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Critical Technical Gaps & Root Cause Analysis")
    lines.append("")
    lines.append("### Gap 1: Empty Module `14_functional_programming`")
    lines.append("- **Location**: `/home/settings/Documents/pearl/course_-1_python_foundations/14_functional_programming`")
    lines.append("- **Symptom**: Directory exists but has zero files.")
    lines.append("- **Root Cause**: Module was skipped during initial scaffolding or file generation.")
    lines.append("- **Action for Worker M3**: Must create all four files from scratch: `README.md` (18 headers, covering lambdas, map, filter, list/dict/set comprehensions, pure functions, closures), `functional.py` (>= 150 lines), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("")
    lines.append("### Gap 2: Third-Party Test Runner Dependency in `21_testing`")
    lines.append("- **Location**: `/home/settings/Documents/pearl/course_-1_python_foundations/21_testing/solutions.py`")
    lines.append("- **Symptom**: Fails with `ModuleNotFoundError: No module named 'pytest'` when executed directly.")
    lines.append("- **Root Cause**: The workspace environment (`.venv`) does not have `pytest` installed. Direct execution `python3 solutions.py` fails on `import pytest`.")
    lines.append("- **Action for Worker M4**: Either install `pytest` in `.venv` or (preferably for zero-dependency beginner foundation) write testing examples using Python standard library `unittest` and conditional `pytest` imports with fallback so `python3 solutions.py` executes cleanly without external dependencies.")
    lines.append("")
    lines.append("### Gap 3: Missing Scaffolding TODOs in Exercise Files (Modules 12, 13, 16, 18, 19, 20)")
    lines.append("- **Location**: Modules 12, 13, 16, 18, 19, 20")
    lines.append("- **Symptom**: `exercises.py` has level headers but 0 `# TODO` comments.")
    lines.append("- **Root Cause**: The stub generator created exercise files with function signatures and `raise NotImplementedError` but omitted `# TODO` comments required by Check 3.")
    lines.append("- **Action for Workers M3 & M4**: Ensure every exercise function contains explicit `# TODO` prompts and authentic `raise NotImplementedError(...)`.")
    lines.append("")
    lines.append("### Gap 4: Near-Complete Modules Needing Single-Component Remediation")
    lines.append("- **`09_scope` (Worker M2)**: `scope.py` (313L), `exercises.py` (139L), and `solutions.py` (158L) are fully compliant and excellent. Only `README.md` needs the 18-header rewrite.")
    lines.append("- **`25_async_concurrency` (Worker M5)**: `README.md` (187L) is 100% compliant and pedagogically rich. Only the code files (`async_concurrency.py`, `exercises.py`, `solutions.py`) need full rewrite to >=150L standard.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Granular Work Orders for Milestone Workers")
    lines.append("")
    lines.append("Based on write-ownership partitioning from `PROJECT.md`, the following work packages are assigned:")
    lines.append("")
    lines.append("### Work Order: Test Writer")
    lines.append("- **Owner**: Test Writer")
    lines.append("- **Exclusive Paths**: `/home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py`, `scripts/verify_course_minus_1.py`")
    lines.append("- **Tasks**:")
    lines.append("  1. Create `/home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py`.")
    lines.append("  2. Implement parametrized tests verifying R1, R2, R3, and R4 across all 33 modules.")
    lines.append("  3. Ensure integration with `pytest` and direct CLI execution.")
    lines.append("")
    lines.append("### Work Order: Worker M1 (Modules 01–06)")
    lines.append("- **Owner**: Worker M1")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/0[1-6]_*`")
    lines.append("- **Status**: 01 and 02 are **COMPLETE** (keep untouched).")
    lines.append("- **Tasks**:")
    lines.append("  1. **`03_variables_and_data_types`**: Full rewrite — `README.md` (18 headers, primitive types, dynamic typing, type conversion, memory model), `vars.py` (>= 150L, type introspection, casting, print outputs), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  2. **`04_operators`**: Full rewrite — `README.md` (18 headers, arithmetic, boolean logic, short-circuiting, bitwise), `ops.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  3. **`05_strings`**: Full rewrite — `README.md` (18 headers, immutability, formatting, slicing, methods, tokenization for agents), `strings.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  4. **`06_collections`**: Full rewrite — `README.md` (18 headers, lists, dicts, sets, tuples, big-O, mutability), `collections_demo.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("")
    lines.append("### Work Order: Worker M2 (Modules 07–11)")
    lines.append("- **Owner**: Worker M2")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/0[7-9]_*`, `course_-1_python_foundations/1[0-1]_*`")
    lines.append("- **Status**: 07 and 08 are **COMPLETE** (keep untouched).")
    lines.append("- **Tasks**:")
    lines.append("  1. **`09_scope`**: **HIGH LEVERAGE** — Code files already pass! Rewrite `README.md` to include all 18 headers in exact order (LEGB rule, global, nonlocal, closures). Leave `scope.py`, `exercises.py`, and `solutions.py` as-is.")
    lines.append("  2. **`10_errors_and_exceptions`**: Full rewrite — `README.md` (18 headers, try/except/else/finally, custom exceptions, error resilience for agents), `errors.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  3. **`11_files`**: Upgrade `README.md` (add missing 12 headers), expand `files.py` from 49 to >= 150 lines (context managers, encodings, JSON file handling, path manipulation). Expand exercises and solutions.")
    lines.append("")
    lines.append("### Work Order: Worker M3 (Modules 12–16)")
    lines.append("- **Owner**: Worker M3")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/1[2-6]_*`")
    lines.append("- **Status**: 0/5 passing. Highest urgency milestone.")
    lines.append("- **Tasks**:")
    lines.append("  1. **`12_modules`**: Upgrade `README.md` (18 headers), expand `modules.py` to >= 150L, add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("  2. **`13_classes_and_oop`**: Upgrade `README.md` (18 headers), expand `classes_and_oop.py` (from 74L to >= 150L, inheritance, encapsulation, dunder methods), add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("  3. **`14_functional_programming`**: **FROM SCRATCH** — Author full 18-header `README.md`, `functional.py` (>= 150L, lambdas, map, filter, list/dict comps, closures), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  4. **`15_type_hints`**: Upgrade `README.md` (18 headers), expand `type_hints.py` (from 55L to >= 150L, Union, Optional, Callable, generics, TypeVar), expand exercises and solutions.")
    lines.append("  5. **`16_dataclasses`**: Upgrade `README.md` (18 headers), expand `dataclasses_lesson.py` (from 40L to >= 150L, field, default_factory, frozen, __post_init__), add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("")
    lines.append("### Work Order: Worker M4 (Modules 17–22)")
    lines.append("- **Owner**: Worker M4")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/1[7-9]_*`, `course_-1_python_foundations/2[0-2]_*`")
    lines.append("- **Status**: 17 is **COMPLETE** (keep untouched).")
    lines.append("- **Tasks**:")
    lines.append("  1. **`18_iterators`**: Upgrade `README.md` (18 headers), expand `iterators.py` (from 51L to >= 150L, iter(), next(), StopIteration, itertools), add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("  2. **`19_decorators`**: Upgrade `README.md` (18 headers), expand `decorators.py` (from 81L to >= 150L, wraps, parameterized decorators, timing/caching), add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("  3. **`20_context_managers`**: Upgrade `README.md` (18 headers), expand `context_managers.py` (from 59L to >= 150L, __enter__/__exit__, contextlib.contextmanager), add `# TODO` to `exercises.py`, expand `solutions.py`.")
    lines.append("  4. **`21_testing`**: **CRITICAL FIX** — Upgrade `README.md` (18 headers), expand `testing.py` to >= 150L. Fix `solutions.py` so it does NOT fail when `pytest` is absent: use standard library `unittest` as primary executable harness, with optional pytest syntax demonstrated inside functions. Verify clean exit 0.")
    lines.append("  5. **`22_logging`**: Full rewrite from 1-line stub — `README.md` (18 headers, levels, handlers, formatters, agent telemetry), `logging_lesson.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("")
    lines.append("### Work Order: Worker M5 (Modules 23–29)")
    lines.append("- **Owner**: Worker M5")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/2[3-9]_*`")
    lines.append("- **Status**: 23 and 24 are **COMPLETE** (keep untouched).")
    lines.append("- **Tasks**:")
    lines.append("  1. **`25_async_concurrency`**: **HIGH LEVERAGE** — `README.md` already passes! Only rewrite code: `async_concurrency.py` (from 27L to >= 150L, asyncio.gather, TaskGroup, Queues, Semaphores), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  2. **`26_http_and_json_intro`**: Full rewrite from stubs — `README.md` (18 headers, HTTP methods, status codes, json dumps/loads, urllib/requests), `http_json_intro.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  3. **`27_environment_variables`**: Full rewrite from stubs — `README.md` (18 headers, os.environ, dotenv, secrets security for API keys), `env_vars.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  4. **`28_subprocesses_intro`**: Full rewrite from stubs — `README.md` (18 headers, subprocess.run, pipes, timeouts, CLI tool execution for agents), `subprocess_intro.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("  5. **`29_sqlite_intro`**: Full rewrite from stubs — `README.md` (18 headers, sqlite3, DDL/DML, parameterized queries, transactions, agent episodic memory), `sqlite_intro.py` (>= 150L), `exercises.py` (4 tiers with TODOs), `solutions.py` (clean exit 0).")
    lines.append("")
    lines.append("### Work Order: Worker M6 (Modules 30–33)")
    lines.append("- **Owner**: Worker M6")
    lines.append("- **Exclusive Paths**: `course_-1_python_foundations/3[0-3]_*`")
    lines.append("- **Status**: 30 and 31 are **COMPLETE** (keep untouched).")
    lines.append("- **Tasks**:")
    lines.append("  1. **`32_python_debugging`**: Full rewrite — `README.md` (18 headers, pdb, breakpoint(), post-mortem debugging, tracebacks), `python_debugging.py` (expand from 47L to >= 150L), author `exercises.py` (4 tiers with TODOs), author `solutions.py` (clean exit 0).")
    lines.append("  2. **`33_integrated_projects`**: Capstone project — Rewrite `README.md` (18 headers, tool-using mini ReAct agent architecture, state machine, logging, memory persistence), expand `mini_agent.py` from 138L to >= 150L, author `exercises.py` (4 tiers with TODOs), author `solutions.py` (clean exit 0).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Verification Method & Acceptance Gate")
    lines.append("")
    lines.append("To verify all 33 modules after worker completion:")
    lines.append("```bash")
    lines.append("# 1. Run full verification harness across all 33 modules")
    lines.append("python3 scripts/verify_course_minus_1.py --verbose")
    lines.append("")
    lines.append("# 2. Verify individual milestones (e.g. Milestone M1)")
    lines.append("python3 scripts/verify_course_minus_1.py --module 01,02,03,04,05,06 --verbose")
    lines.append("")
    lines.append("# 3. Run E2E pytest suite once authored")
    lines.append("pytest tests/e2e/test_course_minus_1_acceptance.py -v")
    lines.append("```")
    lines.append("")
    lines.append("The final gate requires: `Total Modules Checked: 33`, `Fully Passing Modules: 33/33 (100.0%)`, with exit code `0`.")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"audit_report.md successfully created at {report_path} ({len(lines)} lines)")

if __name__ == "__main__":
    generate_report()
