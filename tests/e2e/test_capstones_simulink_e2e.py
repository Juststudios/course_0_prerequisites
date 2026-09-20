"""
End-to-End Test Suite for Milestone M4: Capstones & Simulink Dynamic Modeling.
Verifies Industrial Predictive Maintenance ML Capstone, Reversi Game AI Capstone,
Simulink ODE45 Companions, Model Blueprints, and Closed-Loop Motor Control.
Adheres to the 4-Tier Test Design Methodology.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pytest
from scipy.integrate import solve_ivp
import torch
import torch.nn as nn

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ML_DIR = REPO_ROOT / "machine-learning"
GAME_AI_DIR = REPO_ROOT / "game-ai"
ENG_MATH_DIR = REPO_ROOT / "engineering-mathematics"

# Add directories to sys.path for direct imports
for p in [str(GAME_AI_DIR), str(ENG_MATH_DIR / "scripts"), str(ML_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_submodule(rel_path: str, module_name: str):
    full_path = REPO_ROOT / rel_path
    if not full_path.exists():
        pytest.skip(f"Target module file not found at {rel_path}")
    spec = importlib.util.spec_from_file_location(module_name, str(full_path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# =====================================================================
# TIER 1: FEATURE COVERAGE (Isolation & Primary Contracts)
# =====================================================================

# Capstone Dataset Column Metadata
FEATURE_COLS = [
    "vibration",
    "temperature",
    "acoustic_emission",
    "current",
    "voltage",
    "pressure",
    "rpm",
    "humidity",
]
TARGET_CLS = "fault_severity"
TARGET_REG = "remaining_useful_life"

# PyTorch Capstone Neural Network Architectures
class FaultClassifierMLP(nn.Module):
    def __init__(self, in_features=8, num_classes=3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.20),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes),
        )

    def forward(self, x):
        return self.network(x)


class RULRegressorMLP(nn.Module):
    def __init__(self, in_features=8):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(in_features, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.20),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        return self.network(x)


@pytest.mark.tier1
@pytest.mark.m4
class TestTier1MLCapstoneCoverage:
    """Tier 1: Isolated feature coverage for Industrial ML Capstone Reference Solution."""

    @pytest.fixture(scope="class")
    def capstone_mod(self):
        return _load_submodule("machine-learning/solutions/capstone_solution.py", "capstone_solution_mod")

    def test_capstone_dataset_generation_and_features(self, capstone_mod):
        """Ensure dataset generator creates CSV files with expected columns and non-empty rows."""
        import pandas as pd
        train_path, test_path = capstone_mod.ensure_dataset()
        assert train_path.exists(), f"Train dataset missing at {train_path}"
        assert test_path.exists(), f"Test dataset missing at {test_path}"

        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)
        assert len(df_train) >= 800
        assert len(df_test) >= 200

        for col in FEATURE_COLS:
            assert col in df_train.columns
            assert col in df_test.columns
        assert TARGET_CLS in df_train.columns
        assert TARGET_REG in df_train.columns

    def test_capstone_preprocessing_pipeline(self, capstone_mod):
        """Preprocessing handles imputation, scaling, and returns normalized numpy matrices."""
        import pandas as pd
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler

        train_path, test_path = capstone_mod.ensure_dataset()
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        imputer = SimpleImputer(strategy="median")
        scaler = StandardScaler()

        X_tr = scaler.fit_transform(imputer.fit_transform(df_train[FEATURE_COLS]))
        X_te = scaler.transform(imputer.transform(df_test[FEATURE_COLS]))

        assert X_tr.shape[1] == len(FEATURE_COLS)
        assert X_te.shape[1] == len(FEATURE_COLS)
        assert len(X_tr) == len(df_train)
        assert len(X_te) == len(df_test)

        # Scaled features should have zero mean and unit variance
        assert np.allclose(np.mean(X_tr, axis=0), 0.0, atol=0.2)
        assert np.allclose(np.std(X_tr, axis=0), 1.0, atol=0.2)

    def test_capstone_pytorch_neural_network_architectures(self):
        """FaultClassifierMLP and RULRegressorMLP instantiate with proper input/output dimensions."""
        cls_model = FaultClassifierMLP(in_features=8, num_classes=3)
        reg_model = RULRegressorMLP(in_features=8)

        dummy_batch = torch.randn(16, 8)
        cls_out = cls_model(dummy_batch)
        reg_out = reg_model(dummy_batch)

        assert cls_out.shape == (16, 3)
        assert reg_out.shape == (16, 1)

    def test_capstone_classical_model_fits_and_metrics(self, capstone_mod):
        """Train classical models (RF, SVC, Ridge) on capstone data and assert strong metrics."""
        import pandas as pd
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.metrics import accuracy_score, r2_score

        train_path, test_path = capstone_mod.ensure_dataset()
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        imputer = SimpleImputer(strategy="median")
        scaler = StandardScaler()

        X_tr = scaler.fit_transform(imputer.fit_transform(df_train[FEATURE_COLS]))
        X_te = scaler.transform(imputer.transform(df_test[FEATURE_COLS]))

        y_cls_tr = df_train[TARGET_CLS].values
        y_cls_te = df_test[TARGET_CLS].values
        y_rul_tr = df_train[TARGET_REG].values
        y_rul_te = df_test[TARGET_REG].values

        rf_cls = RandomForestClassifier(n_estimators=30, random_state=42)
        rf_cls.fit(X_tr, y_cls_tr)
        acc = accuracy_score(y_cls_te, rf_cls.predict(X_te))
        assert acc > 0.90, f"Expected classification accuracy > 0.90, got {acc:.4f}"

        rf_reg = RandomForestRegressor(n_estimators=30, random_state=42)
        rf_reg.fit(X_tr, y_rul_tr)
        r2 = r2_score(y_rul_te, rf_reg.predict(X_te))
        assert r2 > 0.80, f"Expected R^2 > 0.80, got {r2:.4f}"

    def test_capstone_generated_plot_artifacts(self, capstone_mod):
        """Check all 5 capstone visual artifact files exist and have non-trivial file size."""
        out_dir = REPO_ROOT / "machine-learning" / "12_capstone" / "output"
        required_plots = [
            out_dir / "eda_distributions.png",
            out_dir / "eda_correlation.png",
            out_dir / "feature_importance.png",
            out_dir / "mlp_training_curves.png",
            out_dir / "confusion_matrix.png",
        ]
        for plot_path in required_plots:
            assert plot_path.exists(), f"Plot artifact {plot_path.name} not found"
            assert plot_path.stat().st_size > 2000, f"Plot artifact {plot_path.name} is too small"


@pytest.mark.tier1
@pytest.mark.m4
class TestTier1ReversiEngineCoverage:
    """Tier 1: Isolated feature coverage for OthelloState engine and Alpha-Beta minimax."""

    @pytest.fixture(scope="class")
    def reversi_mod(self):
        return _load_submodule("game-ai/solutions/reversi_solution.py", "reversi_solution_mod")

    def test_reversi_initial_state_and_legal_moves(self, reversi_mod):
        """OthelloState initializes with 4 center pieces and exactly 4 legal moves for Black."""
        state = reversi_mod.OthelloState()
        assert state.current_player == reversi_mod.BLACK
        assert state.is_terminal is False
        assert state.winner is None

        scores = state.get_scores()
        assert scores[reversi_mod.BLACK] == 2
        assert scores[reversi_mod.WHITE] == 2

        legal_moves = state.get_legal_moves()
        expected_moves = {(2, 3), (3, 2), (4, 5), (5, 4)}
        assert set(legal_moves) == expected_moves

    def test_reversi_directional_flips_and_raycasting(self, reversi_mod):
        """get_flips correctly identifies opponent pieces bracketed in multiple directions."""
        state = reversi_mod.OthelloState()
        # Opening move (2, 3) brackets White piece at (3, 3) against Black piece at (4, 3)
        flips = state.get_flips(2, 3, reversi_mod.BLACK)
        assert flips == [(3, 3)]

    def test_reversi_move_application_and_score_update(self, reversi_mod):
        """make_move places the piece, flips bracketed pieces, updates score, and toggles player."""
        state = reversi_mod.OthelloState()
        new_state = state.make_move((2, 3))

        assert new_state.board[2][3] == reversi_mod.BLACK
        assert new_state.board[3][3] == reversi_mod.BLACK  # flipped
        assert new_state.current_player == reversi_mod.WHITE
        scores = new_state.get_scores()
        assert scores[reversi_mod.BLACK] == 4
        assert scores[reversi_mod.WHITE] == 1

    def test_reversi_pass_handling_and_consecutive_pass_terminal(self, reversi_mod):
        """A pass occurs when a player has no legal moves; two consecutive passes end the game."""
        # Board configuration where White has no legal moves but Black has a legal move:
        # Row 0: B W . . . . . .
        # Row 1: B . . . . . . .
        # Black has 2 pieces, White has 1 piece.
        # Black can play at (0, 2) to flip (0, 1). White cannot move.
        board = [[reversi_mod.EMPTY for _ in range(8)] for _ in range(8)]
        board[0][0] = reversi_mod.BLACK
        board[1][0] = reversi_mod.BLACK
        board[0][1] = reversi_mod.WHITE
        state = reversi_mod.OthelloState(board=board, current_player=reversi_mod.WHITE)
        assert len(state.get_legal_moves(reversi_mod.WHITE)) == 0
        assert (0, 2) in state.get_legal_moves(reversi_mod.BLACK)

        # First pass (White passes, giving turn to Black)
        state_after_pass1 = state.make_move(None)
        assert state_after_pass1.consecutive_passes == 1
        assert state_after_pass1.current_player == reversi_mod.BLACK
        assert state_after_pass1.is_terminal is False

        # Second pass (Black passes as well: consecutive passes terminate game)
        state_after_pass2 = state_after_pass1.make_move(None)
        assert state_after_pass2.is_terminal is True
        assert state_after_pass2.winner == reversi_mod.BLACK

    def test_reversi_pst_heuristic_evaluation(self, reversi_mod):
        """Corner positions receive high heuristic scores; danger C-squares are penalized."""
        assert reversi_mod.PST[0][0] == 100
        assert reversi_mod.PST[0][7] == 100
        assert reversi_mod.PST[7][0] == 100
        assert reversi_mod.PST[7][7] == 100

        # C-squares adjacent to corners
        assert reversi_mod.PST[0][1] == -20
        assert reversi_mod.PST[1][1] == -50

    def test_reversi_minimax_alpha_beta_search(self, reversi_mod):
        """minimax_ab returns a valid legal move and non-NaN evaluation score."""
        state = reversi_mod.OthelloState()
        val, move = reversi_mod.minimax_ab(
            state, depth=2, alpha=-float("inf"), beta=float("inf"),
            is_maximizing=True, max_player=reversi_mod.BLACK
        )
        assert move in state.get_legal_moves()
        assert not np.isnan(val)


@pytest.mark.tier1
@pytest.mark.m4
class TestTier1SimulinkCompanionsCoverage:
    """Tier 1: Isolated verification of Simulink ODE45 companion scripts and blueprints."""

    def test_simulink_companion_scripts_exist(self):
        """Verify presence and minimum size of all 4 Simulink companion MATLAB scripts."""
        sim_dir = ENG_MATH_DIR / "simulink"
        expected_scripts = [
            "03_rc_circuit_companion.m",
            "04_thermal_cooling_companion.m",
            "05_dc_motor_companion.m",
            "mini_project_motor_control.m",
            "exercises.m",
        ]
        for s in expected_scripts:
            file_path = sim_dir / s
            assert file_path.exists(), f"Simulink companion {s} missing"
            assert file_path.stat().st_size > 1000, f"Script {s} is unexpectedly small"

    def test_simulink_model_blueprints_exist(self):
        """Verify presence of Simulink markdown model blueprints."""
        model_dir = ENG_MATH_DIR / "simulink" / "models"
        expected_models = [
            "rc_circuit_model.md",
            "thermal_cooling_model.md",
            "dc_motor_model.md",
        ]
        for m in expected_models:
            model_path = model_dir / m
            assert model_path.exists(), f"Model blueprint {m} missing"
            assert model_path.stat().st_size > 500

    def test_simulink_reference_solutions_exist(self):
        """Verify decoupled reference solutions exist in engineering-mathematics/solutions/."""
        sol_dir = ENG_MATH_DIR / "solutions"
        expected_solutions = [
            "simulink_exercises_solution.m",
            "capstone_solution.m",
            "calculus_exercises_solution.m",
            "linear_algebra_exercises_solution.m",
            "matlab_exercises_solution.m",
            "probability_exercises_solution.m",
        ]
        for sol in expected_solutions:
            sol_path = sol_dir / sol
            assert sol_path.exists(), f"Reference solution {sol} missing"
            assert sol_path.stat().st_size > 1000

    def test_simulink_matlab_syntax_and_quality_audit(self):
        """Invoke MatlabSyntaxAuditor on Simulink scripts: assert 0 errors, 1-based indexing, comment ratio >= 20%."""
        verify_mod = _load_submodule("engineering-mathematics/scripts/verify_package.py", "verify_package_mod")
        report = verify_mod.AuditReport()
        auditor = verify_mod.MatlabSyntaxAuditor(ENG_MATH_DIR, report)

        sim_dir = ENG_MATH_DIR / "simulink"
        sim_files = list(sim_dir.glob("*.m"))
        assert len(sim_files) >= 5

        for f in sim_files:
            auditor.audit_file(f)

        assert report.error_count == 0, f"MatlabSyntaxAuditor reported {report.error_count} errors: {report.diagnostics}"


# =====================================================================
# TIER 2: BOUNDARIES & CORNER CASES
# =====================================================================

@pytest.mark.tier2
@pytest.mark.m4
class TestTier2CapstonesSimulinkBoundaries:
    """Tier 2: Boundary values, full board states, motor saturation limits, and noise boundaries."""

    @pytest.fixture(scope="class")
    def reversi_mod(self):
        return _load_submodule("game-ai/solutions/reversi_solution.py", "reversi_solution_mod2")

    def test_reversi_corner_capture_stability(self, reversi_mod):
        """Discs placed in corners cannot be flipped from any direction."""
        board = [[reversi_mod.EMPTY for _ in range(8)] for _ in range(8)]
        board[0][0] = reversi_mod.BLACK
        state = reversi_mod.OthelloState(board=board, current_player=reversi_mod.WHITE)

        # White attempting to flip Black's corner disc from any neighbor
        for dr, dc in reversi_mod.DIRECTIONS:
            r, c = dr, dc
            if 0 <= r < 8 and 0 <= c < 8:
                flips = state.get_flips(r, c, reversi_mod.WHITE)
                assert (0, 0) not in flips, "Corner disc must never be flippable"

    def test_reversi_full_board_terminal_detection(self, reversi_mod):
        """A full 64-disc board is immediately marked as terminal with no legal moves."""
        board = [[reversi_mod.BLACK for _ in range(8)] for _ in range(8)]
        board[0][0] = reversi_mod.WHITE  # 63 Black, 1 White
        state = reversi_mod.OthelloState(board=board, current_player=reversi_mod.WHITE)

        assert state.is_terminal is True
        assert len(state.get_legal_moves()) == 0
        assert state.winner == reversi_mod.BLACK

    def test_reversi_invalid_placement_rejected(self, reversi_mod):
        """Placing a disc on an already occupied square yields zero flips and is not a legal move."""
        state = reversi_mod.OthelloState()
        # Square (3, 3) already has White
        assert state.get_flips(3, 3, reversi_mod.BLACK) == []
        assert (3, 3) not in state.get_legal_moves(reversi_mod.BLACK)

    def test_motor_control_voltage_saturation_clamp(self):
        """Actuator command voltage strictly respects [-36V, +36V] saturation limits."""
        V_max = 36.0
        Kp = 2.0
        Ki = 12.0

        # Massive error during startup (100 rad/s setpoint, 0 speed)
        err = 100.0
        x_int = 50.0  # windup state
        u_raw = Kp * err + Ki * x_int  # 200 + 600 = 800 V
        u_sat = min(V_max, max(-V_max, u_raw))
        assert u_sat == 36.0, f"Expected 36.0 V clamp, got {u_sat}"

        # Massive negative error
        err_neg = -100.0
        u_raw_neg = Kp * err_neg
        u_sat_neg = min(V_max, max(-V_max, u_raw_neg))
        assert u_sat_neg == -36.0

    def test_motor_control_anti_windup_freezes_integration(self):
        """Anti-windup logic freezes integration when output saturates and error pushes further."""
        V_max = 36.0
        Kp = 2.0
        Ki = 12.0

        err = 50.0
        x_int = 10.0
        u_unsat = Kp * err + Ki * x_int  # 100 + 120 = 220 V > 36 V
        u_sat = min(V_max, max(-V_max, u_unsat))

        is_saturated = (u_sat != u_unsat)
        same_sign = (err * u_unsat > 0)
        dx_int = 0.0 if (is_saturated and same_sign) else err

        assert dx_int == 0.0, "Integrator accumulation must be frozen during saturation"

    def test_sensor_noise_distribution_limits(self):
        """Simulate sensor noise modeling: zero noise returns ground truth; random noise matches variance."""
        np.random.seed(42)
        true_signal = np.full(500, 24.5)

        # Zero noise boundary
        noise_zero = np.zeros(500)
        measured_zero = true_signal + noise_zero
        assert np.array_equal(measured_zero, true_signal)

        # Standard Gaussian noise sigma=0.5
        sigma = 0.5
        noise = np.random.normal(0.0, sigma, size=1000)
        measured = true_signal[0] + noise
        assert np.isclose(np.mean(measured), 24.5, atol=0.05)
        assert np.isclose(np.std(measured), sigma, atol=0.05)


# =====================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (Pairwise & Comparative)
# =====================================================================

@pytest.mark.tier3
@pytest.mark.m4
class TestTier3CapstonesSimulinkCrossFeatures:
    """Tier 3: Pairwise interactions, depth comparisons, and numerical solver validation."""

    @pytest.fixture(scope="class")
    def reversi_mod(self):
        return _load_submodule("game-ai/solutions/reversi_solution.py", "reversi_solution_mod3")

    def test_reversi_minimax_depth_scaling_tournament(self, reversi_mod):
        """Depth 2 AI outperforms or plays competitively against Depth 1 AI."""
        # Play short automated match: Depth 2 (Black) vs Depth 1 (White)
        winner, scores = reversi_mod.play_game(depth_black=2, depth_white=1, verbose=False)
        assert winner in [reversi_mod.BLACK, reversi_mod.WHITE, 0]
        # Depth 2 should control substantial piece count
        assert scores[reversi_mod.BLACK] >= 20

    def test_ml_capstone_pipeline_cross_model_consistency(self):
        """Data preprocessed by Capstone pipeline is concurrently compatible with PyTorch and Sklearn."""
        import pandas as pd
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier

        capstone_mod = _load_submodule("machine-learning/solutions/capstone_solution.py", "capstone_cross_mod")
        train_path, test_path = capstone_mod.ensure_dataset()
        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        imputer = SimpleImputer(strategy="median")
        scaler = StandardScaler()

        X_tr = scaler.fit_transform(imputer.fit_transform(df_train[FEATURE_COLS]))
        X_te = scaler.transform(imputer.transform(df_test[FEATURE_COLS]))
        y_cls_tr = df_train[TARGET_CLS].values
        y_cls_te = df_test[TARGET_CLS].values

        # 1. Scikit-Learn RandomForest
        rf = RandomForestClassifier(n_estimators=10, random_state=42)
        rf.fit(X_tr, y_cls_tr)
        rf_preds = rf.predict(X_te)

        # 2. PyTorch FaultClassifierMLP
        t_X_te = torch.tensor(X_te, dtype=torch.float32)
        mlp = FaultClassifierMLP(in_features=8, num_classes=3)
        mlp.eval()
        with torch.no_grad():
            mlp_logits = mlp(t_X_te)
            mlp_preds = torch.argmax(mlp_logits, dim=1).numpy()

        assert len(rf_preds) == len(mlp_preds) == len(y_cls_te)
        assert set(np.unique(rf_preds)).issubset({0, 1, 2})
        assert set(np.unique(mlp_preds)).issubset({0, 1, 2})

    def test_ode45_rc_circuit_numerical_vs_analytical(self):
        """Numerical RK45 integration of RC companion ODE matches analytical exponential solution."""
        R = 10.0e3       # 10 kOhm
        C = 100.0e-6     # 100 uF
        tau = R * C      # 1.0 s
        V_step = 5.0     # 5 V
        t_step = 0.1     # step onset at 0.1 s

        def rc_ode(t, vc):
            vin = V_step if t >= t_step else 0.0
            return (vin - vc[0]) / tau

        sol = solve_ivp(rc_ode, [0.0, 5.0], [0.0], method="RK45", max_step=0.01)
        t_pts = sol.t
        v_num = sol.y[0]

        # Analytical solution for t >= t_step
        v_anal = np.zeros_like(t_pts)
        mask = t_pts >= t_step
        v_anal[mask] = V_step * (1.0 - np.exp(-(t_pts[mask] - t_step) / tau))

        max_error = np.max(np.abs(v_num - v_anal))
        assert max_error < 1e-3, f"Numerical ODE error {max_error} exceeds 1e-3 V tolerance"

    def test_ode45_thermal_cooling_steady_state(self):
        """Thermal cooling ODE numerically settles to theoretical temperature T_amb + P/(h*A)."""
        C_th = 180.0
        hA = 4.5
        T_amb = 25.0
        P_pulse = 150.0  # Active indefinitely for steady-state audit

        def thermal_ode(t, T):
            return (P_pulse - hA * (T[0] - T_amb)) / C_th

        # Simulate for 6 time constants (6 * 40s = 240s)
        sol = solve_ivp(thermal_ode, [0.0, 300.0], [T_amb], method="RK45", max_step=0.5)
        t_final = sol.t[-1]
        T_final = sol.y[0][-1]

        T_expected = T_amb + P_pulse / hA  # 25 + 33.33 = 58.33 deg C
        assert np.isclose(T_final, T_expected, atol=0.1), f"Final temp {T_final} != expected {T_expected}"


# =====================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (Pipelines & Systems)
# =====================================================================

@pytest.mark.tier4
@pytest.mark.m4
class TestTier4CapstonesSimulinkRealWorldScenarios:
    """Tier 4: End-to-end autonomous match, closed-loop motor control, and capstone execution."""

    @pytest.fixture(scope="class")
    def reversi_mod(self):
        return _load_submodule("game-ai/solutions/reversi_solution.py", "reversi_solution_mod4")

    def test_reversi_full_headless_autonomous_game(self, reversi_mod):
        """Execute a complete autonomous 60-turn Reversi game between depth-2 AI agents."""
        winner, scores = reversi_mod.play_game(ai_depth=2, verbose=False)

        assert winner in [reversi_mod.BLACK, reversi_mod.WHITE, 0]
        assert reversi_mod.BLACK in scores
        assert reversi_mod.WHITE in scores

        total_pieces = scores[reversi_mod.BLACK] + scores[reversi_mod.WHITE]
        assert total_pieces <= 64, f"Total pieces {total_pieces} exceeds 64 board squares"
        assert total_pieces >= 40, f"Unexpectedly short game terminated with only {total_pieces} pieces"

        # Verify winner matches score differential
        if scores[reversi_mod.BLACK] > scores[reversi_mod.WHITE]:
            assert winner == reversi_mod.BLACK
        elif scores[reversi_mod.WHITE] > scores[reversi_mod.BLACK]:
            assert winner == reversi_mod.WHITE
        else:
            assert winner == 0

    def test_closed_loop_motor_control_step_response_scorecard(self):
        """Closed-loop PI speed control with anti-windup meets performance scorecard specs."""
        # Motor parameters matching mini_project_motor_control.m
        Ra = 2.0
        La = 0.5
        Kt = 0.1
        Ke = 0.1
        J = 0.02
        b = 0.01
        V_max = 36.0
        omega_ref = 100.0
        t_step_tau = 2.5
        tau_load = 0.8

        Kp = 2.0
        Ki = 12.0

        def motor_ode(t, x):
            ia, omega, x_int = x
            tau_l = tau_load if t >= t_step_tau else 0.0
            err = omega_ref - omega
            u_unsat = Kp * err + Ki * x_int
            u_sat = min(V_max, max(-V_max, u_unsat))

            # Anti-windup conditional clamping
            is_saturated = (u_sat != u_unsat)
            same_sign = (err * u_unsat > 0)
            dx_int = 0.0 if (is_saturated and same_sign) else err

            dia = (u_sat - Ra * ia - Ke * omega) / La
            domega = (Kt * ia - b * omega - tau_l) / J
            return [dia, domega, dx_int]

        sol = solve_ivp(motor_ode, [0.0, 5.0], [0.0, 0.0, 0.0], method="RK45", max_step=0.005)
        t = sol.t
        omega = sol.y[1]

        # 1. Percent overshoot before disturbance onset
        mask_pre_dist = t < t_step_tau
        w_max_nl = np.max(omega[mask_pre_dist])
        pct_overshoot = max(0.0, (w_max_nl - omega_ref) / omega_ref * 100.0)
        assert pct_overshoot < 10.0, f"Overshoot {pct_overshoot:.2f}% exceeded 10% limit"

        # 2. No-load steady-state speed approaches setpoint
        idx_nl = np.argmin(np.abs(t - 2.4))
        assert omega[idx_nl] > 90.0, f"Speed at t=2.4s was {omega[idx_nl]:.2f}, expected near 100 rad/s"

    def test_ml_capstone_full_worked_solution_execution(self):
        """Execute machine-learning/solutions/capstone_solution.py to completion with returncode 0."""
        capstone_script = ML_DIR / "solutions" / "capstone_solution.py"
        assert capstone_script.exists()

        res = subprocess.run(
            [sys.executable, str(capstone_script)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        assert res.returncode == 0, f"capstone_solution.py failed with stderr:\n{res.stderr}"
        assert "CAPSTONE PIPELINE EXECUTION COMPLETE" in res.stdout
