"""
End-to-End Test Suite for Milestone M2: Mathematics & Game AI Implementations.
Verifies NumPy PCA From Scratch, Logistic Regression Gradient Descent,
Checkers Game Engine & AI, Monte Carlo Tree Search (MCTS), and Tabular Q-Learning.
Adheres to the 4-Tier Test Design Methodology.
"""

import math
from pathlib import Path
import pytest
import numpy as np
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.linear_model import LogisticRegression as SklearnLogReg
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# =====================================================================
# TIER 1: FEATURE COVERAGE (Isolation & Primary Contracts)
# =====================================================================

@pytest.mark.tier1
@pytest.mark.m2
class TestTier1PCAScratchCoverage:
    """Tier 1: Verify isolated NumPy PCAScratch mathematical contracts."""

    def test_pca_fit_transform_shape(self, load_module):
        """PCAScratch projection dimension matches n_components."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(100, 8)
        pca = mod.PCAScratch(n_components=3)
        Z = pca.fit_transform(X)
        assert Z.shape == (100, 3)
        assert pca.components_.shape == (3, 8)

    def test_pca_mean_centering_and_covariance_symmetry(self, load_module):
        """Verify empirical mean matches sample mean and covariance matrix is symmetric."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(80, 5) * 3.0 + 7.0
        pca = mod.PCAScratch(n_components=2)
        pca.fit(X)
        assert np.allclose(pca.mean_, X.mean(axis=0), atol=1e-5)
        cov = pca.covariance_
        assert np.allclose(cov, cov.T, atol=1e-7)

    def test_pca_explained_variance_ratio_sum(self, load_module):
        """Explained variance ratio must be descending, non-negative, and sum <= 1."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(120, 6)
        pca = mod.PCAScratch(n_components=6)
        pca.fit(X)
        evr = pca.explained_variance_ratio_
        assert np.all(evr >= 0.0)
        assert np.isclose(np.sum(evr), 1.0, atol=1e-4)
        assert np.all(np.diff(evr) <= 1e-7)  # descending order

    def test_pca_inverse_transform_reconstruction(self, load_module):
        """Reconstruction error ||X - X_hat|| must decrease as n_components increases."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(100, 10)
        
        pca2 = mod.PCAScratch(n_components=2)
        Z2 = pca2.fit_transform(X)
        X_hat2 = pca2.inverse_transform(Z2)
        err2 = np.linalg.norm(X - X_hat2)

        pca5 = mod.PCAScratch(n_components=5)
        Z5 = pca5.fit_transform(X)
        X_hat5 = pca5.inverse_transform(Z5)
        err5 = np.linalg.norm(X - X_hat5)

        assert err5 < err2

    def test_pca_orthogonality_of_components(self, load_module):
        """Principal axes must be orthonormal: W @ W.T = I_k."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(150, 7)
        pca = mod.PCAScratch(n_components=4)
        pca.fit(X)
        W = pca.components_
        gram = W @ W.T
        assert np.allclose(gram, np.eye(4), atol=1e-5)

    def test_pca_parity_with_sklearn(self, load_module):
        """Principal components match sklearn up to sign flip (|dot product| approx 1)."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.RandomState(42).randn(200, 6)
        pca_scratch = mod.PCAScratch(n_components=3)
        pca_scratch.fit(X)

        pca_sk = SklearnPCA(n_components=3)
        pca_sk.fit(X)

        for i in range(3):
            dot = np.abs(np.dot(pca_scratch.components_[i], pca_sk.components_[i]))
            assert np.isclose(dot, 1.0, atol=1e-4)


