# Module 04: Speciation & Fitness Sharing

Welcome to Module 04 of the NEAT curriculum. In this module, we examine how NEAT protects novel structural innovations from being outcompeted prematurely through speciation and explicit fitness sharing.

---

## Concept 1: Compatibility Distance

### 1. TERM
**Compatibility Distance** ($\delta$).

### 2. DEFINITION
A continuous topological and parametric metric measuring the structural divergence between two neural network genomes:
$$\delta = \frac{c_1 E}{N} + \frac{c_2 D}{N} + c_3 \cdot \bar{W}$$
where $E$ is the count of excess genes, $D$ is the count of disjoint genes, $\bar{W}$ is the average absolute weight difference of matching genes, and $N$ is the genome size normalizer.

### 3. INTUITION
A genetic distance formula comparing two DNA strands. It counts how many genes are completely unmatched at the tail (excess), how many are unmatched in the middle (disjoint), and how much the shared genes differ in intensity (weight difference).

### 4. WHY IT EXISTS
To cluster similar genomes together into biological "species" (niches) so they compete within their own structural class rather than competing against the entire population.

### 5. HOW IT WORKS
1. Sort connection genes by innovation number for Genome 1 and Genome 2.
2. Align matching innovation numbers and record weight differences $|w_1 - w_2|$.
3. Count disjoint genes (innovations present in one genome but not the other, below the max innovation of the smaller genome).
4. Count excess genes (innovations present in the larger genome exceeding the max innovation of the smaller genome).
5. Compute $\delta$ with weighting coefficients $c_1, c_2, c_3$.

### 6. CODE
```python
def compatibility_distance(g1, g2, c1=1.0, c2=1.0, c3=0.4):
    invs1 = set(g1.connections.keys())
    invs2 = set(g2.connections.keys())
    matching = invs1 & invs2
    max1 = max(invs1) if invs1 else 0
    max2 = max(invs2) if invs2 else 0
    threshold = min(max1, max2)
    
    diff_invs = invs1 ^ invs2
    excess = sum(1 for i in diff_invs if i > threshold)
    disjoint = sum(1 for i in diff_invs if i <= threshold)
    
    avg_w = 0.0
    if matching:
        avg_w = sum(abs(g1.connections[i].weight - g2.connections[i].weight) for i in matching) / len(matching)
        
    n = max(len(g1.connections), len(g2.connections))
    n_norm = float(n) if n >= 20 else 1.0
    return (c1 * excess / n_norm) + (c2 * disjoint / n_norm) + (c3 * avg_w)
```

---

## Concept 2: Speciation Threshold

### 1. TERM
**Speciation Threshold** ($\delta_t$).

### 2. DEFINITION
The maximum compatibility distance boundary allowed for a genome to be assigned to an existing species.

### 3. INTUITION
The fence line separating different animal species. If an animal is within the boundary ($\delta \le \delta_t$), it belongs to the herd; if it crosses the boundary ($\delta > \delta_t$), it forms a new species.

### 4. WHY IT EXISTS
Controls the granularity of niching. A threshold that is too low generates dozens of tiny species; a threshold that is too high consolidates the population into a single monoculture.

### 5. HOW IT WORKS
During speciation:
1. Each existing species retains a representative genome from the previous generation.
2. For each new genome, compute $\delta$ against each species representative in order.
3. Assign the genome to the first species where $\delta \le \delta_t$.
4. If no species matches, create a new species with this genome as the founding representative.

### 6. CODE
```python
def speciate_genome(genome, species_list, threshold=3.0):
    for sp in species_list:
        if genome.compatibility_distance(sp.representative) <= threshold:
            sp.add_member(genome)
            return sp
    new_sp = Species(len(species_list) + 1, genome)
    species_list.append(new_sp)
    return new_sp
```

---

## Concept 3: Explicit Fitness Sharing

### 1. TERM
**Explicit Fitness Sharing**.

### 2. DEFINITION
An ecological niching mechanism where each individual's raw fitness is divided by the total number of individuals in its species:
$$f'_i = \frac{f_i}{|S_k|}$$
where $f_i$ is raw fitness, $S_k$ is the species containing individual $i$, and $f'_i$ is the adjusted fitness.

### 3. INTUITION
A watering hole in a savannah. If 100 antelopes crowd around one small watering hole, each gets only a tiny sip. Even a slightly less fertile watering hole with only 2 zebra affords more water per zebra.

### 4. WHY IT EXISTS
Without fitness sharing, a single topological archetype that achieves high fitness on simple traits will quickly conquer the entire population, driving other exploratory topologies into extinction. Fitness sharing penalizes species that grow too large, maintaining diverse structural niches.

### 5. HOW IT WORKS
1. Compute raw fitness $f_i$ for each individual.
2. For each species $S_k$, compute adjusted fitness $f'_i = f_i / |S_k|$.
3. Sum adjusted fitnesses across species: $\bar{f}'_k = \sum_{i \in S_k} f'_i$.
4. Allocate offspring slots for the next generation in proportion to species shared fitness:
   $$N_k = \text{round}\left(N \cdot \frac{\bar{f}'_k}{\sum_j \bar{f}'_j}\right)$$

### 6. CODE
```python
def calculate_shared_fitness(species_members):
    size = len(species_members)
    for individual in species_members:
        individual.adjusted_fitness = individual.fitness / size
```

---

## Concept 4: Stagnation & Niche Extinction

### 1. TERM
**Stagnation**.

### 2. DEFINITION
The condition in which a species fails to improve its all-time best fitness for a predefined number of consecutive generations ($G_{\text{stagnant}}$).

### 3. INTUITION
A species that has reached an evolutionary dead end. If a niche cannot produce better organisms after 15 generations, nature cuts funding to free up ecological resources for younger, promising lineages.

### 4. WHY IT EXISTS
Prevents unproductive topological niches from consuming population carrying capacity indefinitely.

### 5. HOW IT WORKS
1. In each generation, record `species.best_fitness`.
2. If `current_best > species.best_fitness`, reset `stagnation = 0`.
3. If no improvement, increment `stagnation += 1`.
4. If `stagnation > max_stagnation`, the species is disqualified from producing offspring unless it is one of the top overall species in the population.

### 6. CODE
```python
def check_stagnation(species, max_stagnant=15):
    current_max = max(g.fitness for g in species.members)
    if current_max > species.best_fitness + 1e-4:
        species.best_fitness = current_max
        species.stagnation = 0
    else:
        species.stagnation += 1
    return species.stagnation >= max_stagnant
```

---

## Exercises and Demonstrations
- Run `python3 01_compatibility_distance.py` to calculate excess, disjoint, and weight difference metrics between genomes.
- Run `python3 02_fitness_sharing.py` to see how fitness sharing prevents population takeover by local optima.
