# Course -1 Python Foundations: Test Infrastructure & Verification Architecture

## 1. Overview & Pedagogical Purpose

The Course -1 Python Foundations test infrastructure provides an automated, rigorous, and adversarial acceptance verification framework for all 33 modules in `course_-1_python_foundations/`.

Course -1 transitions learners from complete beginners into engineers capable of building autonomous AI agents. The test harness guarantees that every module delivers authentic instructional depth, complete code examples, structured progressive exercises, and clean reference implementations without shortcuts, stubs, or facades.

---

## 2. Test Architecture Components

The testing infrastructure consists of two interoperable layers:

```
                                  +------------------------------------------+
                                  |         Course -1 Acceptance Harness      |
                                  +------------------------------------------+
                                                       |
                        +------------------------------+------------------------------+
                        |                                                             |
                        v                                                             v
       +----------------------------------+                         +----------------------------------+
       |   scripts/verify_course_minus_1.py|                         | tests/e2e/test_course_minus_1... |
       +----------------------------------+                         +----------------------------------+
       | - Fast standalone CLI auditor    |                         | - Standard Pytest test suite     |
       | - Modular filters (-m, -c)       |                         | - Parametrized per-module tests  |
       | - JSON metrics report generator  |                         | - 8 Adversarial integrity checks |
       | - Colorized ASCII summary table  |                         | - CI/CD and gate review ready    |
       +----------------------------------+                         +----------------------------------+
                        \                                                             /
                         +-----------------------------+-----------------------------+
                                                       |
                                                       v
                                  +------------------------------------------+
                                  | 33 Modules: course_-1_python_foundations |
                                  |   - README.md (18 canonical sections)    |
                                  |   - Primary lesson .py (>= 150 lines)    |
                                  |   - exercises.py (4 distinct levels)     |
                                  |   - solutions.py (exit code 0, no NIE)   |
                                  +------------------------------------------+
```

### 2.1. Standalone Verification Script (`scripts/verify_course_minus_1.py`)
- **Role**: Lightweight, zero-dependency auditor for fast feedback during authoring and milestone reviews.
- **Capabilities**:
  - Validates individual modules or any arbitrary subset via `--module` / `-m`.
  - Runs specific checks (1 to 4) via `--check` / `-c`.
  - Emits human-readable diagnostic tables (`--verbose`) and machine-parsable JSON reports (`--json <path>`).
  - Strict exit codes: `0` when 100% of tested modules pass; `1` when any test fails.

### 2.2. Pytest Acceptance Suite (`tests/e2e/test_course_minus_1_acceptance.py`)
- **Role**: Formal end-to-end acceptance suite executing in pytest runners and CI/CD pipelines.
- **Organization**:
  - `TestR1PedagogicalReadme`: 33 parametrized tests verifying 18 headers in order with non-empty content.
  - `TestR2DetailedLessonScript`: 33 parametrized tests verifying lesson script existence, >= 150 lines, and clean exit 0.
  - `TestR3ExercisesScaffolding`: 33 parametrized tests verifying 4 exercise tiers and authentic scaffolding.
  - `TestR3SolutionsExecution`: 33 parametrized tests verifying reference solutions execute cleanly without `NotImplementedError`.
  - `TestR4ModuleAcceptance`: 33 parametrized tests evaluating full multi-check gate passage per module.
  - `TestAdversarialHarnessIntegrity`: 8 adversarial tests proving the test harness correctly rejects malformed or facade inputs.

---

## 3. Strict Verification Criteria (R1 – R4)

### Requirement R1: Pedagogical README Specification
Every module `README.md` must strictly contain the following **18 exact headers in sequential line order**, with non-empty substantive content in every section:
1. `# Topic` (e.g., `# Topic: What Programming Is`)
2. `## What You Will Learn`
3. `## Prerequisites`
4. `## The Problem`
5. `## Key Terminology`
6. `## Intuition`
7. `## Concept`
8. `## Syntax`
9. `## Example`
10. `## Line-by-Line Explanation`
11. `## What Python Is Doing`
12. `## Common Mistakes`
13. `## Real-World Uses`
14. `## Connection to AI Agents`
15. `## Practice`
16. `## Challenge`
17. `## Summary`
18. `## What You Should Know Before Moving On`

**Validation Rules**:
- Missing any header $\rightarrow$ **FAIL**.
- Headers out of sequential order $\rightarrow$ **FAIL**.
- Any section containing only empty lines or whitespace $\rightarrow$ **FAIL**.

### Requirement R2: Detailed Python Lesson Script
Each module must contain a primary `.py` lesson script:
- Must resolve either via the canonical filename map (e.g., `what_programming_is.py`, `hello.py`, `flow.py`, `functions.py`) or by scanning the directory for the largest non-scaffolding `.py` file.
- Must be **at least 150 lines long** (`min_lines=150`).
- Must execute cleanly (`exit code 0`) under `python3` within a 25-second timeout window.
- Must execute in an isolated subprocess with `PYTHONPATH` configured to resolve both repo root and local module files.

### Requirement R3: Authentic 4-Tier Exercises
Each module must contain `exercises.py`:
- Must include **4 distinct levels**:
  1. `Recall` (e.g., `Level 1: Recall` or `Tier 1: Recall`)
  2. `Modify` (e.g., `Level 2: Modify` or `Tier 2: Modify`)
  3. `Build` (e.g., `Level 3: Build` or `Tier 3: Build`)
  4. `Debug` (e.g., `Level 4: Debug` or `Tier 4: Debug`)
