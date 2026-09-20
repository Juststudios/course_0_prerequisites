"""NEAT (NeuroEvolution of Augmenting Topologies) Engine.

A pure-Python, zero-dependency implementation of the NEAT neuroevolution algorithm.
"""

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.gene import ConnectionGene, NodeGene
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.neat_engine.network import FeedForwardNetwork, RecurrentNetwork
from neat.neat_engine.population import Population
from neat.neat_engine.species import Species

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
