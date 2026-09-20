"""
Adversarial Stress Test Suite: Empirical Verification of ML, Math & Game AI.
Authored by: Challenger 1 (teamwork_preview_challenger_1)

Scope:
  1. Checkers engine: Mandatory jumps, multi-jump sequences, king backward moves,
     stalemate/blocked pieces, 40-move draw, illegal moves in terminal states,
     crowning on steps vs jumps, multiple piece jump options.
  2. MCTS: Rollout stability, terminal node expansion, single-move fast path,
     determinism under fixed seed, immediate winning move identification.
  3. Tabular Q-Learning: GridWorld edge/wall collisions, convergence across discount factors (gamma),
     Q-value mathematical bounds, epsilon decay monotonicity, tie-breaking symmetry,
     alpha=0 zero-learning invariance, policy extraction.
  4. PCA from Scratch: Rank-deficient matrices, constant/zero features, 1D data,
     high-dimensional data (N < D), exact parity with scikit-learn PCA,
     scale invariance/extreme scales, float n_components threshold, input validation.
  5. Logistic Regression GD: Linearly separable data (overflow resistance), colinear features,
     zero iterations (max_iter=0), OvR multiclass and non-consecutive labels,
     threshold sensitivity, input dimension validation.
  6. Neural Networks: Batch size 1 under BatchNorm eval vs train mode,
     Dropout rate 0.0 vs 1.0, dropout expectation preservation, Kaiming He initialization,
     and backpropagation zero/non-zero gradient flow through DeepFaultClassifier.
"""

import math
import random
import sys
from pathlib import Path
import numpy as np
import pytest
import torch
import torch.nn as nn
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.linear_model import LogisticRegression as SklearnLogReg

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Module imports
sys.path.insert(0, str(REPO_ROOT / "game-ai" / "08_checkers"))
import checkers
from checkers import (
    CheckersState, EMPTY, RED_MAN, BLACK_MAN, RED_KING, BLACK_KING,
    PLAYER_RED, PLAYER_BLACK
)

sys.path.insert(0, str(REPO_ROOT / "game-ai" / "10_mcts"))
import mcts
from mcts import MCTS, MCTSNode

sys.path.insert(0, str(REPO_ROOT / "game-ai" / "03_tic_tac_toe"))
from tic_tac_toe import TicTacToeState

sys.path.insert(0, str(REPO_ROOT / "game-ai" / "11_reinforcement_learning"))
import gridworld
from gridworld import (
    GridWorld, ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT
)
import q_learning
from q_learning import QLearningAgent

sys.path.insert(0, str(REPO_ROOT / "machine-learning" / "05_clustering"))
import importlib.util
spec_pca = importlib.util.spec_from_file_location(
    "pca_scratch_mod",
    str(REPO_ROOT / "machine-learning" / "05_clustering" / "04_pca_from_scratch.py")
)
pca_mod = importlib.util.module_from_spec(spec_pca)
spec_pca.loader.exec_module(pca_mod)
PCAScratch = pca_mod.PCAScratch

spec_lr = importlib.util.spec_from_file_location(
    "logistic_regression_gd_mod",
    str(REPO_ROOT / "machine-learning" / "04_classification" / "01_logistic_regression_gd.py")
)
lr_mod = importlib.util.module_from_spec(spec_lr)
spec_lr.loader.exec_module(lr_mod)
LogisticRegressionGD = lr_mod.LogisticRegressionGD
LogisticRegressionOVR = lr_mod.LogisticRegressionOVR
stable_sigmoid = lr_mod.stable_sigmoid

spec_dl = importlib.util.spec_from_file_location(
    "deep_mlp_mod",
    str(REPO_ROOT / "machine-learning" / "09_neural_networks" / "05_deep_mlp_project.py")
)
dl_mod = importlib.util.module_from_spec(spec_dl)
spec_dl.loader.exec_module(dl_mod)
DeepFaultClassifier = dl_mod.DeepFaultClassifier
init_weights_kaiming = dl_mod.init_weights_kaiming


# =============================================================================
# 1. CHECKERS ENGINE STRESS TESTS
# =============================================================================

