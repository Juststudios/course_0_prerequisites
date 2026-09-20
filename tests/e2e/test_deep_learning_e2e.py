"""
End-to-End Test Suite for Milestone M1: Deep Learning Lessons & Neural Networks.
Verifies Batch Normalization, Dropout, Deep MLP Project, and Exercise Solutions.
Adheres to the 4-Tier Test Design Methodology.
"""

import os
import sys
import subprocess
from pathlib import Path
import pytest
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NN_DIR = REPO_ROOT / "machine-learning" / "09_neural_networks"
OUTPUT_DIR = NN_DIR / "output"


# =====================================================================
# TIER 1: FEATURE COVERAGE (Isolation & Primary Contracts)
# =====================================================================

@pytest.mark.tier1
@pytest.mark.m1
class TestTier1BatchNormCoverage:
    """Tier 1: Verify isolated Batch Normalization mathematical and operational contracts."""

    def test_batchnorm_dimension_preservation(self):
        """Verify BatchNorm1d preserves input batch and feature dimensions."""
        bn = nn.BatchNorm1d(num_features=16)
        x = torch.randn(32, 16)
        y = bn(x)
        assert y.shape == (32, 16)

    def test_batchnorm_mean_centering(self):
        """Verify output mini-batch mean is near zero in training mode with unit weights."""
        bn = nn.BatchNorm1d(num_features=8, affine=False)
        bn.train()
        x = torch.randn(128, 8) * 5.0 + 10.0
        y = bn(x)
        mean = y.mean(dim=0)
        assert torch.allclose(mean, torch.zeros_like(mean), atol=1e-4)

    def test_batchnorm_unit_variance(self):
        """Verify output mini-batch variance is near 1 in training mode with unit weights."""
        bn = nn.BatchNorm1d(num_features=8, affine=False)
        bn.train()
        x = torch.randn(256, 8) * 7.5 - 3.0
        y = bn(x)
        var = y.var(dim=0, unbiased=False)
        assert torch.allclose(var, torch.ones_like(var), atol=1e-2)

    def test_batchnorm_learnable_affine_parameters(self):
        """Verify gamma (weight) and beta (bias) scale and shift the normalized outputs."""
        bn = nn.BatchNorm1d(num_features=4)
        with torch.no_grad():
            bn.weight.fill_(2.0)
            bn.bias.fill_(5.0)
        bn.train()
        x = torch.randn(100, 4)
        y = bn(x)
        assert torch.allclose(y.mean(dim=0), torch.tensor([5.0] * 4), atol=1e-2)
        assert torch.allclose(y.std(dim=0, unbiased=False), torch.tensor([2.0] * 4), atol=1e-2)

    def test_batchnorm_running_statistics_ema(self):
        """Verify running mean and variance update via Exponential Moving Average."""
        momentum = 0.1
        bn = nn.BatchNorm1d(num_features=4, momentum=momentum)
        bn.train()
        initial_mean = bn.running_mean.clone()
        x = torch.ones(50, 4) * 10.0
        bn(x)
        # expected running_mean = (1 - 0.1)*0 + 0.1*10.0 = 1.0
        expected_mean = torch.tensor([1.0, 1.0, 1.0, 1.0])
        assert torch.allclose(bn.running_mean, expected_mean, atol=1e-3)
        assert not torch.allclose(bn.running_mean, initial_mean)

    def test_batchnorm_eval_mode_deterministic(self):
        """Verify eval mode uses frozen running stats and produces deterministic predictions."""
        bn = nn.BatchNorm1d(num_features=4)
        bn.train()
        # Feed batches to warm up running stats
        for _ in range(5):
            bn(torch.randn(32, 4) * 2.0 + 3.0)
        bn.eval()
        running_mean_frozen = bn.running_mean.clone()
        test_sample = torch.tensor([[1.0, 2.0, 3.0, 4.0]])
        y1 = bn(test_sample)
        y2 = bn(test_sample)
        assert torch.equal(y1, y2)
        assert torch.equal(bn.running_mean, running_mean_frozen)


