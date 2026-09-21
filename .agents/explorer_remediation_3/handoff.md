# Investigation & Remediation Strategy Report: Course 0 Exercise Workbook Integrity

**Explorer Identity**: `explorer_remediation_3`  
**Timestamp**: 2026-09-21T10:01:00Z  
**Target Work Products**:
- `course_0_prerequisites/exercises/exercises_c0_modules.py`
- `course_0_prerequisites/solutions/solutions_c0_modules.py`
- `tests/e2e/test_course_0_e2e.py`
**Remediation Artifacts Produced**:
- Replacement File: `/home/settings/Documents/pearl/.agents/explorer_remediation_3/proposed_exercises_c0_modules.py`
- Diff Patch: `/home/settings/Documents/pearl/.agents/explorer_remediation_3/exercises_c0_modules.patch`
- Test Patch: `/home/settings/Documents/pearl/.agents/explorer_remediation_3/test_course_0_e2e.patch`

---

## 1. Observation

### 1.1 Direct Observation of the Integrity Violation
- **Target File**: `/home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py` (94 lines).
- **Search Command**: `grep -rn -i "TODO" course_0_prerequisites/exercises/`
- **Search Result**: Exit code 1, **0 matches**.
- **File Content Analysis**:
  In lines 11–65 of `exercises_c0_modules.py`:
  - `student_safe_add(a: float, b: float) -> float` (lines 12–14):
    ```python
    def student_safe_add(a: float, b: float) -> float:
        """Exercise 1.1: Return the sum of two numbers."""
        return a + b
    ```
  - `StudentAgentMessage` (lines 18–29):
    ```python
    class StudentAgentMessage:
        """Exercise 2.1: Implement __repr__ and __str__."""
        def __init__(self, role: str, content: str) -> None:
            self.role = role
            self.content = content

        def __repr__(self) -> str:
            return f"StudentAgentMessage(role={self.role!r}, content={self.content!r})"

        def __str__(self) -> str:
            return f"[{self.role.upper()}]: {self.content}"
    ```
  - `student_strip_fences(text: str) -> str` (lines 32–43): Contains complete regex and boundary slicing implementation.
  - `student_cosine_similarity(u: List[float], v: List[float]) -> float` (lines 46–54): Contains complete dot product and norm computation.
  - `student_softmax(logits: List[float], temp: float = 1.0) -> List[float]` (lines 57–65): Contains complete numerically stable softmax calculation with temperature scaling.
  - `test_student_exercises()` (lines 67–93): Asserts correctness of the above implementations and prints `"All exercise validation checks passed successfully!"`.
- **Finding**: All 5 student exercises were authored with working solutions pre-filled and zero `# TODO` markers, eliminating the workbook function and circumventing the requirement for student exercises.

### 1.2 Status of Reference Solutions
- **Target File**: `/home/settings/Documents/pearl/course_0_prerequisites/solutions/solutions_c0_modules.py` (93 lines).
- **Execution Command**: `python3 course_0_prerequisites/solutions/solutions_c0_modules.py`
- **Output & Exit Code**: Exit code 0:
  ```text
  === Course 0 Reference Solutions Test Runner ===
  [OK] Solution 1 (safe_add) passed.
  [OK] Solution 2 (AgentMessage dunders) passed.
  [OK] Solution 3 (strip_fences) passed.
  [OK] Solution 4 (cosine_similarity) passed.
  [OK] Solution 5 (softmax) passed.

  All reference solutions verified with 100% pass rate!
  ```
- **TODO Check**: `grep -rn -i "TODO" course_0_prerequisites/solutions/` returned 0 matches.
- **Finding**: The reference solution file is already 100% complete, fully working, decoupled from exercises, and contains zero remaining TODOs.

### 1.3 Architectural Reference Patterns in Other Modules
- **NEAT Exercises Pattern** (`neat/exercises/module_01_exercises.py` through `module_06_exercises.py`):
  - 16 `# TODO` markers.
  - Stubs use: `# TODO: Implement ...` followed by `raise NotImplementedError("Implement ...")`.
  - In `__main__`, prints reference guidance: `print("Run solutions/module_01_solutions.py to test reference solutions.")` rather than crashing on stubs.
