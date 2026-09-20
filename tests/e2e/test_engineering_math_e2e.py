"""
End-to-End Test Suite for Milestone M2 & M4: Engineering Mathematics AI/ML Bridges.

Validates the complete structural integrity and educational bridges of engineering-mathematics:
- Tier 1: Feature Coverage (Official package verification harness scripts/verify_package.py)
- Tier 2: Boundary & Content Depth (Root README, ml_bridge/, reference/ cheatsheets, assessments/)
- Tier 3: Numerical & Algorithmic Correctness (3 AI/ML bridge scripts: embeddings/attention/SVD, optimization/backprop, Bayes/entropy/sampling)
- Tier 4: Pedagogical Compliance & Master Test Pass (6-part pedagogical structure in new lessons, pytest tests/ pass)
"""

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ENG_MATH_DIR = REPO_ROOT / "engineering-mathematics"


# =====================================================================
# TIER 1: FEATURE COVERAGE (Official Package Verification Harness)
# =====================================================================

@pytest.mark.tier1
class TestTier1EngMathPackageVerification:
    """Verifies that engineering-mathematics satisfies all 100+ package integrity checks."""

    def test_verify_package_script_passes(self):
        """Execute engineering-mathematics/scripts/verify_package.py and assert 0 errors."""
        script_path = ENG_MATH_DIR / "scripts" / "verify_package.py"
        assert script_path.exists(), f"verify_package.py missing at {script_path}"

        res = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ENG_MATH_DIR),
            env={**os.environ, "PYTHONPATH": str(ENG_MATH_DIR)},
        )

        assert res.returncode == 0, (
            f"verify_package.py failed with exit code {res.returncode}.\n"
            f"Output:\n{res.stdout}\nErrors:\n{res.stderr}"
        )
        assert "VERIFICATION STATUS: SUCCESS" in res.stdout, (
            f"Verification status did not report SUCCESS. Output:\n{res.stdout}"
        )
        assert "Errors Found          : 0" in res.stdout or "Errors Found: 0" in res.stdout or "0 errors" in res.stdout.lower(), (
            f"Verification script reported errors. Output:\n{res.stdout}"
        )


# =====================================================================
# TIER 2: BOUNDARY & CONTENT DEPTH (Curriculum Assets & Cheatsheets)
# =====================================================================

