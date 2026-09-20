# E2E Test Infra: Educational Curriculum Expansion

## Test Philosophy
- Opaque-box, requirement-driven. Derives tests directly from ORIGINAL_REQUEST.md.
- Multi-tier methodology (Tier 1: Feature Coverage, Tier 2: Boundary & Corner Cases, Tier 3: Cross-Feature Combinations, Tier 4: Real-World Applications).
- Zero-external API requirement (all tests must run locally and deterministically).

## Feature Inventory & Test Mapping
| # | Feature | Requirement Source | Tier 1 (Count) | Tier 2 (Count) | Tier 3 | Tier 4 |
|---|---------|-------------------|:--------------:|:--------------:|:------:|:------:|
| 1 | Course 0 Modules (01-15) | ORIGINAL_REQUEST §R1 | 15 (runnable check) | 15 (pedagogical check) | ✓ | ✓ |
| 2 | MiniAgent Capstone | ORIGINAL_REQUEST §R1 | 5 (tools & memory) | 5 (error handling/timeout) | ✓ | ✓ |
| 3 | Math Package Verification | ORIGINAL_REQUEST §R2 | 5 (module health) | 5 (broken links/cheatsheets) | ✓ | ✓ |
| 4 | Math AI/ML Bridges | ORIGINAL_REQUEST §R2 | 5 (script execution) | 5 (analytical vs numerical) | ✓ | ✓ |
| 5 | NEAT Engine Core | ORIGINAL_REQUEST §R3 | 5 (genes/topological sort) | 5 (cycles/disjoint genes) | ✓ | ✓ |
| 6 | NEAT Project 1 (XOR) | ORIGINAL_REQUEST §R3 | 5 (training & convergence) | 5 (non-linear boundary) | ✓ | ✓ |
| 7 | NEAT Project 2 (Cart-Pole) | ORIGINAL_REQUEST §R3 | 5 (simulation steps >= 500) | 5 (extreme angle recovery) | ✓ | ✓ |
| 8 | NEAT Visualizations | ORIGINAL_REQUEST §R3 | 3 (PNG generation) | 3 (file sizes & non-empty) | ✓ | ✓ |

## Test Runner Architecture
- `pytest tests/e2e/test_course_0_e2e.py`
- `pytest tests/e2e/test_engineering_math_e2e.py`
- `pytest tests/e2e/test_neat_e2e.py`
- `python3 engineering-mathematics/scripts/verify_package.py`
- `python3 neat/projects/01_xor/verify_xor.py`
- `python3 neat/projects/02_cartpole/evaluate_controller.py`

## Acceptance Criteria Checklist
- [ ] Course 0 contains functional, runnable Python scripts for every major concept.
- [ ] The Course 0 `mini_agent` project executes successfully, combining async, sqlite, and a tool registry without syntax errors.
- [ ] The NEAT XOR project executes correctly and successfully evolves a neural network.
- [ ] The Math course enhancements explicitly reference AI/ML applications rather than creating a duplicate standalone math course.
- [ ] All new Markdown lessons rigorously follow the requested structured pedagogical format (`TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE`).
