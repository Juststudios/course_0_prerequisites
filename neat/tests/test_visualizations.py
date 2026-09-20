"""Tests for the pure-Matplotlib NEAT visualization suite."""

import os
import pytest

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.visualizations.visualizer import plot_fitness, plot_network, plot_species


def _assert_valid_png(path: str, min_bytes: int = 2000):
    assert os.path.exists(path), f"File {path} does not exist"
    size = os.path.getsize(path)
    assert size >= min_bytes, f"File {path} size {size} is smaller than {min_bytes}"
    with open(path, "rb") as f:
        header = f.read(8)
    # PNG magic bytes: \x89PNG\r\n\x1a\n
    assert header == b"\x89PNG\r\n\x1a\n", f"Invalid PNG header in {path}"


class TestVisualizations:
    @pytest.fixture
    def tmp_vis_dir(self, tmp_path):
        out = tmp_path / "vis_output"
        out.mkdir()
        return str(out)

    def test_plot_fitness_generates_valid_png(self, tmp_vis_dir):
        save_path = os.path.join(tmp_vis_dir, "test_fitness.png")
        history = {
            "best_fitness": [1.0, 1.5, 2.2, 3.1, 3.9],
            "mean_fitness": [0.5, 0.8, 1.2, 1.8, 2.5],
        }
        plot_fitness(history, save_path=save_path, title="Unit Test Fitness", threshold=3.9)
        _assert_valid_png(save_path)

    def test_plot_species_generates_valid_png(self, tmp_vis_dir):
        save_path = os.path.join(tmp_vis_dir, "test_species.png")
        species_history = {
            1: [50, 40, 30, 20, 10],
            2: [0, 10, 20, 30, 40],
        }
        plot_species(species_history, save_path=save_path, title="Unit Test Species")
        _assert_valid_png(save_path)

    def test_plot_network_generates_valid_png(self, tmp_vis_dir):
        save_path = os.path.join(tmp_vis_dir, "test_network.png")
        cfg = NEATConfig(num_inputs=2, num_outputs=1, has_bias=True)
        tracker = InnovationTracker(initial_node_count=3)
        genome = Genome.create_minimal(cfg, tracker, genome_id=1)
        genome.mutate_add_node(cfg, tracker)
        genome.mutate_add_connection(cfg, tracker)

        plot_network(genome, save_path=save_path, title="Unit Test Topology")
        _assert_valid_png(save_path)