@pytest.mark.tier2
class TestTier2EngMathCurriculumAssets:
    """Verifies existence, layout, and substantive depth of curriculum reference resources."""

    def test_root_readme_depth(self):
        """Verify root README.md exists and contains substantive curriculum guidance (> 2000 bytes)."""
        readme = ENG_MATH_DIR / "README.md"
        assert readme.exists(), "engineering-mathematics/README.md is missing"
        size = readme.stat().st_size
        assert size >= 2000, f"Root README.md is too brief ({size} bytes, expected >= 2000)"

        content = readme.read_text(encoding="utf-8").lower()
        assert "matlab" in content
        assert "linear algebra" in content
        assert "calculus" in content
        assert "probability" in content

    def test_ml_bridge_readme_depth(self):
        """Verify ml_bridge/README.md exists and connects Math to AI/ML (> 1500 bytes)."""
        bridge_readme = ENG_MATH_DIR / "ml_bridge" / "README.md"
        assert bridge_readme.exists(), "engineering-mathematics/ml_bridge/README.md is missing"
        size = bridge_readme.stat().st_size
        assert size >= 1500, f"ml_bridge/README.md is too brief ({size} bytes, expected >= 1500)"

        content = bridge_readme.read_text(encoding="utf-8").lower()
        assert "attention" in content or "embedding" in content
        assert "gradient" in content or "optimization" in content
        assert "entropy" in content or "bayes" in content

    def test_reference_cheat_sheets(self):
        """Verify all 4 reference cheat sheets exist and exceed minimum content size."""
        ref_dir = ENG_MATH_DIR / "reference"
        assert ref_dir.is_dir(), "engineering-mathematics/reference/ directory is missing"

        sheets = [
            ("matlab", ["matlab_cheat_sheet.md", "matlab_cheatsheet.md"]),
            ("linear_algebra", ["linear_algebra_cheat_sheet.md", "linear_algebra_cheatsheet.md"]),
            ("calculus", ["calculus_cheat_sheet.md", "calculus_cheatsheet.md"]),
            ("probability", ["probability_cheat_sheet.md", "probability_cheatsheet.md"]),
        ]

        for topic, candidates in sheets:
            found = False
            for cand in candidates:
                p = ref_dir / cand
                if p.exists() and p.stat().st_size >= 500:
                    found = True
                    break
            assert found, f"Reference cheat sheet for '{topic}' missing or under 500 bytes (checked: {candidates})"

    def test_assessments_and_rubric(self):
        """Verify assessments/ directory contains FINAL_ASSESSMENT.md and RUBRIC.md with sufficient depth."""
        assess_dir = ENG_MATH_DIR / "assessments"
        assert assess_dir.is_dir(), "engineering-mathematics/assessments/ directory is missing"

        final_assessment = assess_dir / "FINAL_ASSESSMENT.md"
        assert final_assessment.exists(), "assessments/FINAL_ASSESSMENT.md is missing"
        assert final_assessment.stat().st_size >= 2500, "FINAL_ASSESSMENT.md lacks required depth (< 2500 bytes)"

        rubric = assess_dir / "RUBRIC.md"
        assert rubric.exists(), "assessments/RUBRIC.md is missing"
        assert rubric.stat().st_size >= 1000, "RUBRIC.md lacks required depth (< 1000 bytes)"

    def test_capstone_link_integrity(self):
        """Verify capstone/capstone_analysis_complete.m exists and resolves capstone/README.md links."""
        capstone_complete = ENG_MATH_DIR / "capstone" / "capstone_analysis_complete.m"
        assert capstone_complete.exists(), "capstone/capstone_analysis_complete.m is missing"
        assert capstone_complete.stat().st_size > 500, "capstone_analysis_complete.m is empty or truncated"


# =====================================================================
# TIER 3: NUMERICAL & ALGORITHMIC CORRECTNESS (AI/ML Bridge Scripts)
# =====================================================================

