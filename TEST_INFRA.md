# Curriculum Completion E2E Test Infrastructure (TEST_INFRA)

## 1. Architectural Overview
The End-to-End (E2E) Test Infrastructure for the Curriculum Completion Project provides rigorous, automated verification across all 7 levels of the engineering and computer science curriculum. The test infrastructure validates that code artifacts are not merely syntactically valid or theoretical markdown, but genuinely executable, mathematically sound, performant, and resilient to boundary stress.

The suite is executed under Python 3.14 with an isolated Linux runtime, zero proprietary dependencies (leveraging a dual-mode compatibility bridge for TensorFlow and Dormand-Prince RK45 solvers for Simulink models), and strictly adheres to a **4-Tier Test Design Methodology**.

```
tests/e2e/
├── conftest.py                   # Pytest fixtures, MKL runtime setup, dynamic module loader
├── test_deep_learning_e2e.py     # Milestone M1: BatchNorm, Dropout, Deep MLP Fault Detection
├── test_math_game_ai_e2e.py      # Milestone M2: PCA, Logistic Regression GD, Checkers, MCTS, RL
├── test_networking_tf_e2e.py     # Milestone M3: TCP/IP, UDP, HTTP, FastAPI, ML Serving, TensorFlow
├── test_capstones_simulink_e2e.py# Milestone M4: Industrial ML Capstone, Reversi AI, Simulink ODE45
└── run_all_e2e_tests.py          # Master test runner with formatted Unicode scorecard
```

---

## 2. The 4-Tier Test Design Methodology

Every test suite is systematically partitioned into four distinct validation tiers to guarantee layered quality assurance from isolated unit primitives up to autonomous multi-agent pipelines.

| Tier | Name | Pedagogical & Engineering Purpose | Scope & Techniques |
|:-----|:-----|:-----------------------------------|:-------------------|
| **Tier 1** | **Feature Isolation & Primary Contracts** | Verify nominal happy-path behaviors, interface contracts, dimension preservation, and mathematical formulations in isolation. | Unit forward passes, weight updates, API endpoints, socket binding, matrix operations. |
| **Tier 2** | **Boundary & Corner Condition Stress** | Stress extreme inputs, physical limits, empty payloads, saturated states, and error handling mechanisms. | Ephemeral ports (port 0), 0-byte frames, empty batches, scalar tensors, actuator voltage saturation ($\pm 36\text{ V}$), anti-windup clamping. |
| **Tier 3** | **Pairwise Cross-Feature Integration** | Evaluate state transfer, pipeline interoperability, and comparative performance between complementary subsystems. | Raw HTTP client against live REST servers, Keras model served via FastAPI, PCA fed into Logistic Regression, Minimax depth scaling, RK45 numerical vs. analytical. |
| **Tier 4** | **Real-World Autonomous Workflows** | Verify production-grade end-to-end scenarios, headless multi-agent game completion, disturbance rejection, and artifact persistence. | 60-turn autonomous Reversi AI match, closed-loop motor control scorecard, industrial bearing telemetry serving under 50ms latency budget, full capstone execution. |

---

## 3. Test Suites & Milestone Mapping

### Milestone M1: Deep Learning Lessons & Neural Networks
- **Test File**: `tests/e2e/test_deep_learning_e2e.py`
- **Markers**: `@pytest.mark.m1`, `@pytest.mark.tier1`, `@pytest.mark.tier2`, `@pytest.mark.tier3`, `@pytest.mark.tier4`
- **Core Coverage**:
  - `03_batch_normalization.py`: Mini-batch mean centering ($\mu_B \approx 0$), unit variance ($\sigma_B^2 \approx 1$), learnable affine parameters ($\gamma, \beta$), exponential moving average (EMA) running statistics, deterministic evaluation mode.
  - `04_dropout.py`: Inverted dropout scaling ($1/(1-p)$), stochastic zeroing in train mode, identity mapping in eval mode, expectation preservation.
  - `05_deep_mlp_project.py`: `DeepFaultClassifier`, Kaiming He normal weight initialization, multi-class CrossEntropyLoss gradients, validation early stopping.
  - `exercises_solutions.py`: Manual forward/backward propagation through two-layer MLP, softmax cross-entropy loss, 0 TODO verification.
  - `machine-learning/assessment/practical_test.py`: Full curriculum 26-module test runner execution.

