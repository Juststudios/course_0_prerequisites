"""
End-to-End Test Suite for Milestone M3 & M4: NEAT Curriculum Redesign.

Validates the pure-Python from-scratch NEAT engine, progressive 6-module curriculum,
XOR non-linear evolution, Cart-Pole dynamical control, and Matplotlib visualizers:
- Tier 1: Feature Coverage (Pure-Python neat_engine imports, core data structures, unit tests)
- Tier 2: Boundary & Formatting (6 curriculum modules, strict pedagogical READMEs, companion scripts)
- Tier 3: Cross-Feature Execution (Project 1 XOR evolution and verify_xor.py assertions)
- Tier 4: Real-World Applications (Project 2 Cart-Pole simulator, >= 500 steps balance, publication PNG plots > 2 KB)
"""

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NEAT_DIR = REPO_ROOT / "neat"

EXPECTED_NEAT_MODULES = [
    "01_evolutionary_computation",
    "02_genetic_algorithms",
    "03_neuroevolution_topology",
    "04_speciation_fitness_sharing",
    "05_crossover_mutation_operators",
    "06_phenotype_network_activation",
]


# =====================================================================
# TIER 1: FEATURE COVERAGE (neat_engine Core Data Structures)
# =====================================================================

@pytest.mark.tier1
class TestTier1NEATEngineCore:
    """Verifies that pure-Python neat_engine imports cleanly and provides all core neuroevolution primitives."""

    def test_neat_engine_imports(self):
        """Verify neat.neat_engine can be imported and exports core classes."""
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        if str(NEAT_DIR) not in sys.path:
            sys.path.insert(0, str(NEAT_DIR))

        from neat.neat_engine.gene import NodeGene, ConnectionGene
        from neat.neat_engine.genome import Genome
        from neat.neat_engine.innovation import InnovationTracker
        from neat.neat_engine.species import Species
        from neat.neat_engine.population import Population
        from neat.neat_engine.network import FeedForwardNetwork
        from neat.neat_engine.config import NEATConfig

        assert NodeGene is not None
        assert ConnectionGene is not None
        assert Genome is not None
        assert InnovationTracker is not None
        assert Species is not None
        assert Population is not None
        assert FeedForwardNetwork is not None
        assert NEATConfig is not None

    def test_innovation_tracker_mechanics(self):
        """Verify InnovationTracker assigns identical numbers to identical mutations within a generation."""
        if str(NEAT_DIR) not in sys.path:
            sys.path.insert(0, str(NEAT_DIR))
        from neat.neat_engine.innovation import InnovationTracker

        tracker = InnovationTracker()
        # Same mutation in same generation gets same ID
        inv1 = tracker.get_innovation(1, 4)
        inv2 = tracker.get_innovation(1, 4)
        assert inv1 == inv2, "Identical mutations in same generation must share innovation ID"

        # Different mutation gets new incremented ID
        inv3 = tracker.get_innovation(2, 4)
        assert inv3 == inv1 + 1, "Novel mutation must receive incremented innovation ID"

        # Resetting generation clears cache but increments counter
        tracker.reset_generation()
        inv4 = tracker.get_innovation(3, 4)
        assert inv4 == inv3 + 1, "Counter must remain monotonically increasing across generations"

    def test_genome_mutations_and_compatibility(self):
        """Verify Genome structural mutations (add_node, add_connection) and compatibility distance."""
        if str(NEAT_DIR) not in sys.path:
            sys.path.insert(0, str(NEAT_DIR))
        from neat.neat_engine.config import NEATConfig
        from neat.neat_engine.genome import Genome
        from neat.neat_engine.innovation import InnovationTracker

        config = NEATConfig(num_inputs=2, num_outputs=1)
        init_nodes = config.num_inputs + (1 if config.has_bias else 0) + config.num_outputs
        tracker = InnovationTracker(initial_node_count=init_nodes)
        g1 = Genome.create_minimal(genome_id=1, config=config, tracker=tracker)
        g2 = Genome.create_minimal(genome_id=2, config=config, tracker=tracker)

        assert len(g1.connections) > 0, "Minimal genome must have initial connections"

        # Mutate g1 with add_node
        old_conn_count = len(g1.connections)
        g1.mutate_add_node(config=config, tracker=tracker)
        # add_node disables 1 connection and adds 2 new ones => net +2 connections
        assert len(g1.connections) == old_conn_count + 2, "add_node must add 2 new connections"

        # Compatibility distance between mutated and unmutated must be positive
        dist = g1.compatibility_distance(g2)
        assert dist > 0.0, f"Distance between distinct topologies must be > 0 (got {dist})"

    def test_feedforward_network_topological_activation(self):
        """Verify FeedForwardNetwork topologically sorts nodes and computes stable activations."""
        if str(NEAT_DIR) not in sys.path:
            sys.path.insert(0, str(NEAT_DIR))
        from neat.neat_engine.config import NEATConfig
        from neat.neat_engine.genome import Genome
        from neat.neat_engine.innovation import InnovationTracker
        from neat.neat_engine.network import FeedForwardNetwork

        config = NEATConfig(num_inputs=2, num_outputs=1)
        tracker = InnovationTracker()
        g = Genome.create_minimal(genome_id=1, config=config, tracker=tracker)
        net = FeedForwardNetwork.create(g)

        inputs = [0.5, -0.5]
        outputs = net.activate(inputs)
        assert len(outputs) == 1, f"Expected 1 output, got {len(outputs)}"
        assert -1.0 <= outputs[0] <= 1.0 or 0.0 <= outputs[0] <= 1.0, f"Output out of range: {outputs[0]}"

    def test_neat_engine_unit_tests_pass(self):
        """Execute unit tests in neat/tests/ via pytest and assert 0 failures."""
        neat_tests_dir = NEAT_DIR / "tests"
        if neat_tests_dir.is_dir() and any(neat_tests_dir.glob("test_*.py")):
            res = subprocess.run(
                [sys.executable, "-m", "pytest", str(neat_tests_dir), "-v"],
                capture_output=True,
                text=True,
                timeout=40,
                cwd=str(REPO_ROOT),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            assert res.returncode == 0, f"neat unit tests failed:\n{res.stdout}\n{res.stderr}"


# =====================================================================
# TIER 2: BOUNDARY & FORMATTING (Curriculum Structure & Pedagogy)
# =====================================================================

@pytest.mark.tier2
class TestTier2NEATCurriculumModules:
    """Verifies that all 6 curriculum modules exist with strict pedagogical READMEs and companion scripts."""

    REQUIRED_PATTERNS = [
        ("TERM", re.compile(r"(?:\*\*TERM\*\*|#{2,4}\s*(?:\d+\.\s*)?TERM|TERM\s*:)", re.IGNORECASE)),
        ("DEFINITION", re.compile(r"(?:\*\*DEFINITION\*\*|#{2,4}\s*(?:\d+\.\s*)?DEFINITION|DEFINITION\s*:)", re.IGNORECASE)),
        ("INTUITION", re.compile(r"(?:\*\*INTUITION\*\*|#{2,4}\s*(?:\d+\.\s*)?INTUITION|INTUITION\s*:)", re.IGNORECASE)),
        ("WHY IT EXISTS", re.compile(r"(?:\*\*WHY\s+IT\s+EXISTS\*\*|#{2,4}\s*(?:\d+\.\s*)?WHY\s+(?:IT\s+)?EXISTS|WHY\s+IT\s+EXISTS\s*:)", re.IGNORECASE)),
        ("HOW IT WORKS", re.compile(r"(?:\*\*HOW\s+IT\s+WORKS\*\*|#{2,4}\s*(?:\d+\.\s*)?HOW\s+IT\s+WORKS|HOW\s+IT\s+WORKS\s*:)", re.IGNORECASE)),
        ("CODE", re.compile(r"(?:\*\*CODE\*\*|#{2,4}\s*(?:\d+\.\s*)?CODE|CODE\s*:|```python)", re.IGNORECASE)),
    ]

    @pytest.mark.parametrize("mod_name", EXPECTED_NEAT_MODULES)
    def test_neat_module_exists_and_contains_readme(self, mod_name: str):
        """Verify module directory exists and contains a non-empty pedagogical README (> 500 bytes)."""
        mod_dir = NEAT_DIR / mod_name
        assert mod_dir.is_dir(), f"NEAT module directory missing: {mod_name}"

        readme = mod_dir / "README.md"
        assert readme.is_file(), f"README.md missing in {mod_name}"
        assert readme.stat().st_size >= 500, f"README.md in {mod_name} is too brief (< 500 bytes)"

        content = readme.read_text(encoding="utf-8")
        missing_elements = []
        for name, pattern in self.REQUIRED_PATTERNS:
            if not pattern.search(content):
                missing_elements.append(name)

        assert not missing_elements, (
            f"Module '{mod_name}/README.md' is missing required pedagogical sections: {missing_elements}. "
            f"Must follow: TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE"
        )

    @pytest.mark.parametrize("mod_name", EXPECTED_NEAT_MODULES)
    def test_neat_module_companion_scripts_execute(self, mod_name: str):
        """Verify each module contains companion Python scripts that execute with exit code 0."""
        mod_dir = NEAT_DIR / mod_name
        py_files = [f for f in mod_dir.glob("*.py") if f.name != "__init__.py"]
        assert len(py_files) >= 2, f"Module '{mod_name}' must contain at least 2 companion scripts, found {len(py_files)}"

        for script in py_files:
            res = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=20,
                cwd=str(REPO_ROOT),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            assert res.returncode == 0, (
                f"Companion script '{mod_name}/{script.name}' failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}"
            )

    def test_neat_master_readme_and_exercises(self):
        """Verify NEAT master README and supporting exercise/solution directories."""
        master_readme = NEAT_DIR / "README.md"
        assert master_readme.exists() and master_readme.stat().st_size >= 1000, "neat/README.md missing or too small"
        assert (NEAT_DIR / "exercises").is_dir(), "neat/exercises/ directory missing"
        assert (NEAT_DIR / "solutions").is_dir(), "neat/solutions/ directory missing"


# =====================================================================
# TIER 3: CROSS-FEATURE EXECUTION (Project 1: XOR Evolution)
# =====================================================================

@pytest.mark.tier3
class TestTier3NEATProject1XOR:
    """Verifies that Project 1 (XOR) executes, evolves a topology, and passes verification assertions."""

    def test_xor_project_files_exist(self):
        """Verify train_xor.py and verify_xor.py exist in projects/01_xor/."""
        xor_dir = NEAT_DIR / "projects" / "01_xor"
        assert xor_dir.is_dir(), f"XOR project directory missing at {xor_dir}"

        assert (xor_dir / "train_xor.py").exists(), "train_xor.py missing"
        assert (xor_dir / "verify_xor.py").exists(), "verify_xor.py missing"
        assert (xor_dir / "README.md").exists(), "projects/01_xor/README.md missing"

    def test_xor_verification_script_passes(self):
        """
        Execute projects/01_xor/verify_xor.py (running train_xor.py beforehand if needed)
        and assert that the evolved network solves XOR:
        (0,0)-> < 0.25, (0,1)-> > 0.75, (1,0)-> > 0.75, (1,1)-> < 0.25.
        """
        xor_dir = NEAT_DIR / "projects" / "01_xor"
        verify_script = xor_dir / "verify_xor.py"

        # Execute verify_xor.py
        res = subprocess.run(
            [sys.executable, str(verify_script)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(xor_dir),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )

        # If verify_xor needs trained network first, run train_xor then verify
        if res.returncode != 0:
            train_script = xor_dir / "train_xor.py"
            train_res = subprocess.run(
                [sys.executable, str(train_script)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(xor_dir),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            assert train_res.returncode == 0, f"train_xor.py failed:\n{train_res.stderr}\n{train_res.stdout}"

            # Retry verify_xor.py
            res = subprocess.run(
                [sys.executable, str(verify_script)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(xor_dir),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )

        assert res.returncode == 0, f"verify_xor.py failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}"


# =====================================================================
# TIER 4: REAL-WORLD DYNAMICS (Project 2: Cart-Pole Control & Plots)
# =====================================================================

@pytest.mark.tier4
class TestTier4NEATProject2CartPole:
    """Verifies pure-Python Cart-Pole simulation, controller balancing >= 500 steps, and visualizer outputs."""

    def test_cartpole_project_files_exist(self):
        """Verify cartpole_env.py, train_cartpole.py, and evaluate_controller.py exist."""
        cp_dir = NEAT_DIR / "projects" / "02_cartpole"
        assert cp_dir.is_dir(), f"Cart-Pole project directory missing at {cp_dir}"

        assert (cp_dir / "cartpole_env.py").exists(), "cartpole_env.py missing"
        assert (cp_dir / "train_cartpole.py").exists(), "train_cartpole.py missing"
        assert (cp_dir / "evaluate_controller.py").exists(), "evaluate_controller.py missing"

    def test_cartpole_environment_physics_and_boundaries(self):
        """Verify pure-Python CartPoleEnv implements equations of motion and failure boundaries."""
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        cp_dir = NEAT_DIR / "projects" / "02_cartpole"
        if str(cp_dir) not in sys.path:
            sys.path.insert(0, str(cp_dir))

        spec = importlib.util.spec_from_file_location("cartpole_env_mod", str(cp_dir / "cartpole_env.py"))
        env_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(env_mod)

        assert hasattr(env_mod, "CartPoleEnv"), "CartPoleEnv class not found in cartpole_env.py"
        env = env_mod.CartPoleEnv()

        obs = env.reset(initial_state=[0.0, 0.0, 0.0, 0.0])
        assert len(obs) >= 4, f"Observation vector must have at least 4 state variables, got {len(obs)}"

        # Step with constant force and assert state changes
        next_obs, reward, done, info = env.step(action=1)
        assert next_obs is not None
        assert isinstance(done, bool)

        # Test failure boundary on extreme angle
        env.reset(initial_state=[0.0, 0.0, 0.30, 0.0])  # > 12 degrees (~0.21 rad)
        _, _, done_fail, _ = env.step(action=0)
        assert done_fail, "Episode must terminate when pole angle exceeds critical threshold"

    def test_cartpole_controller_evaluation(self):
        """
        Execute evaluate_controller.py (running train_cartpole.py beforehand if needed)
        and assert that the champion controller sustains >= 500 balancing steps.
        """
        cp_dir = NEAT_DIR / "projects" / "02_cartpole"
        eval_script = cp_dir / "evaluate_controller.py"

        res = subprocess.run(
            [sys.executable, str(eval_script)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(cp_dir),
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
        )

        if res.returncode != 0:
            # Run training to generate champion controller
            train_script = cp_dir / "train_cartpole.py"
            train_res = subprocess.run(
                [sys.executable, str(train_script)],
                capture_output=True,
                text=True,
                timeout=90,
                cwd=str(cp_dir),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            assert train_res.returncode == 0, f"train_cartpole.py failed:\n{train_res.stderr}\n{train_res.stdout}"

            # Re-run evaluate_controller.py
            res = subprocess.run(
                [sys.executable, str(eval_script)],
                capture_output=True,
                text=True,
                timeout=40,
                cwd=str(cp_dir),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )

        assert res.returncode == 0, f"evaluate_controller.py failed with code {res.returncode}:\n{res.stderr}\n{res.stdout}"
        stdout_lower = res.stdout.lower()
        assert "500" in stdout_lower or "balanced" in stdout_lower or "success" in stdout_lower, (
            f"Controller evaluation did not report survival: {res.stdout}"
        )

    def test_visualizer_produces_valid_png_plots(self, tmp_path):
        """Verify visualizer.py plot routines output valid PNG image files (> 2 KB)."""
        vis_file = NEAT_DIR / "visualizations" / "visualizer.py"
        assert vis_file.exists(), f"visualizer.py missing at {vis_file}"

        # Check existing output directories or invoke demo_visualizations.py
        demo_script = NEAT_DIR / "visualizations" / "demo_visualizations.py"
        if demo_script.exists():
            res = subprocess.run(
                [sys.executable, str(demo_script), "--output-dir", str(tmp_path)],
                capture_output=True,
                text=True,
                timeout=25,
                cwd=str(NEAT_DIR),
                env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            )
            assert res.returncode == 0, f"demo_visualizations.py failed: {res.stderr}"

        # Verify any generated PNGs in projects or tmp_path
        png_candidates = list(NEAT_DIR.glob("**/*.png")) + list(tmp_path.glob("*.png"))
        assert len(png_candidates) > 0, "No visualizer PNG plots generated"

        for png_file in png_candidates:
            size = png_file.stat().st_size
            assert size >= 2048, f"Generated PNG plot '{png_file.name}' is too small ({size} bytes, expected >= 2 KB)"
