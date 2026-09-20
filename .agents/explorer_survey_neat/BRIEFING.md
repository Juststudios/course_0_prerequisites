# BRIEFING — 2026-09-20T12:37:55Z

## Mission
Survey the existing NEAT course directory and plan its comprehensive redesign according to the updated R3 requirements, delivering a detailed curriculum, projects, and visualization architecture report.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, curriculum designer, project architect
- Working directory: /home/settings/Documents/pearl/.agents/explorer_survey_neat
- Original parent: 2ef70cdb-ba1b-4189-9c08-55fbd1aced3e
- Milestone: NEAT Course Redesign Survey and Plan (R3)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement code in /home/settings/Documents/pearl/neat
- Only write metadata, reports, and working notes inside /home/settings/Documents/pearl/.agents/explorer_survey_neat/
- Pedagogical format strictly required: TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE
- Must design two runnable projects: XOR Evolution and Cart-Pole Control
- Must design Matplotlib visualizations: fitness curves, speciation tracking, network topology

## Current Parent
- Conversation ID: 2ef70cdb-ba1b-4189-9c08-55fbd1aced3e
- Updated: 2026-09-20T12:37:55Z

## Investigation State
- **Explored paths**:
  - `/home/settings/Documents/pearl/ORIGINAL_REQUEST.md`
  - `/home/settings/Documents/pearl/neat/` (all subdirectories)
  - `/home/settings/Documents/pearl/generate_neat.py`
  - `/home/settings/Documents/pearl/course_0_prerequisites/`
  - `/home/settings/Documents/pearl/TEST_READY.md`
- **Key findings**:
  - `neat/` currently contains only 4 files across 14 directories; all instructional lesson directories are completely empty.
  - Existing `06_xor/train.py` relies on `neat-python` which is not installed, crashing immediately upon launch.
  - Python environment has `numpy` (2.4.6) and `matplotlib` (3.11.0) installed.
  - Designed full progressive curriculum (Modules 1-6), zero-dependency `neat_engine/`, XOR project, Cart-Pole physics project, and pure-Matplotlib visualizers.
- **Unexplored areas**: None. Architectural survey is complete.

## Key Decisions Made
- Designed self-contained `neat_engine/` in pure Python/NumPy to eliminate brittle external dependencies and teach inner algorithmic mechanics transparently.
- Formulated Cart-Pole dynamical simulation using classical Euler-Cromer equations of motion without requiring `gym`.
- Formulated network topology visualizer using pure Matplotlib layer placement without requiring system `graphviz` or `dot` binaries.
- Formatted all modules according to `TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE`.

## Artifact Index
- `DISPATCH.md` — record of incoming dispatch messages
- `progress.md` — task progress and liveness tracking
- `BRIEFING.md` — persistent situational awareness
- `handoff.md` — comprehensive final survey, blueprint, and handoff report
