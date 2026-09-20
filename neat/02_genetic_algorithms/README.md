# Module 02: Genetic Algorithms

Welcome to Module 02 of the NEAT curriculum. Genetic Algorithms (GAs) build upon evolutionary computation foundations by defining concrete recombination, mutation, and generational replacement operators.

---

## Concept 1: Genetic Representation

### 1. TERM
**Genetic Representation** (Allelic Encoding).

### 2. DEFINITION
The mathematical format chosen to encode candidate solution parameters into a manipulable chromosome structure.

### 3. INTUITION
The chosen alphabet used to write the genetic book. If writing in binary bits ($0, 1$), parameters must be discretized. If writing in continuous real numbers ($\mathbb{R}^D$), parameters correspond directly to physical or mathematical quantities.

### 4. WHY IT EXISTS
The choice of representation fundamentally shapes the topology of the search space. A poorly matched representation creates Hamming cliffs (where adjacent numerical values require mutating multiple bits simultaneously), whereas continuous representations enable smooth local gradient exploration.

### 5. HOW IT WORKS
- **Binary Representation**: Strings of $\{0, 1\}$. Evaluated via decoding functions.
- **Real-Valued Representation**: Vectors $\mathbf{x} \in \mathbb{R}^D$. Directly injected into objective functions.
- **Permutation Representation**: Ordered lists for combinatorial problems (e.g., TSP).

### 6. CODE
```python
from dataclasses import dataclass
from typing import List
import random

@dataclass
class RealValuedIndividual:
    genes: List[float]

    @classmethod
    def random(cls, dimension: int, low: float = -1.0, high: float = 1.0) -> "RealValuedIndividual":
        return cls([random.uniform(low, high) for _ in range(dimension)])
```

---

## Concept 2: Crossover Operators

### 1. TERM
**Crossover Operator** (Recombination).

### 2. DEFINITION
A binary genetic operator that combines genetic material from two parent chromosomes to construct one or more offspring chromosomes.

### 3. INTUITION
Sexual reproduction in biology. Offspring inherit a blend of maternal and paternal traits, potentially combining beneficial building blocks (schemas) discovered independently by different ancestral lineages.

### 4. WHY IT EXISTS
Mutation alone is a localized random walk. Crossover performs large, structured leaps across the search space by synthesizing disparate high-performing traits.

### 5. HOW IT WORKS
- **Single-Point Crossover**: A single cut point $c \in [1, L-1]$ is selected; offspring inherits genes $0 \dots c-1$ from Parent 1 and $c \dots L-1$ from Parent 2.
- **Two-Point Crossover**: Two points $c_1, c_2$ are selected, swapping the enclosed segment.
- **Uniform Crossover**: For every gene position $i$, a coin flip chooses whether to inherit from Parent 1 or Parent 2 with probability $p = 0.5$.

### 6. CODE
```python
def single_point_crossover(p1: List[float], p2: List[float]) -> Tuple[List[float], List[float]]:
    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2
```

---

## Concept 3: Mutation Operators

### 1. TERM
**Mutation Operator**.

### 2. DEFINITION
A unary stochastic operator that introduces exploratory perturbations into an individual chromosome with small probability.

### 3. INTUITION
Copy errors during DNA replication. While mostly neutral or slightly detrimental, occasional mutations introduce novel features that never existed in the ancestral gene pool.

### 4. WHY IT EXISTS
Crossover can only recombine alleles already present in the current population. If all individuals possess allele $0$ at gene position $k$, crossover can never generate allele $1$. Mutation ensures ergodicity—the theoretical guarantee that any point in the search space remains reachable.

### 5. HOW IT WORKS
- **Bit-Flip Mutation**: Each bit is inverted ($0 \to 1, 1 \to 0$) with probability $p_m \approx 1/L$.
- **Gaussian Perturbation**: For continuous genes, additive Gaussian noise is added: $w' = w + \mathcal{N}(0, \sigma^2)$.
- **Uniform Replacement**: The gene is reset to a completely new random value within bounds.

### 6. CODE
```python
def gaussian_mutate(genes: List[float], rate: float = 0.8, power: float = 0.5) -> List[float]:
    mutated = []
    for g in genes:
        if random.random() < rate:
            mutated.append(g + random.gauss(0.0, power))
        else:
            mutated.append(g)
    return mutated
```

---

## Concept 4: Elitism

### 1. TERM
**Elitism** (Elitist Generational Preservation).

### 2. DEFINITION
An evolutionary preservation mechanism wherein a fixed number $E$ of the highest-fitness individuals from generation $t$ are copied unaltered into generation $t+1$.

### 3. INTUITION
The "safe deposit box" of evolutionary computation. It guarantees that if a population discovers an extraordinary solution, stochastic crossover or mutation will not accidentally destroy it before it can propagate.

### 4. WHY IT EXISTS
Without elitism, maximum population fitness can fluctuate wildly or regress due to destructive genetic operations. Elitism guarantees that the best-so-far fitness curve is monotonically non-decreasing:
$$\max_{i} \mathcal{F}(x_i^{(t+1)}) \ge \max_{j} \mathcal{F}(x_j^{(t)})$$

### 5. HOW IT WORKS
1. Evaluate and sort population by fitness in descending order.
2. Directly copy the top $E$ individuals into the next generation's pool.
3. Fill the remaining $N - E$ slots via tournament selection, crossover, and mutation.

### 6. CODE
```python
def generational_step_with_elitism(pop: List[List[float]], fitnesses: List[float], elitism_count: int = 2) -> List[List[float]]:
    paired = sorted(zip(pop, fitnesses), key=lambda x: x[1], reverse=True)
    next_gen = [list(indiv) for indiv, _ in paired[:elitism_count]]
    # Fill remaining slots through reproduction...
    return next_gen
```

---

## Exercises and Demonstrations
- Run `python3 01_representation_and_mutation.py` to compare binary vs continuous representation and mutation dynamics.
- Run `python3 02_crossover_and_elitism.py` to see how elitism guarantees monotonic optimization progress on continuous benchmark functions.
