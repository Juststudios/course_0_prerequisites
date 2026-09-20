"""Module 01 Exercises: Foundations of Evolutionary Computation.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Tournament Selection)
- Tier 4: Challenge (Rank Selection)
"""

import random
from typing import List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    """Answer conceptual questions by returning a dictionary with keys 'q1', 'q2'."""
    # TODO: Fill in your answers
    return {
        # Q1: In Evolutionary Computation, what is the abstract encoding of a solution called?
        "q1": "FILL_ME_IN",  # 'genotype' or 'phenotype'
        # Q2: Does increasing tournament size k increase or decrease selection pressure?
        "q2": "FILL_ME_IN",  # 'increase' or 'decrease'
    }


# --- Tier 2: Understanding / Debugging ---
def buggy_roulette_wheel(fitnesses: List[float], pick: float) -> int:
    """DEBUG CHALLENGE: This function has a bug where it fails to accumulate cumulative fitness.
    Fix the bug so it correctly selects the index where cumulative fitness exceeds `pick`.
    """
    # BUGGY CODE:
    current = 0.0
    for i, f in enumerate(fitnesses):
        # BUG: current is not accumulating!
        if current >= pick:
            return i
    return len(fitnesses) - 1


# --- Tier 3: Application ---
def tournament_selection(population: List[int], fitnesses: List[float], k: int, rng: random.Random) -> int:
    """Implement tournament selection:
    Sample k random candidate indices from population (with replacement),
    and return the candidate from the sample that has the highest fitness.
    """
    # TODO: Implement tournament selection
    raise NotImplementedError("Implement tournament_selection")


# --- Tier 4: Challenge ---
def rank_selection_probabilities(fitnesses: List[float]) -> List[float]:
    """Implement linear rank-based selection probabilities:
    Sort individuals from lowest to highest fitness.
    Assign linear ranks from 1 (lowest) to N (highest).
    Return normalized selection probabilities proportional to rank.
    """
    # TODO: Implement rank selection probability calculation
    raise NotImplementedError("Implement rank_selection_probabilities")


if __name__ == "__main__":
    print("Run solutions/module_01_solutions.py to test reference solutions.")
