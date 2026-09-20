# Module 01: Foundations of Evolutionary Computation

Welcome to Module 01 of the NEAT curriculum. In this module, we introduce the first principles of Evolutionary Computation (EC): how biological Darwinian evolution is abstracted into numerical optimization algorithms.

---

## Concept 1: Genotype

### 1. TERM
**Genotype** (Genetic Encoding).

### 2. DEFINITION
The abstract data structure (encoding) representing the hereditary information of a candidate solution in an evolutionary algorithm.

### 3. INTUITION
The genotype is the digital "DNA blueprint." Like an architect's paper schematic, the genotype does not perform any physical work itself; rather, it stores the instructions needed to construct the entity.

### 4. WHY IT EXISTS
Computers cannot directly mutate or recombine complex physical or computational behaviors (such as a trained neural network controller driving a car). The genotype provides a standardized, manipulable representation (e.g., bit strings, real-valued vectors, or graph gene lists) that genetic operators (mutation, crossover) can alter algorithmically.

### 5. HOW IT WORKS
1. Define a mapping scheme from parameters to genes.
2. Initialize genes with random values within valid allele domains.
3. Apply genetic variation operators directly to the genotype without needing to understand the problem domain during variation.

### 6. CODE
```python
from dataclasses import dataclass
from typing import List
import random

@dataclass
class BinaryGenotype:
    genes: List[int]

    @classmethod
    def random(cls, length: int) -> "BinaryGenotype":
        return cls([random.randint(0, 1) for _ in range(length)])

# Example: 8-bit chromosome
g = BinaryGenotype.random(8)
print("Genotype:", g.genes)
```

---

## Concept 2: Phenotype

### 1. TERM
**Phenotype** (Expressed Candidate Solution).

### 2. DEFINITION
The physical, behavioral, or functional realization constructed by decoding the genotype into the target problem environment.

### 3. INTUITION
If the genotype is the architect's schematic, the phenotype is the constructed skyscraper. It is the living organism that interacts with the wind, weather, and gravity.

### 4. WHY IT EXISTS
Evolutionary selection cannot act on hidden code; selection acts exclusively on observable performance. The phenotype is what is actually evaluated against the fitness landscape.

### 5. HOW IT WORKS
1. A decoder reads the genotype data structure.
2. The decoder translates discrete or continuous alleles into domain-specific parameters (e.g., neural network weights, coordinates, controller gains).
3. The phenotype interacts with the environment (e.g., predicts XOR outputs or balances a simulated cart-pole).

### 6. CODE
```python
def decode_binary_to_real(genotype: BinaryGenotype, min_val: float = -5.0, max_val: float = 5.0) -> float:
    """Decode an 8-bit binary string into a continuous real number in [min_val, max_val]."""
    integer_val = 0
    for bit in genotype.genes:
        integer_val = (integer_val << 1) | bit
    max_int = (1 << len(genotype.genes)) - 1
    return min_val + (integer_val / max_int) * (max_val - min_val)

phenotype_val = decode_binary_to_real(g)
print(f"Decoded Phenotype Value: {phenotype_val:.4f}")
```

---

## Concept 3: Fitness Function

### 1. TERM
**Fitness Function** (Objective / Evaluation Function).

### 2. DEFINITION
A mathematical mapping $\mathcal{F}: \text{Phenotype} \to \mathbb{R}$ that quantifies the reproductive suitability and quality of a candidate solution.

### 3. INTUITION
The fitness function is Mother Nature's scoreboard. It grades how well each creature survives in its specific environment.

### 4. WHY IT EXISTS
Without a quantitative measure of performance, an algorithm cannot distinguish beneficial mutations from destructive ones. The fitness function defines the gradient of evolutionary progress.

### 5. HOW IT WORKS
1. Expose the phenotype to a problem test suite or dynamic simulation.
2. Measure error, task completion rate, energy efficiency, or survival duration.
3. Compute a scalar score where higher values correspond to superior performance.

### 6. CODE
```python
def sphere_fitness(x: float) -> float:
    """Maximize proximity to target 0.0 using an inverted quadratic penalty."""
    return 10.0 - (x ** 2)

score = sphere_fitness(phenotype_val)
print(f"Fitness Score: {score:.4f}")
```

---

## Concept 4: Selection Pressure

### 1. TERM
**Selection Pressure**.

### 2. DEFINITION
The degree of bias in an evolutionary algorithm favoring individuals with higher fitness over individuals with lower fitness during parent selection.

### 3. INTUITION
Selection pressure acts like a filter or sieve. If the holes in the sieve are too large (low selection pressure), weak candidates pass through freely and progress is a sluggish random walk. If the holes are too microscopic (high selection pressure), only a tiny fraction passes through, choking diversity and causing premature convergence to local optima.

### 4. WHY IT EXISTS
Balancing exploration (searching new regions of the parameter space) with exploitation (refining the best discoveries) requires carefully tuning selection pressure.

### 5. HOW IT WORKS
- In proportionate selection: probability of selection is directly proportional to fitness.
- In tournament selection: tournament size $k$ directly modulates pressure (larger $k$ increases pressure).
- In truncation selection: only the top $p\%$ of individuals are allowed to reproduce.

### 6. CODE
```python
import numpy as np

def calculate_selection_probabilities(fitnesses: List[float]) -> List[float]:
    """Compute fitness-proportionate selection probabilities."""
    total = sum(fitnesses)
    return [f / total for f in fitnesses]

probs = calculate_selection_probabilities([1.0, 3.0, 6.0])
print("Selection Probabilities:", [f"{p:.2f}" for p in probs])
```

---

## Concept 5: Tournament Selection

### 1. TERM
**Tournament Selection**.

### 2. DEFINITION
A selection operator where $k$ individuals are drawn uniformly at random from the population, and the individual with the highest fitness among them is selected for reproduction.

### 3. INTUITION
Like a sporting bracket: sample a small group of competitors from the crowd; whoever among that small group is best wins the trophy (reproductive rights).

### 4. WHY IT EXISTS
Unlike roulette wheel selection, tournament selection does not require non-negative fitness values, is invariant to constant fitness offsets, and does not require computing population-wide fitness sums ($O(k)$ vs $O(N)$).

### 5. HOW IT WORKS
1. Sample $k$ participants uniformly at random with replacement.
2. Compare their fitness values.
3. Return the participant with the maximal fitness.

### 6. CODE
```python
def tournament_selection(population: List[BinaryGenotype], fitnesses: List[float], k: int = 3) -> BinaryGenotype:
    indices = random.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx]
```

---

## Exercises and Demonstrations
- Run `python3 01_genotype_to_phenotype.py` to see genotype-to-phenotype mapping in action.
- Run `python3 02_selection_schemes.py` to benchmark tournament, roulette wheel, and truncation selection schemes.
