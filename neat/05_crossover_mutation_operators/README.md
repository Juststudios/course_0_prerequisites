# Module 05: Crossover & Mutation Operators in NEAT

Welcome to Module 05 of the NEAT curriculum. In this module, we dissect the genetic variation operators that allow neural network topologies to recombine safely and complexify incrementally.

---

## Concept 1: Gene Alignment

### 1. TERM
**Gene Alignment** (Homologous Innovation Pairing).

### 2. DEFINITION
The process of lining up the connection genes of two parent genomes in ascending order of their historical innovation numbers.

### 3. INTUITION
Like lining up two zipper halves. When two people compare receipts, matching item numbers line up side-by-side, while items bought by only one person stand out clearly.

### 4. WHY IT EXISTS
Neural network genomes have variable lengths and arbitrary node numbering. Without alignment by historical origin, crossover cannot determine which connections in Parent 1 correspond to connections in Parent 2.

### 5. HOW IT WORKS
1. Sort connection genes of Parent 1 and Parent 2 by their `innovation` integer tag.
2. Step through the innovation lists simultaneously using two pointers.
3. Group genes into three distinct categories:
   - **Matching Genes**: Innovations present in both parents.
   - **Disjoint Genes**: Innovations present in only one parent, within the innovation range of the other parent.
   - **Excess Genes**: Innovations present in only one parent, beyond the maximum innovation of the other parent.

### 6. CODE
```python
def align_genes(parent1, parent2):
    p1_invs = set(parent1.connections.keys())
    p2_invs = set(parent2.connections.keys())
    matching = sorted(p1_invs & p2_invs)
    max_p1, max_p2 = max(p1_invs), max(p2_invs)
    threshold = min(max_p1, max_p2)
    
    diff = p1_invs ^ p2_invs
    disjoint = sorted(i for i in diff if i <= threshold)
    excess = sorted(i for i in diff if i > threshold)
    return matching, disjoint, excess
```

---

## Concept 2: NEAT Crossover Operator

### 1. TERM
**NEAT Crossover Operator**.

### 2. DEFINITION
A recombination operator where matching genes are inherited randomly (50/50 probability) from either parent, while disjoint and excess genes are inherited exclusively from the fitter parent.

### 3. INTUITION
The fitter parent provides the architectural foundation (all its non-matching genes are preserved). For the traits both parents share, the child gets a coin-flip choice between the mother's weight or the father's weight.

### 4. WHY IT EXISTS
Inheriting disjoint or excess genes from a less-fit parent often introduces incomplete, damaged, or incompatible topological structures. Prioritizing the fitter parent's architecture ensures offspring retain functional integrity.

### 5. HOW IT WORKS
1. Identify fitter parent $P_{\text{fit}}$ and less-fit parent $P_{\text{other}}$.
2. For each matching innovation $i$:
   - Inherit connection gene from $P_{\text{fit}}$ or $P_{\text{other}}$ with 50% probability.
   - If the gene is disabled in either parent, disable it in the child with 75% probability.
3. For each disjoint or excess innovation:
   - Inherit only if it originates from $P_{\text{fit}}$. (If parents have identical fitness, disjoint/excess from both parents can be included).
4. Reconstruct necessary nodes referenced by inherited connections.

### 6. CODE
```python
def neat_crossover(parent1, parent2, rng=random):
    fitter, other = (parent1, parent2) if parent1.fitness >= parent2.fitness else (parent2, parent1)
    child = Genome()
    
    for inv, conn in fitter.connections.items():
        if inv in other.connections:
            # Matching: coin flip
            chosen = conn if rng.random() < 0.5 else other.connections[inv]
            child.connections[inv] = chosen.copy()
        else:
            # Disjoint/Excess from fitter parent
            child.connections[inv] = conn.copy()
            
    return child
```

---

## Concept 3: Add Connection Mutation

### 1. TERM
**Add Connection Mutation**.

### 2. DEFINITION
A structural mutation operator that creates a novel directed synaptic connection between two previously unconnected nodes.

### 3. INTUITION
Building a new bridge between two isolated islands. It opens a direct communication pathway where signals could not previously flow.

### 4. WHY IT EXISTS
Allows the neural network to integrate information from different sensory inputs or combine features computed by intermediate hidden layers.

### 5. HOW IT WORKS
1. Identify candidate source nodes (inputs, biases, hidden nodes) and target nodes (hidden nodes, output nodes).
2. Filter out existing connections, self-loops, and connections that would introduce cycles in a feedforward network.
3. If candidate pairs exist, pick one uniformly at random.
4. Assign a random initial synaptic weight (e.g., $w \sim \mathcal{U}(-1.0, 1.0)$).
5. Query the global `InnovationTracker` for an innovation number.

### 6. CODE
```python
def mutate_add_connection(genome, tracker, rng=random):
    sources = [nid for nid, n in genome.nodes.items() if n.node_type != 'output']
    targets = [nid for nid, n in genome.nodes.items() if n.node_type not in ('input', 'bias')]
    # Select unconnected pair (u, v) without creating cycles...
    inv = tracker.get_innovation(u, v)
    genome.connections[inv] = ConnectionGene(in_node=u, out_node=v, weight=rng.uniform(-1, 1), innovation=inv)
```

---

## Concept 4: Add Node Mutation

### 1. TERM
**Add Node Mutation** (Connection Splitting).

### 2. DEFINITION
A structural mutation operator that disables an existing connection and splices a new hidden neuron into that pathway via two newly created connections.

### 3. INTUITION
Inserting a relay station or signal processing amplifier along an existing telephone wire without cutting off the ongoing communication.

### 4. WHY IT EXISTS
Enables **incremental complexification**. By inserting the new neuron with an incoming weight of $1.0$ and an outgoing weight equal to the disabled connection's original weight, the immediate behavioral disruption to the network's function is minimized, allowing evolution to gently elaborate existing features.

### 5. HOW IT WORKS
1. Select an existing enabled connection $A \to B$ with weight $w$.
2. Disable the original connection: `conn.enabled = False`.
3. Request a novel node ID $C$ from `InnovationTracker`.
4. Create incoming connection $A \to C$ with weight $1.0$ and assign new innovation number.
5. Create outgoing connection $C \to B$ with weight $w$ and assign new innovation number.

### 6. CODE
```python
def mutate_add_node(genome, tracker):
    enabled_conns = [c for c in genome.connections.values() if c.enabled]
    target = random.choice(enabled_conns)
    target.enabled = False
    
    new_nid = tracker.get_node_id(target.innovation)
    genome.nodes[new_nid] = NodeGene(id=new_nid, node_type='hidden')
    
    inv_in = tracker.get_innovation(target.in_node, new_nid)
    genome.connections[inv_in] = ConnectionGene(target.in_node, new_nid, weight=1.0, innovation=inv_in)
    
    inv_out = tracker.get_innovation(new_nid, target.out_node)
    genome.connections[inv_out] = ConnectionGene(new_nid, target.out_node, weight=target.weight, innovation=inv_out)
```

---

## Exercises and Demonstrations
- Run `python3 01_alignment_and_crossover.py` to trace step-by-step innovation alignment and recombination.
- Run `python3 02_topological_mutations.py` to inspect the mathematical weight preservation of connection splitting.