- **Engineering Math Exercises Pattern** (`engineering-mathematics/*/exercises.m`):
  - 175+ `% TODO` markers with unfilled assignment stubs (`v_row = []; % REPLACE WITH YOUR CODE`).
  - Strict validation enforced in `engineering-mathematics/scripts/verify_package.py` lines 937–989 (`ExerciseTierAuditor` checks that exercises contain `TODO`/`TASK` and solutions contain zero `TODO` comments).

### 1.4 Test Suite Coverage & Verification Gap
- **Target Test File**: `tests/e2e/test_course_0_e2e.py` lines 115–123:
  ```python
  def test_course_0_root_readme_and_resources(self):
      """Verify Course 0 root README and supporting folders (exercises, solutions)."""
      root_readme = COURSE_0_DIR / "README.md"
      assert root_readme.exists() and root_readme.stat().st_size > 300, (
          "Course 0 root README.md missing or too small"
      )
      assert (COURSE_0_DIR / "exercises").is_dir(), "exercises/ directory missing"
      assert (COURSE_0_DIR / "solutions").is_dir(), "solutions/ directory missing"
  ```
- **Observation**: The E2E test only checked directory existence (`assert (COURSE_0_DIR / "exercises").is_dir()`), and did not assert that `exercises_c0_modules.py` has `# TODO` markers or that `solutions_c0_modules.py` executes cleanly without TODOs.
- **Project E2E Execution**: `pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v` executed cleanly with **107 passed in 16.98s**.

---

## 2. Logic Chain

1. **Mandate**: Requirement 2 and `ORIGINAL_REQUEST.md §R1` specify that student exercise workbooks must present exercises for completion (marked with `TODO` markers and stubs), while reference solutions in `solutions/` provide complete, working, decoupled implementations with zero remaining `TODO` markers.
2. **Breach**: As observed in §1.1, `course_0_prerequisites/exercises/exercises_c0_modules.py` has 0 `TODO` markers and has the complete solutions pre-implemented.
3. **Auditor Verdict**: Under the strict binary veto rule, `auditor_gate_1` properly issued an **INTEGRITY VIOLATION** verdict because pre-solving exercises is an implementation shortcut that degrades the pedagogical integrity of the courseware.
4. **Remediation Needs**:
   - In `exercises_c0_modules.py`: Replace the pre-implemented bodies of `student_safe_add`, `StudentAgentMessage.__repr__`, `StudentAgentMessage.__str__`, `student_strip_fences`, `student_cosine_similarity`, and `student_softmax` with explicit `# TODO` prompts and `raise NotImplementedError(...)` stubs.
   - In `exercises_c0_modules.py` `__main__`: Gracefully catch `NotImplementedError` when students run the script before completion, reporting which exercises remain pending and pointing them to the reference solution.
   - In `solutions_c0_modules.py`: Maintain as-is, as it is already complete, working, and has 0 TODOs.
   - In `tests/e2e/test_course_0_e2e.py`: Add `test_course_0_exercises_and_solutions_integrity` under `TestTier1Course0Structure` to permanently automate this gate check (verifying $\ge 5$ TODOs in exercises, 0 TODOs in solutions, and clean `solutions_c0_modules.py` execution).
   - Verify that all E2E tests across Course 0, Engineering Math, and NEAT continue to pass 100%.

---

## 3. Caveats

- **Scope of Violation**: The integrity issue was confined entirely to `course_0_prerequisites/exercises/exercises_c0_modules.py`. The companion markdown guide `exercises_c0_comprehensive.md` (356 lines) already contains extensive 4-tier pedagogical problems across all 15 modules.
- **No Malicious Intent**: The pre-implementation appeared to be a shortcut so that `python3 exercises_c0_modules.py` was self-passing.
- **Read-Only Explorer Compliance**: No codebase files outside `.agents/explorer_remediation_3/` were modified by this explorer. All remediations are prepared as ready-to-apply patches and replacement files for the Worker.

