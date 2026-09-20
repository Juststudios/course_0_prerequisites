"""Population management and generational evolution loop for NEAT.

Coordinates speciation, dynamic reproduction allocation, genetic operations,
and telemetry recording across evolutionary generations.
"""

import math
import random
from typing import Callable, Dict, List, Optional, Tuple

from neat.neat_engine.config import NEATConfig
from neat.neat_engine.genome import Genome
from neat.neat_engine.innovation import InnovationTracker
from neat.neat_engine.species import Species


class Population:
    """Evolutionary population manager implementing the NEAT epoch cycle."""

    def __init__(self, config: NEATConfig):
        self.config: NEATConfig = config
        self.rng: random.Random = random.Random(config.seed) if config.seed is not None else random.Random()

        total_initial_nodes = config.num_inputs + (1 if config.has_bias else 0) + config.num_outputs
        self.tracker: InnovationTracker = InnovationTracker(initial_node_count=total_initial_nodes - 1)

        self.generation: int = 0
        self.species: List[Species] = []
        self.species_counter: int = 0
        self.champion: Optional[Genome] = None

        self.history: Dict[str, List] = {
            'best_fitness': [],
            'mean_fitness': [],
            'species_sizes': [],
            'species_history': {},  # Maps species_id -> list of sizes per generation
        }

        # Create initial population of minimal genomes
        initial_genomes = [
            Genome.create_minimal(self.config, self.tracker, genome_id=i, rng=self.rng)
            for i in range(config.pop_size)
        ]
        self._speciate(initial_genomes)

    @property
    def population(self) -> List[Genome]:
        """Return a flat list of all active genomes across all species."""
        members = []
        for sp in self.species:
            members.extend(sp.members)
        return members

    def _speciate(self, genomes: List[Genome]) -> None:
        """Partition genomes into compatible species niches."""
        # Clear members of current species but keep representatives
        for sp in self.species:
            sp.members = []

        for genome in genomes:
            matched = False
            for sp in self.species:
                dist = genome.compatibility_distance(
                    sp.representative,
                    c1=self.config.compatibility_c1,
                    c2=self.config.compatibility_c2,
                    c3=self.config.compatibility_c3,
                )
                if dist <= self.config.compatibility_threshold:
                    sp.add_member(genome)
                    matched = True
                    break

            if not matched:
                self.species_counter += 1
                new_sp = Species(self.species_counter, genome)
                self.species.append(new_sp)

        # Remove empty species
        self.species = [sp for sp in self.species if sp.members]

        # Update representatives to a randomly chosen member
        for sp in self.species:
            sp.representative = self.rng.choice(sp.members).copy()

    def evaluate(self, fitness_func: Callable[[Genome], float]) -> None:
        """Evaluate raw fitness for all genomes in the population."""
        for sp in self.species:
            for genome in sp.members:
                genome.fitness = float(fitness_func(genome))

    def epoch(self) -> None:
        """Execute one complete NEAT evolutionary generation epoch."""
        # 1. Explicit fitness sharing & stagnation updates
        species_fitness_sums: List[Tuple[Species, float]] = []
        for sp in self.species:
            sp_sum = sp.calculate_shared_fitness()
            sp.update_stagnation()
            species_fitness_sums.append((sp, sp_sum))

        # 2. Prune stagnant species (preserve at least top performing species)
        self.species.sort(key=lambda s: s.best_fitness, reverse=True)
        surviving_species: List[Species] = []
        for i, sp in enumerate(self.species):
            # Top 2 species or species under max_stagnation survive
            if i < 2 or sp.stagnation < self.config.max_stagnation:
                surviving_species.append(sp)

        if not surviving_species:
            surviving_species = [self.species[0]]

        self.species = surviving_species

        # 3. Offspring allocation proportional to shared fitness
        total_shared_fitness = sum(sp.calculate_shared_fitness() for sp in self.species)
        if total_shared_fitness <= 0.0:
            # Uniform allocation fallback
            allocations = [self.config.pop_size // len(self.species)] * len(self.species)
            allocations[0] += self.config.pop_size - sum(allocations)
        else:
            allocations = [
                int(round(self.config.pop_size * (sp.calculate_shared_fitness() / total_shared_fitness)))
                for sp in self.species
            ]
            diff = self.config.pop_size - sum(allocations)
            if diff != 0 and allocations:
                allocations[0] += diff

        # Ensure all allocations are non-negative
        for i in range(len(allocations)):
            if allocations[i] < 0:
                allocations[i] = 0

        # 4. Reproduce next generation
        next_generation_genomes: List[Genome] = []
        new_genome_id = 0
        for sp, count in zip(self.species, allocations):
            offspring = sp.reproduce(count, self.tracker, self.config, rng=self.rng)
            for child in offspring:
                child.id = new_genome_id
                new_genome_id += 1
                next_generation_genomes.append(child)

        # Fallback in case rounding left the population short
        while len(next_generation_genomes) < self.config.pop_size:
            p = self.rng.choice(self.species[0].members)
            clone = p.copy(new_id=new_genome_id)
            clone.mutate_weights(self.config, rng=self.rng)
            next_generation_genomes.append(clone)
            new_genome_id += 1

        # 5. Advance generation
        self.tracker.reset_generation()
        self._speciate(next_generation_genomes)
        self.generation += 1

    def run(
        self,
        fitness_func: Callable[[Genome], float],
        max_generations: int = 100,
        fitness_threshold: Optional[float] = None,
    ) -> Tuple[Genome, Dict]:
        """Run evolutionary search until max_generations or fitness_threshold is met."""
        for gen in range(max_generations):
            self.evaluate(fitness_func)

            all_genomes = self.population
            all_fitnesses = [g.fitness for g in all_genomes]
            current_best = max(all_genomes, key=lambda g: g.fitness)
            mean_fitness = sum(all_fitnesses) / len(all_fitnesses)

            if self.champion is None or current_best.fitness > self.champion.fitness:
                self.champion = current_best.copy()

            # Record telemetry
            self.history['best_fitness'].append(self.champion.fitness)
            self.history['mean_fitness'].append(mean_fitness)

            # Record species sizes
            current_sizes = {sp.id: len(sp.members) for sp in self.species}
            self.history['species_sizes'].append(current_sizes)

            # Track species sizes per ID for stackplots
            all_known_species = set(self.history['species_history'].keys()).union(current_sizes.keys())
            for sp_id in all_known_species:
                if sp_id not in self.history['species_history']:
                    # Pad previous generations with 0
                    self.history['species_history'][sp_id] = [0] * gen
                self.history['species_history'][sp_id].append(current_sizes.get(sp_id, 0))

            if fitness_threshold is not None and self.champion.fitness >= fitness_threshold:
                break

            if gen < max_generations - 1:
                self.epoch()

        assert self.champion is not None
        return self.champion, self.history