@pytest.mark.tier1
@pytest.mark.m1
class TestTier1DropoutCoverage:
    """Tier 1: Verify isolated Inverted Dropout mathematical contracts."""

    def test_dropout_zero_rate_identity(self):
        """Dropout with p=0.0 should act as an exact identity function."""
        drop = nn.Dropout(p=0.0)
        x = torch.randn(10, 10)
        y = drop(x)
        assert torch.equal(y, x)

    def test_dropout_training_zeroing(self):
        """Dropout in train mode should zero out elements with probability approx p."""
        drop = nn.Dropout(p=0.5)
        drop.train()
        x = torch.ones(1000, 100)
        y = drop(x)
        zero_fraction = (y == 0).float().mean().item()
        assert 0.45 <= zero_fraction <= 0.55

    def test_dropout_inverted_scaling(self):
        """Surviving activations must be scaled by 1/(1-p)."""
        p = 0.4
        drop = nn.Dropout(p=p)
        drop.train()
        x = torch.ones(500, 50)
        y = drop(x)
        non_zeros = y[y != 0]
        expected_val = 1.0 / (1.0 - p)
        assert torch.allclose(non_zeros, torch.tensor(expected_val), atol=1e-5)

    def test_dropout_expectation_preservation(self):
        """Verify empirical mean of output matches empirical mean of input (unbiasedness)."""
        drop = nn.Dropout(p=0.3)
        drop.train()
        x = torch.randn(2000, 100) + 5.0
        y = drop(x)
        assert abs(x.mean().item() - y.mean().item()) < 0.15

    def test_dropout_eval_mode_identity(self):
        """In eval mode, dropout must never drop activations and must equal input."""
        drop = nn.Dropout(p=0.5)
        drop.eval()
        x = torch.randn(50, 50)
        y = drop(x)
        assert torch.equal(x, y)


