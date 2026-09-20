# Comprehensive Survey Report: R4 Capstones, Reference Solutions, and Simulink / Motor Control

**Surveyor Identity:** `teamwork_preview_explorer_survey_3`  
**Date:** 2026-09-17  
**Working Directory:** `/home/settings/Documents/pearl/.agents/teamwork_preview_explorer_survey_3`  
**Target Areas:**
1. R4 Capstones & Reference Solutions: Machine Learning Capstone, Deep Learning Capstone/Project, Reversi/Othello Game AI Capstone.
2. R4 Simulink Companion Scripts & Motor Control Project: `engineering-mathematics/simulink/` and associated solution files.

---

## 1. Observation

### 1.1 Machine Learning & Deep Learning Capstone / Solutions
* **ML Capstone Directory:** `/home/settings/Documents/pearl/machine-learning/12_capstone/`
  * Existing files:
    * `README.md` (6,505 bytes)
    * `generate_capstone_data.py` (9,557 bytes)
    * `starter_template.py` (10,873 bytes, 295 lines)
  * Missing files:
    * `machine-learning/solutions/capstone_solution.py` is **completely missing**.
    * Line 161 of `machine-learning/12_capstone/README.md` explicitly references:
      ```bash
      # (Do NOT look at solutions/capstone_solution.py until you submit)
      ```
    * Lines 123–133 of `machine-learning/README.md` declare the expected solution manifest:
      ```text
      ├── solutions/
      │   ├── ml_fundamentals_solutions.py
      │   ├── sklearn_solutions.py
      │   ├── regression_solutions.py
      │   ├── classification_solutions.py
      │   ├── clustering_solutions.py
      │   ├── model_evaluation_solutions.py
      │   ├── pytorch_solutions.py
      │   ├── advanced_dl_solutions.py
      │   └── capstone_solution.py
      ```
    * Actual contents of `machine-learning/solutions/`:
      * `ml_fundamentals_solutions.py` (6,173 bytes)
      * `sklearn_regression_clustering_solutions.py` (11,020 bytes)
      * `pytorch_neural_net_solutions.py` (10,509 bytes)
      * `output/` directory
      * `capstone_solution.py` is absent.
  * Capstone Requirements in `starter_template.py`:
    * Generates `datasets/industrial_sensor_train.csv` (1000 rows) and `datasets/industrial_sensor_test.csv` (200 rows) via `generate_capstone_data.py`.
    * Features (8 channels): `temperature`, `vibration`, `pressure`, `current`, `rpm`, `humidity`, `voltage`, `acoustic_emission`.
    * Dual prediction targets:
      1. Multiclass Classification: `fault_severity` (0=OK, 1=WARNING, 2=FAULT).
      2. Regression: `remaining_useful_life` (0–500 hours).
    * Section 1: Data Exploration (statistics, class distribution, histograms to `output/eda_distributions.png`, correlation heatmap to `output/eda_correlation.png`).
    * Section 2: Preprocessing (median imputation, `StandardScaler` fitted on train only, 80/20 train/validation stratified split).
    * Section 3: Classical ML (`RandomForestClassifier`, 2nd classifier e.g. `SVC`, 5-fold CV, accuracy, macro & per-class F1, confusion matrix; `RandomForestRegressor`, 2nd regressor e.g. `Ridge` / `GradientBoostingRegressor`, $R^2$, RMSE; feature importance plot to `output/feature_importance.png`).
    * Section 4: Deep Learning MLP (`FaultClassifierMLP` with $\ge 2$ hidden layers, ReLU activations, `CrossEntropyLoss`, Adam optimizer, loss curve plot; Regression MLP with `MSELoss`; comparison between PyTorch MLP and Random Forest).
    * Section 5: Evaluation & Comparison (summary comparison table, confusion matrix plot to `output/confusion_matrix.png`).
    * Section 6: Engineering Interpretation (critical sensor insights, fault pattern signatures, maintenance thresholds, deployment constraints).

### 1.2 Deep Learning Flagship Project & Exercises
* **Deep Learning Module 9 Directory:** `/home/settings/Documents/pearl/machine-learning/09_neural_networks/`
  * Existing files:
    * `01_activation_functions.py` (8,414 bytes)
    * `02_backpropagation_and_deep_mlp.py` (9,345 bytes)
    * `README.md` (5,012 bytes)
    * `exercises.py` (8,688 bytes)
    * `output/` directory
  * Missing files:
    * `03_batch_normalization.py` (missing; tracked under R1)
    * `04_dropout.py` (missing; tracked under R1)
    * `05_deep_mlp_project.py` (missing; referenced in Module 9 `README.md` lines 123 & 138, and required by `ORIGINAL_REQUEST.md` line 106).
    * `exercises_solutions.py` (missing; referenced in Module 9 `README.md` line 125).
  * `machine-learning/solutions/pytorch_neural_net_solutions.py` currently provides 4 solutions:
    * Solution A: Fixed training loop (Module 7/8).
    * Solution B: `IndustrialSensorDataset` custom dataset loader from CSV (Module 7 challenge).
    * Solution C: `TwoLayerNetSolution` manual autograd implementation (Module 9 challenge).
    * Solution D: `MultiHeadAttentionSolution` scaled dot-product attention (Module 11 challenge).
    * It does not contain the complete Deep Learning project solution or Module 9 exercise suite reference solution.

