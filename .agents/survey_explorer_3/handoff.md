# Survey Explorer 3 Handoff Report: Levels 5, 6, & 7 and Global Curriculum Specifications

**Date:** 2026-09-11  
**Agent:** survey_explorer_3 (Survey Explorer)  
**Working Directory:** `/home/settings/Documents/pearl/.agents/survey_explorer_3`  
**Parent Orchestrator ID:** `27392bad-d624-4f4f-bde1-27fac6bdb384`

---

## 1. Observation

Direct, verbatim observations and file evidence gathered during the survey across the repository:

### 1.1 Global Architecture & Curriculum Specifications
- **Level Taxonomy Inconsistencies:** The repository contains three distinct, overlapping mappings of curriculum levels:
  1. **The Core Pedagogical Learning Path** (observed in `machine-learning/README.md` lines 12–18, `neat/README.md` lines 7–13, and `game-ai/README.md` lines 9–21):
     - Level 1: Python Data Tools (`python-data-tools/`) — NumPy, Pandas, Matplotlib
     - Level 2: Engineering Mathematics (`engineering-mathematics/`) — MATLAB, Linear Algebra, Calculus, Probability, Simulink
     - Level 3: Machine Learning (`machine-learning/01–06`) — Supervised, Unsupervised, Evaluation
     - Level 4: Deep Learning (`machine-learning/07–11`) and Neuroevolution (`neat/`)
     - Level 5+: Game AI & Board-Game Algorithms (`game-ai/01–12`), MLOps, and Capstones
  2. **The Scripted Audit Taxonomy** (observed in `generate_audit_report.py` lines 27–90):
     - Level 1: Python Data Tools (`python-data-tools/lessons/01_numpy`, `02_pandas`, `03_matplotlib`)
     - Level 2: Engineering Math (`engineering-mathematics/matlab`, `linear_algebra`, `calculus`, `probability`, `simulink`)
     - Level 3: Machine Learning (`machine-learning/01_ml_fundamentals` through `06_model_evaluation`)
     - Level 3.5: Math-First ML (`ml-course`)
     - Level 4: NEAT (`neat`)
     - Level 5: Deep Learning (`machine-learning/07_deep_learning_intro`, `08_pytorch_fundamentals`, `09_neural_networks`, `10_cnns`, `11_transformers`, TensorFlow="MISSING")
     - Level 6: Networking (`TCP/IP`, `HTTP/HTTPS`, `REST APIs` all marked `"MISSING"`)
     - Level 7: Game AI (`game-ai/01_pygame` through `11_reinforcement_learning`)
  3. **The Orchestrator Execution Plan** (observed in `.agents/teamwork_preview_orchestrator_2/plan.md` lines 21–27):
     - Batch 1: Level 1 (Foundations)
     - Batch 2: Level 2 (Engineering Mathematics & MATLAB)
     - Batch 3: Level 3 (Machine Learning)
     - Batch 4: Level 4 (Deep Learning & Advanced Modules)
     - Batch 5: Level 5 (Specialized Topics / MLOps / Systems)
     - Batch 6: Levels 6 & 7 (Capstones, Advanced Research & Projects)

