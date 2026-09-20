"""Module 04 Exercises: Speciation & Fitness Sharing.

4-Tier Progressive Exercises:
- Tier 1: Recall & Concepts
- Tier 2: Understanding & Debugging
- Tier 3: Application (Compatibility Distance)
- Tier 4: Challenge (Speciation Clustering)
"""

from typing import Dict, List, Set, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        # Q1: In explicit fitness sharing, an individual's raw fitness is divided by what value?
        "q1": "FILL_ME_IN",  # 'species size' or 'total population size'
        # Q2: What kind of genes occur in one genome and not the other, ABOVE the maximum innovation of the other?
        "q2": "FILL_ME_IN",  # 'excess' or 'disjoint'
    }


# --- Tier 2: Understanding / Debugging ---
def buggy_compatibility_distance(
    invs1: Set[int],
    invs2: Set[int],
    weights1: Dict[int, float],
    weights2: Dict[int, float],
) -> float:
    """DEBUG CHALLENGE: This compatibility distance calculation inverts the definition
    of excess and disjoint genes. Fix it so excess genes are strictly > min(max1, max2).
    """
    max1 = max(invs1) if invs1 else 0
    max2 = max(invs2) if invs2 else 0
    threshold = min(max1, max2)

    diff = invs1 ^ invs2
    # BUG: The logic for excess and disjoint is flipped below!
    excess = sum(1 for i in diff if i <= threshold)
    disjoint = sum(1 for i in diff if i > threshold)

    matching = invs1 & invs2
    avg_w = (sum(abs(weights1[i] - weights2[i]) for i in matching) / len(matching)) if matching else 0.0

    return float(excess + disjoint + 0.4 * avg_w)


# --- Tier 3: Application ---
def calculate_compatibility_distance(
    invs1: Set[int],
    invs2: Set[int],
    weights1: Dict[int, float],
    weights2: Dict[int, float],
    c1: float = 1.0,
    c2: float = 1.0,
    c3: float = 0.4,
) -> float:
    """Implement NEAT compatibility distance:
    delta = (c1 * E / N) + (c2 * D / N) + (c3 * W_bar)
    where N is 1.0 if max(len(invs1), len(invs2)) < 20 else max(len(invs1), len(invs2)).
    """
    # TODO: Implement calculate_compatibility_distance
    raise NotImplementedError


# --- Tier 4: Challenge ---
def speciate_population(
    genomes: List[int],
    distance_matrix: Dict[Tuple[int, int], float],
    threshold: float = 3.0,
) -> List[List[int]]:
    """Cluster genomes into species:
    For each genome:
      Check against existing species representatives in order.
      If distance(genome, representative) <= threshold, add to species.
      Else, create new species with genome as representative.
    Return list of species, where each species is a list of genome IDs.
    """
    # TODO: Implement speciate_population
    raise NotImplementedError


if __name__ == "__main__":
    print("Run solutions/module_04_solutions.py to test reference solutions.")
