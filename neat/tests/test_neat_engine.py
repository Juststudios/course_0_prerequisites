"""Unit tests for the pure-Python NEAT engine.

Tests gene representations, innovation tracking, genome operations (crossover, mutations,
compatibility distance), phenotype evaluation (feedforward & recurrent), speciation,
and population lifecycle.
"""

import math
import random
import pytest

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.neat_engine.network import FeedForwardNetwork, RecurrentNetwork
from neat.neat_engine.population import Population
from neat.neat_engine.species import Species


class TestGenesAndInnovation:
    def test_node_gene_copy(self):
        node = NodeGene(id=1, node_type="hidden", bias=0.5, activation="relu")
        clone = node.copy()
        assert clone.id == 1
        assert clone.node_type == "hidden"
        assert clone.bias == 0.5
        assert clone.activation == "relu"
        clone.bias = 1.0
        assert node.bias == 0.5

    def test_connection_gene_copy(self):
        conn = ConnectionGene(in_node=0, out_node=2, weight=1.5, enabled=True, innovation=1)
        clone = conn.copy()
        assert clone.in_node == 0
        assert clone.out_node == 2
        assert clone.weight == 1.5
        assert clone.enabled is True
        assert clone.innovation == 1
        clone.weight = -2.0
        assert conn.weight == 1.5

    def test_innovation_tracker_memoization(self):
        tracker = InnovationTracker(initial_node_count=3)
        inv1 = tracker.get_innovation(0, 3)
        inv2 = tracker.get_innovation(0, 3)
        inv3 = tracker.get_innovation(1, 3)
        assert inv1 == inv2
        assert inv3 == inv1 + 1

    def test_innovation_tracker_reset_generation(self):
        tracker = InnovationTracker(initial_node_count=3)
        inv1 = tracker.get_innovation(0, 3)
        tracker.reset_generation()
        inv2 = tracker.get_innovation(0, 3)
        assert inv2 > inv1

    def test_innovation_tracker_node_splitting(self):
        tracker = InnovationTracker(initial_node_count=3)
        node1 = tracker.get_node_id(connection_innovation=1)
        node2 = tracker.get_node_id(connection_innovation=1)
        node3 = tracker.get_node_id(connection_innovation=2)
        assert node1 == node2
        assert node3 == node1 + 1


class TestGenomeOperations:
    @pytest.fixture
    def config(self):
        return NEATConfig(num_inputs=2, num_outputs=1, has_bias=True, pop_size=10, seed=42)

    @pytest.fixture
    def tracker(self):
        return InnovationTracker(initial_node_count=3)

    def test_minimal_genome_creation(self, config, tracker):
        g = Genome.create_minimal(config, tracker, genome_id=1)
        assert len(g.nodes) == 4  # 2 inputs (0, 1) + 1 bias (2) + 1 output (3)
        assert len(g.connections) == 3  # (0->3, 1->3, 2->3)
        for c in g.connections.values():
            assert c.enabled is True
            assert c.out_node == 3

    def test_weight_mutation(self, config, tracker):
        rng = random.Random(42)
        g = Genome.create_minimal(config, tracker, rng=rng)
        initial_weights = [c.weight for c in g.connections.values()]
        g.mutate_weights(config, rng=rng)
        mutated_weights = [c.weight for c in g.connections.values()]
        assert initial_weights != mutated_weights

    def test_add_node_mutation(self, config, tracker):
        rng = random.Random(42)
        g = Genome.create_minimal(config, tracker, rng=rng)
        orig_conn_count = len(g.connections)
        success = g.mutate_add_node(config, tracker, rng=rng)
        assert success is True
        # Original connection should be disabled
        disabled_conns = [c for c in g.connections.values() if not c.enabled]
        assert len(disabled_conns) == 1
        # Two new connections added
        assert len(g.connections) == orig_conn_count + 2
        # One new hidden node added
        hidden_nodes = [n for n in g.nodes.values() if n.node_type == "hidden"]
        assert len(hidden_nodes) == 1

    def test_add_connection_mutation(self, config, tracker):
        rng = random.Random(42)
        g = Genome.create_minimal(config, tracker, rng=rng)
        g.mutate_add_node(config, tracker, rng=rng)
        initial_count = len(g.connections)
        added = g.mutate_add_connection(config, tracker, rng=rng)
        assert added is True
        assert len(g.connections) == initial_count + 1

    def test_crossover_disjoint_excess_inheritance(self):
        p1 = Genome()
        p1.fitness = 10.0  # Fitter parent
        p1.nodes[0] = NodeGene(0, 'input')
        p1.nodes[1] = NodeGene(1, 'output')
        p1.connections[1] = ConnectionGene(0, 1, 1.0, True, 1)
        p1.connections[2] = ConnectionGene(0, 1, 2.0, True, 2)
        p1.connections[3] = ConnectionGene(0, 1, 3.0, True, 3)

        p2 = Genome()
        p2.fitness = 5.0  # Less-fit parent
        p2.nodes[0] = NodeGene(0, 'input')
        p2.nodes[1] = NodeGene(1, 'output')
        p2.connections[1] = ConnectionGene(0, 1, 10.0, True, 1)
        p2.connections[4] = ConnectionGene(0, 1, 40.0, True, 4)  # Excess in p2

        child = p1.crossover(p2, rng=random.Random(42))
        # Child must have innovations 1, 2, 3 from fitter parent
        assert set(child.connections.keys()) == {1, 2, 3}
        # Innovation 4 from less-fit parent must NOT be inherited
        assert 4 not in child.connections

    def test_compatibility_distance(self):
        g1 = Genome()
        g1.connections[1] = ConnectionGene(0, 2, 1.0, True, 1)
        g1.connections[2] = ConnectionGene(1, 2, 2.0, True, 2)

        g2 = Genome()
        g2.connections[1] = ConnectionGene(0, 2, 1.5, True, 1)
        g2.connections[3] = ConnectionGene(1, 2, 3.0, True, 3)

        # Innovation 1 is matching (weight diff = 0.5)
        # Innovation 2 is disjoint in g1 (inv 2 <= min(2, 3))
        # Innovation 3 is excess in g2 (inv 3 > min(2, 3))
        dist = g1.compatibility_distance(g2, c1=1.0, c2=1.0, c3=0.4)
        # delta = (1.0 * 1 / 1.0) + (1.0 * 1 / 1.0) + (0.4 * 0.5) = 2.2
        assert abs(dist - 2.2) < 1e-5


