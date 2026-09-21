# Remediation Investigation Report: Course 0 Student Exercises Integrity

**Agent**: `explorer_remediation_2`  
**Date**: 2026-09-21T09:58:45Z  
**Target Issue**: Forensic Integrity Audit Failure (Strict Binary Veto on `course_0_prerequisites/exercises/exercises_c0_modules.py`)  
**Auditor Report**: `/home/settings/Documents/pearl/.agents/auditor_gate_1/handoff.md`  
**Proposed Artifacts Created**:
- Replacement File: `/home/settings/Documents/pearl/.agents/explorer_remediation_2/proposed_exercises_c0_modules.py`
- Diff Patch File: `/home/settings/Documents/pearl/.agents/explorer_remediation_2/exercises_remediation.patch`

---

## Executive Summary

The Forensic Auditor (`auditor_gate_1`) placed a strict binary veto on the curriculum expansion work product due to Requirement 2:
> *"Check that student exercises in `exercises/` have TODO markers, and decoupled solutions in `solutions/` contain complete, working implementations without remaining TODOs."*

Investigation confirmed that while `neat/exercises/` (16 TODOs, `NotImplementedError` stubs) and `engineering-mathematics/*/exercises.m` (175+ TODOs) properly decouple student workbooks from solutions, `course_0_prerequisites/exercises/exercises_c0_modules.py` was authored with **0 TODO markers** and contained pre-implemented solutions directly copied from `solutions/solutions_c0_modules.py`.

This investigation has formulated an exact, verified remediation strategy for the implementation Worker:
1. Update `course_0_prerequisites/exercises/exercises_c0_modules.py` with 12 explicit `# TODO:` markers and `raise NotImplementedError(...)` stubs.
2. Maintain `course_0_prerequisites/solutions/solutions_c0_modules.py` as the 100% complete reference solution (already verified clean with 0 TODOs).
3. Extend `tests/e2e/test_course_0_e2e.py` with dedicated E2E tests asserting exercise workbook TODO markers/stubs and reference solution execution.
4. Guarantee that all 107 (expanding to 109) E2E tests continue to pass 100%.

---

## 1. Observation

### 1.1 State of `course_0_prerequisites/exercises/exercises_c0_modules.py`
- Path: `/home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py`
- Total Lines: 94 lines
- `grep -rn -i "TODO" course_0_prerequisites/exercises/` returned **0 matches** (exit code 1).
- Direct file inspection shows lines 11–65 contain fully solved code rather than student exercise stubs:
  ```python
  11: # Exercise 1: Safe AST Calculator (Module 01 & 09)
  12: def student_safe_add(a: float, b: float) -> float:
  13:     """Exercise 1.1: Return the sum of two numbers."""
  14:     return a + b
  15: 
  16: 
  17: # Exercise 2: Dunder representation (Module 02)
  18: class StudentAgentMessage:
  19:     """Exercise 2.1: Implement __repr__ and __str__."""
  20:     def __init__(self, role: str, content: str) -> None:
  21:         self.role = role
  22:         self.content = content
  23: 
  24:     def __repr__(self) -> str:
  25:         return f"StudentAgentMessage(role={self.role!r}, content={self.content!r})"
  26: 
  27:     def __str__(self) -> str:
  28:         return f"[{self.role.upper()}]: {self.content}"
  29: 
  30: 
  31: # Exercise 3: Code fence stripper (Module 07)
  32: def student_strip_fences(text: str) -> str:
  33:     """Exercise 7.1: Extract JSON from markdown backticks."""
  34:     text = text.strip()
  35:     match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
  36:     if match:
  37:         return match.group(1).strip()
  38:     start = text.find("{")
  39:     end = text.rfind("}")
  40:     if start != -1 and end != -1 and end > start:
  41:         return text[start : end + 1].strip()
  42:     return text
  43: 
  44: 
  45: # Exercise 4: Cosine similarity (Module 15)
  46: def student_cosine_similarity(u: List[float], v: List[float]) -> float:
  47:     """Exercise 15.1: Calculate cosine similarity between two vectors."""
  48:     dot = sum(a * b for a, b in zip(u, v))
  49:     norm_u = math.sqrt(sum(a * a for a in u))
  50:     norm_v = math.sqrt(sum(b * b for b in v))
  51:     if norm_u == 0.0 or norm_v == 0.0:
  52:         return 0.0
  53:     return dot / (norm_u * norm_v)
  54: 
  55: 
  56: # Exercise 5: Softmax with temperature (Module 15)
  57: def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
  58:     """Exercise 15.2: Calculate numerically stable softmax with temperature."""
  59:     t = max(1e-4, temp)
  60:     scaled = [z / t for z in logits]
  61:     max_z = max(scaled)
  62:     exp_vals = [math.exp(z - max_z) for z in scaled]
  63:     sum_exp = sum(exp_vals)
  64:     return [ev / sum_exp for ev in exp_vals]
  ```

