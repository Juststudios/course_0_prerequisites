"""Empirical Adversarial Verification and Stress Testing for NEAT Engine and Projects.

Authored by Challenger 1 (challenger_gate_1) for Milestone Gate Verification.
Empirically tests:
1. Innovation tracking under concurrent additions, node splitting, and generation resets.
2. Speciation compatibility distance on disjoint-only, excess-only, and weight-difference-only genomes.
3. Crossover & mutation gene alignment and node reconstruction integrity between differing fitness parents.
4. Phenotype network activation on cyclic/recurrent graphs vs feedforward DAGs, and numerical stability.
5. Project 1 (XOR) tight margin bounds and epsilon-neighborhood input perturbations.
6. Project 2 (Cart-Pole) Euler-Cromer Hamiltonian energy conservation and controller disturbance boundaries.
"""

import importlib
import math
import os
import pickle
import random
from typing import List, Tuple
import pytest

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.neat_engine.network import FeedForwardNetwork, RecurrentNetwork

_cartpole_env_mod = importlib.import_module("neat.projects.02_cartpole.cartpole_env")
CartPoleEnv = _cartpole_env_mod.CartPoleEnv


# =====================================================================
# 1. EMPIRICAL CHALLENGE: INNOVATION TRACKING
# =====================================================================
class TestAdversarialInnovationTracking:
    """Stress tests for historical markings and innovation tracking."""

    def test_concurrent_multiple_gene_additions_homology(self):
        """Verify that identical structural additions in the same generation share innovation numbers."""
        tracker = InnovationTracker(initial_node_count=4)

        # Genome 1 adds edge (0 -> 3)
        inv1 = tracker.get_innovation(0, 3)
        # Genome 2 adds identical edge (0 -> 3) in same generation
        inv2 = tracker.get_innovation(0, 3)
        # Genome 3 adds different edge (1 -> 3)
        inv3 = tracker.get_innovation(1, 3)

        assert inv1 == inv2, f"Homologous mutations in same generation must have identical innovation: {inv1} != {inv2}"
        assert inv3 == inv1 + 1, f"Novel mutation must receive sequentially next innovation: {inv3} != {inv1 + 1}"
        assert tracker.current_innovation == 2, f"Counter incremented incorrectly: {tracker.current_innovation}"

    def test_cross_generation_historical_markings(self):
        """Verify that innovation numbers increment monotonically across generation boundaries."""
        tracker = InnovationTracker(initial_node_count=4)

        inv_gen1 = tracker.get_innovation(0, 3)
        tracker.reset_generation()
        # Edge (0 -> 3) added in generation 2 should receive a NEW innovation number
        inv_gen2 = tracker.get_innovation(0, 3)

        assert inv_gen2 > inv_gen1, f"Innovation must advance across generations: gen1={inv_gen1}, gen2={inv_gen2}"
        assert inv_gen2 == inv_gen1 + 1, f"Expected sequential innovation {inv_gen1 + 1}, got {inv_gen2}"

    def test_concurrent_node_splits_homology(self):
        """Verify that splitting the same connection across distinct genomes preserves node ID and edge innovations."""
        tracker = InnovationTracker(initial_node_count=4)  # nodes 0, 1, 2, 3

        # In generation 1, Connection 1 (0 -> 3) is split
        node_a = tracker.get_node_id(connection_innovation=1)
        in_edge_a = tracker.get_innovation(0, node_a)
        out_edge_a = tracker.get_innovation(node_a, 3)

        # In same generation 1, another genome splits the same Connection 1
        node_b = tracker.get_node_id(connection_innovation=1)
        in_edge_b = tracker.get_innovation(0, node_b)
        out_edge_b = tracker.get_innovation(node_b, 3)

        assert node_a == node_b == 5, f"Split node ID mismatch: node_a={node_a}, node_b={node_b}"
        assert in_edge_a == in_edge_b, f"Input connection innovation mismatch: {in_edge_a} != {in_edge_b}"
        assert out_edge_a == out_edge_b, f"Output connection innovation mismatch: {out_edge_a} != {out_edge_b}"

    def test_high_volume_stochastic_mutation_invariants(self):
        """Stress test tracker under high mutation volume with 50 genomes and 1000 mutations."""
        tracker = InnovationTracker(initial_node_count=5)
        seen_edges_this_gen = {}

        for gen in range(10):
            tracker.reset_generation()
            seen_edges_this_gen.clear()

            for _ in range(100):
                u = random.randint(0, 10)
                v = random.randint(0, 10)
                inv = tracker.get_innovation(u, v)

                if (u, v) in seen_edges_this_gen:
                    assert inv == seen_edges_this_gen[(u, v)], "Cached innovation inconsistency within generation"
                else:
                    seen_edges_this_gen[(u, v)] = inv

        assert tracker.current_innovation > 100, "Tracker failed to accumulate innovations across generations"


