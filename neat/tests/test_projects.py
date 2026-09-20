"""End-to-End and Integration tests for NEAT projects (XOR and Cart-Pole)."""

import importlib
import os
import pickle
import pytest

from neat.neat_engine.network import FeedForwardNetwork


class TestXORProject:
    @pytest.fixture(scope="class")
    def xor_module(self):
        return importlib.import_module("neat.projects.01_xor.train_xor")

    @pytest.fixture(scope="class")
    def trained_xor_champion(self, xor_module, tmp_path_factory):
        tmp_dir = str(tmp_path_factory.mktemp("xor_test_output"))
        champion, history = xor_module.train_xor(output_dir=tmp_dir, seed=3, max_generations=80, fitness_threshold=3.9)
        return champion, tmp_dir

    def test_xor_fitness_threshold(self, trained_xor_champion):
        champion, _ = trained_xor_champion
        assert champion.fitness >= 3.9, f"Expected XOR fitness >= 3.9, got {champion.fitness}"

    def test_xor_truth_table_assertions(self, trained_xor_champion, xor_module):
        champion, _ = trained_xor_champion
        net = FeedForwardNetwork.create(champion)

        p00 = net.activate([0.0, 0.0])[0]
        p01 = net.activate([0.0, 1.0])[0]
        p10 = net.activate([1.0, 0.0])[0]
        p11 = net.activate([1.0, 1.0])[0]

        assert p00 < 0.25, f"XOR(0, 0) prediction {p00:.4f} exceeds 0.25"
        assert p01 > 0.75, f"XOR(0, 1) prediction {p01:.4f} is below 0.75"
        assert p10 > 0.75, f"XOR(1, 0) prediction {p10:.4f} is below 0.75"
        assert p11 < 0.25, f"XOR(1, 1) prediction {p11:.4f} exceeds 0.25"

    def test_xor_output_artifacts_generated(self, trained_xor_champion):
        _, output_dir = trained_xor_champion
        expected_files = [
            "champion_xor.pkl",
            "xor_fitness_curve.png",
            "xor_species_tracking.png",
            "xor_best_network.png",
        ]
        for fname in expected_files:
            fpath = os.path.join(output_dir, fname)
            assert os.path.exists(fpath), f"Missing expected artifact: {fpath}"
            assert os.path.getsize(fpath) > 2000, f"Artifact {fname} is smaller than 2 KB"


class TestCartPoleProject:
    @pytest.fixture(scope="class")
    def cartpole_env_mod(self):
        return importlib.import_module("neat.projects.02_cartpole.cartpole_env")

    @pytest.fixture(scope="class")
    def cartpole_train_mod(self):
        return importlib.import_module("neat.projects.02_cartpole.train_cartpole")

    def test_cartpole_physics_environment(self, cartpole_env_mod):
        env = cartpole_env_mod.CartPoleEnv(max_steps=500)
        s0 = env.reset([0.0, 0.0, 0.0, 0.0])
        assert len(s0) == 4

        # Initial steps with upright pole should succeed
        for _ in range(3):
            s, reward, done, info = env.step(1.0)
            assert len(s) == 4
            assert reward == 1.0
            assert not done

        # Uncontrolled constant force causes pole to tip over within 15 steps
        done_flag = False
        for _ in range(20):
            s, reward, done_flag, info = env.step(1.0)
            if done_flag:
                break
        assert done_flag is True
        assert info['failed'] is True

        # Test failure boundary on extreme angle
        env.reset([0.0, 0.0, 0.5, 0.0])  # ~28 degrees, exceeds 12 deg
        s, reward, done, info = env.step(1.0)
        assert done is True
        assert info['failed'] is True

    def test_cartpole_controller_balance(self, cartpole_env_mod, cartpole_train_mod, tmp_path_factory):
        tmp_dir = str(tmp_path_factory.mktemp("cartpole_test_output"))
        champion, _ = cartpole_train_mod.train_cartpole(
            output_dir=tmp_dir,
            seed=42,
            max_generations=20,
            fitness_threshold=1500.0,
        )
        assert champion is not None

        # Validate balancing over test perturbations
        net = FeedForwardNetwork.create(champion)
        env = cartpole_env_mod.CartPoleEnv(max_steps=500)

        for tilt in [-0.05, 0.0, 0.05]:
            s = env.reset([0.0, 0.0, tilt, 0.0])
            steps = 0
            while steps < env.max_steps:
                norm_s = env.normalize_state(s)
                action = net.activate(norm_s)[0]
                s, _, done, _ = env.step(action)
                steps += 1
                if done:
                    break
            assert steps >= 500, f"Cart-Pole controller failed early on tilt {tilt} ({steps} steps)"

        # Check visual outputs
        for fname in ["champion_cartpole.pkl", "cartpole_fitness.png", "cartpole_network.png"]:
            fpath = os.path.join(tmp_dir, fname)
            assert os.path.exists(fpath), f"Missing artifact: {fpath}"
            assert os.path.getsize(fpath) > 500
