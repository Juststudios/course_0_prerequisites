"""Demonstration of Crossover Operators and Elitist Generational Preservation.

Module 02: Genetic Algorithms.
"""

import math
import random
from typing import List, Tuple


def single_point_crossover(p1: List[float], p2: List[float], rng: random.Random) -> Tuple[List[float], List[float]]:
    pt = rng.randint(1, len(p1) - 1)
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]


def uniform_crossover(p1: List[float], p2: List[float], rng: random.Random) -> Tuple[List[float], List[float]]:
    c1, c2 = [], []
    for g1, g2 in zip(p1, p2):
        if rng.random() < 0.5:
            c1.append(g1)
            c2.append(g2)
        else:
            c1.append(g2)
            c2.append(g1)
    return c1, c2


def sphere_objective(x: List[float]) -> float:
    """Sphere function: f(x) = sum(x_i^2). Maximize fitness: 100 / (1 + sum(x_i^2))."""
    return 100.0 / (1.0 + sum(v**2 for v in x))


def run_ga_simulation(use_elitism: bool, seed: int = 101) -> List[float]:
    """Runs a 30-generation continuous optimizer with or without elitism."""
    rng = random.Random(seed)
    dim = 5
    pop_size = 20
    generations = 25
    pop = [[rng.uniform(-3.0, 3.0) for _ in range(dim)] for _ in range(pop_size)]

    best_curve = []

    for _ in range(generations):
        fitnesses = [sphere_objective(indiv) for indiv in pop]
        best_fit = max(fitnesses)
        best_curve.append(best_fit)

        # Pair population with fitness
        ranked = sorted(zip(pop, fitnesses), key=lambda x: x[1], reverse=True)

        next_gen = []
        if use_elitism:
            # Preserve top 2 individuals unchanged
            next_gen.append(list(ranked[0][0]))
            next_gen.append(list(ranked[1][0]))

        # Breed remainder
        while len(next_gen) < pop_size:
            # Tournament selection
            idx1 = max(rng.sample(range(pop_size), 3), key=lambda i: fitnesses[i])
            idx2 = max(rng.sample(range(pop_size), 3), key=lambda i: fitnesses[i])
            c1, c2 = uniform_crossover(pop[idx1], pop[idx2], rng)

            # Mutate
            for child in [c1, c2]:
                if len(next_gen) < pop_size:
                    mut = [v + rng.gauss(0.0, 0.4) if rng.random() < 0.3 else v for v in child]
                    next_gen.append(mut)

        pop = next_gen

    return best_curve


def main():
    print("=== Crossover Operators & Elitism Demonstration ===")
    rng = random.Random(42)
    p1 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    p2 = [9.1, 9.2, 9.3, 9.4, 9.5, 9.6]

    sp_c1, sp_c2 = single_point_crossover(p1, p2, rng)
    un_c1, un_c2 = uniform_crossover(p1, p2, rng)

    print("Parent 1:", p1)
    print("Parent 2:", p2)
    print("Single-Point Crossover Child 1:", [round(x, 1) for x in sp_c1])
    print("Single-Point Crossover Child 2:", [round(x, 1) for x in sp_c2])
    print("Uniform Crossover Child 1     :", [round(x, 1) for x in un_c1])
    print("Uniform Crossover Child 2     :", [round(x, 1) for x in un_c2])

    print("\n--- Testing Monotonic Fitness Preservation with Elitism ---")
    curve_with_elitism = run_ga_simulation(use_elitism=True)
    curve_without_elitism = run_ga_simulation(use_elitism=False)

    print(f"{'Gen':<5} | {'With Elitism':<15} | {'Without Elitism':<15}")
    print("-" * 42)
    for g in range(0, len(curve_with_elitism), 5):
        print(f"{g:<5} | {curve_with_elitism[g]:<15.4f} | {curve_without_elitism[g]:<15.4f}")
    print(f"{len(curve_with_elitism)-1:<5} | {curve_with_elitism[-1]:<15.4f} | {curve_without_elitism[-1]:<15.4f}")

    # Monotonicity check
    is_monotonic = all(curve_with_elitism[i] <= curve_with_elitism[i+1] for i in range(len(curve_with_elitism)-1))
    print(f"\nMonotonicity guaranteed with elitism: {is_monotonic}")


if __name__ == "__main__":
    main()