# =====================================================================
# 2. EMPIRICAL CHALLENGE: SPECIATION & COMPATIBILITY DISTANCE
# =====================================================================
class TestAdversarialSpeciationAndCompatibility:
    """Stress tests for compatibility distance edge cases and metric invariants."""

    def _build_simple_genome(self, conn_dict: dict, nodes_count: int = 4) -> Genome:
        g = Genome()
        for i in range(nodes_count):
            g.nodes[i] = NodeGene(id=i, node_type="input" if i < 2 else ("bias" if i == 2 else "output"))
        for inv, (u, v, w, en) in conn_dict.items():
            g.connections[inv] = ConnectionGene(in_node=u, out_node=v, weight=w, enabled=en, innovation=inv)
        return g

    def test_disjoint_only_distance(self):
        """Disjoint genes only: Both genomes share max innovation, but have differing interior innovations."""
        # Genome 1: Inovations 1, 3 (weight 1.0)
        # Genome 2: Innovations 1, 2, 3 (weight 1.0)
        # Max in both is 3. Innovation 2 is <= 3, so it is strictly DISJOINT.
        # Excess = 0, Disjoint = 1, Avg Weight Diff = 0.0.
        # N < 20, so N_normalizer = 1.0.
        c1, c2, c3 = 1.5, 2.0, 0.4
        g1 = self._build_simple_genome({1: (0, 3, 1.0, True), 3: (1, 3, 1.0, True)})
        g2 = self._build_simple_genome({1: (0, 3, 1.0, True), 2: (2, 3, 1.0, True), 3: (1, 3, 1.0, True)})

        dist = g1.compatibility_distance(g2, c1=c1, c2=c2, c3=c3)
        expected = c2 * 1.0 / 1.0  # 1 disjoint gene, normalizer 1.0
        assert math.isclose(dist, expected, rel_tol=1e-9), f"Disjoint-only distance mismatch: {dist} vs {expected}"

    def test_excess_only_distance(self):
        """Excess genes only: One genome extends strictly beyond the maximum innovation of the other."""
        # Genome 1: Innovations 1, 2 (weight 1.0)
        # Genome 2: Innovations 1, 2, 4, 5 (weight 1.0)
        # Max of g1 is 2. Max of g2 is 5. Threshold = 2.
        # Innovations 4 and 5 are > 2, so strictly EXCESS.
        # Excess = 2, Disjoint = 0, Avg Weight Diff = 0.0.
        c1, c2, c3 = 1.5, 2.0, 0.4
        g1 = self._build_simple_genome({1: (0, 3, 1.0, True), 2: (1, 3, 1.0, True)})
        g2 = self._build_simple_genome({
            1: (0, 3, 1.0, True),
            2: (1, 3, 1.0, True),
            4: (2, 3, 1.0, True),
            5: (0, 3, 1.0, True),
        })

        dist = g1.compatibility_distance(g2, c1=c1, c2=c2, c3=c3)
        expected = c1 * 2.0 / 1.0  # 2 excess genes, normalizer 1.0
        assert math.isclose(dist, expected, rel_tol=1e-9), f"Excess-only distance mismatch: {dist} vs {expected}"

    def test_weight_difference_only_distance(self):
        """Weight difference only: Identical topology (0 disjoint, 0 excess), purely differing weights."""
        c1, c2, c3 = 1.0, 1.0, 0.5
        g1 = self._build_simple_genome({1: (0, 3, 1.0, True), 2: (1, 3, 2.5, True)})
        g2 = self._build_simple_genome({1: (0, 3, 1.8, True), 2: (1, 3, 1.5, True)})
        # Weight diffs: |1.0 - 1.8| = 0.8, |2.5 - 1.5| = 1.0. Mean = 0.9.
        # Excess = 0, Disjoint = 0.
        dist = g1.compatibility_distance(g2, c1=c1, c2=c2, c3=c3)
        expected = c3 * 0.9
        assert math.isclose(dist, expected, rel_tol=1e-9), f"Weight-only distance mismatch: {dist} vs {expected}"

    def test_normalizer_threshold_scaling_at_twenty(self):
        """Verify normalizer N transitions from 1.0 (N < 20) to float(N) (N >= 20)."""
        c1, c2, c3 = 1.0, 1.0, 0.0
        # 19 genes
        conns_19 = {i: (0, 3, 1.0, True) for i in range(1, 20)}
        g_base = self._build_simple_genome(conns_19)
        # g_sub has 10 matching genes
        conns_10 = {i: (0, 3, 1.0, True) for i in range(1, 11)}
        g_sub = self._build_simple_genome(conns_10)

        # N = 19 < 20 -> normalizer is 1.0. Disjoint/excess = 9 genes.
        dist_19 = g_base.compatibility_distance(g_sub, c1=c1, c2=c2, c3=c3)
        assert math.isclose(dist_19, 9.0, rel_tol=1e-9)

        # Now add 1 gene to reach N = 20 -> normalizer becomes 20.0. Disjoint/excess = 10 genes.
        conns_20 = {i: (0, 3, 1.0, True) for i in range(1, 21)}
        g_20 = self._build_simple_genome(conns_20)
        dist_20 = g_20.compatibility_distance(g_sub, c1=c1, c2=c2, c3=c3)
        assert math.isclose(dist_20, 10.0 / 20.0, rel_tol=1e-9)

    def test_metric_symmetry_and_identity(self):
        """Verify metric symmetry: dist(A, B) == dist(B, A) and identity dist(A, A) == 0."""
        rng = random.Random(123)
        config = NEATConfig(num_inputs=3, num_outputs=2)
        tracker = InnovationTracker(initial_node_count=6)

        genomes = [Genome.create_minimal(config, tracker, genome_id=i, rng=rng) for i in range(10)]
        for g in genomes:
            for _ in range(5):
                if rng.random() < 0.5:
                    g.mutate_add_connection(config, tracker, rng=rng)
                else:
                    g.mutate_add_node(config, tracker, rng=rng)
                g.mutate_weights(config, rng=rng)

        for i in range(len(genomes)):
            # Identity
            assert genomes[i].compatibility_distance(genomes[i]) == 0.0
            for j in range(i + 1, len(genomes)):
                d_ij = genomes[i].compatibility_distance(genomes[j])
                d_ji = genomes[j].compatibility_distance(genomes[i])
                assert math.isclose(d_ij, d_ji, rel_tol=1e-9), f"Asymmetric distance: {d_ij} != {d_ji}"
                assert d_ij >= 0.0, f"Negative distance: {d_ij}"

    def test_empty_genomes_compatibility(self):
        """Verify compatibility distance when one or both genomes have zero connections."""
        g_empty1 = Genome()
        g_empty2 = Genome()
        assert g_empty1.compatibility_distance(g_empty2) == 0.0

        g_nonempty = self._build_simple_genome({1: (0, 3, 1.0, True), 2: (1, 3, 1.0, True)})
        dist = g_empty1.compatibility_distance(g_nonempty, c1=1.0)
        assert dist == 2.0  # 2 excess genes, normalizer 1.0


