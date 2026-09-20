"""Module 02 Exercises: Genetic Algorithms.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Single-Point Crossover)
- Tier 4: Challenge (Elitist Generational Preservation)
"""

import random
from typing import List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        # Q1: What genetic operator guarantees that best population fitness never regresses?
        "q1": "FILL_ME_IN",  # 'crossover', 'elitism', or 'mutation'
        # Q2: In continuous optimization, which distribution is typically used for perturbing weights?
        "q2": "FILL_ME_IN",  # 'gaussian' or 'uniform'
    }


# --- Tier 2: Understanding / Debugging ---
def buggy_uniform_crossover(p1: List[float], p2: List[float], rng: random.Random) -> List[float]:
    """DEBUG CHALLENGE: This uniform crossover function fails to alternate genes properly
    and always returns a pure copy of Parent 1. Fix it so each gene is drawn from p1 or p2
    with equal 50% probability.
    """
    child = []
    for g1, g2 in zip(p1, p2):
        # BUG: coin flip always evaluates to True or ignores p2
        child.append(g1)
    return child


# --- Tier 3: Application ---
def single_point_crossover(p1: List[float], p2: List[float], cut_point: int) -> Tuple[List[float], List[float]]:
    """Implement single-point crossover given explicit cut_point:
    Child 1: p1[:cut_point] + p2[cut_point:]
    Child 2: p2[:cut_point] + p1[cut_point:]
    """
    # TODO: Implement single_point_crossover
    raise NotImplementedError("Implement single_point_crossover")


# --- Tier 4: Challenge ---
def apply_elitism(
    old_population: List[List[float]],
    old_fitnesses: List[float],
    offspring: List[List[float]],
    elitism_count: int = 2,
) -> List[List[float]]:
    """Preserve top `elitism_count` individuals from old_population unchanged,
    and fill the remaining slots with the best individuals from `offspring`
    so total returned population size equals len(old_population).
    """
    # TODO: Implement apply_elitism
    raise NotImplementedError("Implement apply_elitism")


if __name__ == "__main__":
    print("Run solutions/module_02_solutions.py to test reference solutions.")
