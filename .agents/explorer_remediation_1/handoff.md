# Forensic Audit Remediation Plan: Course 0 Exercises vs Decoupled Solutions

**Author**: Explorer 1 (`explorer_remediation_1`)  
**Timestamp**: 2026-09-21T09:58:30Z  
**Target Repository**: `/home/settings/Documents/pearl`  
**Target Files**:
- `/home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py`
- `/home/settings/Documents/pearl/course_0_prerequisites/solutions/solutions_c0_modules.py`
- `/home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py`

---

## 1. Observation

### 1.1 Forensic Auditor Finding & Integrity Violation
The forensic auditor report at `/home/settings/Documents/pearl/.agents/auditor_gate_1/handoff.md` flagged an **INTEGRITY VIOLATION** under Requirement 2:
> *"Check that student exercises in exercises/ have TODO markers, and decoupled solutions in solutions/ contain complete, working implementations without remaining TODOs."*

Specifically:
- In `course_0_prerequisites/exercises/exercises_c0_modules.py`:
  - `grep -rn -i "TODO" course_0_prerequisites/exercises/` returned **0 matches** (exit code 1).
  - All 5 student exercises contain pre-implemented solutions directly copied from `solutions/solutions_c0_modules.py`:
    1. `student_safe_add(a: float, b: float) -> float` (lines 12–14)
    2. `StudentAgentMessage` with `__repr__` and `__str__` (lines 18–28)
    3. `student_strip_fences(text: str) -> str` (lines 32–42)
    4. `student_cosine_similarity(u: List[float], v: List[float]) -> float` (lines 46–54)
    5. `student_softmax(logits: List[float], temp: float = 1.0) -> List[float]` (lines 57–64)
  - The file ended with `test_student_exercises()` executed under `if __name__ == "__main__":`, making the file self-testing and self-passing instead of an uncompleted student workbook.

### 1.2 Benchmark Implementation in NEAT and Engineering Mathematics
1. **NEAT Course Standard** (`neat/exercises/module_01_exercises.py` through `module_06_exercises.py`):
   - Every unsolved exercise contains explicit `# TODO: Implement ...` instructional comments.
   - Function bodies raise `raise NotImplementedError("Implement ...")`.
   - The file ends with:
     ```python
     if __name__ == "__main__":
         print("Run solutions/module_01_solutions.py to test reference solutions.")
     ```
   - Decoupled reference solutions in `neat/solutions/module_01_solutions.py` contain fully solved code with 0 TODO markers and an automated test harness (`test_solutions()`).
2. **Engineering Mathematics Standard** (`engineering-mathematics/*/exercises.m`):
   - Contains 175+ explicit `% TODO: ...` markers with assignment stubs (e.g. `v_row = []; % REPLACE WITH YOUR CODE`).
   - Decoupled `solutions/` contains complete working `.m` scripts.
3. **Deep Learning E2E Test Precedent** (`tests/e2e/test_deep_learning_e2e.py` lines 253–260):
   - Explicitly asserts that reference solution file exists and contains zero `# TODO` markers.

### 1.3 Decoupled Reference Solutions Status
File: `/home/settings/Documents/pearl/course_0_prerequisites/solutions/solutions_c0_modules.py`
- Total lines: 93.
- Grep for `TODO`: **0 matches**.
- Execution: `python3 course_0_prerequisites/solutions/solutions_c0_modules.py` exits with code 0 and prints:
  ```
  === Course 0 Reference Solutions Test Runner ===
  [OK] Solution 1 (safe_add) passed.
  [OK] Solution 2 (AgentMessage dunders) passed.
  [OK] Solution 3 (strip_fences) passed.
  [OK] Solution 4 (cosine_similarity) passed.
  [OK] Solution 5 (softmax) passed.

  All reference solutions verified with 100% pass rate!
  ```
- **Status**: 100% compliant, fully working reference solution. Requires NO logic changes.

### 1.4 Test Suite Status
- `pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v` passed all 107 tests in 16.82s.
- However, `tests/e2e/test_course_0_e2e.py` lines 115–123 currently only tests:
  ```python
  assert (COURSE_0_DIR / "exercises").is_dir()
  assert (COURSE_0_DIR / "solutions").is_dir()
  ```
  It does not verify the content of `exercises_c0_modules.py` (TODO presence, NotImplementedError stubs) or `solutions_c0_modules.py` (0 TODOs, execution pass).

---

## 2. Logic Chain