### 1.3 Reversi / Othello Game AI Capstone
* **Game AI Capstone Directory:** `/home/settings/Documents/pearl/game-ai/capstone/`
  * Existing files:
    * `README.md` (2,494 bytes, 44 lines)
    * `reversi_starter.py` (1,416 bytes, 59 lines)
  * Code inspection of `game-ai/capstone/reversi_starter.py`:
    * Line 9: `class OthelloState:` has `__init__` setting up an $8 \times 8$ board with initial pieces:
      `board[3][3] = 2`, `board[4][4] = 2` (White = 2), `board[3][4] = 1`, `board[4][3] = 1` (Black = 1).
    * Line 26: `def get_legal_moves(self): pass` — Stubbed!
    * Line 33: `def make_move(self, move): pass` — Stubbed!
    * Line 41: `def heuristic(state, player): pass` — Stubbed!
    * Line 48: `def minimax_ab(state, depth, alpha, beta, is_maximizing): pass` — Stubbed!
    * Line 53: `def main(): pass` — Stubbed!
  * Existing files in `game-ai/solutions/`:
    * Only `debugging_solutions.py` (2,625 bytes) exists.
    * No Reversi/Othello reference solution exists in `game-ai/solutions/` or `game-ai/capstone/`.
  * Requirements from `game-ai/capstone/README.md`:
    * Milestone 1 (Engine): State, $8 \times 8$ board, 8-directional legal move scan with bracketing and piece flipping, player alternation with pass detection, terminal state & winner evaluation.
    * Milestone 2 (Pygame UI): $8 \times 8$ green grid, black and white circle rendering, legal move highlight dots, mouse interaction, game-over banner. Must also support headless execution for automated testing (`SDL_VIDEODRIVER="dummy"`).
    * Milestone 3 (AI & Heuristic): Alpha-Beta minimax with depth limit (e.g., depth 3–5), positional piece-square table (corners $+100$, squares adjacent to corners $-20$ to $-50$, edges $+10$ to $+20$), mobility calculation, corner differential, piece parity.
    * Deliverables: Fully playable game (Human vs AI), technical report.

### 1.4 Engineering Mathematics: Simulink Module & Motor Control Project
* **Simulink Directory:** `/home/settings/Documents/pearl/engineering-mathematics/simulink/`
  * Existing files:
    * `README.md` (25,704 bytes, 365 lines)
    * `01_block_diagram_basics.md` (12,314 bytes, 222 lines)
    * `02_solvers_and_simulation.md` (11,832 bytes, 202 lines)
    * `models/rc_circuit_model.md` (7,783 bytes, 150 lines)
  * Missing files documented in `simulink/README.md` (lines 353–364):
    * `models/thermal_cooling_model.md` — Block-diagram blueprint for Newton convective cooling.
    * `models/dc_motor_model.md` — Block-diagram blueprint for electromechanical DC motor.
    * `03_rc_circuit_companion.m` — Standalone MATLAB script for RC circuit ODE45 simulation.
    * `04_thermal_cooling_companion.m` — Standalone MATLAB script for thermal cooling ODE45 simulation.
    * `05_dc_motor_companion.m` — Standalone MATLAB script for coupled 2nd-order DC motor ODE45 simulation.
    * `mini_project_motor_control.m` — Closed-loop PI speed control mini-project with anti-windup and load torque disturbance rejection.
    * `exercises.m` — 4-tier progressive exercises template.
  * Missing files in `engineering-mathematics/solutions/`:
    * `solutions/simulink_exercises_solution.m` — Decoupled reference solution for `simulink/exercises.m`.
    * `solutions/probability_exercises_solution.m` — Decoupled reference solution for `probability/exercises.m`.
    * `solutions/capstone_solution.m` (or `capstone/capstone_analysis_complete.m`) — Decoupled reference solution for EV telemetry capstone.
* **Verification Runner Diagnostics (`python3 scripts/verify_package.py`):**
  * Verbatim errors reported by `verify_package.py`:
    * `[ERROR] [DirectoryStructure] simulink/exercises.m — Mandatory file 'simulink/exercises.m' is missing.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:356 — Broken relative link 'models/thermal_cooling_model.md': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:357 — Broken relative link 'models/dc_motor_model.md': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:358 — Broken relative link '03_rc_circuit_companion.m': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:359 — Broken relative link '04_thermal_cooling_companion.m': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:360 — Broken relative link '05_dc_motor_companion.m': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:361 — Broken relative link 'mini_project_motor_control.m': target does not exist.`
    * `[ERROR] [MarkdownLinks] simulink/README.md:363 — Broken relative link '../solutions/simulink_exercises_solution.m': target does not exist.`
    * `[ERROR] [ExerciseTierAuditor] probability/exercises.m — Missing decoupled reference solution for 'probability/exercises.m'.`
    * `[ERROR] [DirectoryStructure] capstone/capstone_analysis_complete.m — Mandatory resource 'capstone_solution' missing.`

