# Dispatch for Remediation Worker

## 2026-09-19T16:38:30Z
You are the Remediation Worker for the curriculum completion project.
Your identity: teamwork_preview_worker_remediation_2
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_remediation_2

MANDATORY: Read /home/settings/Documents/pearl/ORIGINAL_REQUEST.md first (under ## Follow-up — 2026-09-17T15:02:54Z and ## Follow-up — 2026-09-19T16:34:45Z).
Read /home/settings/Documents/pearl/PROJECT.md.
Read /home/settings/Documents/pearl/.agents/teamwork_preview_reviewer_1/handoff.md.
Read /home/settings/Documents/pearl/.agents/teamwork_preview_challenger_2/handoff.md.

YOUR TASKS:
Apply the 4 precise fixes identified during Phase 2B Verification by Reviewer 1 and Challenger 2:

1. `game-ai/10_mcts/play_mcts.py`:
   - In `run_tictactoe_vs_minimax()`, add `random.seed(42)` at the start of the function and ensure non-loss threshold handles stochastic rollouts robustly (`mcts_losses <= 2` or `mcts_wins + draws >= num_games - 2`). Also ensure `num_simulations=600` or appropriately configured.
   - Run `python3 game-ai/10_mcts/play_mcts.py` and verify exit code 0.

2. `networking/01_tcp_ip/02_tcp_client.py`:
   - In `connect(self)`: wrap socket creation and connection in `try... except Exception:` so that on failure, `sock.close()`, `self._sock = None`, and re-raise the exception.
   - Verify that when `connect()` fails (e.g. `ConnectionRefusedError`), `client.is_connected()` returns `False` and no socket FD is leaked.

3. `machine-learning/08_tensorflow_fundamentals/tf_compat.py`:
   - In `GradientTape.gradient(self, target, sources)`:
     Only pass tensors that have `_torch` and `requires_grad=True` to `torch.autograd.grad(..., allow_unused=True)`.
     For sources where `requires_grad` is False or missing, initialize the output gradient to zeros (`zeros(src.shape, dtype=src.dtype)`).
     Map the computed `torch_grads` back to their corresponding source indices.
     Ensure that when a mix of trainable and non-trainable variables are differentiated (or variables containing frozen tensors), the trainable variables receive their genuine non-zero gradients instead of collapsing to 0.

4. `machine-learning/assessment/practical_test.py`:
   - Fix legacy keyword arguments / warnings:
     - Check `machine-learning/01_ml_fundamentals/01_what_is_ml.py`: ensure `traditional_house_price` accepts kwargs or matches the example dict (e.g. `distance_km`).
     - Check `machine-learning/06_model_evaluation/02_cross_validation.py`: change `labels=` to `tick_labels=` for `ax.boxplot(...)` if matplotlib version expects `tick_labels`.
     - Increase timeout in `run_test()` for `02_backpropagation_and_deep_mlp.py` (e.g. from 120s to 180s) so it doesn't time out.
   - In `main()` of `practical_test.py`: ensure `if failed: sys.exit(1)` so test failures are properly propagated to exit codes.
   - Run `python3 machine-learning/assessment/practical_test.py` and verify that all tests pass cleanly with exit code 0.

5. Run Verification Suites and Direct Scripts:
   - `pytest tests/adversarial/test_challenger_2_adversarial.py -v`
   - `pytest tests/stress/test_adversarial_stress.py -v`
   - `pytest tests/e2e/test_deep_learning_e2e.py -v`
   - `pytest tests/e2e/test_math_game_ai_e2e.py -v`
   - `pytest tests/e2e/test_networking_tf_e2e.py -v`
   - `pytest tests/e2e/test_capstones_simulink_e2e.py -v`
   - `python3 tests/e2e/run_all_e2e_tests.py`
   - Confirm all suites pass with 100% success.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Write your report to `/home/settings/Documents/pearl/.agents/teamwork_preview_worker_remediation_2/handoff.md` and send a message when done.