@pytest.mark.tier1
@pytest.mark.m1
class TestTier1DeepMLPProjectCoverage:
    """Tier 1: Verify Deep MLP Industrial Fault Detection Project components."""

    def test_telemetry_generator_shapes(self, load_module):
        """Verify generate_telemetry creates 8-channel features and integer class targets."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        X, y = mod.generate_telemetry(n_per_class=100, seed=42)
        assert X.shape == (300, 8)
        assert y.shape == (300,)
        assert set(np.unique(y)) == {0, 1, 2}

    def test_kaiming_initialization_finite_variance(self, load_module):
        """Verify Kaiming normal initialization initializes linear weights properly."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        linear = nn.Linear(64, 64)
        mod.init_weights_kaiming(linear)
        assert linear.bias is not None
        assert torch.allclose(linear.bias, torch.zeros_like(linear.bias))
        std = linear.weight.std().item()
        assert 0.10 <= std <= 0.25

    def test_deep_fault_classifier_instantiation_and_forward(self, load_module):
        """Verify DeepFaultClassifier forward pass produces (B, 3) logits."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        model = mod.DeepFaultClassifier(in_features=8, num_classes=3, dropout_rate=0.25)
        batch = torch.randn(16, 8)
        out = model(batch)
        assert out.shape == (16, 3)

    def test_deep_fault_classifier_softmax_probabilities(self, load_module):
        """Softmax over output logits must sum to 1 across classes."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        model = mod.DeepFaultClassifier(in_features=8, num_classes=3)
        model.eval()
        with torch.no_grad():
            logits = model(torch.randn(8, 8))
            probs = torch.softmax(logits, dim=1)
            sums = probs.sum(dim=1)
            assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)

    def test_deep_fault_classifier_loss_backward(self, load_module):
        """Verify loss backward computes gradients for all trainable parameters."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        model = mod.DeepFaultClassifier(in_features=8, num_classes=3)
        model.train()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        optimizer.zero_grad()
        out = model(torch.randn(10, 8))
        loss = criterion(out, torch.tensor([0, 1, 2, 0, 1, 2, 0, 1, 2, 0]))
        loss.backward()
        for name, param in model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None
                assert not torch.isnan(param.grad).any()


@pytest.mark.tier1
@pytest.mark.m1
class TestTier1DLExerciseSolutionsCoverage:
    """Tier 1: Verify Deep Learning Exercise Solutions contracts."""

    def test_corrected_mlp_structure(self, load_module):
        """Verify CorrectedMLP resolves training issues from Level 2 exercises."""
        mod = load_module("exercises_solutions", "machine-learning/09_neural_networks/exercises_solutions.py")
        model = mod.CorrectedMLP()
        out = model(torch.randn(10, 10))
        assert out.shape == (10, 2)

    def test_deep_fault_mlp_regularization(self, load_module):
        """Verify DeepFaultMLP contains both BatchNorm and Dropout modules."""
        mod = load_module("exercises_solutions", "machine-learning/09_neural_networks/exercises_solutions.py")
        model = mod.DeepFaultMLP(in_features=8, num_classes=3)
        has_bn = any(isinstance(m, nn.BatchNorm1d) for m in model.modules())
        has_dropout = any(isinstance(m, nn.Dropout) for m in model.modules())
        assert has_bn, "Model must incorporate BatchNorm1d"
        assert has_dropout, "Model must incorporate Dropout"

    def test_two_layer_net_manual_forward_backward(self, load_module):
        """Verify TwoLayerNet manual forward and autograd step computes gradients."""
        mod = load_module("exercises_solutions", "machine-learning/09_neural_networks/exercises_solutions.py")
        net = mod.TwoLayerNet(input_dim=8, h1=16, h2=8, output_dim=3, lr=0.01)
        X = torch.randn(10, 8)
        y = torch.tensor([0, 1, 2, 0, 1, 2, 0, 1, 2, 0])
        net.zero_grad()
        out = net.forward(X)
        assert out.shape == (10, 3)
        loss = mod.cross_entropy_loss_manual(out, y)
        loss.backward()
        for p in net.parameters():
            assert p.grad is not None
            assert not torch.isnan(p.grad).any()
        net.step()

    def test_cross_entropy_loss_manual_consistency(self, load_module):
        """Verify cross_entropy_loss_manual matches PyTorch nn.CrossEntropyLoss."""
        mod = load_module("exercises_solutions", "machine-learning/09_neural_networks/exercises_solutions.py")
        torch.manual_seed(42)
        logits_t = torch.randn(8, 4)
        y_t = torch.tensor([0, 1, 2, 3, 0, 1, 2, 3])
        loss_manual = mod.cross_entropy_loss_manual(logits_t, y_t).item()
        criterion = nn.CrossEntropyLoss()
        loss_torch = criterion(logits_t, y_t).item()
        assert np.isclose(loss_manual, loss_torch, atol=1e-5)

    def test_zero_todos_in_exercises_solutions(self):
        """Verify exercises_solutions.py contains zero unresolved TODO markers."""
        sol_path = NN_DIR / "exercises_solutions.py"
        assert sol_path.exists()
        with open(sol_path) as f:
            content = f.read()
        assert "# TODO" not in content and "# TODO:" not in content


# =====================================================================
# TIER 2: BOUNDARY AND CORNER CASES (Limits, Extrema, Edge Shapes)
# =====================================================================

@pytest.mark.tier2
@pytest.mark.m1
class TestTier2DLBoundariesAndCorners:
    """Tier 2: Boundary and corner conditions for Deep Learning modules."""

    def test_batchnorm_batch_size_one_eval(self):
        """In eval mode, batch size 1 should execute cleanly without error."""
        bn = nn.BatchNorm1d(num_features=4)
        bn.eval()
        x = torch.randn(1, 4)
        y = bn(x)
        assert y.shape == (1, 4)

    def test_batchnorm_identical_constant_features(self):
        """Constant features (zero variance) must handle eps without division-by-zero NaN."""
        bn = nn.BatchNorm1d(num_features=3, eps=1e-5)
        bn.train()
        x = torch.ones(20, 3) * 42.0
        y = bn(x)
        assert not torch.isnan(y).any()
        assert not torch.isinf(y).any()

    def test_batchnorm_extreme_large_values(self):
        """Inputs with large magnitudes (1e6) normalize stably without overflow."""
        bn = nn.BatchNorm1d(num_features=2)
        bn.train()
        x = torch.randn(50, 2) * 1e6
        y = bn(x)
        assert not torch.isnan(y).any()
        assert not torch.isinf(y).any()
        assert torch.allclose(y.var(dim=0, unbiased=False), torch.ones(2), atol=1e-2)

    def test_dropout_rate_boundary_values(self):
        """Edge rates p=0.0 and p=0.99 must execute without ZeroDivisionError."""
        x = torch.randn(50, 20)
        d0 = nn.Dropout(p=0.0)
        d99 = nn.Dropout(p=0.99)
        d0.train()
        d99.train()
        y0 = d0(x)
        y99 = d99(x)
        assert torch.equal(y0, x)
        assert (y99 == 0).sum() > (y99 != 0).sum()

    def test_dropout_single_element_input(self):
        """Dropout handles minimal (1, 1) tensor correctly."""
        drop = nn.Dropout(p=0.5)
        x = torch.tensor([[5.0]])
        drop.eval()
        assert drop(x).item() == 5.0

    def test_deep_fault_classifier_batch_size_extremes(self, load_module):
        """DeepFaultClassifier processes minimal batch (N=2) and large batch (N=512)."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        model = mod.DeepFaultClassifier(in_features=8, num_classes=3)
        model.eval()
        out_small = model(torch.randn(2, 8))
        out_large = model(torch.randn(512, 8))
        assert out_small.shape == (2, 3)
        assert out_large.shape == (512, 3)


