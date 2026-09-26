# Dispatch for Worker M4

## Identity
- Role: teamwork_preview_worker
- Working directory: /home/settings/Documents/pearl/.agents/worker_m4
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Complete and bring to 100% acceptance all modules in Milestone M4 (`course_-1_python_foundations/1[7-9]_*` and `2[0-2]_*`).
Module 17 (`17_generators`) already passes completely — DO NOT modify it.
Your exclusive write scope is:
- `course_-1_python_foundations/18_iterators/`
- `course_-1_python_foundations/19_decorators/`
- `course_-1_python_foundations/20_context_managers/`
- `course_-1_python_foundations/21_testing/`
- `course_-1_python_foundations/22_logging/`

DO NOT touch files outside `1[7-9]_*` and `2[0-2]_*`.

## Mandatory Lesson File Names
- 18: `iterators.py`
- 19: `decorators.py`
- 20: `context_managers.py`
- 21: `testing.py`
- 22: `logging_lesson.py`

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
`python3 scripts/verify_course_minus_1.py --module 17,18,19,20,21,22`
Ensure all 6 modules report status PASS across all 4 checks.
Deliver your report to `/home/settings/Documents/pearl/.agents/worker_m4/handoff.md`.

## 2026-09-21T15:32:35Z
You are Worker M4.
Your working directory is: /home/settings/Documents/pearl/.agents/worker_m4
Your parent is the Project Orchestrator at: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md, /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8/PROJECT.md, and /home/settings/Documents/pearl/.agents/worker_m4/DISPATCH.md.

Scope & Task:
Complete and bring to 100% acceptance all modules in Milestone M4 (17-22).
Module 17 already passes completely. Do not modify it.
Your exclusive write scope is:
- course_-1_python_foundations/18_iterators/ (lesson: iterators.py)
- course_-1_python_foundations/19_decorators/ (lesson: decorators.py)
- course_-1_python_foundations/20_context_managers/ (lesson: context_managers.py)
- course_-1_python_foundations/21_testing/ (lesson: testing.py)
- course_-1_python_foundations/22_logging/ (lesson: logging_lesson.py)

For each module:
1. README.md with all 18 exact required headers in order, with deep, rich pedagogical explanations.
2. Main lesson file >= 150-200 lines, heavily commented, runnable with print outputs, clean exit code 0.
3. exercises.py with 4 distinct levels (Recall, Modify, Build, Debug) and authentic # TODO and raise NotImplementedError scaffolding.
4. solutions.py with complete, working solutions for all 4 levels, clean exit code 0, no NotImplementedError.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Self-verify by running: python3 scripts/verify_course_minus_1.py --module 17,18,19,20,21,22
Deliver handoff to /home/settings/Documents/pearl/.agents/worker_m4/handoff.md and notify parent via send_message.