class TestCheckersAdversarialStress:
    """Adversarial boundary testing for Checkers game engine."""

    def test_mandatory_jumps_suppress_simple_steps(self):
        """When any jump exists, no simple diagonal steps may be returned."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[5, 2] = RED_MAN
        b[4, 3] = BLACK_MAN
        b[5, 6] = RED_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)

        legal_moves = state.get_legal_moves()
        assert len(legal_moves) > 0, "Expected at least one legal move"
        for move in legal_moves:
            assert abs(move[1][0] - move[0][0]) == 2, (
                f"Non-jump move {move} returned when mandatory jump was available!"
            )
        start_positions = [m[0] for m in legal_moves]
        assert (5, 6) not in start_positions, "Piece without jump was allowed to move during mandatory capture!"

    def test_multiple_pieces_with_mandatory_jumps(self):
        """When multiple pieces have jumps, all jump paths must be available, but zero steps."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[5, 2] = RED_MAN
        b[4, 3] = BLACK_MAN  # can jump to (3, 4)
        b[5, 6] = RED_MAN
        b[4, 7] = BLACK_MAN  # wait, (4, 7) cannot be jumped to (3, 8) out of bounds
        b[4, 5] = BLACK_MAN  # can jump to (3, 4) if open, or put at (4, 7) not jumpable
        # Put black at (4, 5) so Red at (5, 6) can jump over (4, 5) to (3, 4)
        # But (3, 4) is shared landing square. Let's make separate landing squares:
        # Red at (5, 2) jumps Black at (4, 1) -> lands at (3, 0)
        # Red at (5, 4) jumps Black at (4, 5) -> lands at (3, 6)
        b = np.zeros((8, 8), dtype=np.int8)
        b[5, 2] = RED_MAN
        b[4, 1] = BLACK_MAN
        b[5, 4] = RED_MAN
        b[4, 5] = BLACK_MAN
        # Red piece at (6, 7) has only simple steps
        b[6, 7] = RED_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)

        moves = state.get_legal_moves()
        starts = {m[0] for m in moves}
        assert (5, 2) in starts
        assert (5, 4) in starts
        assert (6, 7) not in starts, "Step move included when jumps available"

    def test_multi_jump_sequence_and_intermediate_capture(self):
        """Piece must complete the full multi-jump sequence and remove all jumped pieces."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[6, 1] = RED_MAN
        b[5, 2] = BLACK_MAN
        b[3, 4] = BLACK_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)

        moves = state.get_legal_moves()
        expected_move = ((6, 1), (4, 3), (2, 5))
        assert expected_move in moves, f"Expected multi-jump {expected_move} in legal moves: {moves}"
        assert ((6, 1), (4, 3)) not in moves, "Partial jump allowed when multi-jump was available!"

        new_state = state.make_move(expected_move)
        assert new_state.board[6, 1] == EMPTY
        assert new_state.board[5, 2] == EMPTY, "First captured piece was not removed!"
        assert new_state.board[4, 3] == EMPTY, "Intermediate landing square must be empty!"
        assert new_state.board[3, 4] == EMPTY, "Second captured piece was not removed!"
        assert new_state.board[2, 5] == RED_MAN, "Piece failed to land on destination square!"
        assert new_state.current_player == PLAYER_BLACK

    def test_crowning_stops_multi_jump_immediately(self):
        """In American Checkers, reaching king row ends the turn even if a jump is open."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[2, 1] = RED_MAN
        b[1, 2] = BLACK_MAN
        b[1, 4] = BLACK_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)

        moves = state.get_legal_moves()
        assert ((2, 1), (0, 3)) in moves
        new_state = state.make_move(((2, 1), (0, 3)))
        assert new_state.board[0, 3] == RED_KING, "Piece was not crowned to King!"
        assert new_state.current_player == PLAYER_BLACK, "Turn did not toggle after crowning!"

    def test_crowning_on_normal_step(self):
        """Red reaching row 0 or Black reaching row 7 on a simple step is crowned King."""
        # Red crowning (needs at least one Black piece so game is not already won)
        b_red = np.zeros((8, 8), dtype=np.int8)
        b_red[1, 2] = RED_MAN
        b_red[7, 6] = BLACK_MAN
        state_red = CheckersState(board=b_red, current_player=PLAYER_RED)
        moves_red = state_red.get_legal_moves()
        assert ((1, 2), (0, 1)) in moves_red or ((1, 2), (0, 3)) in moves_red
        chosen_move = ((1, 2), (0, 1)) if ((1, 2), (0, 1)) in moves_red else ((1, 2), (0, 3))
        next_red = state_red.make_move(chosen_move)
        assert next_red.board[chosen_move[1]] == RED_KING

        # Black crowning (needs at least one Red piece so game is not already won)
        b_blk = np.zeros((8, 8), dtype=np.int8)
        b_blk[6, 1] = BLACK_MAN
        b_blk[0, 7] = RED_MAN
        state_blk = CheckersState(board=b_blk, current_player=PLAYER_BLACK)
        moves_blk = state_blk.get_legal_moves()
        assert ((6, 1), (7, 0)) in moves_blk or ((6, 1), (7, 2)) in moves_blk
        chosen_move_blk = ((6, 1), (7, 0)) if ((6, 1), (7, 0)) in moves_blk else ((6, 1), (7, 2))
        next_blk = state_blk.make_move(chosen_move_blk)
        assert next_blk.board[chosen_move_blk[1]] == BLACK_KING

    def test_king_backward_moves_and_jumps(self):
        """Kings must move and jump backward as well as forward."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[3, 3] = RED_KING
        b[2, 2] = BLACK_MAN
        b[2, 4] = BLACK_MAN
        b[4, 2] = BLACK_MAN
        b[4, 4] = BLACK_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)

        moves = state.get_legal_moves()
        destinations = {m[-1] for m in moves}
        assert (1, 1) in destinations  # Up-left
        assert (1, 5) in destinations  # Up-right
        assert (5, 1) in destinations  # Down-left (backward for Red)
        assert (5, 5) in destinations  # Down-right (backward for Red)

    def test_stalemate_no_legal_moves_triggers_loss(self):
        """If a player has pieces but zero legal moves, they lose immediately."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[7, 0] = RED_MAN
        b[6, 1] = BLACK_MAN
        b[5, 2] = BLACK_MAN  # Blocks jump
        state = CheckersState(board=b, current_player=PLAYER_RED)

        assert state.is_terminal, "State with no legal moves must be terminal!"
        assert state.winner == PLAYER_BLACK, "Blocked player must be declared the loser!"
        assert len(state.get_legal_moves()) == 0

    def test_zero_pieces_triggers_immediate_loss(self):
        """Player with 0 pieces loses immediately."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[4, 3] = BLACK_MAN
        state = CheckersState(board=b, current_player=PLAYER_RED)
        assert state.is_terminal
        assert state.winner == PLAYER_BLACK

    def test_draw_rule_40_moves(self):
        """80 half-moves without capture or promotion triggers a draw (winner = 0)."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[0, 1] = RED_KING
        b[7, 6] = BLACK_KING
        state = CheckersState(board=b, current_player=PLAYER_RED, halfmove_clock=80)
        assert state.is_terminal
        assert state.winner == 0, "Expected draw (winner=0) under 40-move rule"

    def test_terminal_state_move_rejection(self):
        """Attempting to make a move from a terminal state must raise ValueError."""
        b = np.zeros((8, 8), dtype=np.int8)
        b[0, 1] = RED_KING
        state = CheckersState(board=b, current_player=PLAYER_BLACK)
        assert state.is_terminal
        with pytest.raises(ValueError, match="terminal"):
            state.make_move(((0, 1), (1, 2)))