### 1.2 State of `course_0_prerequisites/solutions/solutions_c0_modules.py`
- Path: `/home/settings/Documents/pearl/course_0_prerequisites/solutions/solutions_c0_modules.py`
- Total Lines: 93 lines
- `grep -rn -i "TODO" course_0_prerequisites/solutions/` returned **0 matches**.
- Standalone execution command: `python3 course_0_prerequisites/solutions/solutions_c0_modules.py`
- Output verbatim:
  ```
  === Course 0 Reference Solutions Test Runner ===
  [OK] Solution 1 (safe_add) passed.
  [OK] Solution 2 (AgentMessage dunders) passed.
  [OK] Solution 3 (strip_fences) passed.
  [OK] Solution 4 (cosine_similarity) passed.
  [OK] Solution 5 (softmax) passed.

  All reference solutions verified with 100% pass rate!
  ```
  Exit code: 0.

### 1.3 State of Comparison Curriculum (`neat/exercises/` and `engineering-mathematics/`)
- In `neat/exercises/module_01_exercises.py` through `module_06_exercises.py`:
  - 16 `# TODO:` markers across 6 modules.
  - Stubs use explicit `# TODO: Implement ...` and `raise NotImplementedError("Implement ...")`.
  - The `__main__` entrypoint prints: `Run solutions/module_XX_solutions.py to test reference solutions.`
- In `engineering-mathematics/*/exercises.m`:
  - 175+ `% TODO:` markers across 5 core modules.
  - Stubs use empty variable assignments (`norm_L1 = []; % TODO: Replace with norm(..., 1)`).

### 1.4 Test Suite Baseline
- Command: `pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v`
- Execution Result: **107 passed in 15.05s** (70 Course 0, 13 Math, 24 NEAT).
- In `tests/e2e/test_course_0_e2e.py`, lines 115–123 check directory existence:
  ```python
  assert (COURSE_0_DIR / "exercises").is_dir()
  assert (COURSE_0_DIR / "solutions").is_dir()
  ```
  However, it currently lacks explicit assertions on TODO markers in exercises or automated execution of `solutions_c0_modules.py`.

---

## 2. Logic Chain

1. **Requirement Definition**: Requirement 2 mandates that student exercises in `exercises/` have TODO markers, and decoupled solutions in `solutions/` contain complete, working implementations without remaining TODOs.
2. **Failure Identification**: `course_0_prerequisites/exercises/exercises_c0_modules.py` contained pre-implemented function bodies and zero TODO markers. This caused the forensic auditor to invoke the strict binary veto.
3. **Decoupling Rationale**:
   - The student workbook (`exercises_c0_modules.py`) must provide problem signatures, docstrings explaining the task, `# TODO:` comments, and `raise NotImplementedError(...)` stubs.
   - The reference solution file (`solutions_c0_modules.py`) already contains 100% complete implementations, zero TODO markers, and passes all assertions.
