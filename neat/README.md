# NeuroEvolution of Augmenting Topologies (NEAT)

A rigorous, self-contained educational curriculum and from-scratch Python engine teaching the theory and implementation of **NeuroEvolution of Augmenting Topologies (NEAT)** (Stanley & Miikkulainen, 2002).

---

## 1. Course Architecture & Directory Map

```
neat/
├── README.md                                  # Course Master Guide & Quickstart (this file)
├── neat_engine/                               # Zero-Dependency Pure-Python NEAT Engine
│   ├── __init__.py                            # Engine public exports
│   ├── gene.py                                # NodeGene & ConnectionGene dataclasses
│   ├── genome.py                              # Genotype graph representation & genetic operators
│   ├── innovation.py                          # Global InnovationTracker historical markings
│   ├── species.py                             # Species niches & explicit fitness sharing
│   ├── population.py                          # Population lifecycle & generational epoch loop
│   ├── network.py                             # Kahn's topological DAG sort & recurrent activation
│   └── config.py                              # Typed NEATConfig parameters
├── 01_evolutionary_computation/               # Module 1: EC Foundations
│   ├── README.md
│   ├── 01_genotype_to_phenotype.py            # Chromosome decoding & fitness landscape
│   └── 02_selection_schemes.py                # Tournament, roulette wheel, truncation, rank
├── 02_genetic_algorithms/                     # Module 2: Genetic Algorithms
│   ├── README.md
│   ├── 01_representation_and_mutation.py      # Binary bit-flips & Gaussian perturbations
│   └── 02_crossover_and_elitism.py            # Crossover operators & elitist preservation
├── 03_neuroevolution_topology/                # Module 3: Neuroevolution & Innovations
│   ├── README.md
│   ├── 01_fixed_vs_variable_topology.py       # Linear fixed topologies vs topology growth
│   └── 02_innovation_tracking.py              # Global historical marking & mutation memoization
├── 04_speciation_fitness_sharing/             # Module 4: Speciation & Niches
│   ├── README.md
│   ├── 01_compatibility_distance.py           # Excess, disjoint, and weight difference delta
│   └── 02_fitness_sharing.py                  # Explicit fitness sharing niche carrying capacity
├── 05_crossover_mutation_operators/           # Module 5: NEAT Genetic Operators
│   ├── README.md
│   ├── 01_alignment_and_crossover.py          # Homologous innovation alignment & crossover
│   └── 02_topological_mutations.py            # Add connection & connection splitting (add node)
├── 06_phenotype_network_activation/           # Module 6: Neural Network Phenotypes
│   ├── README.md
│   ├── 01_topological_sort_feedforward.py     # Kahn's topological sort & feedforward inference
│   └── 02_recurrent_activation.py             # Stateful recurrent dynamics & temporal memory
├── visualizations/                            # Pure-Matplotlib Visualization Suite
│   ├── __init__.py
│   ├── visualizer.py                          # plot_fitness, plot_species, plot_network
│   └── demo_visualizations.py                 # Visualizer demonstration generator
├── projects/                                  # Two Complete Runnable Projects
│   ├── 01_xor/                                # Project 1: XOR Non-Linear Classification
│   │   ├── README.md
│   │   ├── train_xor.py                       # Evolutionary trainer reaching fitness > 3.9
│   │   ├── verify_xor.py                      # Truth table prediction verification
│   │   └── output/                            # Saved PNG curves & champion model
│   └── 02_cartpole/                           # Project 2: Pole Balancing Dynamic Control
│       ├── README.md
│       ├── cartpole_env.py                    # Pure-Python Euler-Cromer Lagrangian simulator
│       ├── train_cartpole.py                  # NEAT controller evolution (>= 500 steps)
│       ├── evaluate_controller.py             # Multi-trial validation & telemetry recorder
│       └── output/                            # Saved PNG telemetry trajectories & network
├── exercises/                                 # 4-Tier Student Practice Exercises
│   ├── module_01_exercises.py
│   ├── module_02_exercises.py
│   ├── module_03_exercises.py
│   ├── module_04_exercises.py
│   ├── module_05_exercises.py
│   └── module_06_exercises.py
├── solutions/                                 # Reference Solutions for all 4 Tiers
│   ├── module_01_solutions.py
│   ├── module_02_solutions.py
│   ├── module_03_solutions.py
│   ├── module_04_solutions.py
│   ├── module_05_solutions.py
│   └── module_06_solutions.py
└── tests/                                     # Automated Test Suite
    ├── conftest.py
    ├── test_neat_engine.py                    # Unit tests for core engine components
    ├── test_projects.py                       # E2E integration tests for XOR & Cart-Pole
    └── test_visualizations.py                 # Tests verifying PNG figure generation
```

