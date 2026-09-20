"""Demonstration of Genotype-to-Phenotype Mapping and Fitness Evaluation.

Module 01: Foundations of Evolutionary Computation.
"""

from dataclasses import dataclass
import math
import random
from typing import List, Tuple


@dataclass
class BitstringGenome:
    """Genotype: Raw chromosome represented as binary bits."""
    bits: List[int]

    @classmethod
    def random(cls, length: int) -> 'BitstringGenome':
        return cls([random.randint(0, 1) for _ in range(length)])


def decode_chromosome(genome: BitstringGenome, num_genes: int, gene_bits: int, val_range: Tuple[float, float]) -> List[float]:
    """Phenotype Decoder: Unpacks binary bitstring into continuous real-valued parameters."""
    low, high = val_range
    phenotype = []
    max_int = (1 << gene_bits) - 1

    for i in range(num_genes):
        slice_bits = genome.bits[i * gene_bits : (i + 1) * gene_bits]
        int_val = 0
        for b in slice_bits:
            int_val = (int_val << 1) | b
        real_val = low + (int_val / max_int) * (high - low)
        phenotype.append(real_val)

    return phenotype


def rastrigin_fitness(phenotype: List[float]) -> float:
    """Fitness Function: Inverted Rastrigin benchmark function.
    
    Global optimum at (0, ..., 0) with maximum fitness 100.0.
    """
    a = 10.0
    n = len(phenotype)
    cost = a * n + sum(x**2 - a * math.cos(2.0 * math.pi * x) for x in phenotype)
    return 100.0 / (1.0 + cost)


def main():
    print("=== Genotype to Phenotype Demonstration ===")
    num_genes = 3
    gene_bits = 10
    total_bits = num_genes * gene_bits
    val_range = (-5.12, 5.12)

    random.seed(42)
    sample_genotypes = [BitstringGenome.random(total_bits) for _ in range(5)]

    for idx, g in enumerate(sample_genotypes):
        phenotype = decode_chromosome(g, num_genes, gene_bits, val_range)
        fitness = rastrigin_fitness(phenotype)
        bit_preview = "".join(map(str, g.bits[:12])) + "..."
        pheno_str = ", ".join(f"{x:+.4f}" for x in phenotype)
        print(f"Candidate #{idx+1}:")
        print(f"  Genotype:  [{bit_preview}] (length: {len(g.bits)})")
        print(f"  Phenotype: [{pheno_str}]")
        print(f"  Fitness:   {fitness:.6f}\n")


if __name__ == "__main__":
    main()
