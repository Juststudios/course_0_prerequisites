# Project 1: XOR Evolution with NEAT

## 1. Problem Statement
The exclusive-OR (XOR) logic function is the foundational benchmark problem in neuroevolution. XOR is non-linearly separable: no linear decision boundary (single-layer perceptron) can classify all four inputs correctly.

| Input $x_1$ | Input $x_2$ | Target Output $y$ |
|:---:|:---:|:---:|
| 0.0 | 0.0 | 0.0 |
| 0.0 | 1.0 | 1.0 |
| 1.0 | 0.0 | 1.0 |
| 1.0 | 1.0 | 0.0 |

A single-layer perceptron without hidden neurons can achieve at most an error of 1.0 (fitness 3.0 out of 4.0), separating at most 3 of the 4 cases.

## 2. NEAT Evolutionary Strategy
NEAT solves XOR by:
1. **Starting Minimally**: Beginning with a population of linear networks containing 2 inputs, 1 bias, and 1 output (0 hidden nodes).
2. **Complexification**: Discovering that linear networks cannot reduce error below 0.75, evolutionary selection favors structural mutations (`add_node` and `add_connection`).
3. **Speciation**: Protecting newly discovered hidden neurons in distinct species niches until their synaptic weights are optimized.
4. **Convergence**: Reaching a fitness threshold $> 3.9$ (total squared error $< 0.1$), correctly solving the non-linear classification boundary.

## 3. Running the Project
Train the XOR controller:
```bash
python3 neat/projects/01_xor/train_xor.py
```

Verify against the XOR truth table:
```bash
python3 neat/projects/01_xor/verify_xor.py
```

## 4. Visual Artifacts
The training run outputs publication-quality Matplotlib figures to `output/`:
- `xor_fitness_curve.png`: Convergence trajectory of best and average population fitness.
- `xor_species_tracking.png`: Species population dynamics stackplot over generations.
- `xor_best_network.png`: Topological graph diagram showing the evolved architecture with discovered hidden neuron(s).
