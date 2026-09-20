"""Reference Solutions for Module 02 Exercises: Genetic Algorithms."""

import random
from typing import List, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "elitism",
        "q2": "gaussian",
    }


# --- Tier 2: Understanding / Debugging ---
def fixed_uniform_crossover(p1: List[float], p2: List[float], rng: random.Random) -> List[float]:
    child = []
    for g1, g2 in zip(p1, p2):
        child.append(g1 if rng.random() < 0.5 else g2)
    return child


# --- Tier 3: Application ---
def single_point_crossover(p1: List[float], p2: List[float], cut_point: int) -> Tuple[List[float], List[float]]:
    c1 = p1[:cut_point] + p2[cut_point:]
    c2 = p2[:cut_point] + p1[cut_point:]
    return c1, c2


# --- Tier 4: Challenge ---
def apply_elitism(
    old_population: List[List[float]],
    old_fitnesses: List[float],
    offspring: List[List[float]],
    elitism_count: int = 2,
) -> List[List[float]]:
    ranked_old = sorted(zip(old_population, old_fitnesses), key=lambda x: x[1], reverse=True)
    elites = [list(indiv) for indiv, _ in ranked_old[:elitism_count]]
    remaining_needed = len(old_population) - elitism_count
    return elites + [list(c) for c in offspring[:remaining_needed]]


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert ans["q1"].lower() == "elitism"
    assert ans["q2"].lower() == "gaussian"

    # Tier 2
    p1 = [1.0] * 10
    p2 = [2.0] * 10
    rng = random.Random(42)
    c = fixed_uniform_crossover(p1, p2, rng)
    assert 1.0 in c and 2.0 in c

    # Tier 3
    a = [1, 2, 3, 4]
    b = [5, 6, 7, 8]
    c1, c2 = single_point_crossover(a, b, cut_point=2)
    assert c1 == [1, 2, 7, 8]
    assert c2 == [5, 6, 3, 4]

    # Tier 4
    old_pop = [[1], [2], [3], [4], [5]]
    fits = [10, 20, 30, 40, 50]  # Elites are [5] (50) and [4] (40)
    offs = [[99], [98], [97], [96]]
    new_pop = apply_elitism(old_pop, fits, offs, elitism_count=2)
    assert len(new_pop) == 5
    assert new_pop[0] == [5]
    assert new_pop[1] == [4]
    assert new_pop[2] == [99]

    print("[SUCCESS] All Module 02 solutions verified!")


if __name__ == "__main__":
    test_solutions()