### 1.2 Level 5 Structure & Topic Inventory (Deep Learning / Specialized Topics / MLOps)
- **Deep Learning Modules in `machine-learning/`**:
  - `07_deep_learning_intro/`: `01_tensors.py` (9964 B), `02_autograd.py` (9409 B), `03_linear_model_in_pytorch.py` (9160 B), `04_datasets_and_dataloaders.py` (10697 B), `README.md` (6457 B), `exercises.py` (7128 B).
  - `08_pytorch_fundamentals/`: `01_nn_module.py` (14056 B), `02_loss_functions.py` (13982 B), `03_optimizers.py` (13520 B), `04_training_loop.py` (11448 B), `05_mlp_classification.py` (10233 B), `README.md` (6254 B), `exercises.py` (8047 B).
  - `09_neural_networks/`: `01_activation_functions.py` (8414 B), `02_backpropagation_and_deep_mlp.py` (9345 B), `README.md` (5012 B), `exercises.py` (8688 B).
    - *Discrepancy:* `README.md` lines 119–125 advertises `02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`, and `exercises_solutions.py`. None of these five files exist on disk.
  - `10_cnns/`: `01_convolution.py` (13873 B), `02_pooling_and_architecture.py` (19403 B), `03_cnn_for_images.py` (11127 B), `04_transfer_learning.py` (13727 B), `README.md` (9376 B), `exercises.py` (9326 B).
  - `11_transformers/`: `01_attention_and_transformers.py` (15015 B), `README.md` (3472 B), `exercises.py` (10569 B).
  - `12_capstone/`: `generate_capstone_data.py` (9557 B), `starter_template.py` (10873 B), `README.md` (6505 B).
    - *Discrepancy:* `README.md` references `solutions/capstone_solution.py` (line 161), but no such file exists in `machine-learning/solutions/`.
  - `reference/`: `ml_cheat_sheet.md` (9071 B), `pytorch_cheat_sheet.md` (10259 B).
    - *Discrepancy:* `machine-learning/README.md` lines 137–138 lists `ml_mathematics.md` and `algorithm_guide.md`, neither of which exists.
  - `solutions/`: Contains only `ml_fundamentals_solutions.py`, `pytorch_neural_net_solutions.py`, and `sklearn_regression_clustering_solutions.py`. Missing separate `advanced_dl_solutions.py`, `classification_solutions.py`, `model_evaluation_solutions.py`, and `capstone_solution.py`.
- **Specialized Topics / NEAT (`neat/`)**:
  - `01_evolutionary_computation/`: `README.md` (3662 B), `examples/01_string_evolution.py` (3375 B), `exercises/` (EMPTY).
  - `02_genetic_algorithms/`: `README.md` (2871 B), `examples/01_function_maximization.py` (3492 B), `exercises/` (EMPTY).
  - `03_neat_fundamentals/`: `README.md` (5466 B), `examples/` (EMPTY), `exercises/` (EMPTY).
  - `04_neat_python/`: `README.md` (4311 B), `configs/example_config.txt` (1928 B), `examples/` (EMPTY).
  - `05_xor/`: `README.md` (2655 B), `config-feedforward.txt` (2193 B), `train.py` (3555 B), `visualize.py` (3243 B).
  - `06_pole_balancing/`: `README.md` (2787 B), `train.py` (3551 B), `config/`.
  - `capstone/`: `README.md` (3030 B), `starter.py` (1006 B). Autonomous Lunar Lander with Gymnasium. No reference solution exists.
  - `exercises/`: `01_debugging.py` (3604 B), `02_practice.py` (3244 B).
  - `solutions/`: `01_debugging_solution.py` (2424 B), `02_practice_solution.py` (2890 B).
  - `reference/`: `NEAT_CHEAT_SHEET.md` (3547 B).
  - `assessment/`: `FINAL_ASSESSMENT.md` (2857 B).
  - `projects/`: EMPTY directory.

### 1.3 Level 6 Structure & Topic Inventory (Networking / Systems / MLOps)
- **Networking Specification**: In `generate_audit_report.py` lines 72–76:
  `"Level 6: Networking": {"TCP/IP": "MISSING", "HTTP/HTTPS": "MISSING", "REST APIs": "MISSING"}`
- **MLOps & Deployment Specification**: In `machine-learning/README.md` lines 257–258:
  `3. Deployment — Serve models as REST APIs with FastAPI`
  `4. MLOps — MLflow for experiment tracking, Docker for reproducibility`
- **Observed Files on Disk**: Zero files, zero directories, and zero configuration scripts exist anywhere in `/home/settings/Documents/pearl` for TCP/IP, HTTP/HTTPS, FastAPI, MLflow, or Docker. Searches for `*tcp*`, `*http*`, `*api*`, and `*mlops*` confirmed no networking modules exist.

