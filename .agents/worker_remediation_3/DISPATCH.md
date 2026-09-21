## 2026-09-21T10:00:57Z
You are Remediation Worker (worker_remediation_3).
Your working directory is /home/settings/Documents/pearl/.agents/worker_remediation_3/
Repository workspace root: /home/settings/Documents/pearl

MANDATORY FIRST STEP:
Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md.
Also read:
- /home/settings/Documents/pearl/.agents/auditor_gate_1/handoff.md (Forensic Audit Violation Report)
- /home/settings/Documents/pearl/.agents/explorer_remediation_1/handoff.md
- /home/settings/Documents/pearl/.agents/explorer_remediation_2/handoff.md
- /home/settings/Documents/pearl/.agents/explorer_remediation_3/handoff.md
- /home/settings/Documents/pearl/TEST_READY.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

EXCLUSIVE WRITE OWNERSHIP:
You exclusively own and may edit:
- /home/settings/Documents/pearl/course_0_prerequisites/exercises/exercises_c0_modules.py
- /home/settings/Documents/pearl/tests/e2e/test_course_0_e2e.py

DO NOT modify /home/settings/Documents/pearl/course_0_prerequisites/solutions/solutions_c0_modules.py (it is already 100% complete and working with 0 TODOs).

YOUR MISSION:
Remediate the integrity violation identified by the forensic auditor:
1. Update `course_0_prerequisites/exercises/exercises_c0_modules.py`:
   - Replace pre-implemented function bodies with explicit `# TODO: ...` markers and `raise NotImplementedError(...)` stubs across all 5 exercises:
     * Exercise 1.1: `student_safe_add`
     * Exercise 2.1: `StudentAgentMessage` (`__repr__` and `__str__`)
     * Exercise 7.1: `student_strip_fences`
     * Exercise 15.1: `student_cosine_similarity`
     * Exercise 15.2: `student_softmax`
   - Include `validate_student_exercises()` so students can test their solutions when completed.
   - In `if __name__ == "__main__":`, catch `NotImplementedError` gracefully and print student guidance pointing to reference solutions in `course_0_prerequisites/solutions/solutions_c0_modules.py`.
2. Update `tests/e2e/test_course_0_e2e.py`:
   - Add contract test `test_course_0_exercises_and_solutions_contracts` (per Explorer 1/2/3 proposals) that asserts:
     * `exercises_c0_modules.py` exists and contains >= 5 `TODO` markers.
     * The uncompleted student stubs raise `NotImplementedError`.
     * `solutions_c0_modules.py` exists, contains exactly 0 `TODO` markers, and executes cleanly with 100% pass rate.
3. Run verification commands and verify 100% pass:
   - `grep -rn -i "TODO" course_0_prerequisites/exercises/` (verify >= 5 matches)
   - `grep -rn -i "TODO" course_0_prerequisites/solutions/` (verify 0 matches)
   - `python3 course_0_prerequisites/exercises/exercises_c0_modules.py` (exits cleanly with pending notice)
   - `python3 course_0_prerequisites/solutions/solutions_c0_modules.py` (exits 0 with 100% pass rate)
   - `pytest tests/e2e/test_course_0_e2e.py -v` (all pass)
   - `pytest tests/e2e/ -v` (all 108+ pass)
4. Document all changes and verification outputs in `handoff.md` in your working directory and notify the orchestrator via send_message.
