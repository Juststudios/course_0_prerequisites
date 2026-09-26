# Dispatch for Test Writer 1

## Identity
- Role: teamwork_preview_test_writer
- Working directory: /home/settings/Documents/pearl/.agents/test_writer_1
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Inspect, create, or update the E2E verification test harness and script for Course -1 Python Foundations, execute the tests against the current codebase, and establish baseline pass/fail status.

## Key Inputs
- Original Request: `/home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md`
- Project Plan: `/home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8/PROJECT.md`
- Course Directory: `/home/settings/Documents/pearl/course_-1_python_foundations/`

## Requirements
1. Inspect or create `/home/settings/Documents/pearl/scripts/verify_course_minus_1.py`.
2. Inspect or create `/home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py`.
3. The test suite must check all 33 modules in `course_-1_python_foundations/`:
   - R1: README.md exists and has all 18 required header sections (1. # Topic, 2. ## What You Will Learn, 3. ## Prerequisites, 4. ## The Problem, 5. ## Key Terminology, 6. ## Intuition, 7. ## Concept, 8. ## Syntax, 9. ## Example, 10. ## Line-by-Line Explanation, 11. ## What Python Is Doing, 12. ## Common Mistakes, 13. ## Real-World Uses, 14. ## Connection to AI Agents, 15. ## Practice, 16. ## Challenge, 17. ## Summary, 18. ## What You Should Know Before Moving On).
   - R2: Main `.py` lesson file exists, is >= 150 lines, and executes cleanly (exit code 0).
   - R3: `exercises.py` exists, contains 4 levels (Recall, Modify, Build, Debug), and has `NotImplementedError` or `# TODO`.
   - R3: `solutions.py` exists, and executes cleanly (exit code 0).
4. Run the script and pytest tests across the current workspace.
5. Create `/home/settings/Documents/pearl/TEST_INFRA.md` and report baseline results in `/home/settings/Documents/pearl/.agents/test_writer_1/handoff.md`.

## 2026-09-21T15:12:48Z
Task received:
1. Inspect or create /home/settings/Documents/pearl/scripts/verify_course_minus_1.py.
2. Inspect or create /home/settings/Documents/pearl/tests/e2e/test_course_minus_1_acceptance.py.
3. The verification script and pytest acceptance tests must strictly and comprehensively verify all 33 modules in course_-1_python_foundations/:
   - R1: README.md exists and contains all 18 exact required headers in order, with non-empty content in every section.
   - R2: Main .py lesson file exists, is at least 150 lines, and executes with exit code 0.
   - R3: exercises.py exists, has 4 distinct levels (Recall, Modify, Build, Debug), and contains NotImplementedError or # TODO.
   - R3: solutions.py exists, contains no NotImplementedError, and executes with exit code 0.
4. Execute the verification script and pytest test suite to determine current baseline status across all 33 modules.
5. Create /home/settings/Documents/pearl/TEST_INFRA.md documenting the test architecture and commands.
6. Write full results and baseline pass/fail counts to /home/settings/Documents/pearl/.agents/test_writer_1/handoff.md.
When finished, notify your parent via send_message.