# =============================================================================
# 2. MCTS STRESS TESTS
# =============================================================================

class TestMCTSAdversarialStress:
    """Adversarial stress testing for Monte Carlo Tree Search."""

    def test_mcts_rollout_stability_and_visit_invariants(self):
        """Rollout must run 200 simulations without NaN, inf, or state corruption."""
        state = TicTacToeState()
        ai = MCTS(c_param=math.sqrt(2.0))
        root = ai.search(state, num_simulations=200)

        assert root.visits == 200, f"Root visits {root.visits} != 200"
        child_visits_sum = sum(child.visits for child in root.children.values())
        assert child_visits_sum == 200, f"Child visits sum {child_visits_sum} != 200"

        for move, child in root.children.items():
            assert child.visits > 0
            win_rate = child.wins / child.visits
            assert 0.0 <= win_rate <= 1.0, f"Win rate {win_rate} outside [0, 1]!"

    def test_mcts_terminal_state_handling(self):
        """MCTSNode and MCTS search must gracefully handle terminal states."""
        board = [
            1, 1, 1,
            2, 2, 0,
            0, 0, 0
        ]
        term_state = TicTacToeState(board=board, current_player=2)
        term_state._check_winner()
        assert term_state.is_terminal

        node = MCTSNode(term_state)
        assert node.is_terminal()
        assert node.is_fully_expanded()
        assert len(node.untried_moves) == 0

        ai = MCTS()
        best_move = ai.get_best_move(term_state, num_simulations=50)
        assert best_move is None, "Expected None when calling get_best_move on terminal state"

    def test_mcts_single_legal_move_fast_path(self):
        """When only 1 legal move is available, MCTS returns it immediately."""
        board = [
            1, 2, 1,
            2, 1, 2,
            2, 1, 0
        ]
        state = TicTacToeState(board=board, current_player=2)
        legal = state.get_legal_moves()
        assert len(legal) == 1
        assert legal[0] == 8

        ai = MCTS()
        best_move = ai.get_best_move(state, num_simulations=500)
        assert best_move == 8

    def test_mcts_seed_determinism(self):
        """MCTS execution with identical random seed produces identical results."""
        state = TicTacToeState()
        ai = MCTS(c_param=1.414)

        random.seed(12345)
        move1 = ai.get_best_move(state, num_simulations=100)

        random.seed(12345)
        move2 = ai.get_best_move(state, num_simulations=100)

        assert move1 == move2, f"MCTS was non-deterministic under identical seed: {move1} vs {move2}"

    def test_mcts_finds_immediate_winning_move(self):
        """MCTS must reliably select an immediate winning move over alternatives."""
        # Player 1 has 2 pieces in row 0: (0, 1) and can win at (2)
        board = [
            1, 1, 0,
            2, 2, 0,
            0, 0, 0
        ]
        state = TicTacToeState(board=board, current_player=1)
        ai = MCTS(c_param=1.414)
        best_move = ai.get_best_move(state, num_simulations=100)
        assert best_move == 2, f"MCTS failed to find immediate win at position 2, chose {best_move}"