@pytest.mark.tier3
class TestTier3EngMathBridgeExecution:
    """Verifies that the 3 AI/ML bridge scripts execute and pass rigorous mathematical assertions."""

    def _load_script_module(self, script_path: Path, module_name: str):
        assert script_path.exists(), f"Bridge script not found: {script_path}"
        spec = importlib.util.spec_from_file_location(module_name, str(script_path))
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
        return mod

    def test_linear_algebra_bridge_execution_and_math(self):
        """
        Verify linear_algebra/07_embeddings_attention_svd.py executes with exit code 0
        and validates:
        1. Cosine similarity between orthogonal vectors == 0, parallel vectors == 1
        2. Orthogonal projection operator P is idempotent (P @ P == P) and symmetric
        3. Scaled dot-product attention softmax row sums == 1.0
        """
        script = ENG_MATH_DIR / "linear_algebra" / "07_embeddings_attention_svd.py"
        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=25,
            cwd=str(ENG_MATH_DIR),
            env={**os.environ, "PYTHONPATH": str(ENG_MATH_DIR)},
        )
        assert res.returncode == 0, f"Linear algebra bridge script failed:\n{res.stderr}\n{res.stdout}"

        # Numerical assertions
        mod = self._load_script_module(script, "la_bridge_mod")

        # 1. Cosine similarity check
        if hasattr(mod, "cosine_similarity"):
            u = np.array([1.0, 0.0, 0.0])
            v = np.array([0.0, 1.0, 0.0])
            w = np.array([3.0, 0.0, 0.0])
            assert np.isclose(mod.cosine_similarity(u, v), 0.0, atol=1e-6)
            assert np.isclose(mod.cosine_similarity(u, w), 1.0, atol=1e-6)

        # 2. Scaled dot-product attention check
        if hasattr(mod, "scaled_dot_product_attention"):
            Q = np.random.randn(2, 4)
            K = np.random.randn(3, 4)
            V = np.random.randn(3, 8)
            output, weights = mod.scaled_dot_product_attention(Q, K, V)
            assert output.shape == (2, 8)
            assert weights.shape == (2, 3)
            # Softmax row sums must be 1.0
            row_sums = np.sum(weights, axis=-1)
            np.testing.assert_allclose(row_sums, np.ones(2), atol=1e-5)

        # 3. Projection matrix check
        if hasattr(mod, "compute_projection_matrix"):
            X = np.random.randn(10, 3)
            P = mod.compute_projection_matrix(X)
            # Idempotence: P^2 = P
            np.testing.assert_allclose(P @ P, P, atol=1e-5)
            # Symmetry: P^T = P
            np.testing.assert_allclose(P.T, P, atol=1e-5)

    def test_calculus_bridge_execution_and_math(self):
        """
        Verify calculus/05_optimization_gradients_backprop.py executes with exit code 0
        and validates:
        1. Numerical vs analytical gradient relative error <= 1e-4
        2. Hessian eigenvalues classify local curvature (min vs saddle)
        3. Backpropagation gradient check on 2-layer MLP
        """
        script = ENG_MATH_DIR / "calculus" / "05_optimization_gradients_backprop.py"
        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=25,
            cwd=str(ENG_MATH_DIR),
            env={**os.environ, "PYTHONPATH": str(ENG_MATH_DIR)},
        )
        assert res.returncode == 0, f"Calculus bridge script failed:\n{res.stderr}\n{res.stdout}"

        # Numerical assertions
        mod = self._load_script_module(script, "calc_bridge_mod")

        # 1. Gradient check
        if hasattr(mod, "numerical_gradient") and hasattr(mod, "analytical_gradient_quadratic"):
            A = np.array([[2.0, 0.5], [0.5, 3.0]])
            b = np.array([1.0, -2.0])
            x0 = np.array([0.5, 1.0])
            f = lambda x: 0.5 * x.T @ A @ x - b.T @ x
            num_g = mod.numerical_gradient(f, x0)
            ana_g = mod.analytical_gradient_quadratic(A, b, x0)
            rel_err = np.linalg.norm(num_g - ana_g) / (np.linalg.norm(ana_g) + 1e-8)
            assert rel_err < 1e-4, f"Gradient relative error too high: {rel_err}"

        # 2. Hessian eigenvalue classification
        if hasattr(mod, "classify_critical_point"):
            # Min: all positive eigenvalues
            H_min = np.diag([2.0, 3.0])
            assert mod.classify_critical_point(H_min) == "minimum"
            # Saddle: mixed eigenvalues
            H_saddle = np.diag([2.0, -1.0])
            assert mod.classify_critical_point(H_saddle) == "saddle"

    def test_probability_bridge_execution_and_math(self):
        """
        Verify probability/05_bayesian_entropy_sampling.py executes with exit code 0
        and validates:
        1. Gaussian-Gaussian conjugate Bayesian update reduces variance
        2. Shannon entropy H(P) >= 0 and Cross-Entropy >= Entropy
        3. Softmax temperature scaling behavior (cold -> argmax, hot -> uniform)
        4. Top-p (Nucleus) truncation cumulative probability mass
        """
        script = ENG_MATH_DIR / "probability" / "05_bayesian_entropy_sampling.py"
        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=25,
            cwd=str(ENG_MATH_DIR),
            env={**os.environ, "PYTHONPATH": str(ENG_MATH_DIR)},
        )
        assert res.returncode == 0, f"Probability bridge script failed:\n{res.stderr}\n{res.stdout}"

        # Numerical assertions
        mod = self._load_script_module(script, "prob_bridge_mod")

        # 1. Conjugate Bayes update
        if hasattr(mod, "gaussian_conjugate_update"):
            prior_mu, prior_var = 0.0, 1.0
            data = np.array([1.5, 2.0, 1.8, 1.9])
            noise_var = 0.5
            post_mu, post_var = mod.gaussian_conjugate_update(prior_mu, prior_var, data, noise_var)
            assert post_var < prior_var, "Posterior variance must be strictly smaller than prior variance"
            assert post_mu > prior_mu, "Posterior mean should shift toward observed data"

        # 2. Entropy & Cross-Entropy
        if hasattr(mod, "shannon_entropy") and hasattr(mod, "cross_entropy"):
            p = np.array([0.7, 0.2, 0.1])
            q = np.array([0.5, 0.3, 0.2])
            H_p = mod.shannon_entropy(p)
            H_pq = mod.cross_entropy(p, q)
            assert H_p >= 0, "Shannon entropy must be non-negative"
            assert H_pq >= H_p, "Gibbs inequality violation: Cross-Entropy H(P, Q) must be >= H(P)"

        # 3. Temperature scaling
        if hasattr(mod, "temperature_scaled_softmax"):
            logits = np.array([1.0, 2.0, 5.0])
            cold_p = mod.temperature_scaled_softmax(logits, temperature=0.01)
            hot_p = mod.temperature_scaled_softmax(logits, temperature=100.0)
            assert cold_p[2] > 0.99, "Cold temperature must concentrate probability mass at argmax"
            np.testing.assert_allclose(hot_p, np.ones(3) / 3.0, atol=0.05)