### 1.4 Level 7 Structure & Topic Inventory (Game AI & Board-Game Algorithms)
- Directory: `/home/settings/Documents/pearl/game-ai/`
- Modules:
  - `01_pygame/`: `01_basics.py` (1154 B), `02_game_loop.py` (1704 B), `03_movement_and_collision.py` (1538 B), `README.md` (1948 B).
  - `02_game_state/`: `README.md` (2684 B). Architecture only; no code files.
  - `03_tic_tac_toe/`: `tic_tac_toe.py` (1967 B), `ui.py` (2393 B), `play_human.py` (1422 B), `play_random_ai.py` (1813 B), `README.md` (1366 B).
  - `04_minimax/`: `minimax.py` (2374 B), `play_minimax_ai.py` (1756 B), `README.md` (2425 B).
  - `05_alpha_beta/`: `alpha_beta.py` (2340 B), `README.md` (2555 B).
  - `06_heuristics/`: `README.md` (2513 B). Conceptual evaluation functions; no code files.
  - `07_connect_four/`: `connect_four.py` (6589 B), `play_ai.py` (3290 B). Missing module `README.md`.
  - `08_checkers/`: `README.md` (1508 B). Explicitly states: *"In the interest of time for this curriculum, we do not require you to build the full Checkers engine from scratch. Move on to Module 9 (Chess)"* (line 26). Zero code files.
  - `09_chess/`: `chess_ai.py` (4788 B), `README.md` (2089 B). Uses `python-chess` library for legal moves, implements Alpha-Beta with Piece-Square Tables and move ordering.
  - `10_mcts/`: `README.md` (2043 B). Explains UCB1, selection, expansion, simulation, backpropagation. Zero code files.
  - `11_reinforcement_learning/`: `README.md` (2431 B). Explains policy networks, RL loop, AlphaZero hybrid concept. Zero code files.
  - `12_neural_game_ai/`: `README.md` (2081 B). Explains policy/value network integration with MCTS. Zero code files.
  - `capstone/`: `reversi_starter.py` (1416 B), `README.md` (2494 B). Othello/Reversi AI project. Zero reference solution.
  - `exercises/`: `FINAL_ASSESSMENT.md` (2542 B), `debugging.py` (2991 B).
  - `solutions/`: `debugging_solutions.py` (2625 B).
  - `reference/`: `GAME_AI_CHEAT_SHEET.md` (2542 B).
  - `requirements.txt`: `pygame`, `numpy`, `matplotlib`, `python-chess` (37 B).
  - `games/`: EMPTY directory.
  - `projects/`: EMPTY directory.

### 1.5 Cross-Level Capstone Project Inventory
Across the entire repository, 5 distinct capstone projects were mapped:
1. **Level 1 (`python-data-tools/capstone/`)**: *Industrial Equipment Reliability & Predictive Maintenance* (6 machines, sensor logs: temperature, vibration, voltage; tabular cleaning with Pandas, NumPy statistics, Matplotlib multi-panel dashboard, 100-point rubric).
2. **Level 2 (`engineering-mathematics/capstone/`)**: *Electric Vehicle Powertrain Telemetry Analysis* (multi-physics electromechanical conversion, numerical integration `trapz`, numerical differentiation `diff`, Gaussian noise filtering, 100-point rubric, paired starter and solution).
3. **Level 3/4 (`machine-learning/12_capstone/`)**: *Meridian Industrial Predictive Failure Detection System* (8 sensor features, RUL regression, fault severity classification: OK/WARNING/FAULT, 200-point rubric, starter template; missing reference solution).
4. **Level 4/5 (`neat/capstone/`)**: *Autonomous Lunar Lander Controller* (OpenAI Gymnasium LunarLander-v3, 8 inputs, 4 discrete actions, fitness accumulation; starter template; missing reference solution).
5. **Level 6/7 (`game-ai/capstone/`)**: *Othello (Reversi) AI* (8x8 board representation, Pygame UI, depth-limited Alpha-Beta search with Piece-Square Table heuristics; starter template; missing reference solution).

---

## 2. Logic Chain

