# Dispatch for Worker M5

## Identity
- Role: teamwork_preview_worker
- Working directory: /home/settings/Documents/pearl/.agents/worker_m5
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Complete and bring to 100% acceptance all modules in Milestone M5 (`course_-1_python_foundations/2[3-9]_*`).
Modules 23 and 24 already pass completely — DO NOT modify them.
Module 25's `README.md` already passes R1 with all 18 headers — preserve it, but rewrite `async_concurrency.py` (>= 150L), `exercises.py`, and `solutions.py`.
Your exclusive write scope is:
- `course_-1_python_foundations/25_async_concurrency/`
- `course_-1_python_foundations/26_http_and_json_intro/`
- `course_-1_python_foundations/27_environment_variables/`
- `course_-1_python_foundations/28_subprocesses_intro/`
- `course_-1_python_foundations/29_sqlite_intro/`

DO NOT touch files outside `2[3-9]_*`.

## Mandatory Lesson File Names
- 25: `async_concurrency.py`
- 26: `http_json_intro.py`
- 27: `env_vars.py`
- 28: `subprocess_intro.py`
- 29: `sqlite_intro.py`

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
`python3 scripts/verify_course_minus_1.py --module 23,24,25,26,27,28,29`
Ensure all 7 modules report status PASS across all 4 checks.
Deliver your report to `/home/settings/Documents/pearl/.agents/worker_m5/handoff.md`.

## 2026-09-21T15:32:35Z
You are Worker M5.
Your working directory is: /home/settings/Documents/pearl/.agents/worker_m5
Your parent is the Project Orchestrator at: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

MANDATORY FIRST STEP: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md, /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8/PROJECT.md, and /home/settings/Documents/pearl/.agents/worker_m5/DISPATCH.md.

Scope & Task:
Complete and bring to 100% acceptance all modules in Milestone M5 (23-29).
23 and 24 already pass completely. Do not modify them.
Module 25's README.md already passes R1 with all 18 headers — preserve it! Rewrite async_concurrency.py (>= 150L), exercises.py, and solutions.py.
Your exclusive write scope is:
- course_-1_python_foundations/25_async_concurrency/ (lesson: async_concurrency.py)
- course_-1_python_foundations/26_http_and_json_intro/ (lesson: http_json_intro.py)
- course_-1_python_foundations/27_environment_variables/ (lesson: env_vars.py)
- course_-1_python_foundations/28_subprocesses_intro/ (lesson: subprocess_intro.py)
- course_-1_python_foundations/29_sqlite_intro/ (lesson: sqlite_intro.py)

For each module:
1. README.md with all 18 exact required headers in order, with deep, rich pedagogical explanations.
2. Main lesson file >= 150-200 lines, heavily commented, runnable with print outputs, clean exit code 0.
3. exercises.py with 4 distinct levels (Recall, Modify, Build, Debug) and authentic # TODO and raise NotImplementedError scaffolding.
4. solutions.py with complete, working solutions for all 4 levels, clean exit code 0, no NotImplementedError.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Self-verify by running: python3 scripts/verify_course_minus_1.py --module 23,24,25,26,27,28,29
Deliver handoff to /home/settings/Documents/pearl/.agents/worker_m5/handoff.md and notify parent via send_message.

