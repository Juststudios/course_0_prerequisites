# Dispatch for Worker M3

## Identity
- Role: teamwork_preview_worker
- Working directory: /home/settings/Documents/pearl/.agents/worker_m3
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Complete and bring to 100% acceptance all modules in Milestone M3 (`course_-1_python_foundations/1[2-6]_*`).
Your exclusive write scope is:
- `course_-1_python_foundations/12_modules/`
- `course_-1_python_foundations/13_classes_and_oop/`
- `course_-1_python_foundations/14_functional_programming/` (Note: Currently completely empty folder; must create README.md, functional.py, exercises.py, solutions.py from scratch)
- `course_-1_python_foundations/15_type_hints/`
- `course_-1_python_foundations/16_dataclasses/`

DO NOT touch files outside `1[2-6]_*`.

## Mandatory Lesson File Names
- 12: `modules.py`
- 13: `classes.py`
- 14: `functional.py`
- 15: `typing_lesson.py`
- 16: `dataclasses_lesson.py`

## Mandatory Requirements (R1 - R4)
1. **README.md** with the 18 exact headers in sequential order, with substantive, rich, deep pedagogical text:
   1. `# Topic`
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
2. **Main Lesson File**: >= 150-200 lines, heavily commented with narrative explanations, progressive examples, clear print() outputs, executes cleanly with exit code 0.
3. **exercises.py**: 4 distinct tiers (`Level 1: Recall`, `Level 2: Modify`, `Level 3: Build`, `Level 4: Debug`), with authentic `# TODO` comments and `raise NotImplementedError` scaffolding.
4. **solutions.py**: Decoupled clean implementations of all 4 levels, NO `NotImplementedError`, executes cleanly with exit code 0.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Self-Verification
Run:
`python3 scripts/verify_course_minus_1.py --module 12,13,14,15,16`
Ensure all 5 modules report status PASS across all 4 checks.
Deliver your report to `/home/settings/Documents/pearl/.agents/worker_m3/handoff.md`.
