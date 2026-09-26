# Dispatch for Worker M2

## Identity
- Role: teamwork_preview_worker
- Working directory: /home/settings/Documents/pearl/.agents/worker_m2
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Complete and bring to 100% acceptance all modules in Milestone M2 (`course_-1_python_foundations/0[7-9]_*` and `1[0-1]_*`).
Modules 07 and 08 already pass completely — DO NOT modify them.
Your exclusive write scope is:
- `course_-1_python_foundations/09_scope/`: Note: `scope.py`, `exercises.py`, and `solutions.py` ALREADY pass! Only rewrite `README.md` with the 18 required headers!
- `course_-1_python_foundations/10_errors_and_exceptions/`
- `course_-1_python_foundations/11_files/`

DO NOT touch files outside `0[7-9]_*` and `1[0-1]_*`.

## Mandatory Lesson File Names
- 09: `scope.py` (already passes, preserve it)
- 10: `errors.py`
- 11: `files.py`

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
`python3 scripts/verify_course_minus_1.py --module 07,08,09,10,11`
Ensure all 5 modules report status PASS across all 4 checks.
Deliver your report to `/home/settings/Documents/pearl/.agents/worker_m2/handoff.md`.

## 2026-09-21T15:32:35Z
You are Worker M2.
Your working directory is: /home/settings/Documents/pearl/.agents/worker_m2
Your parent is the Project Orchestrator at: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md, /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8/PROJECT.md, and /home/settings/Documents/pearl/.agents/worker_m2/DISPATCH.md.

Scope & Task:
Complete and bring to 100% acceptance all modules in Milestone M2 (07-11).
07 and 08 already pass completely. Do not modify them.
Your exclusive write scope is:
- course_-1_python_foundations/09_scope/ (Note: scope.py, exercises.py, solutions.py already pass! Only rewrite README.md with all 18 headers)
- course_-1_python_foundations/10_errors_and_exceptions/ (lesson: errors.py)
- course_-1_python_foundations/11_files/ (lesson: files.py)

For each module:
1. README.md with all 18 exact required headers in order, with deep, rich pedagogical explanations.
2. Main lesson file >= 150-200 lines, heavily commented, runnable with print outputs, clean exit code 0.
3. exercises.py with 4 distinct levels (Recall, Modify, Build, Debug) and authentic # TODO and raise NotImplementedError scaffolding.
4. solutions.py with complete, working solutions for all 4 levels, clean exit code 0, no NotImplementedError.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Self-verify by running: python3 scripts/verify_course_minus_1.py --module 07,08,09,10,11
Deliver handoff to /home/settings/Documents/pearl/.agents/worker_m2/handoff.md and notify parent via send_message.