1. **Premise:** The dispatch requires mapping Levels 5, 6, and 7, any cross-level projects, and global curriculum specifications.
2. **Evidence 1 (Conflicting Taxonomies):**
   - In `machine-learning/README.md` (lines 12–18), the curriculum is described as a 4-level sequence (Level 1: Python Data Tools, Level 2: Engineering Mathematics, Level 3: Machine Learning, Level 4: Deep Learning), followed by Next Steps (MLOps, Deployment).
   - In `generate_audit_report.py` (lines 27–90), the taxonomy explicitly defines 7 levels (L1: Data Tools, L2: Eng Math, L3: ML, L3.5: ml-course, L4: NEAT, L5: Deep Learning, L6: Networking, L7: Game AI).
   - In `.agents/teamwork_preview_orchestrator_2/plan.md` (lines 21–27), the batch audit schedule maps Batch 4 to DL, Batch 5 to Specialized Topics/MLOps/Systems, and Batch 6 to Levels 6 & 7 Capstones, Advanced Research & Projects.
3. **Inference 1:** Because downstream audit batches and milestones rely on both taxonomies, our handoff must explicitly cross-reference the components under both structural frameworks to avoid scope collisions between survey batches.
4. **Evidence 2 (Level 5 / Deep Learning & NEAT Content):**
   - Deep Learning modules 07, 08, 10, and 11 contain substantial runnable code and exercises (~9KB to ~19KB per lesson).
   - Module 09 has a severe internal mismatch: `02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, and `05_deep_mlp_project.py` are advertised in `README.md` but do not exist; only `01_activation_functions.py` and `02_backpropagation_and_deep_mlp.py` exist.
   - NEAT (`neat/`) contains functional tutorials for XOR and CartPole (`05_xor` and `06_pole_balancing`), but modules `01`, `02`, and `03` have empty `exercises/` and `examples/` subdirectories.
5. **Evidence 3 (Level 6 / Networking & MLOps Absence):**
   - `generate_audit_report.py` hardcodes `TCP/IP`, `HTTP/HTTPS`, and `REST APIs` as `"MISSING"`.
   - Direct filesystem searches across the entire workspace yielded zero networking or MLOps files.
6. **Inference 2:** Level 6 is currently a complete phantom in the repository. If the curriculum intention is a 7-level pipeline including networking and MLOps, this represents a P0 curricular void.
7. **Evidence 4 (Level 7 / Game AI Code vs Theory Gap):**
   - Modules 01, 03, 04, 05, 07, and 09 have runnable code implementations.
   - Modules 02, 06, 08, 10, 11, and 12 are purely markdown theory files. Specifically, Checkers (`08_checkers`) explicitly admits skipping the engine, while MCTS (`10_mcts`), Reinforcement Learning (`11_reinforcement_learning`), and Neural Game AI (`12_neural_game_ai`) provide zero code implementations.
   - Directories `game-ai/games/` and `game-ai/projects/` are completely empty.
8. **Evidence 5 (Decoupled Solution Contract Violations):**
   - `PROJECT.md` establishes the interface contract that every exercise template and capstone must have a paired, decoupled solution with zero remaining `% TODO` markers.
   - In `machine-learning/12_capstone`, `neat/capstone`, and `game-ai/capstone`, starter files contain unresolved `TODO` / `pass` markers, but no corresponding reference solutions exist in `solutions/`.

---

## 3. Caveats

1. **Excluded Directory:** The directory `/home/settings/Documents/pearl/hshs` was inspected and verified to be an unrelated Flutter mobile application template (`pubspec.yaml`, Android/iOS/Web wrappers) with no connection to the Python/MATLAB educational curriculum. It was excluded from further curriculum indexing.
2. **Scratch Files:** Root files `a.py` (CLI to-do list), `lesson3.py` (0 bytes), `panda.py` (0 bytes), and `pearl.cpp` (20 lines of C++ syntax practice) are ad-hoc scratch scripts and do not form part of the structured curriculum packages.
3. **No Automated Scripts Used:** Adhering strictly to the Non-Negotiable Inspection Protocol, all findings were derived from direct manual tool inspection (`list_dir`, `view_file`, `grep_search`, `find_by_name`). No automated scanning scripts (`audit.py`, custom ast analyzers) were executed.

---

## 4. Conclusion

1. **Curriculum Completeness Assessment for Levels 5, 6, & 7:**
   - **Level 5 (Deep Learning / NEAT):** **PARTIAL**. Strong foundational code exists in PyTorch (Tensors, Autograd, Module, Optimizers, CNNs, Transformers, XOR, CartPole), but Module 09 has 5 missing files advertised in its README, NEAT has 5 empty exercise/example folders, and TensorFlow is omitted.
   - **Level 6 (Networking & MLOps):** **MISSING (100% GAP)**. Zero instructional files, scripts, or exercises exist for TCP/IP, HTTP/HTTPS, REST APIs (FastAPI), or MLOps (Docker, MLflow).
   - **Level 7 (Game AI):** **PARTIAL (Severe Theory-to-Code Asymmetry)**. Modules 01–05, 07, and 09 are implemented, but Modules 02, 06, 08, 10, 11, and 12 lack code. In particular, modern Game AI topics (MCTS, RL, AlphaZero-style Neural Game AI) exist solely as introductory essays without runnable code, and `games/` and `projects/` directories are empty.
2. **Capstone Integration:** All 5 levels have rich capstone specifications and starter templates, but Levels 3/4, 4/5, and 6/7 lack reference solutions, violating the repository's decoupled solution contract.
3. **Actionable Recommendations for Master TODO List:**
   - **P0:** Implement missing Level 6 Networking & REST API curriculum module (`networking/` or `mlops/`).
   - **P0:** Implement reference solutions for the three uncompleted capstones: `machine-learning/solutions/capstone_solution.py`, `neat/solutions/capstone_solution.py`, and `game-ai/solutions/reversi_capstone_solution.py`.
   - **P1:** Fulfill advertised files in `machine-learning/09_neural_networks/` (`02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`).
   - **P1:** Implement concrete code examples for Game AI Modules 10 (MCTS), 11 (Q-Learning / RL), and 12 (PyTorch Value/Policy Network + Minimax integration).
   - **P2:** Populate empty exercise directories in `neat/01`, `neat/02`, and `neat/03`.

---

## 5. Verification Method

To independently verify these findings:
1. **Verify Missing Files in `machine-learning/09_neural_networks/`:**
   Inspect `machine-learning/09_neural_networks/README.md` lines 117–125 and compare against directory listing of `machine-learning/09_neural_networks/`. Note absence of `02_weight_initialization.py`, `03_batch_normalization.py`, `04_dropout.py`, and `05_deep_mlp_project.py`.
2. **Verify Missing Level 6 Networking Modules:**
   Inspect `generate_audit_report.py` lines 72–76. Run `find_by_name` for `tcp`, `http`, `network`, `fastapi` in the repository root to confirm zero matches.
3. **Verify Game AI Markdown-Only Modules:**
   Inspect `game-ai/08_checkers/README.md` (line 26), `game-ai/10_mcts/`, `game-ai/11_reinforcement_learning/`, and `game-ai/12_neural_game_ai/` to confirm that each contains only a `README.md` and no `.py` scripts.
4. **Verify Missing Capstone Reference Solutions:**
   Inspect `machine-learning/solutions/`, `neat/solutions/`, and `game-ai/solutions/` to confirm absence of capstone solutions.
5. **Invalidation Conditions:**
   This report would be invalidated if any `.py` implementations for TCP/IP, MCTS, or Checkers are discovered in unexpected non-standard directories outside their respective package roots.

---

## 6. Mandatory Reading Record

Every file path opened and manually read during this survey (67 files total):

```text
1.  /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md
2.  /home/settings/Documents/pearl/README.md
3.  /home/settings/Documents/pearl/TEST_INFRA.md
4.  /home/settings/Documents/pearl/TEST_READY.md
5.  /home/settings/Documents/pearl/.agents/PROJECT.md
6.  /home/settings/Documents/pearl/ml-course/README.md
7.  /home/settings/Documents/pearl/machine-learning/README.md
8.  /home/settings/Documents/pearl/generate_audit_report.py
9.  /home/settings/Documents/pearl/full_audit.py
10. /home/settings/Documents/pearl/check_files.py
11. /home/settings/Documents/pearl/list_files.py
12. /home/settings/Documents/pearl/.agents/survey_explorer_1/DISPATCH.md
13. /home/settings/Documents/pearl/.agents/survey_explorer_2/DISPATCH.md
14. /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_2/plan.md
15. /home/settings/Documents/pearl/game-ai/README.md
16. /home/settings/Documents/pearl/neat/README.md
17. /home/settings/Documents/pearl/hshs/README.md
18. /home/settings/Documents/pearl/pearl.cpp
19. /home/settings/Documents/pearl/a.py
20. /home/settings/Documents/pearl/lesson3.py
21. /home/settings/Documents/pearl/panda.py
22. /home/settings/Documents/pearl/game-ai/01_pygame/README.md
23. /home/settings/Documents/pearl/game-ai/01_pygame/01_basics.py
24. /home/settings/Documents/pearl/game-ai/02_game_state/README.md
25. /home/settings/Documents/pearl/game-ai/03_tic_tac_toe/README.md
26. /home/settings/Documents/pearl/game-ai/04_minimax/README.md
27. /home/settings/Documents/pearl/game-ai/05_alpha_beta/README.md
28. /home/settings/Documents/pearl/game-ai/06_heuristics/README.md
29. /home/settings/Documents/pearl/game-ai/07_connect_four/connect_four.py
30. /home/settings/Documents/pearl/game-ai/08_checkers/README.md
31. /home/settings/Documents/pearl/game-ai/09_chess/README.md
32. /home/settings/Documents/pearl/game-ai/10_mcts/README.md
33. /home/settings/Documents/pearl/game-ai/11_reinforcement_learning/README.md
34. /home/settings/Documents/pearl/game-ai/12_neural_game_ai/README.md
35. /home/settings/Documents/pearl/game-ai/capstone/README.md
36. /home/settings/Documents/pearl/game-ai/exercises/FINAL_ASSESSMENT.md
37. /home/settings/Documents/pearl/game-ai/reference/GAME_AI_CHEAT_SHEET.md
38. /home/settings/Documents/pearl/game-ai/solutions/debugging_solutions.py
39. /home/settings/Documents/pearl/game-ai/exercises/debugging.py
40. /home/settings/Documents/pearl/game-ai/requirements.txt
41. /home/settings/Documents/pearl/game-ai/09_chess/chess_ai.py
42. /home/settings/Documents/pearl/game-ai/capstone/reversi_starter.py
43. /home/settings/Documents/pearl/neat/01_evolutionary_computation/README.md
44. /home/settings/Documents/pearl/neat/02_genetic_algorithms/README.md
45. /home/settings/Documents/pearl/neat/03_neat_fundamentals/README.md
46. /home/settings/Documents/pearl/neat/04_neat_python/README.md
47. /home/settings/Documents/pearl/neat/05_xor/README.md
48. /home/settings/Documents/pearl/neat/06_pole_balancing/README.md
49. /home/settings/Documents/pearl/neat/assessment/FINAL_ASSESSMENT.md
50. /home/settings/Documents/pearl/neat/capstone/README.md
51. /home/settings/Documents/pearl/neat/capstone/starter.py
52. /home/settings/Documents/pearl/neat/exercises/01_debugging.py
53. /home/settings/Documents/pearl/neat/reference/NEAT_CHEAT_SHEET.md
54. /home/settings/Documents/pearl/neat/solutions/01_debugging_solution.py
55. /home/settings/Documents/pearl/machine-learning/07_deep_learning_intro/README.md
56. /home/settings/Documents/pearl/machine-learning/08_pytorch_fundamentals/README.md
57. /home/settings/Documents/pearl/machine-learning/09_neural_networks/README.md
58. /home/settings/Documents/pearl/machine-learning/10_cnns/README.md
59. /home/settings/Documents/pearl/machine-learning/11_transformers/README.md
60. /home/settings/Documents/pearl/machine-learning/12_capstone/README.md
61. /home/settings/Documents/pearl/machine-learning/assessment/FINAL_ASSESSMENT.md
62. /home/settings/Documents/pearl/machine-learning/assessment/practical_test.py
63. /home/settings/Documents/pearl/machine-learning/reference/pytorch_cheat_sheet.md
64. /home/settings/Documents/pearl/python-data-tools/capstone/README.md
65. /home/settings/Documents/pearl/engineering-mathematics/capstone/README.md
66. /home/settings/Documents/pearl/pan.md
67. /home/settings/Documents/pearl/pans.md
```
