# Project: Curriculum Completion (Deep Learning, Math/Game AI, Networking/TF, Capstones/Simulink)

## Architecture
The repository `/home/settings/Documents/pearl` delivers an end-to-end computer science and engineering curriculum spanning 7 levels:
- **Level 1 (`python-data-tools`)**: Python data science fundamentals (NumPy, Pandas, Matplotlib).
- **Level 2 (`engineering-mathematics`)**: MATLAB, Linear Algebra, Calculus, Probability, and Simulink dynamic system modeling.
- **Level 3 & 4/5 (`machine-learning`)**: Classical ML, PyTorch Deep Learning, Neural Networks, CNNs, Transformers, TensorFlow.
- **Level 4 (`neat`)**: NeuroEvolution of Augmenting Topologies.
- **Level 6 (`networking`)**: Computer networking fundamentals (TCP/IP, HTTP protocols, REST APIs with FastAPI).
- **Level 7 (`game-ai`)**: Game algorithms (Minimax, Alpha-Beta, Connect Four, Checkers, MCTS, Tabular Q-Learning, Reversi Capstone).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | `03_batch_normalization.py` | Internal covariate shift, mathematical formulation ($\mu_B, \sigma_B^2, \gamma, \beta$), running mean/var, train vs eval modes, deep MLP comparison experiment, `output/batchnorm_effect.png`. | M1 | R1 |
| 2 | `04_dropout.py` | Co-adaptation prevention, inverted dropout ($1/(1-p)$ scaling), ensemble interpretation, train vs eval modes, overfitting regularization experiment, `output/dropout_effect.png`. | M1 | R1 |
| 3 | `05_deep_mlp_project.py` | Industrial fault detection project combining BatchNorm, Dropout, Kaiming init, training loop with validation early stopping, `output/training_curves.png`, `output/confusion_matrix.png`. | M1 | R1 |
| 4 | Deep Learning Exercise Solutions | Reference solutions for `09_neural_networks/exercises.py` in `exercises_solutions.py` and `machine-learning/solutions/`. | M1 | R1, R4 |
| 5 | NumPy PCA from scratch | Complete manual PCA (`PCAScratch`): mean-centering, covariance matrix $\Sigma$, eigendecomposition `np.linalg.eigh`, SVD equivalence, explained variance, projection $Z = \tilde{X}W$, reconstruction $\hat{X}$, unit test against sklearn. | M2 | R2 |
| 6 | NumPy Logistic Regression GD | Complete manual Logistic Regression (`LogisticRegressionGD`): sigmoid with clipping, BCE loss, analytical gradients $\nabla_w J, \nabla_b J$, gradient descent update loop, One-vs-Rest multiclass. | M2 | R2 |
| 7 | Checkers Game Engine & AI | Complete 8x8 Checkers engine (`CheckersState`): diagonal steps, forced capture jumps, recursive multi-jump expansion, King promotion, depth-limited Alpha-Beta search with heuristic, CLI/playable loop. | M2 | R2 |
| 8 | Monte Carlo Tree Search (MCTS) | Complete MCTS implementation (`MCTSNode`, `MCTS`): UCB1 formula, selection, expansion, random simulation/rollout, backpropagation, integration with TicTacToe/ConnectFour. | M2 | R2 |
| 9 | Reinforcement Learning (RL) | Complete Tabular Q-Learning (`GridWorld`, `QLearningAgent`): MDP gridworld, $\epsilon$-greedy action selection, Bellman updates, training loop, policy extraction, `output/q_learning_training.png`. | M2 | R2 |
| 10 | Level 6 TCP/IP Module | `networking/01_tcp_ip/`: TCP server/client, UDP sockets, multi-client concurrent server, 4-tier exercises, complete README. | M3 | R3 |
| 11 | Level 6 HTTP Module | `networking/02_http_protocols/`: raw socket HTTP client, Python `http.server`, `requests` & `httpx` clients, 4-tier exercises, complete README. | M3 | R3 |
| 12 | Level 6 REST APIs Module | `networking/03_rest_apis/`: REST constraints, FastAPI endpoints, Pydantic schemas, ML model serving endpoint, 4-tier exercises, complete README. | M3 | R3 |
| 13 | Level 6 Reference Solutions & Tests | `networking/solutions/` (tcp, http, rest solutions) and `networking/tests/` (automated structure & execution tests). | M3 | R3 |
| 14 | TensorFlow Curriculum Module | `machine-learning/08_tensorflow_fundamentals/`: `tf_compat.py` (Python 3.14 compatible dual-mode shim), 6 lesson scripts, 4-tier exercises, reference solutions, Rosetta Stone PyTorch vs TF comparison. | M3 | R3 |
| 15 | ML Capstone Reference Solution | `machine-learning/solutions/capstone_solution.py`: complete worked solution for `12_capstone/starter_template.py` (EDA plots, preprocessing, RF/SVC classification, RF/Ridge regression, PyTorch MLPs, comparison table, engineering interpretation). | M4 | R4 |
| 16 | Reversi Game AI Capstone Solution | `game-ai/solutions/reversi_solution.py` & `game-ai/capstone/reversi_game.py`: complete `OthelloState` (8-direction flips, pass handling, terminal detection), PST heuristic, Alpha-Beta minimax, Pygame UI & headless self-play. | M4 | R4 |
| 17 | Simulink Companion Scripts | `engineering-mathematics/simulink/`: `03_rc_circuit_companion.m`, `04_thermal_cooling_companion.m`, `05_dc_motor_companion.m` with standalone ODE45 simulations. | M4 | R4 |
| 18 | Motor Control Mini-Project | `engineering-mathematics/simulink/mini_project_motor_control.m`: closed-loop PI speed control with anti-windup clamping, load torque step rejection, transient metrics scorecard. | M4 | R4 |
| 19 | Simulink Blueprints & Exercises | `models/thermal_cooling_model.md`, `models/dc_motor_model.md`, `exercises.m`, and decoupled reference solutions in `engineering-mathematics/solutions/`. | M4 | R4 |
| 20 | E2E Test Suite & Verification | Requirements-driven E2E tests validating syntax, runtime, and outputs across all modules; publish `TEST_READY.md`. | M5 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Deep Learning Lessons Fix | Features 1, 2, 3, 4 (`machine-learning/09_neural_networks/`) | none | DONE |
| M2 | Math & Game AI Implementations | Features 5, 6, 7, 8, 9 (`machine-learning/`, `game-ai/`) | none | DONE |
| M3 | Networking & TensorFlow Curricula | Features 10, 11, 12, 13, 14 (`networking/`, `machine-learning/08_tensorflow_fundamentals/`) | none | DONE |
| M4 | Capstones, Solutions & Engineering Math | Features 15, 16, 17, 18, 19 (`machine-learning/`, `game-ai/`, `engineering-mathematics/`) | none | DONE |
| M5 | E2E Testing Track | Feature 20: Comprehensive E2E test suite across all 4 areas, publish `TEST_READY.md` | none (runs in parallel) | DONE |
| M6 | Final Verification & Hardening | Run 100% E2E tests, verify all outputs and acceptance criteria | M1, M2, M3, M4, M5 | IN_PROGRESS |

