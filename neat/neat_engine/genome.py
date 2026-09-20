"""Genome representation and genetic operators for NEAT.

Implements the Genome class containing node and connection genes,
weight mutation, structural mutations (add connection, add node),
homologous crossover via innovation alignment, and compatibility distance.
"""

import random
from typing import Dict, List, Optional, Set, Tuple

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.innovation import InnovationTracker


def _is_reachable(start: int, target: int, connections: Dict[int, ConnectionGene]) -> bool:
    """Check if target node is reachable from start node via enabled connections."""
    if start == target:
        return True
    visited: Set[int] = set()
    queue: List[int] = [start]
    while queue:
        curr = queue.pop(0)
        if curr == target:
            return True
        if curr not in visited:
            visited.add(curr)
            for conn in connections.values():
                if conn.enabled and conn.in_node == curr and conn.out_node not in visited:
                    queue.append(conn.out_node)
    return False


class Genome:
    """Represents a candidate neural network genotype."""

    def __init__(self, genome_id: int = 0):
        self.id: int = genome_id
        self.nodes: Dict[int, NodeGene] = {}
        self.connections: Dict[int, ConnectionGene] = {}  # Keyed by innovation number
        self.fitness: float = 0.0
        self.adjusted_fitness: float = 0.0
        self.species_id: Optional[int] = None

    def copy(self, new_id: Optional[int] = None) -> 'Genome':
        """Create a deep copy of this genome."""
        clone = Genome(self.id if new_id is None else new_id)
        clone.nodes = {nid: node.copy() for nid, node in self.nodes.items()}
        clone.connections = {inv: conn.copy() for inv, conn in self.connections.items()}
        clone.fitness = self.fitness
        clone.adjusted_fitness = self.adjusted_fitness
        clone.species_id = self.species_id
        return clone

    @classmethod
    def create_minimal(
        cls,
        config: NEATConfig,
        tracker: InnovationTracker,
        genome_id: int = 0,
        rng: Optional[random.Random] = None,
    ) -> 'Genome':
        """Construct a minimal starting genome with direct input/bias to output connections."""
        r = rng if rng is not None else random
        genome = cls(genome_id)

        # 1. Add input nodes
        input_ids = list(range(config.num_inputs))
        for i in input_ids:
            genome.nodes[i] = NodeGene(id=i, node_type='input', bias=0.0, activation='identity')

        # 2. Add bias node if enabled
        bias_id = None
        if config.has_bias:
            bias_id = config.num_inputs
            genome.nodes[bias_id] = NodeGene(id=bias_id, node_type='bias', bias=1.0, activation='identity')

        # 3. Add output nodes
        start_out = config.num_inputs + (1 if config.has_bias else 0)
        output_ids = list(range(start_out, start_out + config.num_outputs))
        for o in output_ids:
            genome.nodes[o] = NodeGene(
                id=o,
                node_type='output',
                bias=r.uniform(-1.0, 1.0),
                activation=config.activation_default,
            )

        # 4. Connect every input/bias to every output
        sources = input_ids + ([bias_id] if bias_id is not None else [])
        for src in sources:
            for out in output_ids:
                inv = tracker.get_innovation(src, out)
                weight = r.uniform(-1.0, 1.0)
                genome.connections[inv] = ConnectionGene(
                    in_node=src,
                    out_node=out,
                    weight=weight,
                    enabled=True,
                    innovation=inv,
                )

        return genome

    def mutate_weights(self, config: NEATConfig, rng: Optional[random.Random] = None) -> None:
        """Mutate connection weights and node biases in-place."""
        r = rng if rng is not None else random

        # Connection weights
        for conn in self.connections.values():
            if r.random() < config.weight_mutate_rate:
                if r.random() < config.weight_replace_rate:
                    conn.weight = r.uniform(-2.0, 2.0)
                else:
                    conn.weight += r.gauss(0.0, config.weight_mutate_power)

        # Node biases
        for node in self.nodes.values():
            if node.node_type in ('hidden', 'output'):
                if r.random() < config.bias_mutate_rate:
                    if r.random() < config.bias_replace_rate:
                        node.bias = r.uniform(-2.0, 2.0)
                    else:
                        node.bias += r.gauss(0.0, config.bias_mutate_power)

        # Optional toggle enabled
        if config.toggle_enabled_rate > 0 and self.connections:
            if r.random() < config.toggle_enabled_rate:
                conn = r.choice(list(self.connections.values()))
                conn.enabled = not conn.enabled

    def mutate_add_connection(
        self,
        config: NEATConfig,
        tracker: InnovationTracker,
        rng: Optional[random.Random] = None,
    ) -> bool:
        """Attempt to add a novel directed connection between two unconnected nodes."""
        r = rng if rng is not None else random
        sources = [nid for nid, node in self.nodes.items() if node.node_type in ('input', 'bias', 'hidden')]
        targets = [nid for nid, node in self.nodes.items() if node.node_type in ('hidden', 'output')]

        existing_pairs = {(conn.in_node, conn.out_node) for conn in self.connections.values()}

        # Collect candidate edges that do not already exist and do not introduce cycles
        candidate_pairs = []
        for src in sources:
            for tgt in targets:
                if src == tgt:
                    continue
                if (src, tgt) in existing_pairs:
                    continue
                if _is_reachable(tgt, src, self.connections):
                    continue  # Adding src -> tgt would form a cycle
                candidate_pairs.append((src, tgt))

        if not candidate_pairs:
            return False

        src, tgt = r.choice(candidate_pairs)
        inv = tracker.get_innovation(src, tgt)
        weight = r.uniform(-1.0, 1.0)
        self.connections[inv] = ConnectionGene(
            in_node=src,
            out_node=tgt,
            weight=weight,
            enabled=True,
            innovation=inv,
        )
        return True

    def mutate_add_node(
        self,
        config: NEATConfig,
        tracker: InnovationTracker,
        rng: Optional[random.Random] = None,
    ) -> bool:
        """Split an existing enabled connection, inserting a new hidden node."""
        r = rng if rng is not None else random
        enabled_conns = [c for c in self.connections.values() if c.enabled]
        if not enabled_conns:
            return False

        target_conn = r.choice(enabled_conns)
        target_conn.enabled = False

        new_node_id = tracker.get_node_id(target_conn.innovation)
        if new_node_id not in self.nodes:
            self.nodes[new_node_id] = NodeGene(
                id=new_node_id,
                node_type='hidden',
                bias=0.0,
                activation=config.activation_default,
            )

        # Connection in: in_node -> new_node, weight = 1.0
        inv_in = tracker.get_innovation(target_conn.in_node, new_node_id)
        self.connections[inv_in] = ConnectionGene(
            in_node=target_conn.in_node,
            out_node=new_node_id,
            weight=1.0,
            enabled=True,
            innovation=inv_in,
        )

        # Connection out: new_node -> out_node, weight = old connection weight
        inv_out = tracker.get_innovation(new_node_id, target_conn.out_node)
        self.connections[inv_out] = ConnectionGene(
            in_node=new_node_id,
            out_node=target_conn.out_node,
            weight=target_conn.weight,
            enabled=True,
            innovation=inv_out,
        )
        return True

    def crossover(self, parent2: 'Genome', rng: Optional[random.Random] = None) -> 'Genome':
        """Perform NEAT crossover with another genome using historical markings.
        
        Genes matching innovation numbers are randomly chosen from either parent.
        Disjoint and excess genes are inherited exclusively from the fitter parent.
        """
        r = rng if rng is not None else random

        if self.fitness >= parent2.fitness:
            fitter, other = self, parent2
            equal_fitness = (self.fitness == parent2.fitness)
        else:
            fitter, other = parent2, self
            equal_fitness = False

        child = Genome()

        fitter_invs = set(fitter.connections.keys())
        other_invs = set(other.connections.keys())

        common_invs = fitter_invs.intersection(other_invs)
        fitter_only_invs = fitter_invs - other_invs
        other_only_invs = other_invs - fitter_invs

        # 1. Matching genes
        for inv in common_invs:
            c1 = fitter.connections[inv]
            c2 = other.connections[inv]
            chosen = c1 if r.random() < 0.5 else c2
            gene = chosen.copy()
            # If either parent has gene disabled, 75% chance disabled in child
            if (not c1.enabled) or (not c2.enabled):
                if r.random() < 0.75:
                    gene.enabled = False
                else:
                    gene.enabled = True
            child.connections[inv] = gene

        # 2. Excess and Disjoint from fitter parent
        for inv in fitter_only_invs:
            child.connections[inv] = fitter.connections[inv].copy()

        # If equal fitness, disjoint/excess from other parent can also be inherited
        if equal_fitness:
            for inv in other_only_invs:
                if r.random() < 0.5:
                    child.connections[inv] = other.connections[inv].copy()

        # 3. Reconstruct required nodes
        # Always include all input/bias/output nodes
        for nid, node in fitter.nodes.items():
            if node.node_type in ('input', 'bias', 'output'):
                child.nodes[nid] = node.copy()

        # Include nodes referenced by active connections
        for conn in child.connections.values():
            for nid in (conn.in_node, conn.out_node):
                if nid not in child.nodes:
                    if nid in fitter.nodes:
                        child.nodes[nid] = fitter.nodes[nid].copy()
                    elif nid in other.nodes:
                        child.nodes[nid] = other.nodes[nid].copy()

        return child

    def compatibility_distance(
        self,
        other: 'Genome',
        c1: float = 1.0,
        c2: float = 1.0,
        c3: float = 0.4,
    ) -> float:
        """Compute compatibility distance delta between this genome and another.
        
        delta = (c1 * E / N) + (c2 * D / N) + (c3 * W_bar)
        where:
          E = excess genes
          D = disjoint genes
          W_bar = average absolute weight difference of matching genes
          N = maximum connection count (normalized to 1.0 if smaller than 20)
        """
        invs1 = sorted(self.connections.keys())
        invs2 = sorted(other.connections.keys())

        if not invs1 and not invs2:
            return 0.0

        max1 = max(invs1) if invs1 else 0
        max2 = max(invs2) if invs2 else 0
        common_threshold = min(max1, max2)

        set1 = set(invs1)
        set2 = set(invs2)

        matching_weight_diffs = []
        disjoint_count = 0
        excess_count = 0

        for inv in set1.union(set2):
            in1 = inv in set1
            in2 = inv in set2

            if in1 and in2:
                matching_weight_diffs.append(abs(self.connections[inv].weight - other.connections[inv].weight))
            elif in1 or in2:
                if inv > common_threshold:
                    excess_count += 1
                else:
                    disjoint_count += 1

        n_val = max(len(self.connections), len(other.connections))
        n_normalizer = float(n_val) if n_val >= 20 else 1.0

        avg_w = (sum(matching_weight_diffs) / len(matching_weight_diffs)) if matching_weight_diffs else 0.0

        return (c1 * excess_count / n_normalizer) + (c2 * disjoint_count / n_normalizer) + (c3 * avg_w)