- Must contain authentic scaffolding: `# TODO` comments or `raise NotImplementedError` statements.

### Requirement R3: Decoupled Working Solutions
Each module must contain `solutions.py`:
- Must be decoupled from `exercises.py`.
- Must be at least 10 lines long (not an empty stub).
- Must contain **no unresolved `NotImplementedError`** statements.
- Must execute cleanly (`exit code 0`) when run directly with `python3` within 25 seconds.

### Requirement R4: 100% Curriculum Completeness
All 33 modules in `course_-1_python_foundations/` must simultaneously pass all checks (Checks 1–4).

---

## 4. Adversarial Verification & Anti-Facade Guarantees

To ensure that tests cannot pass trivially or via superficial stubs, `TestAdversarialHarnessIntegrity` exercises synthetic edge-case directories and asserts that the harness actively rejects:
1. **Missing Headers**: Verifies failure when a required header (e.g., `Syntax`) is omitted.
2. **Out-of-Order Headers**: Verifies failure when headers are transposed (e.g., `Syntax` before `Concept`).
3. **Empty Sections**: Verifies failure when a header is followed immediately by the next header without text.
4. **Short Lesson Files**: Verifies failure when a lesson script has fewer than 150 lines.
5. **Runtime Crashes**: Verifies failure when a lesson script raises an unhandled exception or non-zero exit code.
6. **Missing Exercise Levels**: Verifies failure when any tier (Recall, Modify, Build, Debug) is absent.
7. **Missing Scaffolding**: Verifies failure when exercises have no `# TODO` or `NotImplementedError`.
8. **Incomplete Solutions**: Verifies failure when a solution file leaves `NotImplementedError` in place.

---

## 5. Execution Commands & Recipes

### 5.1. Standalone Verification Script Commands

```bash
# Run full verification across all 33 modules with ASCII summary table
python3 scripts/verify_course_minus_1.py

# Run with verbose diagnostic logs showing exact missing headers or exit codes
python3 scripts/verify_course_minus_1.py --verbose

# Verify a single module (e.g. Module 01)
python3 scripts/verify_course_minus_1.py --module 01 --verbose

# Verify a batch of modules (e.g. M1 modules 01 through 06)
python3 scripts/verify_course_minus_1.py --module 01,02,03,04,05,06 --verbose

# Run only specific checks (e.g. Check 1 README and Check 2 Lesson)
python3 scripts/verify_course_minus_1.py --check 1,2

# Export full machine-readable verification report to JSON
python3 scripts/verify_course_minus_1.py --json baseline_report.json
```

### 5.2. Pytest Commands

```bash
# Run the complete Course -1 acceptance suite
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -v

# Run verification for a single module
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "01_what_programming_is" -v

# Run only README structure tests (Check 1) across all modules
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "TestR1" -v

# Run only lesson script tests (Check 2)
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "TestR2" -v

# Run only exercise scaffolding tests (Check 3)
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "TestR3Exercises" -v

# Run only solution execution tests (Check 4)
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "TestR3Solutions" -v

# Run the 8 adversarial harness self-verification tests
python3 -m pytest tests/e2e/test_course_minus_1_acceptance.py -k "TestAdversarial" -v
```

---

## 6. Baseline Status Across Curriculum (2026-09-21)

| Check | Requirement | Passing / Total | Pass Rate | Status |
|---|---|---|---|---|
| **Check 1** | README 18 Headers (In Order & Non-Empty) | 10 / 33 | 30.3% | 10 Rewritten Modules Pass |
| **Check 2** | Lesson Script >= 150L & Clean Execution | 10 / 33 | 30.3% | 10 Modules Pass |
| **Check 3** | Exercises 4 Tiers & Scaffolding | 19 / 33 | 57.6% | 19 Modules Pass |
| **Check 4** | Solutions Clean Execution (No NIE) | 19 / 33 | 57.6% | 19 Modules Pass |
| **Overall** | Fully Passing Modules (All 4 Checks) | **9 / 33** | **27.3%** | Baseline Established |

### 6.1. Fully Passing Modules (9 Modules)
1. `01_what_programming_is` (M1)
2. `02_first_python_programs` (M1)
3. `07_control_flow` (M2)
4. `08_functions` (M2)
5. `17_generators` (M4)
6. `23_virtual_environments` (M5)
7. `24_async_python_intro` (M5)
8. `30_basic_software_architecture` (M6)
9. `31_python_project_structure` (M6)

### 6.2. Partially Passing Modules
- `09_scope`: Checks 2, 3, 4 PASS (313L lesson, 4-tier exercises, clean solutions). Check 1 FAIL (needs 18-header README rewrite).
- `25_async_concurrency`: Check 1 PASS (18-header README). Checks 2, 3, 4 FAIL (needs full lesson rewrite >=150L, 4-tier exercises, solutions).
- `11_files`, `12_modules`, `13_classes_and_oop`, `15_type_hints`, `16_dataclasses`, `18_iterators`, `19_decorators`, `20_context_managers`, `21_testing`: Checks 3 and 4 PASS. Need README and lesson rewrites.

### 6.3. Modules Requiring Full Authoring (14 Modules)
- `03_variables_and_data_types`
- `04_operators`
- `05_strings`
- `06_collections`
- `10_errors_and_exceptions`
- `14_functional_programming`
- `22_logging`
- `26_http_and_json_intro`
- `27_environment_variables`
- `28_subprocesses_intro`
- `29_sqlite_intro`
- `32_python_debugging`
- `33_integrated_projects`
