"""Demonstration of Explicit Fitness Sharing and Ecological Niche Carrying Capacity.

Module 04: Speciation & Fitness Sharing.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Organism:
    id: int
    raw_fitness: float
    adjusted_fitness: float = 0.0


def simulate_offspring_allocation(species_sizes: List[int], avg_raw_fitnesses: List[float], pop_size: int = 100):
    """Calculates offspring allocations under raw fitness vs explicit fitness sharing."""
    # 1. Create simulated populations per species
    all_organisms = []
    species_map = {}
    current_id = 1
    for s_idx, (size, raw_f) in enumerate(zip(species_sizes, avg_raw_fitnesses)):
        sp_members = []
        for _ in range(size):
            org = Organism(id=current_id, raw_fitness=raw_f)
            sp_members.append(org)
            all_organisms.append(org)
            current_id += 1
        species_map[s_idx + 1] = sp_members

    # WITHOUT FITNESS SHARING (Raw Fitness Domination)
    total_raw = sum(o.raw_fitness for o in all_organisms)
    raw_allocations = {}
    for s_idx, members in species_map.items():
        sp_raw_sum = sum(o.raw_fitness for o in members)
        raw_allocations[s_idx] = round(pop_size * (sp_raw_sum / total_raw))

    # WITH EXPLICIT FITNESS SHARING (Niche Protection)
    for s_idx, members in species_map.items():
        sp_size = len(members)
        for o in members:
            o.adjusted_fitness = o.raw_fitness / sp_size

    total_adj = sum(o.adjusted_fitness for o in all_organisms)
    shared_allocations = {}
    for s_idx, members in species_map.items():
        sp_adj_sum = sum(o.adjusted_fitness for o in members)
        shared_allocations[s_idx] = round(pop_size * (sp_adj_sum / total_adj))

    return raw_allocations, shared_allocations


def main():
    print("=== Explicit Fitness Sharing Demonstration ===")
    print("Scenario: A large dominant species on a local optimum vs a small innovative species.")
    species_names = [
        "Species 1 (Bloated Local Optimum)",
        "Species 2 (Moderate Balanced Niche)",
        "Species 3 (Novel Fragile Innovation)",
    ]
    species_sizes = [80, 15, 5]
    avg_fitness = [8.0, 7.5, 9.0]  # Novel species actually has higher individual fitness!
    pop_size = 100

    print(f"\nPopulation Setup (Total N = {pop_size}):")
    for name, size, fit in zip(species_names, species_sizes, avg_fitness):
        print(f"  {name:<38}: Size={size:>2}, Avg Raw Fitness={fit:>4.1f}")

    raw_alloc, shared_alloc = simulate_offspring_allocation(species_sizes, avg_fitness, pop_size)

    print("\nNext Generation Offspring Allocation Comparison:")
    print(f"{'Species':<38} | {'Raw Allocation':<16} | {'Shared Allocation (NEAT)':<24}")
    print("-" * 84)
    for idx, name in enumerate(species_names, 1):
        r_count = raw_alloc[idx]
        s_count = shared_alloc[idx]
        print(f"{name:<38} | {r_count:>5} slots ({r_count/pop_size*100:>5.1f}%) | {s_count:>5} slots ({s_count/pop_size*100:>5.1f}%)")

    print("\nInsight:")
    print("Under Raw Fitness, Species 1 takes over 80% of offspring simply because of sheer headcount.")
    print("Under NEAT Fitness Sharing, Species 3 (novel innovation) receives its fair share of offspring")
    print("proportional to individual quality, protecting it from being choked out by the crowd!")


if __name__ == "__main__":
    main()