---

## 2. Logic Chain

1. **ML Capstone Reference Solution:**
   - *Observation:* `machine-learning/12_capstone/README.md` lines 161 states: `# (Do NOT look at solutions/capstone_solution.py until you submit)`.
   - *Observation:* `machine-learning/README.md` line 132 lists `solutions/capstone_solution.py`.
   - *Observation:* `starter_template.py` contains 6 distinct TODO sections covering EDA, preprocessing, classical ML (classification & regression), PyTorch MLP (classification & regression), model evaluation, and engineering interpretation.
   - *Inference:* An end-to-end reference solution named `machine-learning/solutions/capstone_solution.py` must be authored that executes without error, loads `datasets/industrial_sensor_train.csv` and `test.csv`, trains both classical and neural models, exports the figures (`eda_distributions.png`, `eda_correlation.png`, `feature_importance.png`, `confusion_matrix.png`) to `12_capstone/output/`, and prints a comprehensive comparison table and interpretation findings.

2. **Deep Learning Capstone & Project:**
   - *Observation:* `machine-learning/09_neural_networks/README.md` lines 123 and 138 describe `05_deep_mlp_project.py` as the full engineering fault detection MLP project, and line 125 lists `exercises_solutions.py`.
   - *Observation:* `ORIGINAL_REQUEST.md` line 106 and 114 specifically demand implementing `05_deep_mlp_project.py` and writing missing reference solutions for ML and Deep Learning.
   - *Observation:* `machine-learning/solutions/pytorch_neural_net_solutions.py` covers isolated exercises (training loop, dataset loader, TwoLayerNet, attention) but does not contain the complete Deep MLP project solution or the 4-tier exercise solutions for Module 9.
   - *Inference:* To satisfy R1 and R4 for Deep Learning:
     a. Implement `05_deep_mlp_project.py` under `machine-learning/09_neural_networks/` with a production-grade multi-layer perceptron (Linear + BatchNorm1d + ReLU/GELU + Dropout), early stopping, checkpointing, and evaluation on synthetic fault telemetry.
     b. Provide reference solutions for Module 9 exercises either in `machine-learning/09_neural_networks/exercises_solutions.py` or extended within `machine-learning/solutions/pytorch_neural_net_solutions.py`.
     c. Implement Section 4 of `machine-learning/solutions/capstone_solution.py` which provides the deep learning capstone solution.

3. **Reversi / Othello Game AI Capstone:**
   - *Observation:* `game-ai/capstone/reversi_starter.py` contains only an empty class `OthelloState` and empty function stubs returning `pass`.
   - *Observation:* `game-ai/solutions/` contains only `debugging_solutions.py`.
   - *Observation:* `ORIGINAL_REQUEST.md` line 114 explicitly mandates: *"Write the missing reference solutions for ML, Deep Learning, and the Reversi Game AI Capstone."*
   - *Inference:* A complete, production-grade reference solution must be created at `game-ai/solutions/reversi_solution.py` (and/or `game-ai/capstone/reversi_solution.py`). The solution must:
     a. Implement full `OthelloState` dynamics: 8-direction ray-casting for legal move validation and piece flipping; pass detection when a player has no legal moves; terminal detection when both players pass or board is full; piece tally winner resolution.
     b. Implement heuristic evaluation function combining a calibrated $8 \times 8$ Piece-Square Table (PST) (assigning high positive weights to corners, high negative weights to adjacent X/C squares, moderate positive weights to edges), mobility differential (legal move counts), and corner capture differential.
     c. Implement Minimax with Alpha-Beta pruning (`minimax_ab`) supporting depth limiting, move ordering, and pass handling.
     d. Implement an interactive Pygame GUI in `game-ai/capstone/` (or callable from the solution) with board rendering, piece drawing, legal move highlight dots, score display, and human vs. AI turn processing.
     e. Provide a programmatic / headless self-play mode (`play_game(bot1, bot2, render=False)`) so that automated tests and benchmarks can verify AI playability without an X11 screen.

