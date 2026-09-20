"""Typed configuration for the NEAT algorithm."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class NEATConfig:
    """Configuration parameters for NEAT population, reproduction, and operators."""
    num_inputs: int = 2
    num_outputs: int = 1
    has_bias: bool = True
    pop_size: int = 150

    # Speciation parameters
    compatibility_c1: float = 1.0  # Excess gene coefficient
    compatibility_c2: float = 1.0  # Disjoint gene coefficient
    compatibility_c3: float = 0.4  # Weight difference coefficient
    compatibility_threshold: float = 3.0
    survival_threshold: float = 0.2  # Fraction of species allowed to reproduce
    max_stagnation: int = 15
    elitism: int = 1
    min_species_size: int = 2

    # Mutation probabilities and step sizes
    weight_mutate_rate: float = 0.8
    weight_mutate_power: float = 0.5
    weight_replace_rate: float = 0.1
    bias_mutate_rate: float = 0.7
    bias_mutate_power: float = 0.5
    bias_replace_rate: float = 0.1
    add_connection_rate: float = 0.3
    add_node_rate: float = 0.1
    toggle_enabled_rate: float = 0.05

    # Phenotype activation
    activation_default: str = 'sigmoid'  # 'sigmoid', 'tanh', 'relu', 'identity'

    # Reproducibility
    seed: Optional[int] = None
