## 2026-09-17T15:22:02Z

You are Worker M1 for the curriculum completion project.
Your identity: teamwork_preview_worker_m1
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m1

MANDATORY: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md first (under ## Follow-up — 2026-09-17T15:02:54Z, requirement R1).
Read /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_3/PROJECT.md (Milestone M1).
Read /home/settings/Documents/pearl/.agents/teamwork_preview_explorer_survey_1/handoff.md (Sections 1.1 and 4.1).

EXCLUSIVE OWNED WRITE PATHS:
- `machine-learning/09_neural_networks/03_batch_normalization.py`
- `machine-learning/09_neural_networks/04_dropout.py`
- `machine-learning/09_neural_networks/05_deep_mlp_project.py`
- `machine-learning/09_neural_networks/exercises_solutions.py`
- `machine-learning/assessment/practical_test.py`
- `machine-learning/09_neural_networks/output/`

TASKS:
1. Implement `machine-learning/09_neural_networks/03_batch_normalization.py`:
   - Internal covariate shift explanation, mathematical formulation (batch mean, variance, gamma, beta, running mean/var EMA), train vs eval modes (`model.train()` vs `model.eval()`).
   - Deep MLP comparison experiment (with vs without BatchNorm at high learning rate).
   - Headless plotting (`matplotlib.use('Agg')`), saving loss curves and activation distributions to `output/batchnorm_effect.png`.
2. Implement `machine-learning/09_neural_networks/04_dropout.py`:
   - Co-adaptation explanation, inverted dropout (1/(1-p) scaling), ensemble interpretation, train vs eval modes.
   - Overfitting regularization experiment comparing wide MLP without dropout vs with dropout on small noisy dataset.
   - Save train/val loss and accuracy comparison plots to `output/dropout_effect.png`.
3. Implement `machine-learning/09_neural_networks/05_deep_mlp_project.py`:
   - Industrial machine fault detection classifier on synthetic 8-channel sensor telemetry.
   - Full deep architecture combining BatchNorm1d, Dropout(0.25-0.3), Kaiming normal initialization, Adam optimizer, validation loop with early stopping, classification report.
   - Save `output/training_curves.png` and `output/confusion_matrix.png`.
4. Implement `machine-learning/09_neural_networks/exercises_solutions.py`:
   - Fully resolve all 4 exercise tiers from `09_neural_networks/exercises.py` with 0 remaining TODOs.
5. Update `machine-learning/assessment/practical_test.py` so Module 9 includes `03_batch_normalization.py`, `04_dropout.py`, and `05_deep_mlp_project.py` in test assertions.
6. Run builds/tests:
   - `python3 machine-learning/09_neural_networks/03_batch_normalization.py`
   - `python3 machine-learning/09_neural_networks/04_dropout.py`
   - `python3 machine-learning/09_neural_networks/05_deep_mlp_project.py`
   - `python3 machine-learning/09_neural_networks/exercises_solutions.py`
   - `python3 machine-learning/assessment/practical_test.py`
   Document commands and test outcomes in your handoff report.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Write your report to `/home/settings/Documents/pearl/.agents/teamwork_preview_worker_m1/handoff.md` and send a message when done.