@pytest.mark.tier1
@pytest.mark.m2
class TestTier1LogisticRegressionGDCoverage:
    """Tier 1: Verify isolated NumPy Logistic Regression GD contracts."""

    def test_logreg_sigmoid_numerically_stable(self, load_module):
        """Sigmoid function handles large positive/negative values without overflow."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        sig = mod.stable_sigmoid
        assert np.isclose(sig(0.0), 0.5)
        assert np.isclose(sig(100.0), 1.0)
        assert np.isclose(sig(-100.0), 0.0)
        assert not np.isnan(sig(np.array([-1000.0, 0.0, 1000.0]))).any()

    def test_logreg_binary_fit_and_predict(self, load_module):
        """LogisticRegressionGD learns separable binary data with high accuracy."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        rng = np.random.RandomState(42)
        X0 = rng.randn(60, 4) - 2.5
        X1 = rng.randn(60, 4) + 2.5
        X = np.vstack([X0, X1])
        y = np.array([0] * 60 + [1] * 60)

        clf = mod.LogisticRegressionGD(learning_rate=0.1, max_iter=500, random_state=42)
        clf.fit(X, y)
        preds = clf.predict(X)
        acc = np.mean(preds == y)
        assert acc >= 0.95
        assert clf.coef_.shape == (4,)
        assert isinstance(clf.intercept_, float)

    def test_logreg_predict_proba_range(self, load_module):
        """predict_proba outputs are strictly in [0, 1] and sum to 1."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        X = np.random.RandomState(42).randn(50, 3)
        y = (X[:, 0] > 0).astype(int)
        clf = mod.LogisticRegressionGD(learning_rate=0.05, max_iter=200)
        clf.fit(X, y)
        probs = clf.predict_proba(X)
        assert probs.shape == (50, 2)
        assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
        assert np.allclose(probs.sum(axis=1), np.ones(50), atol=1e-5)

    def test_logreg_loss_monotonic_decrease(self, load_module):
        """Training loss decreases significantly from initial epoch to final epoch."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        X, y = mod.generate_binary_fault_data(n_samples=200, random_state=42)
        X_scaled = StandardScaler().fit_transform(X)
        clf = mod.LogisticRegressionGD(learning_rate=0.05, max_iter=300, random_state=42)
        clf.fit(X_scaled, y)
        assert len(clf.losses_) > 10
        assert clf.losses_[-1] < clf.losses_[0] * 0.7

    def test_logreg_parity_with_sklearn(self, load_module):
        """LogisticRegressionGD predictions achieve comparable accuracy to sklearn."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        X, y = mod.generate_binary_fault_data(n_samples=300, random_state=42)
        X = StandardScaler().fit_transform(X)

        clf_gd = mod.LogisticRegressionGD(learning_rate=0.1, max_iter=1000, random_state=42)
        clf_gd.fit(X, y)
        acc_gd = np.mean(clf_gd.predict(X) == y)

        clf_sk = SklearnLogReg(max_iter=1000, random_state=42)
        clf_sk.fit(X, y)
        acc_sk = np.mean(clf_sk.predict(X) == y)

        assert abs(acc_gd - acc_sk) <= 0.05

    def test_logreg_ovr_multiclass(self, load_module):
        """LogisticRegressionOVR supports 3-class classification."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        X, y = mod.generate_multiclass_fault_data(n_samples=300, random_state=7)
        X_scaled = StandardScaler().fit_transform(X)
        ovr = mod.LogisticRegressionOVR(learning_rate=0.1, max_iter=800, random_state=42)
        ovr.fit(X_scaled, y)
        preds = ovr.predict(X_scaled)
        acc = np.mean(preds == y)
        assert acc >= 0.85
        assert set(np.unique(preds)).issubset({0, 1, 2})


@pytest.mark.tier1
@pytest.mark.m2
class TestTier1CheckersEngineCoverage:
    """Tier 1: Verify isolated Checkers Game Engine and AI contracts."""

    def test_checkers_initial_board_setup(self, load_module):
        """Checkers initial board has 12 red pieces and 12 black pieces."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod.CheckersState()
        counts = state.count_pieces()
        assert counts["red_men"] == 12
        assert counts["black_men"] == 12
        assert counts["red_kings"] == 0
        assert counts["black_kings"] == 0
        assert not state.is_terminal

    def test_checkers_diagonal_step_moves(self, load_module):
        """Initial Red player has valid forward diagonal step moves (decreasing rows)."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod.CheckersState()
        legal_moves = state.get_legal_moves()
        assert len(legal_moves) > 0
        # Red men start at rows 5, 6, 7 moving UP toward row 0
        for move in legal_moves:
            assert len(move) == 2
            start_r, start_c = move[0]
            end_r, end_c = move[1]
            assert end_r < start_r  # Moving toward row 0 for Red

    def test_checkers_forced_capture_rule(self, load_module):
        """When a jump capture is available, all returned legal moves must be jumps."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        board = np.zeros((8, 8), dtype=int)
        board[5, 3] = mod.RED_MAN
        board[4, 2] = mod.BLACK_MAN
        # Landing square (3, 1) is empty
        state = mod.CheckersState(board=board, current_player=mod.PLAYER_RED)
        moves = state.get_legal_moves()
        assert len(moves) == 1
        jump_move = moves[0]
        assert jump_move[0] == (5, 3)
        assert jump_move[1] == (3, 1)

    def test_checkers_king_promotion(self, load_module):
        """Red man reaching row 0 promotes to King."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        board = np.zeros((8, 8), dtype=int)
        board[1, 2] = mod.RED_MAN  # dark square (1 + 2 = 3 odd)
        board[7, 0] = mod.BLACK_MAN  # Opponent piece so game is non-terminal
        state = mod.CheckersState(board=board, current_player=mod.PLAYER_RED)
        moves = state.get_legal_moves()
        step_to_king = [m for m in moves if m[-1][0] == 0][0]
        next_state = state.make_move(step_to_king)
        r_end, c_end = step_to_king[-1]
        assert next_state.board[r_end, c_end] == mod.RED_KING

    def test_checkers_ai_alpha_beta_search(self, load_module):
        """Alpha-Beta AI selects a valid legal move from current state."""
        mod_game = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        mod_ai = load_module("checkers_ai", "game-ai/08_checkers/checkers_ai.py")
        state = mod_game.CheckersState()
        best_move = mod_ai.get_best_move(state, depth=2)
        assert best_move is not None
        legal_moves = state.get_legal_moves()
        assert best_move in legal_moves


