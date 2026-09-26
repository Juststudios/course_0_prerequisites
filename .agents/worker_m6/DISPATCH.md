# Dispatch for Worker M6

## 2026-09-21T15:32:35Z

## Identity
- Role: teamwork_preview_worker
- Working directory: /home/settings/Documents/pearl/.agents/worker_m6
- Parent Orchestrator: /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_8

## Mission
Complete and bring to 100% acceptance all modules in Milestone M6 (`course_-1_python_foundations/3[0-3]_*`).
Modules 30 and 31 already pass completely — DO NOT modify them.
Your exclusive write scope is:
- `course_-1_python_foundations/32_python_debugging/`
- `course_-1_python_foundations/33_integrated_projects/` (Capstone: Tool-using Mini ReAct Agent pipeline)

DO NOT touch files outside `3[0-3]_*`.

## Mandatory Lesson File Names
- 32: `python_debugging.py`
- 33: `mini_agent.py`

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
`python3 scripts/verify_course_minus_1.py --module 30,31,32,33`
Ensure all 4 modules report status PASS across all 4 checks.
Deliver your report to `/home/settings/Documents/pearl/.agents/worker_m6/handoff.md`.
