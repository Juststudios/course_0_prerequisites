# BRIEFING — 2026-09-20T12:41:00Z

## Mission
Implement Milestone M3: NEAT Curriculum Redesign & Projects, including pure-Python zero-dependency neat_engine, 6 progressive curriculum modules with standard README format and runnable scripts, visualizers, Project 1 (XOR), Project 2 (Cart-Pole), exercises & solutions, and comprehensive unit/project tests.

## 🔒 My Identity
- Archetype: worker_neat
- Roles: implementer, qa, specialist
- Working directory: /home/settings/Documents/pearl/.agents/worker_neat/
- Original parent: 2ef70cdb-ba1b-4189-9c08-55fbd1aced3e
- Milestone: M3 (NEAT Curriculum Redesign & Projects)

## 🔒 Key Constraints
- EXCLUSIVE WRITE OWNERSHIP: Only write under `/home/settings/Documents/pearl/neat/` and own `.agents/worker_neat/`.
- Do NOT write to `course_0_prerequisites/`, `engineering-mathematics/`, or `tests/e2e/`.
- DO NOT CHEAT: Genuine implementation, no hardcoded values/test results, no dummy facades.
- Pure Python, zero external dependencies for `neat_engine/` (only standard library: random, math, typing, dataclasses, collections, copy).
- Visualizer uses only pure Matplotlib (no graphviz binary required).
- Strict 6-part README template for curriculum: TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE.
- Project 1 (XOR): fitness > 3.9, outputs PNGs.
- Project 2 (Cart-Pole): pure-Python dynamical simulation (Lagrangian, Euler-Cromer), balances >= 500 steps, multi-trial evaluation, outputs PNGs.

## Current Parent
- Conversation ID: 2ef70cdb-ba1b-4189-9c08-55fbd1aced3e
- Updated: not yet

## Task Summary
- **What to build**: Pure-Python NEAT engine, 6 curriculum modules with runnable scripts, Matplotlib visualizers, XOR project, Cart-Pole dynamical simulator & project, exercises & solutions, unit & project tests.
- **Success criteria**: All tests pass, XOR evolves controller fitness > 3.9, Cart-Pole balances >= 500 steps, visualizer generates plots, all curriculum READMEs follow 6-part format.
- **Interface contracts**: See PROJECT.md and ORIGINAL_REQUEST.md.
- **Code layout**: Under `neat/`.

## Key Decisions Made
- [TBD]

## Artifact Index
- [TBD]

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Not yet run
- **Lint status**: 0 violations
- **Tests added/modified**: None yet

## Loaded Skills
- None specified in dispatch