4. **Execution Safety**:
   - When a student or test runner executes `exercises_c0_modules.py`, it should either report unimplemented stubs cleanly or raise `NotImplementedError` when methods are invoked.
   - Wrapping the `test_student_exercises()` call in `if __name__ == "__main__":` with a `try ... except NotImplementedError` ensures that invoking `python3 exercises_c0_modules.py` prints clear instructions directing the student to the reference solutions without crashing.
5. **E2E Suite Strengthening**:
   - Adding tests in `tests/e2e/test_course_0_e2e.py` that enforce:
     (a) `exercises_c0_modules.py` has $\ge 5$ TODO markers and raises `NotImplementedError` on stubs, and
     (b) `solutions_c0_modules.py` has zero TODO markers and executes to completion with 100% pass rate.
   - This directly covers Feature 17 in `TEST_READY.md` (`C0-Exercises & Solutions`) and permanently prevents regression.

---

## 3. Caveats

- **No other files in Course 0 are affected**: `course_0_prerequisites/exercises/exercises_c0_comprehensive.md` (356 lines) and `course_0_prerequisites/solutions/solutions_c0_comprehensive.md` (260 lines) already contain complete 4-tier conceptual exercises and worked solutions.
- **NEAT and Math modules require zero changes**: Forensic audit confirmed 100% compliance across NEAT and Engineering Mathematics.
- **Read-only role respected**: As Explorer, this agent did not modify any repository source files. Complete proposed replacement files and diff patches have been staged in `.agents/explorer_remediation_2/` for the implementation Worker.

---

## 4. Conclusion & Concrete Remediation Plan

### 4.1 Actionable Remediation Steps for Worker

The Worker must execute two concrete edits:

#### Step 1: Replace `course_0_prerequisites/exercises/exercises_c0_modules.py`
Apply the proposed content from `.agents/explorer_remediation_2/proposed_exercises_c0_modules.py` (or patch via `.agents/explorer_remediation_2/exercises_remediation.patch`).

**Target File**: `/home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py`  
**Exact Proposed Content**:
```python
"""exercises_c0_modules.py - Practical Coding Exercises for Course 0 Modules.

Student exercise workbook containing problem stubs with TODO markers.
Reference solutions are located in ../solutions/solutions_c0_modules.py.
"""

from typing import List, Dict, Any, Optional
import math
import re


# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers.

    TODO: Implement safe numeric addition returning a float.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 1.1 (student_safe_add) not yet implemented by student.")


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__ for Agent Message."""

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        # TODO: Implement unambiguous developer representation: StudentAgentMessage(role='...', content='...')
        raise NotImplementedError("Exercise 2.1 (__repr__) not yet implemented by student.")

    def __str__(self) -> str:
        # TODO: Implement clean user-facing prompt representation: [ROLE]: content
        raise NotImplementedError("Exercise 2.1 (__str__) not yet implemented by student.")


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks.

    TODO: Extract JSON substring from markdown backticks (```json ... ``` or ``` ... ```)
    or find the outer matching braces { ... }. Return original string if no fence/braces found.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 7.1 (student_strip_fences) not yet implemented by student.")


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors.

    TODO: Compute the dot product and Euclidean L2 norms of vectors u and v.
    Return dot / (norm_u * norm_v), or 0.0 if either vector has norm 0.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 15.1 (student_cosine_similarity) not yet implemented by student.")


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature.

    TODO: Scale logits by max(1e-4, temp), subtract maximum logit for stability,
    compute exp(z_scaled), and normalize by the sum of exponentials.
    """
    # TODO: Replace with student implementation
    raise NotImplementedError("Exercise 15.2 (student_softmax) not yet implemented by student.")


def test_student_exercises() -> None:
    """Unit test suite for student to verify their implementations once completed."""
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

    print("All exercise validation checks passed successfully!")


if __name__ == "__main__":
    try:
        test_student_exercises()
    except NotImplementedError as exc:
        print(f"[EXERCISE WORKBOOK] Unimplemented exercise stub encountered: {exc}")
        print("Please implement all # TODO stubs above, or run reference solutions:")
        print("  python3 course_0_prerequisites/solutions/solutions_c0_modules.py")
```

