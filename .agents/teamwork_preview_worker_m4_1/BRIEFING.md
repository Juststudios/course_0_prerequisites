# BRIEFING — 2026-09-10T16:45:54Z

## Mission
Implement Module R4: Probability & Uncertainty in Engineering, including teaching README, 4 concept scripts, mini-project, 4-tier exercises, and decoupled complete solutions.

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa, specialist
- Working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m4_1
- Original parent: 6d60e83c-dc1b-4519-8d6e-b180671ecd46
- Milestone: M4 (Probability & Uncertainty in Engineering)

## 🔒 Key Constraints
- Exclusive file ownership:
  - /home/settings/Documents/pearl/engineering-mathematics/probability/README.md
  - /home/settings/Documents/pearl/engineering-mathematics/probability/01_probability_foundations.m
  - /home/settings/Documents/pearl/engineering-mathematics/probability/02_distributions_and_moments.m
  - /home/settings/Documents/pearl/engineering-mathematics/probability/03_monte_carlo_simulation.m
  - /home/settings/Documents/pearl/engineering-mathematics/probability/04_sensor_noise_filtering.m
  - /home/settings/Documents/pearl/engineering-mathematics/probability/mini_project_reliability.m
  - /home/settings/Documents/pearl/engineering-mathematics/probability/exercises.m
  - /home/settings/Documents/pearl/engineering-mathematics/solutions/probability_exercises_solution.m
- MANDATORY INTEGRITY WARNING: DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task.
- 9-section teaching standard in README.md ("Explain WHY before HOW").
- 4-tier progressive exercises (Recall, Understanding & Debugging, Application, Challenge) with `% TODO` in exercises.m.
- Solutions file must have 0 `% TODO` and complete runnable reference code.
- Code quality: >= 20% comment lines, valid syntax, balanced blocks and delimiters, no 0-based indexing.
- Independent verification via scripts/verify_package.py and pytest.

## Current Parent
- Conversation ID: 6d60e83c-dc1b-4519-8d6e-b180671ecd46
- Updated: not yet

## Task Summary
- **What to build**: Full M4 Probability & Uncertainty curriculum module and solutions.
- **Success criteria**: All 8 assigned files implemented to standard; 100% pass on verify_package.py (--module probability) and pytest suites; >= 20% comment ratio; 0 syntax errors.
- **Interface contracts**: /home/settings/Documents/pearl/.agents/PROJECT.md § Interface Contracts
- **Code layout**: /home/settings/Documents/pearl/.agents/PROJECT.md § Module Boundaries & Directory Layout

## Key Decisions Made
- Architecture: 4 concept scripts covering foundations & Bayes (01), distributions & moments (02), Monte Carlo & LLN (03), sensor noise & filtering (04).
- Mini-project: Component and system reliability modeling (series/parallel, MTBF, exponential distribution, survival probability curves).
- 4-Tier exercises:
  - Level 1: Recall (normal noise generation, sample mean & variance calculation)
  - Level 2: Understanding & Debugging (sample variance N-1 vs N biased estimator, Bayes theorem false alarm calculation)
  - Level 3: Application (sensor telemetry noise suppression and SNR optimization)
  - Level 4: Challenge (Monte Carlo reliability simulation of an aircraft quad-redundant hydraulic system)
- Decoupled solution in solutions/probability_exercises_solution.m.

## Artifact Index
- /home/settings/Documents/pearl/engineering-mathematics/probability/README.md — 9-section pedagogical guide
- /home/settings/Documents/pearl/engineering-mathematics/probability/01_probability_foundations.m — Foundations & Bayes
- /home/settings/Documents/pearl/engineering-mathematics/probability/02_distributions_and_moments.m — Distributions & moments
- /home/settings/Documents/pearl/engineering-mathematics/probability/03_monte_carlo_simulation.m — Monte Carlo simulations
- /home/settings/Documents/pearl/engineering-mathematics/probability/04_sensor_noise_filtering.m — Noise modeling & filtering
- /home/settings/Documents/pearl/engineering-mathematics/probability/mini_project_reliability.m — Reliability mini-project
- /home/settings/Documents/pearl/engineering-mathematics/probability/exercises.m — 4-tier student exercise template
- /home/settings/Documents/pearl/engineering-mathematics/solutions/probability_exercises_solution.m — Complete reference solution

## Change Tracker
- **Files modified**: None yet (initial setup)
- **Build status**: Not run yet
- **Pending issues**: All 8 files to be created and verified

## Quality Status
- **Build/test result**: verify_package.py failed initially due to missing files (expected)
- **Lint status**: 0 violations so far
- **Tests added/modified**: TBD

## Loaded Skills
- None specified