# =====================================================================
# 3. EMPIRICAL CHALLENGE: CROSSOVER & MUTATION
# =====================================================================
class TestAdversarialCrossoverAndMutation:
    """Stress tests for gene alignment and inheritance during sexual recombination."""

    def test_crossover_fitness_asymmetry_inheritance(self):
        """Disjoint and excess genes must be inherited strictly from the fitter parent."""
        g_fitter = Genome(genome_id=1)
        g_fitter.fitness = 100.0
        g_fitter.nodes = {
            0: NodeGene(0, 'input'),
            1: NodeGene(1, 'bias'),
            2: NodeGene(2, 'output'),
            10: NodeGene(10, 'hidden'),
        }
        # Fitter has matching gene 1, and disjoint gene 2, and excess gene 5
        g_fitter.connections = {
            1: ConnectionGene(0, 2, weight=1.0, enabled=True, innovation=1),
            2: ConnectionGene(0, 10, weight=2.0, enabled=True, innovation=2),
            5: ConnectionGene(10, 2, weight=5.0, enabled=True, innovation=5),
        }

        g_weaker = Genome(genome_id=2)
        g_weaker.fitness = 10.0
        g_weaker.nodes = {
            0: NodeGene(0, 'input'),
            1: NodeGene(1, 'bias'),
            2: NodeGene(2, 'output'),
            20: NodeGene(20, 'hidden'),
        }
        # Weaker has matching gene 1, and disjoint gene 3, and excess gene 6
        g_weaker.connections = {
            1: ConnectionGene(0, 2, weight=-1.0, enabled=True, innovation=1),
            3: ConnectionGene(1, 20, weight=-3.0, enabled=True, innovation=3),
            6: ConnectionGene(20, 2, weight=-6.0, enabled=True, innovation=6),
        }

        child = g_fitter.crossover(g_weaker, rng=random.Random(42))

        # Offspring must contain genes 1, 2, 5 (all from fitter)
        assert set(child.connections.keys()) == {1, 2, 5}, (
            f"Child connections must strictly match fitter parent's topology. Got {set(child.connections.keys())}"
        )
        # Weaker parent's unique genes 3 and 6 must NOT be present
        assert 3 not in child.connections
        assert 6 not in child.connections

        # Node 10 must be in child.nodes because connection 2 and 5 use it
        assert 10 in child.nodes
        # Node 20 from weaker parent must NOT be present
        assert 20 not in child.nodes

    def test_crossover_topological_node_reconstruction_integrity(self):
        """Every endpoint of every connection in child must exist in child.nodes."""
        config = NEATConfig(num_inputs=3, num_outputs=2)
        tracker = InnovationTracker(initial_node_count=6)
        rng = random.Random(999)

        for _ in range(50):
            p1 = Genome.create_minimal(config, tracker, rng=rng)
            p2 = Genome.create_minimal(config, tracker, rng=rng)

            for _ in range(8):
                p1.mutate_add_node(config, tracker, rng=rng)
                p1.mutate_add_connection(config, tracker, rng=rng)
                p2.mutate_add_node(config, tracker, rng=rng)
                p2.mutate_add_connection(config, tracker, rng=rng)

            p1.fitness = rng.uniform(0, 100)
            p2.fitness = rng.uniform(0, 100)

            child = p1.crossover(p2, rng=rng)

            # Check that every connection references valid nodes
            for conn in child.connections.values():
                assert conn.in_node in child.nodes, f"Orphan in_node {conn.in_node} not found in child.nodes"
                assert conn.out_node in child.nodes, f"Orphan out_node {conn.out_node} not found in child.nodes"

    def test_disabled_gene_inheritance_statistical_ratio(self):
        """If a gene is disabled in either parent, it has a 75% chance of being disabled in the offspring."""
        p1 = Genome()
        p1.fitness = 10.0
        p1.nodes = {0: NodeGene(0, 'input'), 1: NodeGene(1, 'output')}
        p1.connections = {1: ConnectionGene(0, 1, weight=1.0, enabled=False, innovation=1)}

        p2 = Genome()
        p2.fitness = 10.0
        p2.nodes = {0: NodeGene(0, 'input'), 1: NodeGene(1, 'output')}
        p2.connections = {1: ConnectionGene(0, 1, weight=1.0, enabled=True, innovation=1)}

        num_trials = 1000
        disabled_count = 0
        rng = random.Random(42)

        for _ in range(num_trials):
            child = p1.crossover(p2, rng=rng)
            if not child.connections[1].enabled:
                disabled_count += 1

        empirical_ratio = disabled_count / num_trials
        # Expected ratio is 0.75. With N=1000, 99.9% CI is roughly [0.71, 0.79]
        assert 0.70 <= empirical_ratio <= 0.80, f"Disabled gene inheritance ratio unexpected: {empirical_ratio:.3f}"


