"""Global Innovation Tracker for NEAT.

Maintains historical markings (innovation numbers) for connection and node
mutations across generations, solving the Competing Conventions problem
without requiring graph isomorphism tests.
"""

from typing import Dict, Tuple


class InnovationTracker:
    """Tracks global chronological innovation numbers and node IDs across evolution."""

    def __init__(self, initial_node_count: int = 0):
        self.current_innovation: int = 0
        self.current_node_id: int = initial_node_count
        self.generation_innovations: Dict[Tuple[int, int], int] = {}
        self.node_innovations: Dict[int, int] = {}

    def get_innovation(self, in_node: int, out_node: int) -> int:
        """Get or assign an innovation number for a directed edge (in_node -> out_node).
        
        If this connection was already created during the current generation,
        re-uses the existing innovation ID to keep homologous mutations aligned.
        """
        key = (in_node, out_node)
        if key in self.generation_innovations:
            return self.generation_innovations[key]
        self.current_innovation += 1
        self.generation_innovations[key] = self.current_innovation
        return self.current_innovation

    def get_node_id(self, connection_innovation: int) -> int:
        """Get or assign a novel node ID when splitting an existing connection.
        
        If the same connection was split multiple times in the same generation,
        they share the same intermediate node ID.
        """
        if connection_innovation in self.node_innovations:
            return self.node_innovations[connection_innovation]
        self.current_node_id += 1
        self.node_innovations[connection_innovation] = self.current_node_id
        return self.current_node_id

    def reset_generation(self) -> None:
        """Clear generation caches while preserving monotonic counters."""
        self.generation_innovations.clear()
        self.node_innovations.clear()