class TestPhenotypeNetworks:
    def test_feedforward_dag_evaluation(self):
        g = Genome()
        g.nodes[0] = NodeGene(0, 'input')
        g.nodes[1] = NodeGene(1, 'input')
        g.nodes[2] = NodeGene(2, 'bias', bias=1.0)
        g.nodes[3] = NodeGene(3, 'output', bias=0.0, activation='sigmoid')

        g.connections[1] = ConnectionGene(0, 3, 2.0, True, 1)
        g.connections[2] = ConnectionGene(1, 3, -1.0, True, 2)
        g.connections[3] = ConnectionGene(2, 3, 0.5, True, 3)

        net = FeedForwardNetwork.create(g)
        # Activation for inputs [1.0, 1.0]:
        # z = 0.0 + 1.0*2.0 + 1.0*(-1.0) + 1.0*0.5 = 1.5
        # output = 1 / (1 + exp(-1.5)) ~ 0.817574
        out = net.activate([1.0, 1.0])[0]
        expected = 1.0 / (1.0 + math.exp(-1.5))
        assert abs(out - expected) < 1e-4

    def test_feedforward_topological_sort_order(self):
        g = Genome()
        for i in [0, 1]:
            g.nodes[i] = NodeGene(i, 'input')
        g.nodes[2] = NodeGene(2, 'hidden')
        g.nodes[3] = NodeGene(3, 'hidden')
        g.nodes[4] = NodeGene(4, 'output')

        # 0 -> 2 -> 3 -> 4
        g.connections[1] = ConnectionGene(0, 2, 1.0, True, 1)
        g.connections[2] = ConnectionGene(2, 3, 1.0, True, 2)
        g.connections[3] = ConnectionGene(3, 4, 1.0, True, 3)

        net = FeedForwardNetwork.create(g)
        assert net.eval_order.index(2) < net.eval_order.index(3) < net.eval_order.index(4)

    def test_recurrent_network_state_persistence(self):
        g = Genome()
        g.nodes[0] = NodeGene(0, 'input')
        g.nodes[1] = NodeGene(1, 'output', bias=0.0, activation='tanh')
        # Self loop 1 -> 1
        g.connections[1] = ConnectionGene(0, 1, 1.0, True, 1)
        g.connections[2] = ConnectionGene(1, 1, 1.5, True, 2)

        net = RecurrentNetwork.create(g, relaxation_steps=1)
        # Pulse input
        out1 = net.activate([1.0])[0]
        assert out1 > 0.0
        # Zero input: state should persist
        out2 = net.activate([0.0])[0]
        assert out2 > 0.0


class TestSpeciationAndPopulation:
    def test_explicit_fitness_sharing(self):
        g1 = Genome(1)
        g1.fitness = 10.0
        g2 = Genome(2)
        g2.fitness = 20.0

        sp = Species(species_id=1, representative=g1)
        sp.add_member(g2)
        total_adj = sp.calculate_shared_fitness()
        # Size = 2 -> shared fitnesses are 10/2 = 5.0 and 20/2 = 10.0
        assert abs(g1.adjusted_fitness - 5.0) < 1e-4
        assert abs(g2.adjusted_fitness - 10.0) < 1e-4
        assert abs(total_adj - 15.0) < 1e-4

    def test_population_evolution_loop(self):
        cfg = NEATConfig(num_inputs=2, num_outputs=1, pop_size=20, seed=42)
        pop = Population(cfg)
        assert len(pop.population) == 20

        # Simple dummy objective: target weight sum
        def target_func(genome: Genome) -> float:
            return sum(c.weight for c in genome.connections.values())

        champ, history = pop.run(target_func, max_generations=5)
        assert champ is not None
        assert len(history['best_fitness']) == 5
        assert len(history['mean_fitness']) == 5
        assert pop.generation == 4  # 0 to 4 is 5 generations