---

## 4. Conclusion & Actionable Worker Remediation Plan

### 4.1 Remediation Artifacts Created
In `.agents/explorer_remediation_3/`:
1. `proposed_exercises_c0_modules.py`: Complete replacement file for `course_0_prerequisites/exercises/exercises_c0_modules.py`.
2. `exercises_c0_modules.patch`: Unified diff patch against `course_0_prerequisites/exercises/exercises_c0_modules.py`.
3. `test_course_0_e2e.patch`: Unified diff patch against `tests/e2e/test_course_0_e2e.py`.

### 4.2 Exact Code Modifications Required for Worker

#### Modification 1: `course_0_prerequisites/exercises/exercises_c0_modules.py`
Replace lines 11–65 and lines 86–94 with `# TODO` comments and `raise NotImplementedError(...)` stubs:

```python
# Exercise 1: Safe AST Calculator (Module 01 & 09)
def student_safe_add(a: float, b: float) -> float:
    """Exercise 1.1: Return the sum of two numbers."""
    # TODO: Implement safe addition of two floating-point numbers
    raise NotImplementedError("Exercise 1.1: student_safe_add not implemented")


# Exercise 2: Dunder representation (Module 02)
class StudentAgentMessage:
    """Exercise 2.1: Implement __repr__ and __str__."""
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        # TODO: Return formal representation: StudentAgentMessage(role='...', content='...')
        raise NotImplementedError("Exercise 2.1: StudentAgentMessage.__repr__ not implemented")

    def __str__(self) -> str:
        # TODO: Return user-facing string representation: [ROLE]: content (with role in uppercase)
        raise NotImplementedError("Exercise 2.1: StudentAgentMessage.__str__ not implemented")


# Exercise 3: Code fence stripper (Module 07)
def student_strip_fences(text: str) -> str:
    """Exercise 7.1: Extract JSON from markdown backticks."""
    # TODO: Extract raw JSON content from markdown code fences (```json ... ``` or ``` ... ```),
    # or isolate the outermost balanced curly braces { ... }
    raise NotImplementedError("Exercise 7.1: student_strip_fences not implemented")


# Exercise 4: Cosine similarity (Module 15)
def student_cosine_similarity(u: List[float], v: List[float]) -> float:
    """Exercise 15.1: Calculate cosine similarity between two vectors."""
    # TODO: Compute cosine similarity = (u . v) / (||u|| * ||v||)
    # Return 0.0 if either norm is zero.
    raise NotImplementedError("Exercise 15.1: student_cosine_similarity not implemented")


# Exercise 5: Softmax with temperature (Module 15)
def student_softmax(logits: List[float], temp: float = 1.0) -> List[float]:
    """Exercise 15.2: Calculate numerically stable softmax with temperature."""
    # TODO: Calculate numerically stable softmax with temperature scaling:
    # 1. Clamp temperature to minimum 1e-4 to avoid division by zero.
    # 2. Scale logits: scaled = [z / t for z in logits].
    # 3. Shift by max(scaled) for numerical stability.
    # 4. Compute exponentials and return normalized probability distribution.
    raise NotImplementedError("Exercise 15.2: student_softmax not implemented")
```

And in `if __name__ == "__main__":`:
```python
if __name__ == "__main__":
    print("=== Course 0 Student Exercises Workbook ===")
    print("Complete all # TODO items across the 5 exercises above.")
    print("For reference solutions, run: python3 course_0_prerequisites/solutions/solutions_c0_modules.py\n")
    try:
        test_student_exercises()
    except NotImplementedError as exc:
        print(f"[PENDING IMPLEMENTATION] {exc}")
        print("Keep going! Implement each TODO stub to pass the verification suite.")
```

