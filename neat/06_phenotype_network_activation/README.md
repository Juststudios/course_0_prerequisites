# Module 06: Neural Network Phenotype & Activation

Welcome to Module 06 of the NEAT curriculum. In this module, we explore how arbitrary directed graph genotypes are decoded into executable computational graphs and evaluated in feedforward or recurrent modes.

---

## Concept 1: Phenotype Decoding

### 1. TERM
**Phenotype Decoding** (Graph Instantiation).

### 2. DEFINITION
The deterministic translation of discrete `NodeGene` and `ConnectionGene` records into an operational computational graph structure ready for forward numerical inference.

### 3. INTUITION
Translating an electronic circuit diagram into real soldered wires and chips on a breadboard.

### 4. WHY IT EXISTS
Genotypes are designed for efficient reproduction, storage, mutation, and crossover (lists of flat gene objects). Phenotypes are optimized for fast linear algebraic or graph-traversal tensor evaluation.

### 5. HOW IT WORKS
1. Filter out disabled connections (`enabled == False`).
2. Identify input, bias, hidden, and output node sets.
3. Build adjacency lists mapping source nodes to destination nodes with synaptic weights.
4. Verify directed graph invariants.

### 6. CODE
```python
def decode_genome(genome):
    active_edges = [(c.in_node, c.out_node, c.weight) for c in genome.connections.values() if c.enabled]
    return active_edges
```

---

## Concept 2: Topological Sorting (Kahn's Algorithm)

### 1. TERM
**Topological Sort** (Kahn's Algorithm).

### 2. DEFINITION
A linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $u \to v$, vertex $u$ appears before vertex $v$ in the sequence.

### 3. INTUITION
A domino chain or recipe sequence. You cannot bake a cake before mixing the batter, and you cannot mix the batter before cracking the eggs. Every step must wait until all prerequisite ingredients have arrived.

### 4. WHY IT EXISTS
In traditional layered neural networks, computation proceeds trivially from Layer 0 to Layer $L$. In NEAT, arbitrary structural mutations can create skip-connections, cross-layer edges, or irregular topologies with no fixed layers. Topological sorting guarantees single-pass feedforward evaluation without race conditions or undefined inputs.

### 5. HOW IT WORKS
1. Compute in-degree (number of incoming enabled edges) for all nodes in the graph.
2. Initialize a queue with all nodes having in-degree 0 (inputs, bias, and independent nodes).
3. While queue is non-empty:
   - Dequeue node $u$, append to ordering.
   - For each outgoing neighbor $v$ of $u$, decrement in-degree of $v$.
   - If in-degree of $v$ becomes 0, enqueue $v$.
4. If ordering length is less than total nodes, a cycle exists (handled by cycle breaking or recurrent evaluation).

### 6. CODE
```python
def kahns_topological_sort(nodes, edges):
    in_degree = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for u, v in edges:
        in_degree[v] += 1
        adj[u].append(v)
        
    queue = [n for n in nodes if in_degree[n] == 0]
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order
```

---

## Concept 3: Feedforward DAG Activation

### 1. TERM
**Feedforward DAG Activation**.

### 2. DEFINITION
The forward computation of neural activations across a directed acyclic graph following topological ordering:
$$z_v = b_v + \sum_{u \in \text{In}(v)} w_{uv} a_u$$
$$a_v = \sigma(z_v)$$
where $b_v$ is node bias, $\text{In}(v)$ is the set of incoming nodes, and $\sigma(\cdot)$ is the activation function.

### 3. INTUITION
Signal propagation down a one-way river delta. Water flows forward through channels, combining at junction pools, until it empties out into the sea (output nodes).

### 4. WHY IT EXISTS
Enables stateless, memoryless inference for classification, regression, and reactive control policies (e.g., XOR classification or Cart-Pole reactive balancing).

### 5. HOW IT WORKS
1. Load input features into input nodes.
2. Set bias node value to 1.0.
3. Iterate through topologically ordered hidden and output nodes:
   - Accumulate weighted inputs from incoming edges.
   - Add node bias.
   - Apply non-linear activation (sigmoid, tanh, relu).
4. Read values from output nodes.

### 6. CODE
```python
def activate_feedforward(inputs, eval_order, in_edges, biases, activation_fn):
    values = dict(inputs)
    for node in eval_order:
        z = biases.get(node, 0.0)
        for in_node, weight in in_edges[node]:
            z += values[in_node] * weight
        values[node] = activation_fn(z)
    return values
```

---

## Concept 4: Recurrent Network Activation

### 1. TERM
**Recurrent Network Activation** (Stateful Temporal Dynamics).

### 2. DEFINITION
Evaluation of neural networks containing cyclic or self-referential directed connections ($v \to u$ where $u$ precedes $v$), simulated across discrete time-steps using state persistence or relaxation steps.

### 3. INTUITION
Short-term working memory. Unlike a stateless calculator, a recurrent network remembers past sensory inputs, allowing it to estimate velocities from raw position sensors or track temporal patterns over time.

### 4. WHY IT EXISTS
Many real-world control tasks (such as double pole balancing without velocity sensors) violate the Markov property. Controllers require internal hidden state memory to infer unobserved derivatives.

### 5. HOW IT WORKS
1. Maintain internal activation states $\mathbf{h}_t \in \mathbb{R}^{|V|}$ across calls.
2. At time step $t$, compute new activations using states from time step $t-1$:
   $$z_v^{(t)} = b_v + \sum_{u} w_{uv} a_u^{(t-1)}$$
   $$a_v^{(t)} = \sigma(z_v^{(t)})$$
3. Alternatively, perform $K$ relaxation steps per input to settle activations.

### 6. CODE
```python
class SimpleRecurrentNet:
    def __init__(self, in_edges, num_nodes):
        self.in_edges = in_edges
        self.state = {i: 0.0 for i in range(num_nodes)}
        
    def step(self, inputs):
        self.state.update(inputs)
        next_state = dict(self.state)
        for node, edges in self.in_edges.items():
            z = sum(self.state[u] * w for u, w in edges)
            next_state[node] = 1.0 / (1.0 + math.exp(-z))
        self.state = next_state
        return self.state
```

---

## Exercises and Demonstrations
- Run `python3 01_topological_sort_feedforward.py` to trace Kahn's algorithm and forward activation on an irregular graph.
- Run `python3 02_recurrent_activation.py` to observe temporal memory dynamics in a recurrent NEAT network.