#### Step 2: Add Exercise & Solution Integrity Tests to `tests/e2e/test_course_0_e2e.py`
In `/home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py`, inside class `TestTier1Course0Structure` (after line 123), add two test methods:

```python
    def test_course_0_exercises_workbook_integrity(self):
        """Verify exercises_c0_modules.py contains explicit TODO markers and NotImplementedError stubs."""
        ex_file = COURSE_0_DIR / "exercises" / "exercises_c0_modules.py"
        assert ex_file.exists() and ex_file.is_file(), "exercises_c0_modules.py missing"
        content = ex_file.read_text(encoding="utf-8")

        # Verify explicit TODO markers exist (>= 5)
        todo_matches = re.findall(r"TODO", content)
        assert len(todo_matches) >= 5, (
            f"Expected at least 5 TODO markers in exercises_c0_modules.py, found {len(todo_matches)}"
        )

        # Verify NotImplementedError stubs exist
        assert "NotImplementedError" in content, (
            "exercises_c0_modules.py must contain NotImplementedError stubs"
        )

        # Programmatically verify student functions raise NotImplementedError
        import importlib.util
        spec = importlib.util.spec_from_file_location("exercises_c0_modules", ex_file)
        ex_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ex_mod)

        with pytest.raises(NotImplementedError):
            ex_mod.student_safe_add(1.0, 2.0)

        with pytest.raises(NotImplementedError):
            ex_mod.student_strip_fences("test")

    def test_course_0_solutions_execution_and_zero_todos(self):
        """Verify solutions_c0_modules.py contains zero unresolved TODOs and executes with 100% pass."""
        sol_file = COURSE_0_DIR / "solutions" / "solutions_c0_modules.py"
        assert sol_file.exists() and sol_file.is_file(), "solutions_c0_modules.py missing"
        content = sol_file.read_text(encoding="utf-8")

        # Verify zero unresolved TODO markers
        assert "# TODO" not in content and "# TODO:" not in content, (
            "solutions_c0_modules.py must contain zero TODO markers"
        )

        # Execute reference solution runner and verify output
        res = subprocess.run(
            [sys.executable, str(sol_file)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )
        assert res.returncode == 0, f"solutions_c0_modules.py failed: {res.stderr}"
        assert "verified with 100% pass rate" in res.stdout, (
            f"solutions_c0_modules.py did not report 100% pass: {res.stdout}"
        )
```

---

## 5. Verification Method

To independently verify this remediation before requesting final re-audit:

1. **Verify TODO markers in exercises workbook**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/exercises/
   ```
   *Expected Result*: $\ge 5$ matches (12 matches found in proposed file).

2. **Verify 0 TODO markers in reference solutions**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/solutions/
   ```
   *Expected Result*: 0 matches.

3. **Verify Reference Solution execution**:
   ```bash
   python3 course_0_prerequisites/solutions/solutions_c0_modules.py
   ```
   *Expected Result*: Exit code 0, prints `All reference solutions verified with 100% pass rate!`.

4. **Verify Student Workbook execution**:
   ```bash
   python3 course_0_prerequisites/exercises/exercises_c0_modules.py
   ```
   *Expected Result*: Exit code 0, prints `[EXERCISE WORKBOOK] Unimplemented exercise stub encountered: Exercise 1.1...`.

5. **Run the Full Unified E2E Test Suite**:
   ```bash
   pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v
   ```
   *Expected Result*: **109 passed in < 20s**, exit code 0.

### Invalidation Conditions
- Any failure in `pytest tests/e2e/test_course_0_e2e.py`.
- Any remaining `# TODO` markers in `course_0_prerequisites/solutions/`.
- Failure of `exercises_c0_modules.py` to raise `NotImplementedError` when stubs are called.
