## 2026-09-17T15:22:02Z

You are Worker M4 for the curriculum completion project.
Your identity: teamwork_preview_worker_m4
Your working directory: /home/settings/Documents/pearl/.agents/teamwork_preview_worker_m4

MANDATORY: Read /home/settings/Documents/pearl/.agents/ORIGINAL_REQUEST.md first (under ## Follow-up — 2026-09-17T15:02:54Z, requirement R4).
Read /home/settings/Documents/pearl/.agents/teamwork_preview_orchestrator_3/PROJECT.md (Milestone M4).
Read /home/settings/Documents/pearl/.agents/teamwork_preview_explorer_survey_3/handoff.md (Sections 4.1, 4.2).

EXCLUSIVE OWNED WRITE PATHS:
- `machine-learning/solutions/capstone_solution.py`
- `game-ai/solutions/reversi_solution.py`
- `game-ai/capstone/reversi_starter.py`
- `game-ai/capstone/reversi_game.py`
- `engineering-mathematics/simulink/` (`03_rc_circuit_companion.m`, `04_thermal_cooling_companion.m`, `05_dc_motor_companion.m`, `mini_project_motor_control.m`, `exercises.m`, `models/thermal_cooling_model.md`, `models/dc_motor_model.md`)
- `engineering-mathematics/solutions/simulink_exercises_solution.m`
- `engineering-mathematics/solutions/probability_exercises_solution.m`
- `engineering-mathematics/solutions/capstone_solution.m`

TASKS:
1. Machine Learning Capstone Solution:
   - Implement `machine-learning/solutions/capstone_solution.py`: complete worked solution for `12_capstone/starter_template.py` covering EDA (distributions & correlation plots to `12_capstone/output/`), preprocessing (median imputation, StandardScaler, stratified split), classical ML (RandomForest + SVC classification, RandomForest + Ridge regression, CV, feature importance plot), PyTorch MLP (classification & regression), summary table, and engineering interpretation.
2. Reversi Game AI Capstone:
   - Implement `game-ai/solutions/reversi_solution.py` and complete `game-ai/capstone/reversi_starter.py` / `reversi_game.py`: full `OthelloState` (8 directions, bracketing, flips, pass handling, terminal detection), PST heuristic evaluation, Alpha-Beta minimax AI, Pygame visual mode, and headless self-play `play_game(ai_depth=2)` for CI.
3. Simulink Dynamic Modeling & Motor Control (`engineering-mathematics/simulink/`):
   - `03_rc_circuit_companion.m`: ODE45 RC filter charging, rise/settling time, analytical exponential comparison.
   - `04_thermal_cooling_companion.m`: ODE45 convective cooling with ambient feedback and pulse heating.
   - `05_dc_motor_companion.m`: ODE45 coupled electromechanical DC motor state-space simulation under load step.
   - `mini_project_motor_control.m`: Closed-loop PI speed control with anti-windup clamping, load torque step rejection, performance scorecard (t_r < 0.5s, %OS < 10%, e_ss = 0).
   - Blueprints: `models/thermal_cooling_model.md` and `models/dc_motor_model.md` matching `models/rc_circuit_model.md`.
   - `exercises.m`: 4-tier progressive exercises with `% TODO`.
   - Solutions in `engineering-mathematics/solutions/`: `simulink_exercises_solution.m`, `probability_exercises_solution.m`, and `capstone_solution.m`.
4. Run builds/tests:
   - `python3 machine-learning/solutions/capstone_solution.py`
   - `python3 -c "from game_ai.solutions.reversi_solution import play_game; print(play_game(ai_depth=2))"` (or local module import)
   - `python3 engineering-mathematics/scripts/verify_package.py --all`
   - `pytest engineering-mathematics/tests/ -v`
   Document commands and test outcomes in your handoff report.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Write your report to `/home/settings/Documents/pearl/.agents/teamwork_preview_worker_m4/handoff.md` and send a message when done.