# =============================================================================
# 3. TABULAR Q-LEARNING STRESS TESTS
# =============================================================================

class TestQLearningAdversarialStress:
    """Boundary and stress tests for GridWorld and Tabular Q-Learning."""

    def test_gridworld_boundary_and_wall_collisions(self):
        """Agent moving into boundary or obstacle wall must bounce back with step penalty."""
        env = GridWorld()
        env.reset()
        assert env.agent_pos == (0, 0)

        pos, reward, done, info = env.step(ACTION_UP)
        assert pos == (0, 0), "Agent moved through top boundary!"
        assert reward == -1.0
        assert not done

        pos, reward, done, info = env.step(ACTION_LEFT)
        assert pos == (0, 0), "Agent moved through left boundary!"
        assert reward == -1.0
        assert not done

        pos, _, _, _ = env.step(ACTION_RIGHT)
        assert pos == (0, 1)
        pos, reward, done, info = env.step(ACTION_DOWN)
        assert pos == (0, 1), "Agent walked into obstacle wall at (1, 1)!"
        assert reward == -1.0
        assert not done

    def test_q_learning_convergence_across_discount_factors(self):
        """Verify Q-learning runs stably across gamma = 0.0, 0.5, and 0.99."""
        gammas = [0.0, 0.5, 0.99]
        for gamma in gammas:
            env = GridWorld()
            agent = QLearningAgent(
                actions=env.action_space,
                alpha=0.1,
                gamma=gamma,
                epsilon=0.5,
                random_state=42
            )

            for ep in range(50):
                s = env.reset()
                for step in range(30):
                    a = agent.choose_action(s)
                    s_next, r, done, _ = env.step(a)
                    agent.update(s, a, r, s_next, done)
                    s = s_next
                    if done:
                        break

            for (st, act), q_val in agent.q_table.items():
                assert not math.isnan(q_val), f"NaN Q-value at state {st}, action {act} for gamma={gamma}"
                assert not math.isinf(q_val), f"Inf Q-value at state {st}, action {act} for gamma={gamma}"

    def test_q_learning_reward_bounds(self):
        """Empirical Q-values must respect mathematical theoretical bounds."""
        gamma = 0.90
        env = GridWorld()
        agent = QLearningAgent(
            actions=env.action_space,
            alpha=0.1,
            gamma=gamma,
            epsilon=1.0,
            epsilon_decay=0.95,
            epsilon_min=0.05,
            random_state=42
        )

        for _ in range(100):
            s = env.reset()
            for _ in range(25):
                a = agent.choose_action(s)
                s_next, r, done, _ = env.step(a)
                agent.update(s, a, r, s_next, done)
                s = s_next
                if done:
                    break
            agent.decay_epsilon()

        max_bound = 10.0 / (1.0 - gamma) + 1e-5
        min_bound = -10.0 / (1.0 - gamma) - 1e-5

        for (st, act), q_val in agent.q_table.items():
            assert min_bound <= q_val <= max_bound, (
                f"Q-value {q_val} at ({st}, {act}) violated theoretical bounds [{min_bound}, {max_bound}]"
            )

        assert agent.epsilon <= 0.05 + 1e-4, f"Epsilon {agent.epsilon} did not decay towards epsilon_min"

    def test_q_learning_alpha_zero_invariance(self):
        """With learning rate alpha=0.0, Q-table must remain strictly unchanged at 0.0."""
        agent = QLearningAgent(actions=[0, 1, 2, 3], alpha=0.0, random_state=42)
        agent.update(state=(0, 0), action=0, reward=10.0, next_state=(1, 0), done=True)
        assert agent.get_q((0, 0), 0) == 0.0

    def test_q_learning_policy_and_value_function_extraction(self):
        """Policy and value function extractions produce valid mappings across all accessible states."""
        env = GridWorld()
        states = env.get_all_states()
        agent = QLearningAgent(actions=env.action_space, random_state=42)
        # Train slightly
        for _ in range(20):
            s = env.reset()
            for _ in range(15):
                a = agent.choose_action(s)
                s_next, r, done, _ = env.step(a)
                agent.update(s, a, r, s_next, done)
                s = s_next
                if done:
                    break

        policy = agent.get_policy(states)
        values = agent.get_value_function(states)

        assert len(policy) == len(states)
        assert len(values) == len(states)
        for s in states:
            assert policy[s] in env.action_space
            assert isinstance(values[s], float)