1. The curriculum specification (ORIGINAL_REQUEST §R1 and auditor Requirement 2) mandates:
   *"Check that student exercises in exercises/ have TODO markers, and decoupled solutions in solutions/ contain complete, working implementations without remaining TODOs."*
2. Observation 1.1 proves that `exercises_c0_modules.py` contains 0 TODO markers and has pre-solved functions.
3. This was done by the original author to make `exercises_c0_modules.py` self-passing, but it destroys the student workbook utility and violates the pedagogical decoupling rule.
4. Observation 1.2 shows that `neat/exercises/` provides the canonical precedent: `# TODO: ...` comments, `raise NotImplementedError(...)` stubs, and informative non-crashing main execution.
5. Observation 1.3 proves that `solutions_c0_modules.py` already satisfies the reference solution requirements with zero TODOs and full test pass rate.
6. Observation 1.4 reveals that adding an explicit contract test in `tests/e2e/test_course_0_e2e.py` will continuously enforce this requirement, ensuring the forensic auditor and all future audits pass cleanly.

---

## 3. Caveats

1. `course_0_prerequisites/exercises/exercises_c0_comprehensive.md` already has 356 lines of detailed 4-tier conceptual questions, debugging puzzles, and coding specifications across all 15 modules. The remediation is strictly confined to `exercises_c0_modules.py` and the E2E test assertion.
2. In `exercises_c0_modules.py`, the test runner function at the bottom must NOT be named `test_*` (use `validate_student_exercises()`), otherwise pytest would attempt to collect and execute it as a standalone unit test during directory scans, failing on `NotImplementedError`.
3. No source code modifications were performed during this exploration phase (strictly read-only).

---

## 4. Conclusion & Actionable Remediation Plan

The remediation requires two targeted changes by the Worker:
1. **Remediate `course_0_prerequisites/exercises/exercises_c0_modules.py`**: Convert implementations into authentic student exercise stubs with 6 explicit `# TODO:` markers and `raise NotImplementedError` exceptions.
2. **Enhance `tests/e2e/test_course_0_e2e.py`**: Add `test_course_0_exercises_and_solutions_contracts` to verify that exercises have $\ge 5$ TODOs and raise `NotImplementedError`, and solutions have 0 TODOs and execute cleanly.

### Exact Implementation Specification for Worker

#### File 1: `/home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py`
Replace the entire contents of `exercises_c0_modules.py` with:

```python
"""exercises_c0_modules.py - Practical Coding Exercises for Course 0 Modules.

Student workbook containing 4-tier progressive coding problem templates.
Implement each function marked with # TODO, then run this file or reference solutions
in course_0_prerequisites/solutions/solutions_c0_modules.py.
"""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers."""
    # TODO: Implement safe addition of two floating point numbers (float(a + b))
    raise NotImplementedError("Exercise 1.1 not implemented: student_safe_add")


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__."""

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        # TODO: Implement __repr__ returning e.g. StudentAgentMessage(role='user', content='Hello')
        raise NotImplementedError("Exercise 2.1 not implemented: StudentAgentMessage.__repr__")

    def __str__(self) -> str:
        # TODO: Implement __str__ returning e.g. [USER]: Hello
        raise NotImplementedError("Exercise 2.1 not implemented: StudentAgentMessage.__str__")


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks."""
    # TODO: Extract JSON substring enclosed in ```json ... ``` code fences, or between outer { and }
    raise NotImplementedError("Exercise 7.1 not implemented: student_strip_fences")


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors."""
    # TODO: Calculate dot product divided by product of Euclidean norms. Return 0.0 if either norm is 0.0.
    raise NotImplementedError("Exercise 15.1 not implemented: student_cosine_similarity")


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature."""
    # TODO: Scale logits by temp (clamped >= 1e-4), subtract max for stability, exponentiate, and normalize.
    raise NotImplementedError("Exercise 15.2 not implemented: student_softmax")


def validate_student_exercises() -> None:
    """Self-check test suite that students can run after implementing exercises."""
    # 1. Test math
    assert student_safe_add(15.0, 27.0) == 42.0

    # 2. Test dunders
    msg = StudentAgentMessage("user", "Hello agent!")
    assert str(msg) == "[USER]: Hello agent!"
    assert "StudentAgentMessage(role='user'" in repr(msg)

    # 3. Test fence stripper
    fenced = "Here is the json:\n```json\n{\"test\": true}\n```\nDone."
    assert student_strip_fences(fenced) == '{"test": true}'

    # 4. Test cosine similarity
    assert math.isclose(student_cosine_similarity([1, 0], [1, 0]), 1.0)
    assert math.isclose(student_cosine_similarity([1, 0], [0, 1]), 0.0)

    # 5. Test softmax
    probs = student_softmax([5.0, 1.0], temp=0.1)
    assert probs[0] > 0.99
    assert math.isclose(sum(probs), 1.0)

    print("All student exercise implementations validated successfully!")


if __name__ == "__main__":
    print("=== Course 0 Student Exercise Workbook ===")
    try:
        validate_student_exercises()
    except NotImplementedError as err:
        print(f"[PENDING] {err}")
        print("Implement the # TODO stubs above, then re-run to validate.")
        print("Reference solutions available at:")
        print("  python3 course_0_prerequisites/solutions/solutions_c0_modules.py")
```

#### File 2: `/home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py`
In `tests/e2e/test_course_0_e2e.py`:
1. Add `import importlib.util` to the imports at top (around line 11).
2. Inside `TestTier1Course0Structure` (after line 123), add the contract test:

```python
    def test_course_0_exercises_and_solutions_contracts(self):
        """
        Verify that Course 0 student exercises contain TODO markers and stubs,
        while decoupled solutions contain complete implementations with zero TODOs
        and pass all reference verification checks.
        """
        exercises_file = COURSE_0_DIR / "exercises" / "exercises_c0_modules.py"
        solutions_file = COURSE_0_DIR / "solutions" / "solutions_c0_modules.py"

        assert exercises_file.exists(), f"exercises_c0_modules.py missing at {exercises_file}"
        assert solutions_file.exists(), f"solutions_c0_modules.py missing at {solutions_file}"

        # 1. Verify student exercises contain TODO markers (minimum 5)
        ex_content = exercises_file.read_text(encoding="utf-8")
        ex_todos = re.findall(r"\bTODO\b", ex_content, re.IGNORECASE)
        assert len(ex_todos) >= 5, (
            f"Expected at least 5 TODO markers in {exercises_file.name}, found {len(ex_todos)}"
        )

        # 2. Verify exercise stubs raise NotImplementedError when uncompleted
        spec = importlib.util.spec_from_file_location("exercises_c0_modules", exercises_file)
        ex_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex_mod)

        with pytest.raises(NotImplementedError):
            ex_mod.student_safe_add(1.0, 2.0)
        with pytest.raises(NotImplementedError):
            repr(ex_mod.StudentAgentMessage("user", "test"))
        with pytest.raises(NotImplementedError):
            str(ex_mod.StudentAgentMessage("user", "test"))
        with pytest.raises(NotImplementedError):
            ex_mod.student_strip_fences("```json {} ```")
        with pytest.raises(NotImplementedError):
            ex_mod.student_cosine_similarity([1.0, 0.0], [0.0, 1.0])
        with pytest.raises(NotImplementedError):
            ex_mod.student_softmax([1.0, 2.0])

        # 3. Verify reference solutions contain zero TODO markers
        sol_content = solutions_file.read_text(encoding="utf-8")
        sol_todos = re.findall(r"\bTODO\b", sol_content, re.IGNORECASE)
        assert len(sol_todos) == 0, (
            f"Expected 0 TODO markers in {solutions_file.name}, found {len(sol_todos)}"
        )

        # 4. Verify reference solutions execute cleanly and pass all checks
        res = subprocess.run(
            [sys.executable, str(solutions_file)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, (
            f"solutions_c0_modules.py failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}"
        )
        assert "All reference solutions verified with 100% pass rate" in res.stdout
```

---

## 5. Verification Method

Once the Worker applies the above changes, verify with the following commands:

1. **Verify TODO markers in exercises**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/exercises/
   ```
   *Expected*: Exactly 6 matches corresponding to the 5 exercises (2 in Exercise 2).

2. **Verify zero TODO markers in solutions**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/solutions/
   ```
   *Expected*: 0 matches (exit code 1).

3. **Verify exercises file executes without unhandled exceptions**:
   ```bash
   python3 course_0_prerequisites/exercises/exercises_c0_modules.py
   ```
   *Expected*: Exit code 0, prints pending implementation notice and pointer to reference solutions.

4. **Verify solutions file passes reference tests**:
   ```bash
   python3 course_0_prerequisites/solutions/solutions_c0_modules.py
   ```
   *Expected*: Exit code 0, all 5 reference solutions pass with 100% pass rate.

5. **Execute complete E2E Test Suite**:
   ```bash
   pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v
   ```
   *Expected*: **108 passed in ~17s** (71 in Course 0, 13 in Math, 24 in NEAT). Zero failures.
