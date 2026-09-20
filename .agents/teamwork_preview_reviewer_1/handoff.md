# Milestone Review & Adversarial Challenge Report: M1 & M2

**Reviewer Identity**: `teamwork_preview_reviewer_1`  
**Roles**: Reviewer, Adversarial Critic  
**Date**: 2026-09-18T15:50:00Z  
**Scope**: 
- **Milestone M1 (Deep Learning Fixes)**: `machine-learning/09_neural_networks/` (`03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`, `exercises_solutions.py`) and `machine-learning/assessment/practical_test.py`.
- **Milestone M2 (Math & Game AI Code Gaps)**: `machine-learning/05_clustering/04_pca_from_scratch.py`, `machine-learning/04_classification/01_logistic_regression_gd.py`, `game-ai/08_checkers/`, `game-ai/10_mcts/`, `game-ai/11_reinforcement_learning/`.

---

## Executive Summary & Verdict

**Final Verdict**: **REQUEST_CHANGES**

**Integrity Audit Verdict**: **CLEAN (NO INTEGRITY VIOLATION DETECTED)**.
All mathematical derivations, neural network components, linear algebra routines, gradient descent loops, and game AI algorithms are authentic, rigorous, and implemented from first principles. Zero hardcoded test outputs, zero dummy facade classes, and zero external shortcuts were detected.

However, changes are requested due to two specific findings:
1. **Major Finding (Flaky Test / Direct Execution Failure)**: `game-ai/10_mcts/play_mcts.py` fails with an uncaught `AssertionError: MCTS failed to consistently hold Minimax to a draw!` and **exit code 1** when executed directly, caused by unseeded stochastic simulation variance in `run_tictactoe_vs_minimax`.
2. **Major Finding (Exit Code Suppression & Unhandled Legacy Failures in Test Harness)**: `machine-learning/assessment/practical_test.py` suppresses test failures by returning **exit code 0** even when sub-tests fail or time out (specifically `01_what_is_ml.py`, `02_cross_validation.py`, and `02_backpropagation_and_deep_mlp.py`), leading `test_deep_learning_e2e.py::test_dl_practical_test_suite_passes` to pass erroneously.

---

## 1. Observation

### 1.1 Automated E2E Test Suite Execution
- **Command 1**: `pytest tests/e2e/test_deep_learning_e2e.py -v`
  - **Result**: `34 passed in 254.36s` (Exit code: 0).
- **Command 2**: `pytest tests/e2e/test_math_game_ai_e2e.py -v`
  - **Result**: `36 passed in 5.77s` (Exit code: 0).
- **Total E2E Passed**: 70/70 tests passed.

### 1.2 Direct Script Executions (Exit Codes & Runtime)
1. `python machine-learning/09_neural_networks/03_batch_normalization.py`
   - Exit code: 0.
   - Max difference between manual BatchNorm and `nn.BatchNorm1d`: `1.19209290e-07`.
   - Saved `output/batchnorm_effect.png` (86 KB).
2. `python machine-learning/09_neural_networks/04_dropout.py`
   - Exit code: 0.
   - Inverted dropout mean across 10,000 train units: `1.0000` (preserves expectation). Eval mode identity mapping verified.
   - Saved `output/dropout_effect.png` (133 KB).
3. `python machine-learning/09_neural_networks/05_deep_mlp_project.py`
   - Exit code: 0.
   - 8-channel telemetry, 3 classes, 44,099 parameters, early stopping triggered at epoch 51 (best checkpoint epoch 36, val loss 0.0003). Test accuracy: 100.0%.
   - Saved `output/training_curves.png` (106 KB) and `output/confusion_matrix.png` (66 KB).
4. `python machine-learning/09_neural_networks/exercises_solutions.py`
   - Exit code: 0.
   - All 4 exercise tiers completed. Level 4 from-scratch `TwoLayerNet` with manual autograd and manual stable cross-entropy achieves 100.0% accuracy.
   - Saved `output/nn_exercise_training.png` (80 KB).
5. `python machine-learning/05_clustering/04_pca_from_scratch.py`
   - Exit code: 0.
   - SVD eigenvalue equivalence matches within `1e-8: True`.
   - Max EVR absolute difference vs scikit-learn: `1.39e-17`.
   - Saved `output/pca_from_scratch.png` (187 KB).
6. `python machine-learning/04_classification/01_logistic_regression_gd.py`
   - Exit code: 0.
   - Scratch GD accuracy: `1.0000`, Sklearn accuracy: `1.0000`. OvR multi-class accuracy: `1.0000`.
   - Saved `output/logistic_regression_gd.png` (178 KB).
