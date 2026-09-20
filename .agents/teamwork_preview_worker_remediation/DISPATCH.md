## 2026-09-18T15:53:44Z
You are the Remediation Worker for the curriculum completion project.
Your identity: teamwork_preview_worker_remediation
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_remediation

MANDATORY: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md first (under ## Follow-up — 2026-09-17T15:02:54Z).
Read /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_3/PROJECT.md.
Read /home/settings/Documents/pearl/.agents/teamwork_preview_reviewer_1/handoff.md.
Read /home/settings/Documents/pearl/.agents/teamwork_preview_challenger_2/handoff.md.

YOUR TASKS:
Apply the 4 precise fixes identified during Phase 2B Verification by Reviewer 1 and Challenger 2:

1. `game-ai/10_mcts/play_mcts.py`:
   - In `run_tictactoe_vs_minimax()`, add `random.seed(42)` at the start of the function and ensure non-loss threshold handles stochastic rollouts robustly (`mcts_losses <= 2`).
   - Run `python3 game-ai/10_mcts/play_mcts.py` and verify exit code 0.

2. `networking/01_tcp_ip/02_tcp_client.py`:
   - In `connect(self)`: wrap socket creation and `self._sock.connect((self.host, self.port))` in `try... except Exception: self.disconnect(); raise`.
   - Verify that when `connect()` fails (e.g. ConnectionRefusedError), `is_connected()` returns `False` and no socket FD is leaked.

3. `machine-learning/08_tensorflow_fundamentals/tf_compat.py`:
   - In `GradientTape.gradient(self, target, sources)`:
     Only pass tensors that have `t.requires_grad is True` to `torch.autograd.grad(..., allow_unused=True)`.
     For sources where `t.requires_grad is False`, set the gradient to zeros (`zeros(src.shape, dtype=src.dtype)`).
     Ensure that when a mix of trainable and non-trainable variables are differentiated, the trainable variables receive their genuine non-zero gradients instead of collapsing to 0.

4. `machine-learning/assessment/practical_test.py`:
   - Fix legacy keyword arguments / warnings:
     - Check Module 1 (e.g. `labels` -> `tick_labels` for matplotlib bar/boxplot if needed)
     - Check Module 2 `02_cross_validation.py` / distance keyword argument if needed
   - In `main()` of `practical_test.py`: ensure `if failed: sys.exit(1)` so test failures are properly propagated to exit codes.
   - Run `python3 machine-learning/assessment/practical_test.py` and verify that Module 9 and the overall suite pass cleanly with exit code 0.

5. Run Verification Suites:
   - `pytest tests/adversarial/test_challenger_2_adversarial.py -v`
   - `pytest tests/stress/test_adversarial_stress.py -v`
   - `pytest tests/e2e/test_deep_learning_e2e.py -v`
   - `pytest tests/e2e/test_networking_tf_e2e.py -v`
   - `python3 tests/e2e/run_all_e2e_tests.py`
   - Confirm all suites pass with 100% success.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work.

Write your report to `/home/settings/Documents/pearl/.agents/teamwork_preview_worker_remediation/handoff.md` and send a message when done.