# =====================================================================
# 4. EMPIRICAL CHALLENGE: NETWORK ACTIVATION (DAG VS RECURRENT)
# =====================================================================
class TestAdversarialNetworkActivation:
    """Stress tests for feedforward DAG and recurrent network activations."""

    def test_feedforward_dag_analytical_verification(self):
        """Verify multi-hop feedforward calculation against exact analytical formulas."""
        # Architecture:
        # Input 0, Bias 1
        # Hidden 2: relu(in0 * 2.0 + bias * (-1.0)) = relu(2*x - 1)
        # Hidden 3: identity(h2 * 3.0 + in0 * 0.5) = 3*h2 + 0.5*x
        # Output 4: sigmoid(h3 * 1.0)
        g = Genome()
        g.nodes = {
            0: NodeGene(0, 'input', bias=0.0, activation='identity'),
            1: NodeGene(1, 'bias', bias=1.0, activation='identity'),
            2: NodeGene(2, 'hidden', bias=-1.0, activation='relu'),
            3: NodeGene(3, 'hidden', bias=0.0, activation='identity'),
            4: NodeGene(4, 'output', bias=0.0, activation='sigmoid'),
        }
        g.connections = {
            1: ConnectionGene(0, 2, weight=2.0, enabled=True, innovation=1),
            2: ConnectionGene(2, 3, weight=3.0, enabled=True, innovation=2),
            3: ConnectionGene(0, 3, weight=0.5, enabled=True, innovation=3),
            4: ConnectionGene(3, 4, weight=1.0, enabled=True, innovation=4),
        }

        net = FeedForwardNetwork.create(g)

        for x in [0.0, 1.0, 2.5, -1.0]:
            out = net.activate([x])[0]
            # Analytical:
            z2 = 2.0 * x - 1.0  # bias=-1.0 on node 2
            h2 = max(0.0, z2)
            z3 = 3.0 * h2 + 0.5 * x
            h3 = z3  # identity
            expected_out = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, h3))))

            assert math.isclose(out, expected_out, rel_tol=1e-6), f"Feedforward DAG mismatch for x={x}: {out} vs {expected_out}"

    def test_feedforward_graceful_handling_of_cycles(self):
        """FeedForwardNetwork must not hang in an infinite loop if genome contains an unintended cycle."""
        g = Genome()
        g.nodes = {
            0: NodeGene(0, 'input'),
            1: NodeGene(1, 'bias'),
            2: NodeGene(2, 'hidden'),
            3: NodeGene(3, 'hidden'),
            4: NodeGene(4, 'output'),
        }
        # Intentional cycle: 2 -> 3 and 3 -> 2
        g.connections = {
            1: ConnectionGene(0, 2, weight=1.0, enabled=True, innovation=1),
            2: ConnectionGene(2, 3, weight=1.0, enabled=True, innovation=2),
            3: ConnectionGene(3, 2, weight=1.0, enabled=True, innovation=3),  # Cycle
            4: ConnectionGene(3, 4, weight=1.0, enabled=True, innovation=4),
        }

        # Decoding must terminate
        net = FeedForwardNetwork.create(g)
        # Activation must compute finite number
        out = net.activate([1.0])
        assert len(out) == 1
        assert math.isfinite(out[0])

    def test_recurrent_network_cycle_dynamics_and_reset(self):
        """RecurrentNetwork must preserve internal hidden states across steps and clear on reset()."""
        g = Genome()
        g.nodes = {
            0: NodeGene(0, 'input'),
            1: NodeGene(1, 'output', bias=0.0, activation='identity'),
        }
        # Self-recurrent output: 1 -> 1 with weight 0.5, input 0 -> 1 with weight 1.0
        g.connections = {
            1: ConnectionGene(0, 1, weight=1.0, enabled=True, innovation=1),
            2: ConnectionGene(1, 1, weight=0.5, enabled=True, innovation=2),
        }

        rnn = RecurrentNetwork.create(g, relaxation_steps=1)
        # Step 1: Input 1.0. State[1] = 0.5 * 0.0 + 1.0 * 1.0 = 1.0
        out1 = rnn.activate([1.0])[0]
        assert math.isclose(out1, 1.0, rel_tol=1e-5)

        # Step 2: Input 0.0. State[1] = 0.5 * 1.0 + 1.0 * 0.0 = 0.5
        out2 = rnn.activate([0.0])[0]
        assert math.isclose(out2, 0.5, rel_tol=1e-5)

        # Step 3: Input 0.0. State[1] = 0.5 * 0.5 = 0.25
        out3 = rnn.activate([0.0])[0]
        assert math.isclose(out3, 0.25, rel_tol=1e-5)

        # Reset
        rnn.reset()
        out_reset = rnn.activate([0.0])[0]
        assert math.isclose(out_reset, 0.0, abs_tol=1e-5)

    def test_numerical_stability_extreme_inputs_and_weights(self):
        """Verify activation clipping prevents math.exp overflow on extreme values."""
        g = Genome()
        g.nodes = {
            0: NodeGene(0, 'input'),
            1: NodeGene(1, 'output', bias=0.0, activation='sigmoid'),
        }
        g.connections = {
            1: ConnectionGene(0, 1, weight=1e8, enabled=True, innovation=1),
        }

        net = FeedForwardNetwork.create(g)

        # Massive positive input: z clipped to 30.0 -> sigmoid ~ 1.0
        out_pos = net.activate([1e8])[0]
        assert math.isclose(out_pos, 1.0, abs_tol=1e-5)

        # Massive negative input: z clipped to -30.0 -> sigmoid ~ 0.0
        out_neg = net.activate([-1e8])[0]
        assert math.isclose(out_neg, 0.0, abs_tol=1e-5)


