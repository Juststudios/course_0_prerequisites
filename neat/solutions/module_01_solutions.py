"""Reference Solutions for Module 01 Exercises: Foundations of Evolutionary Computation."""

import random
from typing import List


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "genotype",
        "q2": "increase",
    }


# --- Tier 2: Understanding / Debugging ---
def fixed_roulette_wheel(fitnesses: List[float], pick: float) -> int:
    """FIXED: Accumulate current += f before checking >= pick."""
    current = 0.0
    for i, f in enumerate(fitnesses):
        current += f
        if current >= pick:
            return i
    return len(fitnesses) - 1


# --- Tier 3: Application ---
def tournament_selection(population: List[int], fitnesses: List[float], k: int, rng: random.Random) -> int:
    indices = rng.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx]


# --- Tier 4: Challenge ---
def rank_selection_probabilities(fitnesses: List[float]) -> List[float]:
    n = len(fitnesses)
    # Get sorted indices by fitness
    sorted_indices = sorted(range(n), key=lambda i: fitnesses[i])
    probs = [0.0] * n
    total_rank = n * (n + 1) / 2.0

    for rank, orig_idx in enumerate(sorted_indices, start=1):
        probs[orig_idx] = rank / total_rank

    return probs


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert ans["q1"].lower() == "genotype"
    assert ans["q2"].lower() == "increase"

    # Tier 2
    fits = [2.0, 3.0, 5.0]  # total = 10.0
    assert fixed_roulette_wheel(fits, 1.5) == 0
    assert fixed_roulette_wheel(fits, 3.5) == 1
    assert fixed_roulette_wheel(fits, 8.0) == 2

    # Tier 3
    pop = [10, 20, 30, 40, 50]
    fits = [1.0, 2.0, 3.0, 4.0, 5.0]
    rng = random.Random(42)
    selected = tournament_selection(pop, fits, k=3, rng=rng)
    assert selected in pop

    # Tier 4
    fits = [10.0, 50.0, 20.0]
    # Ranks: idx 0 has 10 (rank 1), idx 2 has 20 (rank 2), idx 1 has 50 (rank 3)
    # Total rank = 6 -> probs: 1/6, 3/6, 2/6
    probs = rank_selection_probabilities(fits)
    assert abs(probs[0] - 1.0 / 6.0) < 1e-5
    assert abs(probs[1] - 3.0 / 6.0) < 1e-5
    assert abs(probs[2] - 2.0 / 6.0) < 1e-5
    assert abs(sum(probs) - 1.0) < 1e-5

    print("[SUCCESS] All Module 01 solutions verified!")


if __name__ == "__main__":
    test_solutions()