7. `python game-ai/08_checkers/play_checkers.py --games 2 --depth 2`
   - Exit code: 0.
   - Alpha-Beta AI vs Random: AI won 1, drew 1, lost 0. Forced capture integrity verified.
8. `python game-ai/10_mcts/play_mcts.py`
   - **Initial Run (Task-167)**: **EXIT CODE 1**.
     ```
     =================================================================
     BENCHMARK 2: Tic-Tac-Toe — MCTS vs Perfect Minimax (10 games)
     MCTS Simulations per move: 500
     =================================================================
     Results over 10 games:
       MCTS Wins:     0
       Minimax Wins:  2
       Draws:         8 (80.0%)
     =================================================================
     Traceback (most recent call last):
       File "/home/settings/Documents/pearl/game-ai/10_mcts/play_mcts.py", line 185, in <module>
         run_tictactoe_vs_minimax(num_games=10, num_simulations=500)
       File "/home/settings/Documents/pearl/game-ai/10_mcts/play_mcts.py", line 122, in run_tictactoe_vs_minimax
         assert mcts_wins + draws >= num_games - 1, "MCTS failed to consistently hold Minimax to a draw!"
     AssertionError: MCTS failed to consistently hold Minimax to a draw!
     ```
   - **Second Run (Task-178)**: Exit code 0 (Minimax Wins: 1, Draws: 9 (90.0%)).
9. `python game-ai/11_reinforcement_learning/train_rl.py`
   - Exit code: 0.
   - GridWorld 4x5 MDP: Converged to optimal 7-step path `[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)]`, reward 4.0.
   - Saved `output/q_learning_training.png` (149 KB).
10. `python machine-learning/assessment/practical_test.py`
   - Exit code: 0 (suppressed failures).
   - Verbose log output:
     ```
     Results: 23/26 tests passed
     Failed tests:
       ❌ Module 1: What is ML?
          Path: 01_ml_fundamentals/01_what_is_ml.py
          Reason: TypeError: traditional_house_price() got an unexpected keyword argument 'distance_km'
       ❌ Module 6: Cross-Validation
          Path: 06_model_evaluation/02_cross_validation.py
          Reason: TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'. Did you mean 'label'?
       ❌ Module 9: Backprop & MLP
          Path: 09_neural_networks/02_backpropagation_and_deep_mlp.py
          Reason: TIMEOUT (> 120s)
     ```
   - All M1 modules under review passed:
     - `✅ Module 9: Batch Normalization PASS`
     - `✅ Module 9: Dropout PASS`
     - `✅ Module 9: Deep MLP Project PASS`

### 1.3 Physical Artifacts Inspection
All required output figures exist on disk and possess non-zero, healthy file sizes:
- `machine-learning/09_neural_networks/output/batchnorm_effect.png` (86 KB)
- `machine-learning/09_neural_networks/output/dropout_effect.png` (133 KB)
- `machine-learning/09_neural_networks/output/training_curves.png` (106 KB)
- `machine-learning/09_neural_networks/output/confusion_matrix.png` (66 KB)
- `machine-learning/09_neural_networks/output/nn_exercise_training.png` (80 KB)
- `machine-learning/05_clustering/output/pca_from_scratch.png` (187 KB)
- `machine-learning/04_classification/output/logistic_regression_gd.png` (178 KB)
- `game-ai/11_reinforcement_learning/output/q_learning_training.png` (149 KB)

---

## 2. Logic Chain

1. **Test Verification**:
   - Both `pytest tests/e2e/test_deep_learning_e2e.py` (34 tests) and `pytest tests/e2e/test_math_game_ai_e2e.py` (36 tests) pass with 100% success.
   - However, Task 1 explicitly requires: *"Execute individual scripts directly to verify exit code 0."*

2. **Analysis of `game-ai/10_mcts/play_mcts.py`**:
   - `play_mcts.py` is an executable benchmark script provided for the MCTS curriculum module.
   - Lines 84-89 define `run_tictactoe_vs_minimax(num_games=10, num_simulations=600)`, with an assertion on line 122:
     `assert mcts_wins + draws >= num_games - 1, "MCTS failed to consistently hold Minimax to a draw!"`
   - In the script's `__main__` entry point (line 185), the simulation count is decreased:
     `run_tictactoe_vs_minimax(num_games=10, num_simulations=500)`
   - The script does not set `random.seed()`. Pure Monte Carlo rollouts are stochastic. Against an optimal Minimax searcher (which never blunders), 500 unguided rollouts will occasionally blunder on 2 out of 10 games, yielding 8 draws and 2 losses.
   - In our direct execution test (Task-167), this triggered the assertion error `8 >= 9 == False`, exiting with **code 1**.
   - Testing with `random.seed(42)` immediately resulted in 9 draws, 1 loss, and exit code 0.
   - The E2E test suite `test_math_game_ai_e2e.py` only tested isolated methods (`MCTSNode`, `mcts.get_best_move` with small simulation counts) and never executed `play_mcts.py`, allowing this flake to escape E2E testing.