## Interface Contracts

### M1 (Deep Learning) ↔ Assessment
- Files: `03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`
- Headless execution: `matplotlib.use('Agg')`
- Output artifacts: `output/batchnorm_effect.png`, `output/dropout_effect.png`, `output/confusion_matrix.png`, `output/training_curves.png`
- Return / Exit Code: 0 on successful run

### M2 (Math & Game AI) ↔ Assessment
- `PCAScratch`: `fit(X)`, `transform(X)`, `inverse_transform(Z)`, `components_`, `explained_variance_ratio_`
- `LogisticRegressionGD`: `fit(X, y)`, `predict(X)`, `predict_proba(X)`, `coef_`, `intercept_`
- `CheckersState`: `get_legal_moves()`, `make_move(move)`, `is_terminal`, `winner`
- `MCTS`: `get_best_move(state, num_simulations=1000)`
- `GridWorld`: `reset()`, `step(action)` returning `(next_state, reward, done, info)`
- `QLearningAgent`: `choose_action(state)`, `update(state, action, reward, next_state, done)`

### M3 (Networking & TensorFlow) ↔ Assessment
- Networking: Ephemeral ports (port 0) for socket and HTTP server tests to prevent address conflicts.
- FastAPI endpoints: Testable via `starlette.testclient.TestClient(app)` without socket binding.
- TensorFlow: Dual-mode `tf_compat.py` fallback bridge ensuring 100% runnable under Python 3.14 without binary wheel errors.

### M4 (Capstones & Simulink) ↔ Assessment
- `capstone_solution.py`: Self-contained, generates dataset if absent, trains models, outputs figures to `12_capstone/output/`.
- `reversi_solution.py`: Supports `play_game(ai_depth=2)` headlessly returning `(winner, scores)`.
- MATLAB `.m` scripts: Pure MATLAB syntax, ODE45 solvers, 1-based indexing, comment ratio >= 20%, matching `verify_package.py` assertions.

## Code Layout & Write Boundaries

| Milestone | Exclusive Owned Write Paths |
|:---|:---|
| **M1** | `machine-learning/09_neural_networks/03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`, `exercises_solutions.py`, `machine-learning/assessment/practical_test.py` |
| **M2** | `machine-learning/05_clustering/04_dimensionality_reduction.py` (or PCA scratch companion), `machine-learning/04_classification/01_logistic_regression.py` (or GD scratch companion), `game-ai/08_checkers/`, `game-ai/10_mcts/`, `game-ai/11_reinforcement_learning/` |
| **M3** | `networking/`, `machine-learning/08_tensorflow_fundamentals/`, `machine-learning/solutions/tensorflow_fundamentals_solutions.py` |
| **M4** | `machine-learning/solutions/capstone_solution.py`, `game-ai/solutions/reversi_solution.py`, `game-ai/capstone/`, `engineering-mathematics/simulink/`, `engineering-mathematics/solutions/` |
| **M5 (Test Track)** | `tests/e2e/`, `TEST_READY.md` |
