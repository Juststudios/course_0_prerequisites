"""Gene representations for NEAT (NeuroEvolution of Augmenting Topologies).

Provides NodeGene and ConnectionGene dataclasses representing the fundamental
units of genetic encoding in topology-evolving neural networks.
"""

from dataclasses import dataclass


@dataclass
class NodeGene:
    """Represents a single neuron in a genome."""
    id: int
    node_type: str  # 'input', 'bias', 'hidden', 'output'
    bias: float = 0.0
    activation: str = 'sigmoid'

    def copy(self) -> 'NodeGene':
        """Return a shallow copy of this node gene."""
        return NodeGene(
            id=self.id,
            node_type=self.node_type,
            bias=self.bias,
            activation=self.activation,
        )


@dataclass
class ConnectionGene:
    """Represents a directed synaptic connection between two neurons."""
    in_node: int
    out_node: int
    weight: float
    enabled: bool = True
    innovation: int = 0

    def copy(self) -> 'ConnectionGene':
        """Return a shallow copy of this connection gene."""
        return ConnectionGene(
            in_node=self.in_node,
            out_node=self.out_node,
            weight=self.weight,
            enabled=self.enabled,
            innovation=self.innovation,
        )