3. **Analysis of `machine-learning/assessment/practical_test.py`**:
   - `practical_test.py` is specifically listed in M1 review scope (`machine-learning/assessment/practical_test.py`) and owned by M1 in `PROJECT.md`.
   - In `practical_test.py`, `main()` runs 26 lesson files using `subprocess.run()`.
   - When a lesson file fails, `main()` appends it to `failed`. At the end of `main()`, it prints `Results: {passed}/{len(TESTS)} tests passed`, but **omits `sys.exit(1)`**.
   - As a result, `practical_test.py` exits with status 0 even when 3 tests fail.
   - In `tests/e2e/test_deep_learning_e2e.py`, `test_dl_practical_test_suite_passes` checks only `assert res.returncode == 0`. It therefore registered a PASS despite 3 test failures in the underlying curriculum.
   - While the 3 new M1 files passed (`03_batch_normalization.py`, `04_dropout.py`, `05_deep_mlp_project.py`), the assessment harness itself is flawed because it fails to signal failure to downstream CI/E2E runners.

4. **Integrity & Code Quality Assessment**:
   - We probed `PCAScratch` with rank-deficient, wide ($N < D$), and constant-column data. The implementation cleanly handles all cases, reconstructing full feature matrices to within $1.78 \times 10^{-15}$.
   - We probed `LogisticRegressionGD` with extreme logits ($\pm 10^9$) and strong L2 regularization ($\lambda = 100$). Sigmoid values remained strictly bounded in $[0, 1]$ with zero NaNs, and weight norms shrunk from $2.982$ to $0.156$.
   - We verified that `CheckersState` strictly disallows regular diagonal moves when a capture jump is available, correctly handles king promotion crowning rules (crowning terminates turn), and handles terminal states when a player is blocked.
   - We verified that `QLearningAgent` implements proper Bellman equation updates where terminal transitions set future discount to 0 (`if done: target = reward`).
   - We verified that `03_batch_normalization.py`, `04_dropout.py`, and `05_deep_mlp_project.py` correctly implement `model.train()` vs `model.eval()`, Kaiming He initialization, and `bias=False` on linear layers preceding `BatchNorm1d`.
   - No integrity violations or cheating shortcuts were found.

---

## 3. Findings

### Finding 1 [Major]: Flaky Stochastic Assertion Failure in `play_mcts.py`
- **What**: Direct execution of `game-ai/10_mcts/play_mcts.py` fails with an uncaught `AssertionError` and exit code 1 due to random rollout variance.
- **Where**: `game-ai/10_mcts/play_mcts.py`, lines 122 & 185.
- **Why**: `run_tictactoe_vs_minimax` plays 10 games with 500 simulations per move and no random seed. Minimax plays perfectly. Unseeded stochastic rollouts occasionally lead MCTS to lose 2 games instead of 1, failing the rigid threshold `assert mcts_wins + draws >= num_games - 1`. This directly violates Task 1's requirement that scripts execute with exit code 0.
- **Suggestion**: 
  1. Add `random.seed(42)` at the beginning of `run_tictactoe_vs_minimax` (or in `__main__`) to guarantee deterministic execution.
  2. Increase `num_simulations` to 750+ in line 185 (or align with the function default of 600).
  3. Or relax the tolerance to `assert mcts_wins + draws >= num_games - 2` (80% non-loss rate, matching the Connect Four benchmark on line 172).