# =============================================================================
# 4. PCA FROM SCRATCH STRESS TESTS
# =============================================================================

class TestPCAFromScratchAdversarialStress:
    """Stress testing for NumPy PCAScratch on pathological inputs."""

    def test_rank_deficient_matrix(self):
        """PCA on rank-deficient data (colinear features) must identify zero-variance axes."""
        rng = np.random.RandomState(42)
        f1 = rng.randn(100, 1)
        f2 = rng.randn(100, 1)
        f3 = 2.0 * f1 + 3.0 * f2
        f4 = -1.5 * f1
        f5 = f2 - f1
        X = np.hstack([f1, f2, f3, f4, f5])
        assert np.linalg.matrix_rank(X) == 2

        pca = PCAScratch(n_components=5)
        pca.fit(X)

        assert np.all(pca.explained_variance_[2:] < 1e-10)
        assert np.isclose(np.sum(pca.explained_variance_ratio_), 1.0, atol=1e-5)

        pca_k2 = PCAScratch(n_components=2)
        Z = pca_k2.fit_transform(X)
        X_hat = pca_k2.inverse_transform(Z)
        recon_error = np.linalg.norm(X - X_hat, ord='fro') / np.linalg.norm(X, ord='fro')
        assert recon_error < 1e-6, f"Rank-2 reconstruction error too high: {recon_error}"

    def test_all_constant_zero_features(self):
        """Data with zero variance across all features should not trigger division by zero."""
        X = np.zeros((20, 4))
        pca = PCAScratch(n_components=2)
        pca.fit(X)
        assert np.all(pca.explained_variance_ == 0.0)
        assert np.all(pca.explained_variance_ratio_ == 0.0)
        Z = pca.transform(X)
        assert Z.shape == (20, 2)
        assert np.all(Z == 0.0)

    def test_single_feature_1d_input(self):
        """PCA on 1D feature array (N, 1) preserves variance and reconstructs perfectly."""
        rng = np.random.RandomState(42)
        X = rng.randn(50, 1) * 4.5 + 2.0
        pca = PCAScratch(n_components=1)
        Z = pca.fit_transform(X)
        assert Z.shape == (50, 1)
        X_hat = pca.inverse_transform(Z)
        assert np.allclose(X, X_hat, atol=1e-10)
        sample_var = np.var(X, ddof=1)
        assert np.isclose(pca.explained_variance_[0], sample_var, atol=1e-5)

    def test_high_dimensional_n_less_than_d(self):
        """High-dimensional scenario where N < D (e.g. 10 samples, 40 features)."""
        rng = np.random.RandomState(42)
        N, D = 10, 40
        X = rng.randn(N, D)

        pca = PCAScratch(n_components=None)
        pca.fit(X)
        assert pca.n_components_ == N - 1

        sk_pca = SklearnPCA(n_components=pca.n_components_)
        sk_pca.fit(X)

        assert np.allclose(pca.explained_variance_, sk_pca.explained_variance_, atol=1e-5)
        assert np.allclose(pca.singular_values_, sk_pca.singular_values_, atol=1e-5)

    def test_exact_parity_with_sklearn_on_full_pipeline(self):
        """Rigorous parity test: eigenvalues, EVR, and absolute projections vs sklearn."""
        rng = np.random.RandomState(99)
        X = rng.randn(150, 6) @ rng.randn(6, 6)

        scratch = PCAScratch(n_components=3).fit(X)
        sk = SklearnPCA(n_components=3).fit(X)

        assert np.allclose(scratch.explained_variance_, sk.explained_variance_, rtol=1e-4)
        assert np.allclose(scratch.explained_variance_ratio_, sk.explained_variance_ratio_, rtol=1e-4)
        Z_scratch = scratch.transform(X)
        Z_sk = sk.transform(X)
        assert np.allclose(np.abs(Z_scratch), np.abs(Z_sk), atol=1e-5)

    def test_float_variance_ratio_threshold(self):
        """Setting n_components as float (e.g. 0.95) must select sufficient components."""
        rng = np.random.RandomState(42)
        X = rng.randn(100, 10)
        pca = PCAScratch(n_components=0.90)
        pca.fit(X)
        cum_var = np.sum(pca.explained_variance_ratio_)
        assert cum_var >= 0.90, f"Cumulative variance {cum_var} < requested 0.90"

    def test_pca_input_validation(self):
        """PCA raises proper exceptions for invalid dimensions or component counts."""
        # 1 sample
        with pytest.raises(ValueError, match="at least 2 samples"):
            PCAScratch().fit(np.array([[1.0, 2.0]]))
        # 1D array instead of 2D
        with pytest.raises(ValueError, match="Expected 2D array"):
            PCAScratch().fit(np.array([1.0, 2.0, 3.0]))
        # n_components > n_features
        with pytest.raises(ValueError, match="between 1 and"):
            PCAScratch(n_components=10).fit(np.random.randn(20, 3))