4. **Simulink Dynamic Modeling & Motor Control Project:**
   - *Observation:* `engineering-mathematics/simulink/` has comprehensive markdown documentation (`README.md`, `01_block_diagram_basics.md`, `02_solvers_and_simulation.md`, `models/rc_circuit_model.md`) but **zero `.m` files**.
   - *Observation:* `simulink/README.md` lines 353–364 list 7 specific missing `.m` and `.md` files (`models/thermal_cooling_model.md`, `models/dc_motor_model.md`, `03_rc_circuit_companion.m`, `04_thermal_cooling_companion.m`, `05_dc_motor_companion.m`, `mini_project_motor_control.m`, `exercises.m`, `solutions/simulink_exercises_solution.m`).
   - *Observation:* `verify_package.py` specifically asserts the existence and syntax of `simulink/exercises.m`, `solutions/simulink_exercises_solution.m`, `solutions/probability_exercises_solution.m`, and `solutions/capstone_solution.m`.
   - *Inference:* The following artifacts must be created to achieve 100% compliance with R4 and pass `verify_package.py`:
     a. `03_rc_circuit_companion.m`: Standalone ODE45 script modeling RC filter charging, computing rise time $t_r = \tau \ln(9)$, settling time $t_s = -\tau \ln(0.02)$, and comparing against analytical exponential.
     b. `04_thermal_cooling_companion.m`: Standalone ODE45 script modeling convective thermal dissipation:
        $$\frac{dT}{dt} = \frac{P_{\text{in}}(t)}{C_{\text{th}}} - \frac{h A}{C_{\text{th}}}(T - T_{\text{amb}})$$
        Evaluating multi-step heat inputs, thermal equilibrium, and time constant $\tau = C_{\text{th}} / (h A)$.
     c. `05_dc_motor_companion.m`: Standalone ODE45 script modeling coupled 2nd-order electromechanical DC motor state-space:
        $$\frac{di_a}{dt} = \frac{1}{L_a}(V_{\text{in}} - R_a i_a - K_e \omega)$$
        $$\frac{d\omega}{dt} = \frac{1}{J}(K_t i_a - b \omega - \tau_L)$$
        Simulating open-loop step response, back-EMF, and load torque disturbance.
     d. `mini_project_motor_control.m`: Standalone closed-loop motor control project implementing a Proportional-Integral (PI) speed regulator with anti-windup clamping to voltage limits ($\pm V_{\max}$), demonstrating load torque rejection ($\tau_L$ step), comparing Open-Loop vs. P-only vs. PI with anti-windup, and verifying transient specs ($t_r < 0.5\text{ s}$, $\%OS < 10\%$, $e_{ss} = 0$).
     e. `models/thermal_cooling_model.md` and `models/dc_motor_model.md`: Block-diagram blueprints matching the structure of `models/rc_circuit_model.md` (physical equations, ASCII diagram, block parameters table, wiring schedule).
     f. `simulink/exercises.m`: 4-tier progressive exercise suite (Level 1: Recall, Level 2: Understanding, Level 3: Application, Level 4: Challenge) with `% TODO` student prompts.
     g. `engineering-mathematics/solutions/simulink_exercises_solution.m`: Fully resolved solution for all 4 tiers without TODO markers.
     h. `engineering-mathematics/solutions/probability_exercises_solution.m` and `engineering-mathematics/solutions/capstone_solution.m`: Reference solutions for the remaining open modules required by `verify_package.py`.

---

## 3. Caveats

1. **Read-Only Inspection Scope:** In accordance with the survey explorer instructions, no files outside `.agents/teamwork_preview_explorer_survey_3/` were modified or created. All proposed implementations and blueprints in this report are for downstream implementing agents.
2. **Pygame Headless Constraints in CI:** Standard Pygame scripts fail if run in a headless environment without a virtual framebuffer (`xvfb`) or `SDL_VIDEODRIVER="dummy"`. All Game AI implementations should include a fallback or headless self-play function so testing does not require an active display.
3. **MATLAB Syntax Validator Quirks:** The custom MATLAB syntax auditor in `engineering-mathematics/scripts/verify_package.py` enforces:
   - 1-based indexing (catches any `v(0)` as Python slip).
   - Strict block balancing (`if/for/while/function/switch` matched with `end`).
   - Strict delimiter balancing (`()`, `[]`, `{}`).
   - Comment ratio $\ge 20\%$ for non-empty lines.
   - All newly authored `.m` files must strictly adhere to these rules.

---

## 4. Conclusion & Actionable Blueprint

### 4.1 Summary of Exact Files to Create