@pytest.mark.tier1
@pytest.mark.m2
class TestTier1MCTSCoverage:
    """Tier 1: Verify isolated Monte Carlo Tree Search contracts."""

    def test_mcts_node_creation_and_expansion(self, load_module):
        """MCTSNode tracks state, visits, and untried moves."""
        mod_mcts = load_module("mcts_engine", "game-ai/10_mcts/mcts.py")
        mod_checkers = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod_checkers.CheckersState()
        node = mod_mcts.MCTSNode(state)
        assert node.visits == 0
        assert node.wins == 0.0
        assert not node.is_fully_expanded()
        
        # Add a child
        move = node.untried_moves[0]
        next_state = state.make_move(move)
        child = node.add_child(move, next_state)
        assert child.parent is node
        assert len(node.children) == 1

    def test_mcts_ucb1_unvisited_bonus(self, load_module):
        """Unvisited child node receives inf score ensuring selection."""
        mod_mcts = load_module("mcts_engine", "game-ai/10_mcts/mcts.py")
        mod_checkers = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod_checkers.CheckersState()
        parent = mod_mcts.MCTSNode(state)
        parent.visits = 10
        
        c1 = parent.add_child(state.get_legal_moves()[0], state)
        c1.visits = 5
        c1.wins = 3.0
        
        c2 = parent.add_child(state.get_legal_moves()[1], state)
        c2.visits = 0  # Unvisited
        
        best = parent.best_child(c_param=math.sqrt(2.0))
        assert best is c2

    def test_mcts_backpropagation_updates(self, load_module):
        """Backpropagation loop increments visits up the tree."""
        mod_mcts = load_module("mcts_engine", "game-ai/10_mcts/mcts.py")
        mod_checkers = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod_checkers.CheckersState()
        root = mod_mcts.MCTSNode(state)
        child = root.add_child(state.get_legal_moves()[0], state)
        
        # Backpropagate simulation result
        curr = child
        while curr is not None:
            curr.update(winner=mod_checkers.PLAYER_RED)
            curr = curr.parent
            
        assert child.visits == 1
        assert root.visits == 1

    def test_mcts_get_best_move_returns_legal_action(self, load_module):
        """MCTS search returns a legal move from root state."""
        mod_mcts = load_module("mcts_engine", "game-ai/10_mcts/mcts.py")
        mod_checkers = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod_checkers.CheckersState()
        mcts = mod_mcts.MCTS()
        best_move = mcts.get_best_move(state, num_simulations=20)
        assert best_move in state.get_legal_moves()

    def test_mcts_move_statistics(self, load_module):
        """get_move_statistics returns list of dicts with move visit stats."""
        mod_mcts = load_module("mcts_engine", "game-ai/10_mcts/mcts.py")
        mod_checkers = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod_checkers.CheckersState()
        mcts = mod_mcts.MCTS()
        stats = mcts.get_move_statistics(state, num_simulations=25)
        assert isinstance(stats, list) and len(stats) > 0
        total_visits = sum(s["visits"] for s in stats)
        assert total_visits == 25