# =============================================================================
# 5. LOGISTIC REGRESSION GRADIENT DESCENT STRESS TESTS
# =============================================================================

class TestLogisticRegressionGDAdversarialStress:
    """Stress testing for NumPy Logistic Regression Gradient Descent."""

    def test_perfectly_separable_data_no_overflow(self):
        """Linearly separable clusters must train without NaN/Inf in sigmoid or BCE loss."""
        rng = np.random.RandomState(42)
        X0 = rng.uniform(-30.0, -20.0, size=(100, 2))
        X1 = rng.uniform(20.0, 30.0, size=(100, 2))
        X = np.vstack([X0, X1])
        y = np.array([0] * 100 + [1] * 100)

        clf = LogisticRegressionGD(learning_rate=0.01, max_iter=200, l2_reg=0.0, random_state=42)
        clf.fit(X, y)

        assert len(clf.losses_) > 0
        for loss in clf.losses_:
            assert not math.isnan(loss) and not math.isinf(loss), f"Invalid loss: {loss}"
        assert clf.losses_[-1] < clf.losses_[0]

        preds = clf.predict(X)
        assert np.mean(preds == y) == 1.0

        probs = clf.predict_proba(X)
        assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
        assert np.allclose(probs.sum(axis=1), 1.0)

    def test_colinear_features_stability(self):
        """Colinear (redundant) features must converge stably in GD without singular matrix errors."""
        rng = np.random.RandomState(42)
        x1 = rng.randn(100, 1)
        x2 = 2.5 * x1
        x3 = -1.2 * x1
        X = np.hstack([x1, x2, x3])
        y = (x1.ravel() > 0).astype(int)

        clf = LogisticRegressionGD(learning_rate=0.05, max_iter=300, l2_reg=0.1, random_state=42)
        clf.fit(X, y)
        assert clf.coef_ is not None
        assert np.all(np.isfinite(clf.coef_))
        assert clf.predict(X).shape == (100,)

    def test_zero_iterations_edge_case(self):
        """max_iter=0 initializes weights and permits prediction without training."""
        X = np.array([[1.0, 2.0], [3.0, 4.0]])
        y = np.array([0, 1])

        clf = LogisticRegressionGD(max_iter=0)
        clf.fit(X, y)
        assert clf.n_iter_ == 0
        assert len(clf.losses_) == 0
        probs = clf.predict_proba(X)
        assert probs.shape == (2, 2)
        assert np.allclose(probs.sum(axis=1), 1.0)

    def test_unfitted_model_raises_runtime_error(self):
        """Calling predict or predict_proba before fit must raise RuntimeError."""
        clf = LogisticRegressionGD()
        with pytest.raises(RuntimeError):
            clf.predict(np.array([[1.0, 2.0]]))
        with pytest.raises(RuntimeError):
            clf.predict_proba(np.array([[1.0, 2.0]]))

    def test_ovr_multiclass_and_non_consecutive_labels(self):
        """LogisticRegressionOVR must handle arbitrary non-consecutive class labels."""
        rng = np.random.RandomState(42)
        c1 = rng.randn(40, 3) + np.array([0.0, 0.0, 0.0])
        c2 = rng.randn(40, 3) + np.array([8.0, 8.0, 8.0])
        c3 = rng.randn(40, 3) + np.array([-8.0, -8.0, -8.0])
        X = np.vstack([c1, c2, c3])
        y = np.array([10] * 40 + [50] * 40 + [99] * 40)

        # 600 iterations allows GD to reach optimal convergence (> 98% accuracy)
        ovr = LogisticRegressionOVR(learning_rate=0.05, max_iter=600, l2_reg=0.01, random_state=42)
        ovr.fit(X, y)

        assert set(ovr.classes_) == {10, 50, 99}
        probs = ovr.predict_proba(X)
        assert probs.shape == (120, 3)
        assert np.allclose(probs.sum(axis=1), 1.0)

        preds = ovr.predict(X)
        accuracy = np.mean(preds == y)
        assert accuracy >= 0.98, f"OvR accuracy unexpectedly low: {accuracy}"

        single_x = np.array([[8.5, 8.2, 7.9]])
        pred_single = ovr.predict(single_x)
        assert pred_single[0] == 50

    def test_decision_threshold_sensitivity(self):
        """Varying decision threshold changes positive class predictions monotonically."""
        rng = np.random.RandomState(42)
        X = rng.randn(100, 2)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)

        clf = LogisticRegressionGD(learning_rate=0.05, max_iter=200, random_state=42).fit(X, y)
        preds_low = clf.predict(X, threshold=0.1)
        preds_mid = clf.predict(X, threshold=0.5)
        preds_high = clf.predict(X, threshold=0.9)

        # Number of predicted positives must decrease as threshold increases
        assert np.sum(preds_low) >= np.sum(preds_mid) >= np.sum(preds_high)


