"""Phenotype network decoding and evaluation for NEAT.

Implements FeedForwardNetwork (using Kahn's topological sort for DAG evaluation)
and RecurrentNetwork (for recurrent / stateful activation dynamics).
"""

import math
from typing import Dict, List, Optional, Set, Tuple

from neat.neat_engine.genome import Genome


def _clip(val: float, low: float = -30.0, high: float = 30.0) -> float:
    return max(low, min(high, val))


def _activate_node(z: float, func_name: str) -> float:
    """Apply activation function with numerical stability clipping."""
    z_clipped = _clip(z)
    if func_name == 'sigmoid':
        return 1.0 / (1.0 + math.exp(-z_clipped))
    elif func_name == 'tanh':
        return math.tanh(z_clipped)
    elif func_name == 'relu':
        return max(0.0, z)
    elif func_name == 'identity':
        return z
    else:
        # Default to sigmoid
        return 1.0 / (1.0 + math.exp(-z_clipped))


class FeedForwardNetwork:
    """Directed Acyclic Graph (DAG) feedforward neural network phenotype."""

    def __init__(
        self,
        inputs: List[int],
        outputs: List[int],
        eval_order: List[int],
        in_edges: Dict[int, List[Tuple[int, float]]],
        node_bias: Dict[int, float],
        node_activation: Dict[int, str],
        bias_node_id: Optional[int] = None,
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.eval_order = eval_order
        self.in_edges = in_edges
        self.node_bias = node_bias
        self.node_activation = node_activation
        self.bias_node_id = bias_node_id

    @classmethod
    def create(cls, genome: Genome) -> 'FeedForwardNetwork':
        """Decode a genome into a feedforward computational graph using Kahn's topological sort."""
        input_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'input']
        input_nodes.sort()

        bias_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'bias']
        bias_id = bias_nodes[0] if bias_nodes else None

        output_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'output']
        output_nodes.sort()

        node_bias = {nid: n.bias for nid, n in genome.nodes.items()}
        node_activation = {nid: n.activation for nid, n in genome.nodes.items()}

        # Build in-edges and adjacency from enabled connections
        in_edges: Dict[int, List[Tuple[int, float]]] = {nid: [] for nid in genome.nodes}
        adj: Dict[int, List[int]] = {nid: [] for nid in genome.nodes}
        in_degree: Dict[int, int] = {nid: 0 for nid in genome.nodes}

        for conn in genome.connections.values():
            if conn.enabled:
                if conn.in_node in in_edges and conn.out_node in in_edges:
                    in_edges[conn.out_node].append((conn.in_node, conn.weight))
                    adj[conn.in_node].append(conn.out_node)
                    in_degree[conn.out_node] += 1

        # Kahn's topological sort
        queue = [nid for nid in genome.nodes if in_degree[nid] == 0]
        full_order: List[int] = []

        while queue:
            curr = queue.pop(0)
            full_order.append(curr)
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # In case of broken cycles or unreachable nodes, append remaining
        if len(full_order) < len(genome.nodes):
            remaining = [nid for nid in genome.nodes if nid not in full_order]
            full_order.extend(remaining)

        # Evaluation order consists of hidden and output nodes
        eval_order = [nid for nid in full_order if genome.nodes[nid].node_type in ('hidden', 'output')]

        return cls(
            inputs=input_nodes,
            outputs=output_nodes,
            eval_order=eval_order,
            in_edges=in_edges,
            node_bias=node_bias,
            node_activation=node_activation,
            bias_node_id=bias_id,
        )

    def activate(self, inputs: List[float]) -> List[float]:
        """Compute feedforward activation through the network."""
        if len(inputs) != len(self.inputs):
            raise ValueError(f"Expected {len(self.inputs)} inputs, got {len(inputs)}")

        values: Dict[int, float] = {}

        # 1. Set input node activations
        for i, inp_id in enumerate(self.inputs):
            values[inp_id] = float(inputs[i])

        # 2. Set bias node activation
        if self.bias_node_id is not None:
            values[self.bias_node_id] = 1.0

        # 3. Evaluate hidden and output nodes in topological order
        for nid in self.eval_order:
            z = self.node_bias.get(nid, 0.0)
            for in_node, weight in self.in_edges.get(nid, []):
                z += values.get(in_node, 0.0) * weight
            act_func = self.node_activation.get(nid, 'sigmoid')
            values[nid] = _activate_node(z, act_func)

        # 4. Return output activations
        return [values[out_id] for out_id in self.outputs]


class RecurrentNetwork:
    """Recurrent neural network phenotype maintaining internal hidden state over time."""

    def __init__(
        self,
        inputs: List[int],
        outputs: List[int],
        all_nodes: List[int],
        in_edges: Dict[int, List[Tuple[int, float]]],
        node_bias: Dict[int, float],
        node_activation: Dict[int, str],
        bias_node_id: Optional[int] = None,
        relaxation_steps: int = 2,
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.all_nodes = all_nodes
        self.in_edges = in_edges
        self.node_bias = node_bias
        self.node_activation = node_activation
        self.bias_node_id = bias_node_id
        self.relaxation_steps = relaxation_steps
        self.state: Dict[int, float] = {nid: 0.0 for nid in all_nodes}

    @classmethod
    def create(cls, genome: Genome, relaxation_steps: int = 2) -> 'RecurrentNetwork':
        """Instantiate a recurrent phenotype from genome."""
        input_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'input']
        input_nodes.sort()

        bias_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'bias']
        bias_id = bias_nodes[0] if bias_nodes else None

        output_nodes = [nid for nid, n in genome.nodes.items() if n.node_type == 'output']
        output_nodes.sort()

        all_nodes = list(genome.nodes.keys())
        node_bias = {nid: n.bias for nid, n in genome.nodes.items()}
        node_activation = {nid: n.activation for nid, n in genome.nodes.items()}

        in_edges: Dict[int, List[Tuple[int, float]]] = {nid: [] for nid in all_nodes}
        for conn in genome.connections.values():
            if conn.enabled and conn.out_node in in_edges:
                in_edges[conn.out_node].append((conn.in_node, conn.weight))

        return cls(
            inputs=input_nodes,
            outputs=output_nodes,
            all_nodes=all_nodes,
            in_edges=in_edges,
            node_bias=node_bias,
            node_activation=node_activation,
            bias_node_id=bias_id,
            relaxation_steps=relaxation_steps,
        )

    def reset(self) -> None:
        """Reset internal recurrent activation states to zero."""
        self.state = {nid: 0.0 for nid in self.all_nodes}

    def activate(self, inputs: List[float]) -> List[float]:
        """Compute recurrent network output across relaxation steps."""
        if len(inputs) != len(self.inputs):
            raise ValueError(f"Expected {len(self.inputs)} inputs, got {len(inputs)}")

        # Step inputs and bias
        for i, inp_id in enumerate(self.inputs):
            self.state[inp_id] = float(inputs[i])
        if self.bias_node_id is not None:
            self.state[self.bias_node_id] = 1.0

        eval_nodes = [nid for nid in self.all_nodes if nid not in self.inputs and nid != self.bias_node_id]

        for _ in range(self.relaxation_steps):
            next_state = dict(self.state)
            for nid in eval_nodes:
                z = self.node_bias.get(nid, 0.0)
                for in_node, weight in self.in_edges.get(nid, []):
                    z += self.state.get(in_node, 0.0) * weight
                act_func = self.node_activation.get(nid, 'sigmoid')
                next_state[nid] = _activate_node(z, act_func)
            self.state = next_state

        return [self.state[out_id] for out_id in self.outputs]