---

## 2. Pedagogical Framework

Every instructional lesson across all six modules rigorously follows the uniform 6-component pedagogical sequence:

$$\text{TERM} \longrightarrow \text{DEFINITION} \longrightarrow \text{INTUITION} \longrightarrow \text{WHY IT EXISTS} \longrightarrow \text{HOW IT WORKS} \longrightarrow \text{CODE}$$

This structure guarantees that every abstract theoretical concept is immediately anchored in intuitive physical analogies, motivated by real engineering requirements, derived mathematically, and demonstrated in runnable Python code.

---

## 3. Mathematical Reference & NEAT Invariants

| Concept | Mathematical Formulation | Engineering Rationale |
|:---|:---|:---|
| **Compatibility Distance** | $\delta = \frac{c_1 E}{N} + \frac{c_2 D}{N} + c_3 \bar{W}$ | Quantifies topological & parametric divergence to cluster genomes into niches without graph isomorphism tests. |
| **Explicit Fitness Sharing** | $f'_i = \frac{f_i}{\|S_k\|}$ | Divides raw fitness by species size, preventing any single structural archetype from monopolizing the population. |
| **Offspring Allocation** | $N_k = \text{round}\left(N \cdot \frac{\sum_{i \in S_k} f'_i}{\sum_j f'_j}\right)$ | Partitions next generation reproductive bandwidth according to total niche fitness. |
| **Topological Sort** | Kahn's Algorithm: in-degree queue tracking | Determines valid single-pass execution order for arbitrary feedforward DAGs with skip connections. |
| **Add Node Weight Dynamics** | $w_{in \to new} = 1.0, \quad w_{new \to out} = w_{old}$ | Minimizes immediate behavioral shock of structural mutations by preserving signal transmission strength. |
| **Cart-Pole Angular Accel** | $\ddot{\theta} = \frac{g \sin\theta + \cos\theta \left( \frac{-F - m l \dot{\theta}^2 \sin\theta}{M + m} \right)}{l \left( \frac{4}{3} - \frac{m \cos^2\theta}{M + m} \right)}$ | Exact Lagrangian dynamical equation governing inverted pendulum motion. |

---

## 4. Quickstart Guide

### 4.1 Running the Demonstration Scripts
```bash
# Module 01: Foundations of Evolutionary Computation
python3 neat/01_evolutionary_computation/01_genotype_to_phenotype.py
python3 neat/01_evolutionary_computation/02_selection_schemes.py

# Module 02: Genetic Algorithms
python3 neat/02_genetic_algorithms/01_representation_and_mutation.py
python3 neat/02_genetic_algorithms/02_crossover_and_elitism.py

# Module 03: Neuroevolution & Topology
python3 neat/03_neuroevolution_topology/01_fixed_vs_variable_topology.py
python3 neat/03_neuroevolution_topology/02_innovation_tracking.py

# Module 04: Speciation & Fitness Sharing
python3 neat/04_speciation_fitness_sharing/01_compatibility_distance.py
python3 neat/04_speciation_fitness_sharing/02_fitness_sharing.py

# Module 05: Crossover & Mutation Operators
python3 neat/05_crossover_mutation_operators/01_alignment_and_crossover.py
python3 neat/05_crossover_mutation_operators/02_topological_mutations.py

# Module 06: Phenotype & Network Activation
python3 neat/06_phenotype_network_activation/01_topological_sort_feedforward.py
python3 neat/06_phenotype_network_activation/02_recurrent_activation.py
```

### 4.2 Running the Projects
```bash
# Project 1: XOR Evolution
python3 neat/projects/01_xor/train_xor.py
python3 neat/projects/01_xor/verify_xor.py

# Project 2: Cart-Pole Inverted Pendulum Control
python3 neat/projects/02_cartpole/train_cartpole.py
python3 neat/projects/02_cartpole/evaluate_controller.py
```

### 4.3 Running the Visualizer Demonstration
```bash
python3 neat/visualizations/demo_visualizations.py
```

### 4.4 Running the Test Suite
```bash
python3 -m pytest neat/tests/ -v
```

---

## 5. Educational Exercises
Each module contains progressive 4-tier exercises:
- **Tier 1: Recall** — Core definition and concept checks.
- **Tier 2: Understanding & Debugging** — Isolating and fixing deliberate architectural bugs.
- **Tier 3: Application** — Writing from-scratch algorithmic components.
- **Tier 4: Challenge** — Complex evolutionary optimization scenarios.

Reference solutions are located in `neat/solutions/`.
