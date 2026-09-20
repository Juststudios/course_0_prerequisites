"""NEAT (NeuroEvolution of Augmenting Topologies) package."""

import os
import sys

# Ensure package root is available on path
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_pkg_dir)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from neat.neat_engine import (
    NEATConfig,
    NodeGene,
    ConnectionGene,
    Genome,
    InnovationTracker,
    Species,
    Population,
    FeedForwardNetwork,
    RecurrentNetwork,
)

__all__ = [
    "NEATConfig",
    "NodeGene",
    "ConnectionGene",
    "Genome",
    "InnovationTracker",
    "Species",
    "Population",
    "FeedForwardNetwork",
    "RecurrentNetwork",
]
