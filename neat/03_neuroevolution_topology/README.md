# Module 03: Neuroevolution & Topology Evolution

Welcome to Module 03 of the NEAT curriculum. In this module, we transition from classical genetic algorithms on vectors to evolving the graph architecture and synaptic weights of neural networks concurrently.

---

## Concept 1: TWEANNs

### 1. TERM
**TWEANN** (Topology and Weight Evolving Artificial Neural Network).

### 2. DEFINITION
A neuroevolution methodology that concurrently optimizes both the graph connectivity (nodes, directed edges) and the continuous synaptic weight parameters of an artificial neural network.

### 3. INTUITION
Instead of an engineer manually guessing how many layers and neurons a network needs before training, the evolutionary algorithm starts from a minimal blank slate and organically discovers the necessary brain structures to solve the problem.

### 4. WHY IT EXISTS
Manual neural network architecture design is often biased, inefficient, and prone to over-parameterization. Fixed topologies risk either being too small to represent the solution (underfitting) or too large and difficult to optimize (overfitting/bloat). TWEANNs automate structural discovery.

### 5. HOW IT WORKS
1. Genomes encode directed graphs of neurons and synapses.
2. Search begins with minimal topologies (no hidden neurons).
3. Structural mutations periodically insert new connections or split existing connections to add neurons.
4. Parametric mutations adjust synaptic weights.

### 6. CODE
```python
@dataclass
class TWEANNConnection:
    in_node: int
    out_node: int
    weight: float
    enabled: bool = True
```

---

## Concept 2: Fixed vs. Variable Topology

### 1. TERM
**Fixed vs. Variable Topology**.

### 2. DEFINITION
The distinction between neuroevolutionary algorithms constrained to optimize weights on a static, predetermined graph structure vs. algorithms that can dynamically expand, contract, and reconfigure the graph topology during search.

### 3. INTUITION
Fixed topology is like tuning the piano strings on a standard 88-key piano. Variable topology allows the tuner to add entirely new strings, keyboards, and acoustic chambers when the current instrument cannot reach the required notes.

### 4. WHY IT EXISTS
Fixed-topology methods (like conventional backpropagation or fixed-topology GA) require knowing the network structure beforehand. In complex non-linear problems, the minimal sufficient topology is rarely known a priori.

### 5. HOW IT WORKS
- **Fixed Topology**: Weight vector $\mathbf{w} \in \mathbb{R}^M$. Search optimizes $\mathbf{w}$ while graph $G = (V, E)$ remains constant.
- **Variable Topology**: Search operates over the joint space $(G, \mathbf{w}) \in \mathcal{G} \times \mathbb{R}^{|E|}$. Structural operators alter $|V|$ and $|E|$ dynamically.

### 6. CODE
```python
# Fixed topology representation (flat vector)
fixed_weights = [0.25, -1.2, 0.85, 0.4]

# Variable topology representation (graph gene dictionary)
variable_graph = {
    "nodes": {0: "input", 1: "input", 2: "output", 3: "hidden"},
    "edges": [(0, 3, 0.5), (1, 3, -0.8), (3, 2, 1.2), (0, 2, 0.1)]
}
```

---

## Concept 3: The Competing Conventions Problem

### 1. TERM
**Competing Conventions Problem** (The Permutation Problem).

### 2. DEFINITION
The pathological condition in neuroevolution where two parent networks have functionally identical internal logic but represent that logic using different internal hidden neuron permutations, causing genetic crossover to produce damaged, non-functional offspring.

### 3. INTUITION
Imagine two teams writing the same essay. Team 1 writes Section A then Section B. Team 2 writes Section B then Section A. If an editor blindly combines the first half of Team 1 with the second half of Team 2, the result contains two copies of Section A and zero copies of Section B.

### 4. WHY IT EXISTS
In a multi-layer perceptron with $k$ hidden neurons, there are $k!$ mathematically equivalent permutations of those neurons. When two functionally equivalent networks with different neuron labellings are recombined, corresponding functional features are not aligned, resulting in catastrophic loss of information.

### 5. HOW IT WORKS
Before NEAT (2002), researchers attempted to solve this with graph isomorphism algorithms ($O(V!)$), which are computationally intractable for real-time evolutionary loops.

### 6. CODE
```python
# Network 1: Hidden Node A calculates OR, Hidden Node B calculates AND
# Network 2: Hidden Node X calculates AND, Hidden Node Y calculates OR
# Crossover blindly pairing (A, X) creates redundant or broken logic!
```

---

## Concept 4: Innovation Numbers & Historical Markings

### 1. TERM
**Innovation Number** (Historical Marking).

### 2. DEFINITION
A unique, monotonically incrementing integer assigned globally to every novel gene (connection) at the moment of its evolutionary emergence, serving as an immutable chronological timestamp of the gene's historical origin.

### 3. INTUITION
An evolutionary "passport barcode" or "birth certificate." Even if two genomes have mutated drastically over hundreds of generations, inspecting their innovation barcodes allows instant chronological alignment without needing graph isomorphism tests.

### 4. WHY IT EXISTS
Solves the Competing Conventions problem in $O(G)$ linear time. Two connection genes with the same innovation number represent the same homologous evolutionary trait.

### 5. HOW IT WORKS
1. Maintain a global `InnovationTracker` with counter `current_innovation` and cache `generation_innovations: Dict[(in_node, out_node), id]`.
2. When mutation creates edge $(u, v)$, assign existing ID if $(u, v)$ already emerged in the current generation; otherwise increment the counter.
3. During crossover, align genomes by matching their innovation numbers.

### 6. CODE
```python
class InnovationTracker:
    def __init__(self):
        self.current_innovation = 0
        self.generation_innovations = {}

    def get_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key in self.generation_innovations:
            return self.generation_innovations[key]
        self.current_innovation += 1
        self.generation_innovations[key] = self.current_innovation
        return self.current_innovation

    def reset_generation(self):
        self.generation_innovations.clear()
```

---

## Exercises and Demonstrations
- Run `python3 01_fixed_vs_variable_topology.py` to observe the limitations of fixed-topology search on non-linear problems.
- Run `python3 02_innovation_tracking.py` to trace global historical markings across concurrent mutations.