# =====================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS (Pairwise & State Sharing)
# =====================================================================

@pytest.mark.tier3
@pytest.mark.m1
class TestTier3DLCrossFeatureCombinations:
    """Tier 3: Pairwise interactions between BatchNorm, Dropout, and Kaiming init."""

    def test_batchnorm_and_dropout_pipeline(self):
        """Pipeline combining Linear -> BatchNorm -> ReLU -> Dropout maintains valid gradients."""
        model = nn.Sequential(
            nn.Linear(16, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(32, 2)
        )
        model.train()
        x = torch.randn(20, 16)
        out = model(x)
        loss = out.sum()
        loss.backward()
        for p in model.parameters():
            assert p.grad is not None
            assert not torch.isnan(p.grad).any()

    def test_train_to_eval_mode_coordination(self):
        """Switching from train to eval mode freezes BatchNorm AND disables Dropout."""
        bn = nn.BatchNorm1d(8)
        drop = nn.Dropout(p=0.5)
        model = nn.Sequential(bn, drop)
        
        # Warmup in train
        model.train()
        for _ in range(5):
            model(torch.randn(30, 8))
        
        # Switch to eval
        model.eval()
        sample = torch.randn(1, 8)
        out1 = model(sample)
        out2 = model(sample)
        # Deterministic outputs across multiple passes
        assert torch.equal(out1, out2)

    def test_kaiming_init_with_deep_bn_network(self, load_module):
        """Deep network initialized with Kaiming normal preserves activation scale across depth."""
        mod = load_module("deep_mlp_project", "machine-learning/09_neural_networks/05_deep_mlp_project.py")
        model = mod.DeepFaultClassifier(in_features=8, num_classes=3)
        model.apply(mod.init_weights_kaiming)
        model.eval()
        x = torch.randn(100, 8)
        out = model(x)
        assert not torch.isnan(out).any()
        assert out.std() > 0.01  # Not collapsed or dead activations


# =====================================================================
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (Pipelines & Output Artifacts)
# =====================================================================

@pytest.mark.tier4
@pytest.mark.m1
class TestTier4DLRealWorldScenarios:
    """Tier 4: End-to-end execution of deep learning lessons and output artifacts."""

    @staticmethod
    def _run_script(script_path):
        env = os.environ.copy()
        env["MKL_SERVICE_FORCE_INTEL"] = "1"
        env["MKL_THREADING_LAYER"] = "GNU"
        env["MPLBACKEND"] = "Agg"
        env["OMP_NUM_THREADS"] = "2"
        return subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            env=env
        )

    def test_batchnorm_script_execution_and_plot(self):
        """Verify 03_batch_normalization.py executes to completion and produces plot."""
        script = NN_DIR / "03_batch_normalization.py"
        plot = OUTPUT_DIR / "batchnorm_effect.png"
        res = self._run_script(script)
        assert res.returncode == 0, f"Script failed with stderr: {res.stderr}"
        assert plot.exists(), f"Expected plot {plot} was not created"
        assert plot.stat().st_size > 1000

    def test_dropout_script_execution_and_plot(self):
        """Verify 04_dropout.py executes to completion and produces plot."""
        script = NN_DIR / "04_dropout.py"
        plot = OUTPUT_DIR / "dropout_effect.png"
        res = self._run_script(script)
        assert res.returncode == 0, f"Script failed with stderr: {res.stderr}"
        assert plot.exists(), f"Expected plot {plot} was not created"
        assert plot.stat().st_size > 1000

    def test_deep_mlp_project_execution_and_artifacts(self):
        """Verify 05_deep_mlp_project.py executes to completion and produces both figures."""
        script = NN_DIR / "05_deep_mlp_project.py"
        curves_plot = OUTPUT_DIR / "training_curves.png"
        cm_plot = OUTPUT_DIR / "confusion_matrix.png"
        res = self._run_script(script)
        assert res.returncode == 0, f"Script failed with stderr: {res.stderr}"
        assert curves_plot.exists(), f"Expected plot {curves_plot} was not created"
        assert cm_plot.exists(), f"Expected plot {cm_plot} was not created"
        assert curves_plot.stat().st_size > 1000
        assert cm_plot.stat().st_size > 1000

    def test_dl_practical_test_suite_passes(self):
        """Verify machine-learning/assessment/practical_test.py executes cleanly."""
        script = REPO_ROOT / "machine-learning" / "assessment" / "practical_test.py"
        res = self._run_script(script)
        assert res.returncode == 0, f"practical_test.py failed with stderr: {res.stderr}"