# =====================================================================
# 5. EMPIRICAL CHALLENGE: PROJECT 1 (XOR) CORNERS & PERTURBATIONS
# =====================================================================
class TestAdversarialProject1XOR:
    """Stress tests for trained XOR neural network model."""

    @pytest.fixture
    def champion_xor_network(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        pkl_path = os.path.join(repo_root, "neat/projects/01_xor/output/champion_xor.pkl")
        if not os.path.exists(pkl_path):
            train_mod = importlib.import_module("neat.projects.01_xor.train_xor")
            champion, _ = train_mod.train_xor()
        else:
            with open(pkl_path, "rb") as f:
                champion = pickle.load(f)
        return FeedForwardNetwork.create(champion)

    def test_xor_corner_tight_margins(self, champion_xor_network):
        """Evaluate XOR predictions on all 4 corners with tight margins."""
        corners = [
            ([0.0, 0.0], 0.0, "<", 0.15),
            ([0.0, 1.0], 1.0, ">", 0.80),
            ([1.0, 0.0], 1.0, ">", 0.80),
            ([1.0, 1.0], 0.0, "<", 0.20),
        ]
        for inp, target, op, bound in corners:
            pred = champion_xor_network.activate(inp)[0]
            if op == "<":
                assert pred < bound, f"XOR({inp}) predicted {pred:.4f}, expected < {bound}"
            else:
                assert pred > bound, f"XOR({inp}) predicted {pred:.4f}, expected > {bound}"

            # Margin from 0.5 decision boundary
            margin = abs(pred - 0.5)
            assert margin >= 0.30, f"Decision margin too narrow for {inp}: margin={margin:.4f}"

    def test_xor_epsilon_neighborhood_robustness(self, champion_xor_network):
        """Verify model output stability under continuous perturbations near the 4 corners."""
        rng = random.Random(42)
        epsilons = [0.01, 0.03, 0.05]

        for eps in epsilons:
            # (0, 0) neighborhood -> should remain < 0.35
            for _ in range(25):
                dx = rng.uniform(0.0, eps)
                dy = rng.uniform(0.0, eps)
                pred = champion_xor_network.activate([dx, dy])[0]
                assert pred < 0.35, f"Perturbation near (0,0) with eps={eps} failed: pred={pred:.4f}"

            # (0, 1) neighborhood -> should remain > 0.65
            for _ in range(25):
                dx = rng.uniform(0.0, eps)
                dy = rng.uniform(1.0 - eps, 1.0)
                pred = champion_xor_network.activate([dx, dy])[0]
                assert pred > 0.65, f"Perturbation near (0,1) with eps={eps} failed: pred={pred:.4f}"

            # (1, 0) neighborhood -> should remain > 0.65
            for _ in range(25):
                dx = rng.uniform(1.0 - eps, 1.0)
                dy = rng.uniform(0.0, eps)
                pred = champion_xor_network.activate([dx, dy])[0]
                assert pred > 0.65, f"Perturbation near (1,0) with eps={eps} failed: pred={pred:.4f}"

            # (1, 1) neighborhood -> should remain < 0.35
            for _ in range(25):
                dx = rng.uniform(1.0 - eps, 1.0)
                dy = rng.uniform(1.0 - eps, 1.0)
                pred = champion_xor_network.activate([dx, dy])[0]
                assert pred < 0.35, f"Perturbation near (1,1) with eps={eps} failed: pred={pred:.4f}"

    def test_xor_decision_surface_continuity(self, champion_xor_network):
        """Evaluate grid over [0,1]x[0,1] to ensure smooth, finite predictions."""
        grid_steps = 20
        preds = []
        for i in range(grid_steps + 1):
            x = i / grid_steps
            for j in range(grid_steps + 1):
                y = j / grid_steps
                p = champion_xor_network.activate([x, y])[0]
                assert math.isfinite(p)
                assert 0.0 <= p <= 1.0
                preds.append(p)

        assert min(preds) < 0.05
        assert max(preds) > 0.90


# =====================================================================
# 6. EMPIRICAL CHALLENGE: PROJECT 2 (CART-POLE) PHYSICS & STABILITY
# =====================================================================
class TestAdversarialProject2CartPole:
    """Stress tests for Cart-Pole dynamical simulator and balance controller."""

    @pytest.fixture
    def champion_cartpole_network(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        pkl_path = os.path.join(repo_root, "neat/projects/02_cartpole/output/champion_cartpole.pkl")
        if not os.path.exists(pkl_path):
            train_mod = importlib.import_module("neat.projects.02_cartpole.train_cartpole")
            champion, _ = train_mod.train_cartpole()
        else:
            with open(pkl_path, "rb") as f:
                champion = pickle.load(f)
        return FeedForwardNetwork.create(champion)

    def _calculate_total_mechanical_energy(self, env: CartPoleEnv, state: List[float]) -> float:
        """Calculate exact mechanical energy E = T + V for cart-pole system.
        
        T = 0.5 * (M + m) * x_dot^2 + m * l * x_dot * theta_dot * cos(theta) + (2/3) * m * l^2 * theta_dot^2
        V = m * g * l * cos(theta)
        """
        x, x_dot, theta, theta_dot = state
        M = env.masscart
        m = env.masspole
        l = env.length
        g = env.gravity

        T = (
            0.5 * (M + m) * (x_dot ** 2)
            + m * l * x_dot * theta_dot * math.cos(theta)
            + (2.0 / 3.0) * m * (l ** 2) * (theta_dot ** 2)
        )
        V = m * g * l * math.cos(theta)
        return T + V

    def test_euler_cromer_energy_conservation_unforced(self):
        """Verify that symplectic Euler-Cromer integration bounds energy oscillations under free motion."""
        env = CartPoleEnv(max_steps=2000)
        # Set force magnitude to 0.0 to observe unforced Hamiltonian dynamics
        env.force_mag = 0.0

        # Small initial angle oscillation: theta = 0.05 rad (~2.8 deg)
        initial_state = [0.0, 0.0, 0.05, 0.0]
        env.reset(initial_state)

        initial_energy = self._calculate_total_mechanical_energy(env, initial_state)
        energy_history = [initial_energy]

        for _ in range(1000):
            # Step with arbitrary action (force_mag is 0.0)
            state, _, _, _ = env.step(0)
            energy = self._calculate_total_mechanical_energy(env, state)
            energy_history.append(energy)
            assert math.isfinite(energy), "Energy calculation produced NaN/Inf"

        # Check energy drift and bounded oscillations:
        # Symplectic Euler-Cromer conserves a modified shadow Hamiltonian H_shadow = H + O(tau),
        # so continuous energy oscillates with bounded amplitude O(tau) without secular divergence.
        max_energy = max(energy_history)
        min_energy = min(energy_history)
        relative_variation = (max_energy - min_energy) / abs(initial_energy)
        secular_drift = abs(energy_history[-1] - initial_energy) / abs(initial_energy)

        # In standard forward Euler, energy diverges exponentially (variation > 250%).
        # Under Euler-Cromer, peak-to-peak oscillation is bounded (< 20%) and secular drift is negligible (< 2%).
        assert relative_variation < 0.20, (
            f"Euler-Cromer bounded oscillation failed: relative variation = {relative_variation:.4f} >= 0.20"
        )
        assert secular_drift < 0.02, (
            f"Euler-Cromer secular drift failed: drift = {secular_drift:.4f} >= 0.02"
        )

    def test_physics_numerical_stability_under_extreme_dynamics(self):
        """Verify simulator does not emit NaN or inf under extreme state variables."""
        env = CartPoleEnv(max_steps=100)
        extreme_states = [
            [1000.0, 500.0, 100.0, 200.0],
            [-1000.0, -500.0, -100.0, -200.0],
            [0.0, 0.0, math.pi / 2.0, 0.0],  # horizontal pole
            [0.0, 0.0, math.pi, 0.0],  # hanging down
        ]

        for st in extreme_states:
            env.reset(st)
            for _ in range(20):
                next_st, _, _, _ = env.step(1)
                for val in next_st:
                    assert math.isfinite(val), f"Non-finite value produced from state {st}: {next_st}"

    def test_controller_stability_boundary_mining(self, champion_cartpole_network):
        """Map controller operational boundaries across varying initial angles and cart positions."""
        env = CartPoleEnv(max_steps=500)

        # Range of angles: -0.08 to +0.08 must all survive 500 steps
        safe_angles = [-0.08, -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08]
        for angle in safe_angles:
            s = env.reset([0.0, 0.0, angle, 0.0])
            steps = 0
            while steps < 500:
                action = champion_cartpole_network.activate(env.normalize_state(s))[0]
                s, _, done, _ = env.step(action)
                steps += 1
                if done:
                    break
            assert steps == 500, f"Controller failed prematurely at safe angle {angle} (survived {steps} steps)"

        # Boundary mining: angles beyond failure threshold (12 deg ~ 0.209 rad) must immediately fail
        extreme_fail_angles = [0.22, -0.22, 0.5, -0.5]
        for angle in extreme_fail_angles:
            s = env.reset([0.0, 0.0, angle, 0.0])
            s, _, done, info = env.step(1)
            assert done is True and info['failed'] is True, f"Simulator failed to register failure for extreme angle {angle}"

    def test_controller_position_displacement_stability(self, champion_cartpole_network):
        """Challenge controller when cart starts off-center with zero initial angle."""
        env = CartPoleEnv(max_steps=500)
        displacements = [-0.5, -0.2, 0.0, 0.2, 0.5]

        for pos in displacements:
            s = env.reset([pos, 0.0, 0.0, 0.0])
            steps = 0
            while steps < 500:
                action = champion_cartpole_network.activate(env.normalize_state(s))[0]
                s, _, done, _ = env.step(action)
                steps += 1
                if done:
                    break
            assert steps >= 400, f"Controller showed poor recovery for initial cart position {pos}: survived {steps} steps"

    def test_controller_impulse_disturbance_recovery(self, champion_cartpole_network):
        """Apply a lateral velocity disturbance pulse mid-run and test if controller stabilizes."""
        env = CartPoleEnv(max_steps=500)
        s = env.reset([0.0, 0.0, 0.02, 0.0])

        steps = 0
        disturbed = False

        while steps < 500:
            # At step 100, inject an impulse disturbance to pole angular velocity
            if steps == 100 and not disturbed:
                env.state[3] += 0.05  # +0.05 rad/s impulse
                disturbed = True

            action = champion_cartpole_network.activate(env.normalize_state(env.state))[0]
            s, _, done, _ = env.step(action)
            steps += 1
            if done:
                break

        assert steps == 500, f"Controller failed to recover from mid-trajectory impulse disturbance (survived {steps} steps)"