@pytest.mark.tier1
@pytest.mark.m2
class TestTier1ReinforcementLearningCoverage:
    """Tier 1: Verify isolated GridWorld MDP and Tabular Q-Learning contracts."""

    def test_gridworld_reset_initial_state(self, load_module):
        """GridWorld reset sets agent to start state (0, 0)."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        env = mod_gw.GridWorld(rows=4, cols=5)
        state = env.reset()
        assert state == (0, 0)

    def test_gridworld_step_transitions_and_walls(self, load_module):
        """Stepping into boundary or wall keeps agent in place."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        env = mod_gw.GridWorld(rows=4, cols=5)
        env.reset()
        # Action 0 = UP from (0, 0) hits top boundary
        next_state, reward, done, _ = env.step(0)
        assert next_state == (0, 0)
        assert done is False

    def test_gridworld_terminal_goal_reward(self, load_module):
        """Stepping into goal gives +10 reward and sets done=True."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        env = mod_gw.GridWorld(rows=4, cols=5)
        env.reset()
        # Set agent adjacent to goal (3, 3) moving RIGHT (3) to goal (3, 4)
        env.agent_pos = (3, 3)
        next_state, reward, done, _ = env.step(3)  # RIGHT
        assert next_state == env.goal_state
        assert reward == 10.0
        assert done is True

    def test_qlearning_bellman_update(self, load_module):
        """Q-table updates correctly according to Bellman optimality equation."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        mod_ql = load_module("q_learning", "game-ai/11_reinforcement_learning/q_learning.py")
        env = mod_gw.GridWorld()
        agent = mod_ql.QLearningAgent(actions=env.action_space, alpha=0.5, gamma=0.9, epsilon=0.0)
        state = (0, 0)
        action = 1  # DOWN
        reward = -1.0
        next_state = (1, 0)
        
        agent.q_table[(next_state, 0)] = 4.0
        agent.update(state, action, reward, next_state, done=False)
        # Expected: Q_new = 0.0 + 0.5 * [-1.0 + 0.9 * 4.0 - 0.0] = 1.3
        q_val = agent.get_q(state, action)
        assert np.isclose(q_val, 1.3, atol=1e-5)

    def test_qlearning_epsilon_decay(self, load_module):
        """Epsilon decays towards min_epsilon across training steps."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        mod_ql = load_module("q_learning", "game-ai/11_reinforcement_learning/q_learning.py")
        env = mod_gw.GridWorld()
        agent = mod_ql.QLearningAgent(actions=env.action_space, epsilon=1.0, epsilon_decay=0.9, epsilon_min=0.05)
        initial_eps = agent.epsilon
        for _ in range(20):
            agent.decay_epsilon()
        assert agent.epsilon < initial_eps
        assert agent.epsilon >= 0.05


# =====================================================================
# TIER 2: BOUNDARY AND CORNER CASES (Degeneracies & Edge Conditions)
# =====================================================================

@pytest.mark.tier2
@pytest.mark.m2
class TestTier2MathGameAIBoundaries:
    """Tier 2: Boundary and corner cases for Math & Game AI modules."""

    def test_pca_colinear_features(self, load_module):
        """PCA on colinear duplicate features handles rank deficiency gracefully."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        base = np.random.randn(50, 1)
        X = np.hstack([base, base * 2.0, base * -3.0])  # Rank 1 in 3D
        pca = mod.PCAScratch(n_components=2)
        Z = pca.fit_transform(X)
        assert Z.shape == (50, 2)
        assert pca.explained_variance_ratio_[0] > 0.999

    def test_pca_single_sample_or_single_component(self, load_module):
        """PCA with n_components=1 preserves primary principal axis."""
        mod = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        X = np.random.randn(40, 5)
        pca = mod.PCAScratch(n_components=1)
        Z = pca.fit_transform(X)
        assert Z.shape == (40, 1)
        assert pca.components_.shape == (1, 5)

    def test_logreg_extreme_saturated_inputs(self, load_module):
        """LogisticRegressionGD handles saturated inputs (magnitudes > 500) without NaN."""
        mod = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        X = np.array([[-500.0, -1000.0], [500.0, 1000.0]])
        y = np.array([0, 1])
        clf = mod.LogisticRegressionGD(learning_rate=0.01, max_iter=10)
        clf.fit(X, y)
        probs = clf.predict_proba(X)
        assert not np.isnan(probs).any()

    def test_checkers_terminal_detection_no_pieces(self, load_module):
        """Board with all enemy pieces captured immediately evaluates as terminal."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        board = np.zeros((8, 8), dtype=int)
        board[4, 4] = mod.RED_MAN
        state = mod.CheckersState(board=board, current_player=mod.PLAYER_BLACK)
        assert state.is_terminal is True
        assert state.winner == mod.PLAYER_RED

    def test_qlearning_terminal_update_ignores_future_discount(self, load_module):
        """When done=True, Bellman update targets only immediate reward (no gamma * max_q)."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        mod_ql = load_module("q_learning", "game-ai/11_reinforcement_learning/q_learning.py")
        env = mod_gw.GridWorld()
        agent = mod_ql.QLearningAgent(actions=env.action_space, alpha=1.0, gamma=0.99)
        state = (3, 3)
        action = 3
        reward = 10.0
        next_state = (3, 4)
        agent.update(state, action, reward, next_state, done=True)
        assert agent.get_q(state, action) == 10.0