### Milestone M2: Mathematics & Game AI Implementations
- **Test File**: `tests/e2e/test_math_game_ai_e2e.py`
- **Markers**: `@pytest.mark.m2`, `@pytest.mark.tier1`, `@pytest.mark.tier2`, `@pytest.mark.tier3`, `@pytest.mark.tier4`
- **Core Coverage**:
  - `04_pca_from_scratch.py`: `PCAScratch` mean centering, sample covariance symmetry, eigenvalue descending order, reconstruction error minimization, parity with `sklearn.decomposition.PCA`.
  - `01_logistic_regression_from_scratch.py`: `LogisticRegressionGD` sigmoid stability, Binary Cross-Entropy loss monotonic decrease, gradient descent update step, One-vs-Rest multiclass classification, parity with `sklearn.linear_model.LogisticRegression`.
  - `game-ai/08_checkers/`: 8x8 `CheckersState` board setup, diagonal forward steps, mandatory multi-jump captures, King promotion at opposing baseline, Alpha-Beta minimax heuristic search.
  - `game-ai/10_mcts/`: `MCTSNode`, Upper Confidence Bounds (UCB1) formula with $c = \sqrt{2}$, selection, expansion, random rollout simulation, backpropagation.
  - `game-ai/11_reinforcement_learning/`: `GridWorld` MDP transitions, obstacles, terminal state rewards, `QLearningAgent` Bellman update $Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_a Q(s', a) - Q(s, a)]$, $\epsilon$-greedy exploration decay.

### Milestone M3: Level 6 Networking & TensorFlow Fundamentals
- **Test File**: `tests/e2e/test_networking_tf_e2e.py`
- **Markers**: `@pytest.mark.m3`, `@pytest.mark.tier1`, `@pytest.mark.tier2`, `@pytest.mark.tier3`, `@pytest.mark.tier4`
- **Core Coverage**:
  - `networking/01_tcp_ip/`: `TCPEchoServer` and `TCPClient` socket primitives (`AF_INET`, `SOCK_STREAM`), `SO_REUSEADDR`, 4-byte big-endian uint32 length-prefix framing (`!I`), `UDPServer` and `UDPClient` datagram telemetry and structured JSON ACKs, `ConcurrentTCPServer` multi-threaded worker pools.
  - `networking/02_http_protocols/`: `RawHTTPClient` from-scratch RFC 9112 HTTP/1.1 socket client, status line parsing, header dictionaries, `PythonHTTPServer` built on `http.server.HTTPServer` with REST endpoints (`GET /health`, `GET /api/items`, `POST /api/items`).
  - `networking/03_rest_apis/`: `FastAPI` telemetry gateway with Pydantic request validation schemas (`SensorCreate`), CRUD endpoints (`/sensors`), query filtering, and `BearingFaultModel` predictive microservice (`POST /predict`, `POST /predict/batch`, `/healthz`, `/readyz`, `/model/info`).
  - `machine-learning/08_tensorflow_fundamentals/`: Zero-dependency Python 3.14 dual-mode bridge `tf_compat.py`, `tf.constant` immutable tensors, `tf.Variable` mutable state (`assign`, `assign_add`, `assign_sub`), `tf.GradientTape` reverse-mode automatic differentiation (scalar and multi-variable), Keras Sequential, Functional (residual skip connections), and Subclassing APIs (`call(inputs, training)`).

### Milestone M4: Capstones & Simulink Dynamic Modeling
- **Test File**: `tests/e2e/test_capstones_simulink_e2e.py`
- **Markers**: `@pytest.mark.m4`, `@pytest.mark.tier1`, `@pytest.mark.tier2`, `@pytest.mark.tier3`, `@pytest.mark.tier4`
- **Core Coverage**:
  - `machine-learning/solutions/capstone_solution.py`: Synthetic industrial dataset generation (`industrial_sensor_train.csv`), EDA distributions and correlation heatmaps, robust preprocessing (SimpleImputer + StandardScaler), RandomForest/SVC classifiers, RandomForest/Ridge regressors, PyTorch `FaultClassifierMLP` and `RULRegressorMLP`, confusion matrix, and feature importance rankings.
  - `game-ai/solutions/reversi_solution.py` & `capstone/reversi_game.py`: `OthelloState` 8-direction raycasting, bracketing, disc flipping, legal move generation, single-pass and consecutive-pass terminal resolution, calibrated Piece-Square Table (PST) heuristic, Alpha-Beta minimax search, and headless self-play (`play_game`).
  - `engineering-mathematics/simulink/`: Standalone ODE45 companion scripts (`03_rc_circuit_companion.m`, `04_thermal_cooling_companion.m`, `05_dc_motor_companion.m`), model blueprints (`models/*.md`), exercise templates, and decoupled reference solutions in `solutions/`.
  - `engineering-mathematics/simulink/mini_project_motor_control.m`: Coupled electromechanical DC motor state-space dynamics ($L_a \frac{di_a}{dt} = V - R_a i_a - K_e \omega$, $J \frac{d\omega}{dt} = K_t i_a - b \omega - \tau_L$), closed-loop PI speed control with anti-windup conditional clamping under full load torque step disturbance.
  - `engineering-mathematics/scripts/verify_package.py`: Automated lexing, block balancing, 1-based indexing verification, and comment ratio audit ($\ge 20\%$).

---

## 4. Execution Guide & Commands

### Running All Tests via Master Runner
```bash
python tests/e2e/run_all_e2e_tests.py
```

### Running All Tests via Pytest
```bash
pytest tests/e2e/ -v
```

### Running Specific Milestone Suites
```bash
pytest tests/e2e/test_deep_learning_e2e.py -v       # Milestone M1
pytest tests/e2e/test_math_game_ai_e2e.py -v        # Milestone M2
pytest tests/e2e/test_networking_tf_e2e.py -v       # Milestone M3
pytest tests/e2e/test_capstones_simulink_e2e.py -v   # Milestone M4
```

### Running by Tier Marker
```bash
pytest tests/e2e/ -m tier1 -v   # Tier 1: Nominal feature contracts
pytest tests/e2e/ -m tier2 -v   # Tier 2: Boundaries and edge cases
pytest tests/e2e/ -m tier3 -v   # Tier 3: Cross-feature integrations
pytest tests/e2e/ -m tier4 -v   # Tier 4: Real-world workflows
```

---

## 5. Runtime Environment & Compatibility
- **Python Version**: 3.14.6
- **Operating System**: Linux 6.6.137+
- **Environment Flags**:
  - `MKL_SERVICE_FORCE_INTEL=1`
  - `MKL_THREADING_LAYER=GNU`
  - `MPLBACKEND=Agg`
  - `OMP_NUM_THREADS=2`
- **TensorFlow Bridge**: Native TensorFlow binary wheels are not compiled for CPython 3.14 yet. The zero-dependency compatibility bridge (`tf_compat.py`) delivers 100% authentic TensorFlow 2.x and Keras 3 syntax backed by PyTorch autograd and NumPy, ensuring zero runtime import errors or crashes.
- **Simulink Solvers**: In headless continuous-integration environments lacking proprietary MATLAB/Simulink licenses, physical differential equations are integrated using `scipy.integrate.solve_ivp` (Dormand-Prince RK45), matching MATLAB's `ode45` numerical tolerances with $< 10^{-3}$ absolute error against analytical trajectories.