| Module | Target Path | File Type | Purpose / Description |
|---|---|---|---|
| **ML Capstone** | `machine-learning/solutions/capstone_solution.py` | Python Script | Complete worked solution for `12_capstone/starter_template.py` covering EDA, Preprocessing, Random Forest + SVC classification, Random Forest + Ridge regression, PyTorch MLP (classification & regression), comparison table, and engineering interpretation. |
| **Deep Learning** | `machine-learning/09_neural_networks/05_deep_mlp_project.py` | Python Script | Production-grade deep MLP engineering fault prediction project combining Linear, BatchNorm1d, ReLU, Dropout, training loop with validation, and loss/confusion matrix plots. |
| **Deep Learning** | `machine-learning/09_neural_networks/exercises_solutions.py` | Python Script | Reference solutions for `09_neural_networks/exercises.py` (4 tiers). |
| **Game AI Capstone** | `game-ai/solutions/reversi_solution.py` | Python Script | Full reference solution for Reversi/Othello: `OthelloState` engine (8 directions, bracketing, flips, pass handling, terminal detection), PST heuristic evaluation, Alpha-Beta minimax AI bot, and Pygame/headless gameplay. |
| **Game AI Capstone** | `game-ai/capstone/reversi_game.py` (or completed `reversi_starter.py`) | Python Script | Playable Pygame human vs AI implementation with visual board and move highlights. |
| **Simulink** | `engineering-mathematics/simulink/03_rc_circuit_companion.m` | MATLAB Script | Standalone ODE45 script simulating 1st-order RC circuit step response, comparing numerical vs analytical solution, computing rise and settling times. |
| **Simulink** | `engineering-mathematics/simulink/04_thermal_cooling_companion.m` | MATLAB Script | Standalone ODE45 script simulating convective thermal dissipation with ambient feedback, multi-phase power losses, and thermal time constant analysis. |
| **Simulink** | `engineering-mathematics/simulink/05_dc_motor_companion.m` | MATLAB Script | Standalone ODE45 script simulating coupled electromechanical DC motor state-space dynamics under voltage step and load torque disturbance. |
| **Simulink Project** | `engineering-mathematics/simulink/mini_project_motor_control.m` | MATLAB Script | Closed-loop DC motor speed control mini-project: PI controller with anti-windup clamping, load torque step rejection, transient metric validation ($t_r < 0.5\text{ s}$, $\%OS < 10\%$, $e_{ss} = 0$). |
| **Simulink Blueprints** | `engineering-mathematics/simulink/models/thermal_cooling_model.md` | Markdown Blueprint | Block-diagram blueprint and parameter specification for Newton thermal cooling model. |
| **Simulink Blueprints** | `engineering-mathematics/simulink/models/dc_motor_model.md` | Markdown Blueprint | Block-diagram blueprint and parameter specification for electromechanical DC motor model. |
| **Simulink Exercises** | `engineering-mathematics/simulink/exercises.m` | MATLAB Script | 4-tier progressive exercise suite (Recall, Understanding & Debugging, Application, Challenge) with student `% TODO` prompts. |
| **Simulink Solutions** | `engineering-mathematics/solutions/simulink_exercises_solution.m` | MATLAB Script | Decoupled reference solution for `simulink/exercises.m` with 100% resolved TODOs. |
| **Probability Solution** | `engineering-mathematics/solutions/probability_exercises_solution.m` | MATLAB Script | Decoupled reference solution for `probability/exercises.m` (4 tiers: Gaussian noise, biased variance / Bayes fallacy debugging, sensor noise filtering, quad-redundant reliability). |
| **Capstone Solution** | `engineering-mathematics/solutions/capstone_solution.m` (or `capstone/capstone_analysis_complete.m`) | MATLAB Script | Decoupled reference solution for EV powertrain telemetry capstone analysis. |

---

### 4.2 Detailed Specifications & Architectural Blueprints

#### A. Machine Learning Capstone Solution (`machine-learning/solutions/capstone_solution.py`)
- **Execution:** Reads `datasets/industrial_sensor_train.csv` and `test.csv` (generating them via `generate_capstone_data.py` if missing).
- **Structure:**
  1. Section 1 (EDA): Descriptive statistics, class counts (`df['fault_severity'].value_counts()`), feature distribution histograms saved to `machine-learning/12_capstone/output/eda_distributions.png`, correlation matrix with target saved to `output/eda_correlation.png`.
  2. Section 2 (Preprocessing): Imputation with median, `StandardScaler` fitted on train only, transform test, 80/20 train/validation split with stratification on `fault_severity`.
  3. Section 3 (Classical ML):
     - Classification: `RandomForestClassifier(n_estimators=100, random_state=42)` and `SVC(C=1.0, kernel='rbf', probability=True)`. 5-fold cross validation (`cross_val_score`), classification reports, macro and weighted F1 scores.
     - Regression: `RandomForestRegressor(n_estimators=100, random_state=42)` and `Ridge(alpha=1.0)`. $R^2$ and RMSE scores on test set.
     - Feature Importance: Extract from Random Forest, print sorted table, save bar chart to `output/feature_importance.png`.
  4. Section 4 (PyTorch Deep Learning):
     - `FaultClassifierMLP(nn.Module)`: Architecture `Linear(8, 64) -> BatchNorm1d(64) -> ReLU() -> Dropout(0.2) -> Linear(64, 32) -> ReLU() -> Linear(32, 3)`.
     - Trained with `nn.CrossEntropyLoss()`, Adam optimizer (`lr=0.005`), batch size 32, 40 epochs.
     - `RULRegressorMLP(nn.Module)`: Architecture `Linear(8, 64) -> ReLU() -> Linear(64, 32) -> ReLU() -> Linear(32, 1)`. Trained with `nn.MSELoss()`.
     - Saves training loss curve to `output/mlp_training_curves.png`.
  5. Section 5 (Model Evaluation):
     - Pretty-printed comparison table comparing Random Forest vs. SVC vs. PyTorch MLP on accuracy, macro-F1, and regression models on $R^2$ / RMSE.
     - Confusion matrix heatmap on best classifier saved to `output/confusion_matrix.png`.
  6. Section 6 (Interpretation):
     - Answers all prompt questions: top sensors (`vibration`, `temperature`, `acoustic_emission`), fault signature patterns, maintenance triggering threshold (e.g. RUL $< 48$ hours), model deployment trade-offs.