### Finding 2 [Major]: Exit Code Suppression in `practical_test.py`
- **What**: `machine-learning/assessment/practical_test.py` exits with code 0 even when internal validation tests fail.
- **Where**: `machine-learning/assessment/practical_test.py`, lines 70–156.
- **Why**: In `main()`, there is no `sys.exit(1)` when `failed` is non-empty. This causes CI and `tests/e2e/test_deep_learning_e2e.py::test_dl_practical_test_suite_passes` to register a green pass even though `01_ml_fundamentals/01_what_is_ml.py` failed with `TypeError`, `06_model_evaluation/02_cross_validation.py` failed with `TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'`, and `09_neural_networks/02_backpropagation_and_deep_mlp.py` timed out (> 120s).
- **Suggestion**: 
  1. In `practical_test.py`, add `if failed: sys.exit(1)` at the conclusion of `main()`.
  2. Fix the two keyword argument regressions in the legacy files:
     - In `01_ml_fundamentals/01_what_is_ml.py`: ensure `traditional_house_price()` signature matches the unpacked `example_house` dictionary or filter kwargs.
     - In `06_model_evaluation/02_cross_validation.py`: update `ax.boxplot(..., labels=...)` to `tick_labels=...` for Matplotlib 3.9+ compatibility.
     - Increase timeout for `02_backpropagation_and_deep_mlp.py` to 180s or reduce its training epochs in non-verbose test mode.

### Finding 3 [Minor]: Unhandled `--benchmark` Flag in `play_checkers.py`
- **What**: `play_checkers.py --benchmark` exits with code 2 (`unrecognized arguments: --benchmark`).
- **Where**: `game-ai/08_checkers/play_checkers.py`, argparse definition.
- **Why**: The script defaults to running the benchmark when `--interactive` is omitted, but does not define `--benchmark` as a recognized flag.
- **Suggestion**: Add `parser.add_argument('--benchmark', action='store_true', help='Run headless benchmark')` to prevent user confusion.

---

## 4. Adversarial Stress-Testing & Integrity Audit

### 4.1 Integrity Audit (Anti-Cheating Checklist)
| Integrity Dimension | Evaluation Result | Evidence / Notes |
|:---|:---:|:---|
| **Hardcoded Outputs** | **NONE** | No test results or metrics are hardcoded in source. Weights, losses, gradients, eigenvalues, and game moves are calculated dynamically. |
| **Dummy / Facade Logic** | **NONE** | All classes (`PCAScratch`, `LogisticRegressionGD`, `CheckersState`, `MCTSNode`, `MCTS`, `GridWorld`, `QLearningAgent`, `TwoLayerNet`) contain genuine, functional implementations. |
| **Task Bypasses / External Delegation** | **NONE** | PCA computes actual covariance eigendecomposition via `np.linalg.eigh`; Logistic Regression calculates analytical gradients; Checkers engine implements full recursive move trees. `sklearn` is only imported in benchmarks for parity assertion. |
| **Fabricated Verification Logs** | **NONE** | All 70 pytest E2E tests executed independently and produced verifiable results. |
| **Self-Certifying Verification** | **FLAGGED** | `practical_test.py` was self-certifying by returning exit code 0 when failing; flagged under Finding 2. |

### 4.2 Adversarial Attack Scenarios & Results
| # | Component | Attack Scenario / Edge Case | Expected Result | Actual Result | Status |
|:---:|:---|:---|:---|:---|:---:|
| 1 | `PCAScratch` | High-dimensional data with $N < D$ (5 samples, 10 features) | Compute covariance and project to $k \le \min(N-1, D)$ | Projected shape $(5, 3)$, eigenvalues non-negative | **PASS** |
| 2 | `PCAScratch` | Feature column with zero variance (constant value) | Handle without division-by-zero or NaNs | No NaNs, zero eigenvalue for constant component | **PASS** |
| 3 | `PCAScratch` | Full reconstruction with $k = \min(N-1, D)$ | Perfect reconstruction of $X$ | Maximum reconstruction error: $1.78 \times 10^{-15}$ | **PASS** |
| 4 | `LogisticRegressionGD` | Extreme input logits $z \in [-10^9, 10^9]$ | Numerically stable sigmoid without overflow or NaNs | Probabilities strictly in $[0, 1]$, zero NaNs | **PASS** |
| 5 | `LogisticRegressionGD` | Extreme L2 regularization ($\lambda = 100$) | Strong shrinkage of weight vector towards 0 | Coefficient norm shrunk from $2.982$ to $0.156$ | **PASS** |
| 6 | `CheckersState` | Mandatory capture with simultaneous simple step option | Suppress all diagonal steps when jump is available | Jumps returned: `[((5, 2), (3, 4)), ((5, 4), (3, 2))]`; zero steps | **PASS** |
| 7 | `CheckersState` | Man reaches king row (row 0) during jump | Crowning ends turn immediately; no multi-jump continuation | Single crowning hop recorded, turn toggled to Black | **PASS** |
| 8 | `CheckersState` | Player has pieces remaining but 0 legal moves | Blocked player declared loser | `is_terminal=True`, opponent declared winner | **PASS** |
| 9 | `QLearningAgent` | Terminal state transitions in Bellman update | Disregard discounted future returns on terminal step | Target set to immediate reward; no discount applied | **PASS** |
| 10 | `play_mcts.py` | Stochastic rollout tournament vs optimal Minimax | Hold Minimax to draw $\ge 90\%$ without random seed | In 10 games, MCTS drew 8 and lost 2 (80%), failing assertion | **FAIL** |

