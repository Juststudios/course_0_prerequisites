"""Demonstration of Chromosome Representations and Mutation Operators.

Module 02: Genetic Algorithms.
"""

import math
import random
from typing import List


def bit_flip_mutate(chromosome: List[int], mutation_prob: float, rng: random.Random) -> List[int]:
    """Mutate binary chromosome: inverts bits with probability mutation_prob."""
    mutated = list(chromosome)
    for i in range(len(mutated)):
        if rng.random() < mutation_prob:
            mutated[i] = 1 - mutated[i]
    return mutated


def real_vector_mutate(
    vector: List[float],
    perturb_rate: float,
    perturb_power: float,
    replace_rate: float,
    val_range: tuple,
    rng: random.Random,
) -> List[float]:
    """Mutate continuous real vector: Gaussian perturbation or uniform reset."""
    low, high = val_range
    mutated = list(vector)
    for i in range(len(mutated)):
        if rng.random() < perturb_rate:
            if rng.random() < replace_rate:
                mutated[i] = rng.uniform(low, high)
            else:
                mutated[i] += rng.gauss(0.0, perturb_power)
                mutated[i] = max(low, min(high, mutated[i]))
    return mutated


def main():
    print("=== Genetic Representation & Mutation Operators ===")
    rng = random.Random(42)

    # 1. Binary Chromosome Mutation
    binary_chrom = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1]
    mut_rate_bin = 1.0 / len(binary_chrom)
    mutated_bin = bit_flip_mutate(binary_chrom, mut_rate_bin, rng)

    diffs = [i for i in range(len(binary_chrom)) if binary_chrom[i] != mutated_bin[i]]
    print("Binary Representation:")
    print("  Original :", "".join(map(str, binary_chrom)))
    print("  Mutated  :", "".join(map(str, mutated_bin)))
    print(f"  Inverted bit positions: {diffs} (mutation rate: {mut_rate_bin:.3f})\n")

    # 2. Continuous Real-Valued Vector Mutation
    real_vec = [1.50, -0.75, 0.00, 3.20, -2.10]
    mutated_vec = real_vector_mutate(
        real_vec,
        perturb_rate=0.8,
        perturb_power=0.25,
        replace_rate=0.1,
        val_range=(-5.0, 5.0),
        rng=rng,
    )

    print("Real-Valued Representation:")
    print("  Original :", [f"{x:+.4f}" for x in real_vec])
    print("  Mutated  :", [f"{x:+.4f}" for x in mutated_vec])
    delta = [m - o for o, m in zip(real_vec, mutated_vec)]
    print("  Delta    :", [f"{d:+.4f}" for d in delta])


if __name__ == "__main__":
    main()
