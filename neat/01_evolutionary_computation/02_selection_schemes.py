"""Empirical comparison of Parent Selection Schemes.

Demonstrates Roulette Wheel, Tournament, Truncation, and Rank Selection.
Module 01: Foundations of Evolutionary Computation.
"""

from collections import Counter
import random
from typing import List, Tuple


def roulette_wheel_select(population: List[str], fitnesses: List[float], rng: random.Random) -> str:
    """Fitness-proportionate roulette wheel selection using cumulative sum."""
    total_fit = sum(fitnesses)
    pick = rng.uniform(0.0, total_fit)
    current = 0.0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return individual
    return population[-1]


def tournament_select(population: List[str], fitnesses: List[float], k: int, rng: random.Random) -> str:
    """Tournament selection with tournament size k."""
    indices = rng.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx]


def truncation_select(population: List[str], fitnesses: List[float], top_ratio: float, rng: random.Random) -> str:
    """Truncation selection: uniform sampling from the top fraction."""
    paired = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    cutoff = max(1, int(len(population) * top_ratio))
    top_pool = [p[0] for p in paired[:cutoff]]
    return rng.choice(top_pool)


def rank_select(population: List[str], fitnesses: List[float], rng: random.Random) -> str:
    """Linear rank-based selection reducing domination by hyper-fit individuals."""
    n = len(population)
    sorted_pairs = sorted(zip(population, fitnesses), key=lambda x: x[1])
    # Assign ranks from 1 (worst) to n (best)
    ranks = list(range(1, n + 1))
    total_rank = sum(ranks)
    pick = rng.uniform(0.0, total_rank)
    current = 0.0
    for (indiv, _), rank in zip(sorted_pairs, ranks):
        current += rank
        if current >= pick:
            return indiv
    return sorted_pairs[-1][0]


def main():
    print("=== Empirical Selection Schemes Benchmark ===")
    candidates = ["Weak_A", "Fair_B", "Good_C", "Elite_D", "Super_E"]
    raw_fitness = [1.0, 5.0, 15.0, 30.0, 100.0]  # Super_E dominates raw fitness

    rng = random.Random(42)
    num_samples = 10000

    print("Population and Raw Fitness Scores:")
    for c, f in zip(candidates, raw_fitness):
        print(f"  {c:<10}: {f:>6.1f} points ({f/sum(raw_fitness)*100:>5.1f}%)")

    print(f"\nSimulating {num_samples} draws per selection scheme...\n")

    schemes = {
        "Roulette Wheel": lambda: roulette_wheel_select(candidates, raw_fitness, rng),
        "Tournament (k=2)": lambda: tournament_select(candidates, raw_fitness, 2, rng),
        "Tournament (k=4)": lambda: tournament_select(candidates, raw_fitness, 4, rng),
        "Truncation (top 40%)": lambda: truncation_select(candidates, raw_fitness, 0.4, rng),
        "Linear Rank": lambda: rank_select(candidates, raw_fitness, rng),
    }

    for name, sampler in schemes.items():
        counts = Counter(sampler() for _ in range(num_samples))
        print(f"--- {name} ---")
        for c in candidates:
            pct = counts[c] / num_samples * 100
            print(f"  {c:<10}: {counts[c]:>5} selections ({pct:>5.1f}%)")
        print()


if __name__ == "__main__":
    main()