#### B. Deep Learning Project (`machine-learning/09_neural_networks/05_deep_mlp_project.py`)
- **Execution:** Self-contained script or ingests synthetic industrial fault data.
- **Components:**
  - Demonstrates the Four Pillars of deep networks in one cohesive model:
    1. Modern activation: ReLU or GELU.
    2. Weight initialization: He normal (`torch.nn.init.kaiming_normal_`).
    3. Batch Normalization: `nn.BatchNorm1d` before activation.
    4. Regularization: `nn.Dropout(p=0.3)`.
  - Architecture: Input (8) $\to$ Linear(64) $\to$ BatchNorm1d(64) $\to$ ReLU $\to$ Dropout(0.25) $\to$ Linear(32) $\to$ BatchNorm1d(32) $\to$ ReLU $\to$ Dropout(0.25) $\to$ Linear(3).
  - Training loop: Tracks train loss, train acc, val loss, val acc per epoch.
  - Generates and saves `output/training_curves.png` and `output/confusion_matrix.png`.

#### C. Reversi / Othello Game AI Capstone (`game-ai/solutions/reversi_solution.py`)
- **1. Game Engine (`OthelloState`):**
  - Board representation: $8 \times 8$ list of lists or 1D array of 64 integers (0 = empty, 1 = Black, 2 = White).
  - Initial configuration:
    - `(3,3)=2, (3,4)=1, (4,3)=1, (4,4)=2`. Current player = 1 (Black).
  - 8 Search Directions: `[(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]`.
  - `get_legal_moves()`:
    - Scans every empty square $(r, c)$. For each direction $(dr, dc)$, steps forward. If the first step is opponent (`3 - player`), continues stepping until either an empty square/boundary is reached (invalid) or player's own piece is reached (valid bracket). Returns list of valid $(r, c)$.
  - `make_move((r, c))`:
    - Creates deepcopy of state. If move is `None` (pass), flips `current_player = 3 - current_player`. If both players pass consecutively, sets `is_terminal = True` and computes winner.
    - If move is $(r, c)$, places piece and traverses all 8 directions, flipping all trapped opponent discs along valid brackets.
    - Updates next player: if opponent has legal moves, next player is opponent; else if current player has legal moves, next player remains current player (opponent passes); else neither has legal moves $\implies$ terminal state.
- **2. Positional Heuristic Function (`heuristic(state, player)`):**
  - Piece-Square Weight Table:
    ```python
    PST = [
        [ 100, -20,  10,   5,   5,  10, -20,  100],
        [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
        [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
        [   5,  -2,  -1,   0,   0,  -1,  -2,    5],
        [   5,  -2,  -1,   0,   0,  -1,  -2,    5],
        [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
        [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
        [ 100, -20,  10,   5,   5,  10, -20,  100]
    ]
    ```
  - Corner Capture Bonus: Additional $+25$ per captured corner.
  - Mobility: Difference in legal moves: $10 \times (\text{len}(\text{my\_moves}) - \text{len}(\text{opp\_moves}))$.
  - End-game transition: When terminal, score is $\pm 10,000 + (\text{my\_discs} - \text{opp\_discs})$.
- **3. Minimax with Alpha-Beta Pruning (`minimax_ab`):**
  - Arguments: `(state, depth, alpha, beta, is_maximizing, max_player)`
  - Base cases: `state.is_terminal` or `depth == 0` $\implies$ return `(heuristic(state, max_player), None)`.
  - Pass turn handling: if legal moves list is empty and not terminal, recurse with same depth or `depth - 1` on passed child state.
  - Move ordering: sort legal moves by positional square weight descending for faster alpha-beta cutoff.
  - Returns `(best_eval, best_move)`.
- **4. UI & Headless Testing:**
  - Interactive Pygame mode: draws 64-square green board, circular pieces, yellow legal move highlight dots on current turn, score counters, game over banner.
  - Headless self-play function: `play_ai_vs_ai(depth_black=3, depth_white=1)` running in $< 2$ seconds, allowing continuous integration testing without GUI.

#### D. Simulink Companion Scripts & Motor Control Project

