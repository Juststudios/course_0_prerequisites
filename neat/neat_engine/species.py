"""Species management and explicit fitness sharing in NEAT.

Species protect novel structural innovations by clustering topologically similar
genomes into niches and partitioning reproductive capacity through explicit fitness sharing.
"""

import math
import random
from typing import List, Optional

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker


class Species:
    """Represents a topological niche containing compatible genomes."""

    def __init__(self, species_id: int, representative: Genome):
        self.id: int = species_id
        self.representative: Genome = representative.copy()
        self.members: List[Genome] = [representative]
        self.age: int = 0
        self.stagnation: int = 0
        self.best_fitness: float = -float('inf')

    def add_member(self, genome: Genome) -> None:
        """Add a compatible genome to this species."""
        genome.species_id = self.id
        self.members.append(genome)

    def calculate_shared_fitness(self) -> float:
        """Apply explicit fitness sharing across all species members.
        
        Adjusted fitness = raw fitness / species size.
        Returns total adjusted fitness for the species.
        """
        size = len(self.members)
        if size == 0:
            return 0.0

        total_adjusted = 0.0
        for genome in self.members:
            # Ensure adjusted fitness is strictly positive
            shared = max(1e-6, genome.fitness) / size
            genome.adjusted_fitness = shared
            total_adjusted += shared
        return total_adjusted

    def update_stagnation(self) -> None:
        """Track generation stagnation by comparing max member fitness."""
        self.age += 1
        if not self.members:
            self.stagnation += 1
            return

        current_best = max(g.fitness for g in self.members)
        if current_best > self.best_fitness + 1e-4:
            self.best_fitness = current_best
            self.stagnation = 0
        else:
            self.stagnation += 1

    def reproduce(
        self,
        offspring_count: int,
        tracker: InnovationTracker,
        config: NEATConfig,
        rng: Optional[random.Random] = None,
    ) -> List[Genome]:
        """Breed the specified number of offspring for the next generation."""
        if offspring_count <= 0:
            return []

        r = rng if rng is not None else random
        # Sort members by raw fitness descending
        self.members.sort(key=lambda g: g.fitness, reverse=True)

        offspring: List[Genome] = []

        # 1. Elitism: preserve top genome unchanged if species is large enough
        if config.elitism > 0 and len(self.members) >= config.min_species_size:
            elite = self.members[0].copy()
            offspring.append(elite)

        # 2. Survival selection: restrict mating pool to top fraction
        survivor_count = max(1, int(math.ceil(len(self.members) * config.survival_threshold)))
        mating_pool = self.members[:survivor_count]

        # 3. Produce remainder of offspring through crossover and mutation
        while len(offspring) < offspring_count:
            if len(mating_pool) == 1 or r.random() < 0.25:
                # Asexual reproduction
                parent = r.choice(mating_pool)
                child = parent.copy()
            else:
                # Sexual reproduction
                p1 = r.choice(mating_pool)
                p2 = r.choice(mating_pool)
                child = p1.crossover(p2, rng=r)

            # Mutate offspring
            child.mutate_weights(config, rng=r)
            if r.random() < config.add_connection_rate:
                child.mutate_add_connection(config, tracker, rng=r)
            if r.random() < config.add_node_rate:
                child.mutate_add_node(config, tracker, rng=r)

            offspring.append(child)

        return offspring