#### Modification 2: `tests/e2e/test_course_0_e2e.py`
Append `test_course_0_exercises_and_solutions_integrity` to `TestTier1Course0Structure` (after line 123):
```python
    def test_course_0_exercises_and_solutions_integrity(self):
        """Verify exercises contain TODO markers and stubs, while solutions are complete with zero TODOs."""
        ex_file = COURSE_0_DIR / "exercises" / "exercises_c0_modules.py"
        sol_file = COURSE_0_DIR / "solutions" / "solutions_c0_modules.py"

        assert ex_file.exists(), f"Exercise file missing at {ex_file}"
        assert sol_file.exists(), f"Solution file missing at {sol_file}"

        # 1. Verify exercise workbook contains TODO markers and NotImplementedError stubs
        ex_content = ex_file.read_text(encoding="utf-8")
        todo_matches = re.findall(r"#\s*TODO", ex_content)
        assert len(todo_matches) >= 5, (
            f"exercises_c0_modules.py must contain >= 5 # TODO markers, found {len(todo_matches)}"
        )
        assert "NotImplementedError" in ex_content, (
            "exercises_c0_modules.py must contain NotImplementedError stubs"
        )

        # 2. Verify solution file contains zero unresolved TODO markers
        sol_content = sol_file.read_text(encoding="utf-8")
        sol_todos = re.findall(r"#\s*TODO", sol_content)
        assert len(sol_todos) == 0, (
            f"solutions_c0_modules.py must not contain unresolved TODO markers, found {len(sol_todos)}"
        )

        # 3. Verify solutions script executes cleanly and passes all assertions
        res = subprocess.run(
            [sys.executable, str(sol_file)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert res.returncode == 0, f"solutions_c0_modules.py failed: {res.stderr}"
```

### 4.3 Two-Step Worker Execution Commands
The Worker can apply the remediation instantly using either:
- **Method A (Direct Patch Application)**:
  ```bash
  patch /home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py < /home/settings/Documents/pearl/.agents/explorer_remediation_3/exercises_c0_modules.patch
  patch /home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py < /home/settings/Documents/pearl/.agents/explorer_remediation_3/test_course_0_e2e.patch
  ```
- **Method B (Drop-in Copy)**:
  ```bash
  cp /home/settings/Documents/pearl/.agents/explorer_remediation_3/proposed_exercises_c0_modules.py /home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py
  patch /home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py < /home/settings/Documents/pearl/.agents/explorer_remediation_3/test_course_0_e2e.patch
  ```

---

## 5. Verification Method

To independently verify the remediation:

1. **Verify TODO markers in exercise workbook**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/exercises/
   ```
   *Expected*: $\ge 5$ matches (actual will be 8 matches with clear instructions).

2. **Verify 0 TODO markers in reference solutions**:
   ```bash
   grep -rn -i "TODO" course_0_prerequisites/solutions/
   ```
   *Expected*: Exit code 1 (0 matches).

3. **Verify Reference Solution Script Execution**:
   ```bash
   python3 course_0_prerequisites/solutions/solutions_c0_modules.py
   ```
   *Expected*: Exit code 0, all 5 solutions reported passed.

4. **Verify Student Exercise Workbook Execution**:
   ```bash
   python3 course_0_prerequisites/exercises/exercises_c0_modules.py
   ```
   *Expected*: Exit code 0, displays `[PENDING IMPLEMENTATION] Exercise 1.1: student_safe_add not implemented`.

5. **Run Full Unified E2E Test Suite**:
   ```bash
   pytest tests/e2e/test_course_0_e2e.py tests/e2e/test_engineering_math_e2e.py tests/e2e/test_neat_e2e.py -v
   ```
   *Expected*: 108 passed (107 existing + 1 new exercise/solution integrity test).

6. **Invalidation Conditions**:
   - Any test failure in `test_course_0_e2e.py`, `test_engineering_math_e2e.py`, or `test_neat_e2e.py`.
   - `grep -rn -i "TODO" course_0_prerequisites/exercises/` returning $< 5$ matches.
   - `grep -rn -i "TODO" course_0_prerequisites/solutions/` returning $> 0$ matches.