# =============================================================================
# 6. NEURAL NETWORKS STRESS TESTS
# =============================================================================

class TestNeuralNetworksAdversarialStress:
    """Stress testing for BatchNorm, Dropout, and Gradient Flow."""

    def test_batchnorm_eval_mode_batch_size_1(self):
        """In eval mode, BatchNorm must evaluate single samples using running statistics."""
        bn = nn.BatchNorm1d(num_features=4)
        bn.train()
        dummy_batch = torch.randn(32, 4) * 2.0 + 5.0
        _ = bn(dummy_batch)

        bn.eval()
        single_sample = torch.tensor([[5.0, 5.0, 5.0, 5.0]])
        out = bn(single_sample)
        assert out.shape == (1, 4)
        assert torch.all(torch.isfinite(out))

    def test_batchnorm_train_mode_batch_size_1_fails_as_expected(self):
        """In train mode, batch size 1 cannot compute sample variance and must raise ValueError."""
        bn = nn.BatchNorm1d(num_features=4)
        bn.train()
        single_sample = torch.randn(1, 4)
        with pytest.raises(ValueError, match="Expected more than 1 value per channel when training"):
            bn(single_sample)

    def test_deep_fault_classifier_eval_single_sample(self):
        """DeepFaultClassifier in eval mode processes single telemetry vector without error."""
        model = DeepFaultClassifier(in_features=8, num_classes=3)
        model.eval()
        single_telemetry = torch.randn(1, 8)
        logits = model(single_telemetry)
        assert logits.shape == (1, 3)
        assert torch.all(torch.isfinite(logits))

    def test_dropout_extreme_rates_zero_vs_one(self):
        """Dropout at p=0.0 is pure identity; p=1.0 zeroes all elements in train mode."""
        x = torch.ones(20)

        drop0 = nn.Dropout(p=0.0)
        drop0.train()
        assert torch.all(drop0(x) == x)
        drop0.eval()
        assert torch.all(drop0(x) == x)

        drop1 = nn.Dropout(p=1.0)
        drop1.train()
        y_train = drop1(x)
        assert torch.all(y_train == 0.0), "Dropout p=1.0 did not zero all elements in train mode!"

        drop1.eval()
        y_eval = drop1(x)
        assert torch.all(y_eval == x), "Dropout p=1.0 did not preserve input in eval mode!"

    def test_dropout_expectation_preservation(self):
        """Inverted dropout scaling 1/(1-p) preserves expected activation magnitude."""
        p = 0.4
        drop = nn.Dropout(p=p)
        drop.train()
        large_input = torch.ones(50000)
        output = drop(large_input)
        empirical_mean = output.mean().item()
        assert abs(empirical_mean - 1.0) < 0.02, f"Dropout output mean {empirical_mean} deviated from 1.0"

    def test_kaiming_initialization_variance(self):
        """Kaiming normal initialization sets standard deviation near sqrt(2 / fan_in)."""
        layer = nn.Linear(512, 256)
        init_weights_kaiming(layer)
        expected_std = math.sqrt(2.0 / 512)
        empirical_std = layer.weight.std().item()
        assert abs(empirical_std - expected_std) < 0.01, (
            f"Kaiming std {empirical_std} deviated from theoretical {expected_std}"
        )
        assert torch.all(layer.bias == 0.0), "Bias not initialized to zero"

    def test_deep_fault_classifier_gradient_flow_and_zero_grad(self):
        """Backpropagation must propagate non-zero, finite gradients to all parameter layers."""
        model = DeepFaultClassifier(in_features=8, num_classes=3)
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        x = torch.randn(16, 8)
        y = torch.tensor([0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0])

        optimizer.zero_grad()
        for p in model.parameters():
            assert p.grad is None

        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()

        found_weights = 0
        for name, param in model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None, f"Parameter {name} has None gradient!"
                assert torch.all(torch.isfinite(param.grad)), f"Parameter {name} gradient contains NaN/Inf!"
                assert torch.any(param.grad != 0.0), f"Parameter {name} gradient is completely zero!"
                found_weights += 1

        assert found_weights >= 8, f"Expected gradients across all linear & BN layers, got {found_weights}"

        optimizer.zero_grad()
        for param in model.parameters():
            assert param.grad is None or torch.all(param.grad == 0.0)