# =====================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (Pairwise & State Sharing)
# =====================================================================

@pytest.mark.tier3
@pytest.mark.m2
class TestTier3MathGameAICrossFeatures:
    """Tier 3: Pairwise combinations and pipeline integrations."""

    def test_pca_to_logistic_regression_pipeline(self, load_module):
        """PCA dimensionality reduction feeds into LogisticRegressionGD classifier."""
        mod_pca = load_module("pca_scratch", "machine-learning/05_clustering/04_pca_from_scratch.py")
        mod_logreg = load_module("logreg_gd", "machine-learning/04_classification/01_logistic_regression_gd.py")
        
        # High dimensional dataset
        rng = np.random.RandomState(42)
        X0 = rng.randn(60, 20) - 2.0
        X1 = rng.randn(60, 20) + 2.0
        X = np.vstack([X0, X1])
        y = np.array([0] * 60 + [1] * 60)

        # Step 1: PCA reduce 20 -> 4 features
        pca = mod_pca.PCAScratch(n_components=4)
        Z = pca.fit_transform(X)
        assert Z.shape == (120, 4)

        # Step 2: Logistic Regression GD on reduced features
        clf = mod_logreg.LogisticRegressionGD(learning_rate=0.1, max_iter=300, random_state=42)
        clf.fit(Z, y)
        preds = clf.predict(Z)
        acc = np.mean(preds == y)
        assert acc >= 0.90

    def test_checkers_state_search_tree_consistency(self, load_module):
        """Iterative Checkers moves update player turns and board state symmetrically."""
        mod = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        state = mod.CheckersState()
        
        # Red turn
        assert state.current_player == mod.PLAYER_RED
        red_move = state.get_legal_moves()[0]
        state2 = state.make_move(red_move)
        
        # Black turn
        assert state2.current_player == mod.PLAYER_BLACK
        black_move = state2.get_legal_moves()[0]
        state3 = state2.make_move(black_move)
        
        assert state3.current_player == mod.PLAYER_RED


# =====================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (Workflows & Training Loops)
# =====================================================================

@pytest.mark.tier4
@pytest.mark.m2
class TestTier4MathGameAIRealWorldScenarios:
    """Tier 4: Realistic multi-step workflows and training convergence."""

    def test_checkers_headless_autonomous_game(self, load_module):
        """Simulate autonomous Checkers game between Alpha-Beta AI agents for 10 moves."""
        mod_game = load_module("checkers_engine", "game-ai/08_checkers/checkers.py")
        mod_ai = load_module("checkers_ai", "game-ai/08_checkers/checkers_ai.py")
        state = mod_game.CheckersState()
        
        move_count = 0
        while not state.is_terminal and move_count < 10:
            best_move = mod_ai.get_best_move(state, depth=2)
            assert best_move is not None
            state = state.make_move(best_move)
            move_count += 1
            
        assert move_count == 10
        assert not np.all(state.board == mod_game.EMPTY)

    def test_reinforcement_learning_training_loop_convergence(self, load_module):
        """Run 150 episodes of GridWorld Q-learning, verifying agent reaches goal."""
        mod_gw = load_module("gridworld", "game-ai/11_reinforcement_learning/gridworld.py")
        mod_ql = load_module("q_learning", "game-ai/11_reinforcement_learning/q_learning.py")
        
        env = mod_gw.GridWorld(rows=4, cols=5)
        agent = mod_ql.QLearningAgent(actions=env.action_space, alpha=0.2, gamma=0.95, epsilon=1.0, epsilon_decay=0.98, epsilon_min=0.05)
        
        goal_reached_count = 0
        for ep in range(150):
            state = env.reset()
            done = False
            steps = 0
            while not done and steps < 40:
                action = agent.choose_action(state)
                next_state, reward, done, _ = env.step(action)
                agent.update(state, action, reward, next_state, done)
                state = next_state
                steps += 1
                if done and reward == 10.0:
                    goal_reached_count += 1
            agent.decay_epsilon()
            
        # Verify policy has learned to reach the goal multiple times
        assert goal_reached_count > 15
        policy = agent.get_policy(env.get_all_states())
        assert len(policy) > 0