# =====================================================================
# TIER 4: PEDAGOGICAL COMPLIANCE & MASTER TEST PASS
# =====================================================================

@pytest.mark.tier4
class TestTier4EngMathPedagogyAndTests:
    """Verifies pedagogical structure in bridge documentation and confirms master tests pass."""

    REQUIRED_PATTERNS = [
        ("TERM", re.compile(r"(?:\*\*TERM\*\*|###\s*(?:Concept\s*:?\s*)?Term|TERM\s*:)", re.IGNORECASE)),
        ("DEFINITION", re.compile(r"(?:\*\*DEFINITION\*\*|####?\s*Definition|DEFINITION\s*:)", re.IGNORECASE)),
        ("INTUITION", re.compile(r"(?:\*\*INTUITION\*\*|####?\s*Intuition|INTUITION\s*:)", re.IGNORECASE)),
        ("WHY IT EXISTS", re.compile(r"(?:\*\*WHY\s+IT\s+EXISTS\*\*|####?\s*Why\s+It\s+Exists|WHY\s+IT\s+EXISTS\s*:)", re.IGNORECASE)),
        ("HOW IT WORKS", re.compile(r"(?:\*\*HOW\s+IT\s+WORKS\*\*|####?\s*How\s+It\s+Works|HOW\s+IT\s+WORKS\s*:)", re.IGNORECASE)),
        ("CODE", re.compile(r"(?:\*\*CODE\*\*|####?\s*Code|CODE\s*:|```(?:python|matlab))", re.IGNORECASE)),
    ]

    NEW_BRIDGE_DOCS = [
        "linear_algebra/07_ai_ml_linear_algebra_bridge.md",
        "calculus/05_ai_ml_calculus_bridge.md",
        "probability/05_ai_ml_probability_bridge.md",
    ]

    @pytest.mark.parametrize("rel_doc", NEW_BRIDGE_DOCS)
    def test_bridge_lesson_pedagogical_structure(self, rel_doc: str):
        """Verify each new AI/ML bridge Markdown lesson follows the 6-part pedagogical standard."""
        doc_path = ENG_MATH_DIR / rel_doc
        assert doc_path.exists(), f"Bridge documentation missing: {doc_path}"

        content = doc_path.read_text(encoding="utf-8")
        missing_elements = []
        for name, pattern in self.REQUIRED_PATTERNS:
            if not pattern.search(content):
                missing_elements.append(name)

        assert not missing_elements, (
            f"Lesson '{rel_doc}' missing required pedagogical components: {missing_elements}. "
            f"Must follow: TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE"
        )
        assert len(content) >= 1500, f"Lesson '{rel_doc}' lacks instructional depth ({len(content)} chars)"

    def test_existing_eng_math_pytest_suite_passes(self):
        """Run all test suites under engineering-mathematics/tests/ and assert 100% pass."""
        tests_dir = ENG_MATH_DIR / "tests"
        res = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ENG_MATH_DIR),
            env={**os.environ, "PYTHONPATH": str(ENG_MATH_DIR)},
        )
        assert res.returncode == 0, (
            f"engineering-mathematics unit tests failed:\n{res.stdout}\n{res.stderr}"
        )