##### 1. `simulink/03_rc_circuit_companion.m`
- Standalone numerical simulation using `ode45`.
- Circuit constants: $R = 10\text{ k}\Omega$, $C = 100\ \mu\text{F}$, $\tau = 1.0\text{ s}$, $V_{\text{step}} = 5.0\text{ V}$, $t_{\text{step}} = 0.1\text{ s}$, $t_{\text{final}} = 6.0\text{ s}$.
- ODE: `rc_ode = @(t, vc) ((t >= t_step) * V_step - vc) / (R * C);`
- Metrics: Rise time $t_r = t_{90\%} - t_{10\%}$ (compares with $\tau \ln(9) \approx 2.197\text{ s}$), settling time $t_s$ (compares with $-\tau \ln(0.02) \approx 3.912\text{ s}$), maximum numerical solver error vs analytical $V_{\text{step}}(1 - e^{-(t - t_0)/\tau}) \le 10^{-4}\text{ V}$.
- Formatted engineering console output.

##### 2. `simulink/04_thermal_cooling_companion.m`
- Standalone numerical simulation of Newton's Law of Cooling with heat generation.
- Physical constants: $C_{\text{th}} = 180\text{ J/K}$, $h A = 4.5\text{ W/K}$, $T_{\text{amb}} = 25.0^\circ\text{C}$, $\tau_{\text{th}} = C_{\text{th}} / (h A) = 40.0\text{ s}$.
- Power profile $P_{\text{in}}(t)$:
  - $0 \le t < 100\text{ s}$: $0\text{ W}$ (cold start at $25^\circ\text{C}$).
  - $100 \le t < 300\text{ s}$: $150\text{ W}$ (inverter pulse heating).
  - $300 \le t \le 600\text{ s}$: $0\text{ W}$ (passive convective cooldown).
- ODE formulation:
  $$\frac{dT}{dt} = \frac{1}{C_{\text{th}}} \big( P_{\text{in}}(t) - h A (T - T_{\text{amb}}) \big)$$
- Analyzes peak junction temperature ($T_{\max} = T_{\text{amb}} + P_{\text{in}} / (h A) = 25 + 150/4.5 = 58.33^\circ\text{C}$), validates exponential cooling curve $T(t) = T_{\text{amb}} + (T_{\text{peak}} - T_{\text{amb}}) e^{-(t - t_{\text{off}})/\tau_{\text{th}}}$, prints transient thermal audit.

##### 3. `simulink/05_dc_motor_companion.m`
- Coupled 2nd-order electromechanical DC motor simulation.
- Physical parameters:
  - Armature resistance: $R_a = 2.0\ \Omega$
  - Armature inductance: $L_a = 0.5\text{ H}$
  - Motor torque constant: $K_t = 0.1\text{ N}\cdot\text{m/A}$
  - Back-EMF constant: $K_e = 0.1\text{ V}\cdot\text{s/rad}$
  - Rotor inertia: $J = 0.02\text{ kg}\cdot\text{m}^2$
  - Viscous friction coefficient: $b = 0.01\text{ N}\cdot\text{m}\cdot\text{s/rad}$
- State vector: $\mathbf{x} = [i_a; \omega]$.
- State-space matrices:
  $$A = \begin{bmatrix} -R_a/L_a & -K_e/L_a \\ K_t/J & -b/J \end{bmatrix} = \begin{bmatrix} -4.0 & -0.2 \\ 5.0 & -0.5 \end{bmatrix}$$
  $$B = \begin{bmatrix} 1/L_a & 0 \\ 0 & -1/J \end{bmatrix} = \begin{bmatrix} 2.0 & 0 \\ 0 & -50.0 \end{bmatrix}$$
- Inputs: Voltage step $V_{\text{in}} = 24.0\text{ V}$ at $t = 0$, external disturbance load torque $\tau_L = 0.5\text{ N}\cdot\text{m}$ applied at $t = 3.0\text{ s}$, simulation duration $t_{\text{final}} = 6.0\text{ s}$.
- Solved via `ode45`, evaluates no-load steady-state speed $\omega_{ss} = \frac{K_t V_{\text{in}}}{R_a b + K_t K_e}$, speed droop under load, and peak inrush current $I_{\text{peak}} \approx V_{\text{in}} / R_a = 12\text{ A}$.

##### 4. `simulink/mini_project_motor_control.m`
- Closed-Loop Proportional-Integral (PI) Speed Control of DC Motor with Anti-Windup.
- Control Objectives:
  - Setpoint speed: $\omega_{\text{ref}} = 100.0\text{ rad/s}$ ($\sim 955\text{ RPM}$).
  - Full load disturbance: $\tau_L = 0.8\text{ N}\cdot\text{m}$ stepped in at $t = 2.5\text{ s}$.
  - Actuator supply limit: $V_{\max} = \pm 36.0\text{ V}$.
  - Specifications: Rise time $t_r < 0.5\text{ s}$, Overshoot $\%OS < 10\%$, Zero steady-state speed error ($e_{ss} = 0$).
