"""Reference Solutions for Module 04 Exercises: Speciation & Fitness Sharing."""

from typing import Dict, List, Set, Tuple


# --- Tier 1: Recall ---
def tier_1_recall_questions() -> dict:
    return {
        "q1": "species size",
        "q2": "excess",
    }


# --- Tier 2: Understanding / Debugging ---
def fixed_compatibility_distance(
    invs1: Set[int],
    invs2: Set[int],
    weights1: Dict[int, float],
    weights2: Dict[int, float],
) -> float:
    max1 = max(invs1) if invs1 else 0
    max2 = max(invs2) if invs2 else 0
    threshold = min(max1, max2)

    diff = invs1 ^ invs2
    # FIXED: Excess genes are beyond threshold; disjoint are within threshold
    excess = sum(1 for i in diff if i > threshold)
    disjoint = sum(1 for i in diff if i <= threshold)

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
    if not invs1 and not invs2:
        return 0.0

    max1 = max(invs1) if invs1 else 0
    max2 = max(invs2) if invs2 else 0
    threshold = min(max1, max2)

    diff = invs1 ^ invs2
    excess = sum(1 for i in diff if i > threshold)
    disjoint = sum(1 for i in diff if i <= threshold)

    matching = invs1 & invs2
    avg_w = (sum(abs(weights1[i] - weights2[i]) for i in matching) / len(matching)) if matching else 0.0

    n_val = max(len(invs1), len(invs2))
    n_norm = float(n_val) if n_val >= 20 else 1.0

    return (c1 * excess / n_norm) + (c2 * disjoint / n_norm) + (c3 * avg_w)


# --- Tier 4: Challenge ---
def speciate_population(
    genomes: List[int],
    distance_matrix: Dict[Tuple[int, int], float],
    threshold: float = 3.0,
) -> List[List[int]]:
    species: List[List[int]] = []
    representatives: List[int] = []

    for g in genomes:
        matched = False
        for i, rep in enumerate(representatives):
            pair = (min(g, rep), max(g, rep))
            dist = distance_matrix.get(pair, 0.0)
            if dist <= threshold:
                species[i].append(g)
                matched = True
                break

        if not matched:
            species.append([g])
            representatives.append(g)

    return species


def test_solutions():
    # Tier 1
    ans = tier_1_recall_questions()
    assert "species" in ans["q1"].lower()
    assert ans["q2"].lower() == "excess"

    # Tier 2
    i1 = {1, 2, 3}
    i2 = {1, 2, 4, 5}
    w1 = {1: 0.5, 2: 0.5, 3: 0.5}
    w2 = {1: 0.5, 2: 0.5, 4: 0.5, 5: 0.5}
    # min max = 3. diff = {3, 4, 5}. 3 is disjoint (<=3), 4,5 are excess (>3)
    d = fixed_compatibility_distance(i1, i2, w1, w2)
    assert abs(d - 3.0) < 1e-4

    # Tier 3
    dist = calculate_compatibility_distance(i1, i2, w1, w2, c1=1.0, c2=1.0, c3=0.4)
    assert abs(dist - 3.0) < 1e-4

    # Tier 4
    # G0, G1 close to each other (dist 1.0). G2 distant from G0, G1 (dist 4.0).
    genomes = [0, 1, 2]
    d_mat = {(0, 1): 1.0, (0, 2): 4.0, (1, 2): 4.0}
    clusters = speciate_population(genomes, d_mat, threshold=2.0)
    assert len(clusters) == 2
    assert clusters[0] == [0, 1]
    assert clusters[1] == [2]

    print("[SUCCESS] All Module 04 solutions verified!")


if __name__ == "__main__":
    test_solutions()