---

## 5. Verified Claims vs Unverified Items

### Verified Claims
- `03_batch_normalization.py` matches `nn.BatchNorm1d` within $1.19 \times 10^{-7}$ numerical tolerance.
- `04_dropout.py` inverted dropout scaling preserves activation expectation ($E[h] = 1.0000$) and functions as identity during eval mode.
- `05_deep_mlp_project.py` trains `DeepFaultClassifier` with early stopping and saves `training_curves.png` and `confusion_matrix.png`.
- `exercises_solutions.py` solves all 4 tiers, contains 0 remaining TODOs, and implements from-scratch `TwoLayerNet`.
- `04_pca_from_scratch.py` matches scikit-learn EVR within $1.39 \times 10^{-17}$ and verifies economy SVD equivalence.
- `01_logistic_regression_gd.py` achieves 100% accuracy on binary and OvR multi-class classification.
- `game-ai/08_checkers/` engine enforces forced captures, multi-jumps, and crowning.
- `game-ai/11_reinforcement_learning/` trains tabular Q-learning to the optimal 7-step path in GridWorld.
- All 8 required image plot artifacts exist and exceed 66 KB in size.

### Unverified Items
- None within the assigned M1 and M2 scope.

---

## 6. Caveats

- Milestone M1 and M2 implementations are mathematically exceptional; the verdict `REQUEST_CHANGES` is driven strictly by:
  1. The flaky assertion in `play_mcts.py` causing exit code 1 under direct execution.
  2. The test harness defect in `practical_test.py` that suppresses non-zero exit codes when sub-tests fail.
- Once these two issues are resolved by the respective milestone workers, the curriculum code for M1 and M2 will be in an exemplary state for final sign-off.

---

## 7. Conclusion & Recommended Action Plan

### Recommended Fixes for Milestone Owners:

1. **For M2 Worker (`game-ai/10_mcts/play_mcts.py`)**:
   - In `play_mcts.py`, add `random.seed(42)` inside `run_tictactoe_vs_minimax` or at the top of the file.
   - Update line 185 to use `num_simulations=600` (matching the function definition).
   - Alternatively, change line 122 to: `assert mcts_wins + draws >= num_games - 2, "MCTS failed to consistently hold Minimax to a draw!"` (allowing an 80% draw rate against perfect Minimax).

2. **For M1 Worker (`machine-learning/assessment/practical_test.py`)**:
   - In `practical_test.py`, add `if failed: sys.exit(1)` at the end of `main()`.
   - Update `machine-learning/06_model_evaluation/02_cross_validation.py` to replace `labels=` with `tick_labels=` in `plt.boxplot()`.
   - Update `machine-learning/01_ml_fundamentals/01_what_is_ml.py` to fix the `traditional_house_price(**example_house)` signature.
   - Increase the timeout in `run_test` from 120s to 180s so that `02_backpropagation_and_deep_mlp.py` has sufficient time to complete training without timing out.

---

## 8. Verification Method for Retesting

To independently verify the fixes when resubmitted:
1. Run direct MCTS tournament:
   ```bash
   python game-ai/10_mcts/play_mcts.py
   # Must exit with code 0 repeatedly across multiple runs
   ```
2. Run practical test harness:
   ```bash
   python machine-learning/assessment/practical_test.py
   # Must report 26/26 passed and exit with code 0
   ```
3. Run both E2E test suites:
   ```bash
   pytest tests/e2e/test_deep_learning_e2e.py -v
   pytest tests/e2e/test_math_game_ai_e2e.py -v
   # Must pass 100% (70/70)
   ```
4. Confirm all individual scripts exit with code 0:
   ```bash
   python machine-learning/09_neural_networks/03_batch_normalization.py
   python machine-learning/09_neural_networks/04_dropout.py
   python machine-learning/09_neural_networks/05_deep_mlp_project.py
   python machine-learning/09_neural_networks/exercises_solutions.py
   python machine-learning/05_clustering/04_pca_from_scratch.py
   python machine-learning/04_classification/01_logistic_regression_gd.py
   python game-ai/08_checkers/play_checkers.py
   python game-ai/11_reinforcement_learning/train_rl.py
   ```