- Comparative Simulation in 3 regimes:
  1. Open-Loop Step Response (large speed droop under load, sluggish rise time).
  2. Closed-Loop Proportional (P) Control ($K_p = 2.5$): faster response, but persistent non-zero steady-state offset under load torque.
  3. Closed-Loop PI Control with Anti-Windup ($K_p = 2.0, K_i = 12.0$):
     - Anti-windup clamping algorithm: if actuator saturates at $\pm V_{\max}$ and error has same sign as output, freeze integrator accumulation to prevent windup.
     - Demonstrates complete recovery from load disturbance, driving error back to zero.
- Exports performance scorecard table with measured vs target specs.

##### 5. `simulink/models/thermal_cooling_model.md` & `simulink/models/dc_motor_model.md`
- Markdown model blueprints structured identically to `models/rc_circuit_model.md`:
  - Section 1: Physical System Description & Governing Differential Equations.
  - Section 2: Complete ASCII Block Diagram Visual Blueprint.
  - Section 3: Block Parameter Specifications Table (Block Label, Library Path, Parameter, Value, Engineering Rationale).
  - Section 4: Signal Connection & Wiring Schedule (Source Block $\to$ Destination Block/Port).
  - Section 5: Verification & Expected Scope Output.

##### 6. `simulink/exercises.m` & `solutions/simulink_exercises_solution.m`
- 4-tier progressive exercise suite strictly following `verify_package.py` regular expressions:
  - `%% Level 1: Recall`
    - Problem 1.1: Signal Tracing & Equivalent Transfer Functions.
    - Problem 1.2: First-Order Time Constant and DC Gain Extraction.
  - `%% Level 2: Understanding & Debugging`
    - Debugging Task 2.1: Diagnosing and Breaking an Algebraic Loop (Direct Feedthrough vs State Delay).
    - Debugging Task 2.2: Forward Euler (`ode1`) Numerical Stability & Critical Time Step $\Delta t_{\text{crit}} = 2 / |\lambda_{\max}|$.
  - `%% Level 3: Application`
    - Application Task 3.1: Second-Order Series RLC Resonant Circuit ODE Integration (Underdamped vs Critically Damped vs Overdamped regimes).
  - `%% Level 4: Challenge`
    - Challenge Task 4.1: Closed-Loop DC Motor PI Controller Tuning with Anti-Windup under Full Load Torque Disturbance.
- Decoupled reference solution `engineering-mathematics/solutions/simulink_exercises_solution.m` implements complete verified numerical solutions for all 4 tiers without TODO markers.

---

## 5. Verification Method

### 5.1 Automated Package Integrity Checks
Downstream agents can verify the implementation using the repository's built-in testing tools:

1. **Engineering Mathematics Full Package Validator:**
   ```bash
   cd /home/settings/Documents/pearl/engineering-mathematics
   python3 scripts/verify_package.py --all
   ```
   *Expected outcome:* 0 errors found across all validators (DirectoryStructure, MarkdownLinks, MatlabSyntax, ExerciseTier, DatasetCapstone).

2. **Simulink-Specific Modular Check:**
   ```bash
   cd /home/settings/Documents/pearl/engineering-mathematics
   python3 scripts/verify_package.py --module simulink --check-structure --check-syntax --check-exercises --check-links
   ```
   *Expected outcome:* All Simulink companion scripts and exercise files pass without syntax errors or broken links.

3. **Pytest Suite:**
   ```bash
   cd /home/settings/Documents/pearl/engineering-mathematics
   pytest tests/ -v
   ```
   *Expected outcome:* 27/27 tests pass.

4. **Machine Learning Package Practical Test:**
   ```bash
   cd /home/settings/Documents/pearl/machine-learning
   python3 assessment/practical_test.py
   ```
   *Expected outcome:* All 23 lesson tests pass, and file completeness check verifies 100% of required files.

5. **ML Capstone Reference Solution Execution:**
   ```bash
   cd /home/settings/Documents/pearl/machine-learning/12_capstone
   python3 generate_capstone_data.py
   python3 ../solutions/capstone_solution.py
   ```
   *Expected outcome:* Generates datasets, trains RF/SVC and PyTorch MLPs, exports 4 visual plots to `12_capstone/output/`, prints evaluation table with $R^2 > 0.85$ and Accuracy $> 90\%$.

6. **Reversi Game AI Headless Verification:**
   ```bash
   cd /home/settings/Documents/pearl/game-ai
   python3 -c "from solutions.reversi_solution import OthelloState, minimax_ab, play_game; winner, scores = play_game(ai_depth=2); print(f'Game completed! Winner: {winner}, Scores: {scores}')"
   ```
   *Expected outcome:* Successfully runs an automated full game of Reversi without requiring an active X11 display, validating state transitions, legal move generation, flipping, and Alpha-Beta minimax evaluation.
