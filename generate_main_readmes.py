from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")

main_readme = """# Course 0: Prerequisites for AI Agent Engineering

Welcome to the foundation of AI Agent Engineering. This course bridges the gap between basic Python programming and building complex AI-agent runtimes like Hermes. 

This is **not** a generic Python course. Every concept taught here is directly tied to a problem you will face when building an agent.

## The Learning Path

```text
PYTHON
 ├── Functions
 ├── Classes
 ├── Type Hints
 ├── Async
 ├── Context Management
 └── ContextVars
          ↓
NETWORKING
 ├── HTTP
 ├── JSON
 └── APIs
          ↓
SYSTEMS
 ├── Environment
 ├── Processes
 └── SQLite
          ↓
ARCHITECTURE
 ├── Registry
 ├── Plugins
 ├── Dependency Injection
 └── Scoped State
          ↓
MATHEMATICS
 ├── Algebra
 ├── Probability
 ├── Vectors
 ├── Matrices
 ├── Derivatives
 ├── Optimization
 └── Complexity
          ↓
AI AGENT DEVELOPMENT
```

## Why These Topics?

* **Python:** Agents are heavily asynchronous, type-driven, and require strict state management across concurrent requests.
* **Networking:** Agents interact with LLMs and external tools via HTTP APIs using JSON payloads.
* **Systems:** Agents spawn subprocesses for code execution, use environment variables for secrets, and require fast local storage like SQLite for memory.
* **Architecture:** Building an agent requires scalable software patterns (registries, dependency injection) rather than spaghetti code.
* **Mathematics:** Understanding how LLMs reason, how search algorithms explore, and how embeddings map meaning requires a foundation in probability, vectors, and complexity.

## Prerequisites

You should already know basic Python (variables, loops, lists, and dictionaries). 
If you need a refresher on Data Tools (NumPy/Pandas) or advanced Calculus/Linear Algebra, refer to `Level 1` and `Level 2` in the broader curriculum.

## Key Terminology

| Term      | Meaning                                       | Example              |
| --------- | --------------------------------------------- | -------------------- |
| Callable  | An object that can be invoked like a function | `add(2,3)`           |
| Coroutine | An async function execution unit              | `fetch_data()`       |
| Context   | Request/task-local execution state            | `request_id`         |
| Endpoint  | A network-accessible API location             | `/v1/models`         |
| Payload   | Data sent with a request                      | JSON body            |
| Process   | Running program                               | Python child process |
| Registry  | Mapping of names to components                | tool registry        |

"""

math_readme = """# Mathematics for AI Agent Engineers

This module introduces the core mathematical concepts that power AI agents, machine learning models, and LLMs. 
We focus on **understanding** rather than mathematical overload. 

## SECTION A — BASIC ALGEBRA

### Terminology
* **Variable:** A symbol representing an unknown or changing quantity.
* **Constant:** A fixed value.
* **Function:** A mapping from an input to an output.

### Intuition
Algebra lets us generalize arithmetic. Instead of saying `2 + 3 = 5`, we say `x + y = z`.

### Agent Connection
Every LLM parameter and tool argument is a variable in a massive algebraic equation.

## SECTION B — LOGARITHMS

### Intuition
A logarithm answers the question: "How many of one number do we multiply to get another number?"

### Formula
```text
log(a * b) = log(a) + log(b)
log(a^b) = b * log(a)
```

### Why This Matters / Agent Connection
LLMs output probabilities for the next word. Multiplying many small probabilities results in underflow (numbers too small for computers). Logarithms let us *add* instead of multiply, preserving precision (e.g., Log-Likelihood).

## SECTION C — PROBABILITY

### Intuition
Probability measures uncertainty. 

### Formula
```text
P(A) = number of favorable outcomes / total outcomes
P(A | B) = P(A ∩ B) / P(B)
```

### What each symbol means
* `P(A)`: Probability of event A occurring.
* `P(A | B)`: Probability of A given that B has occurred (Conditional Probability).

### Step 1
Assume we have an LLM predicting the next word.
### Step 2
The model thinks "apple" has a 30% chance, and "banana" has a 20% chance.
### Step 3
`P(word="apple" | previous="eat an") = 0.30`

### Agent Connection
LLMs don't know facts; they sample from probability distributions.

## SECTION D — EXPECTED VALUE

### Formula
```text
E[X] = Σ x P(x)
```

### What each symbol means
* `E[X]`: Expected value.
* `Σ`: Sum over all possible values.
* `x`: A specific value.
* `P(x)`: Probability of that value.

### Agent Connection
Reinforcement Learning agents (like AlphaGo or MCTS planning agents) choose the action with the highest expected reward.

## SECTION E — VECTORS

### Intuition
A vector is a list of numbers representing a point in space or a direction.

### Formula
```text
x = [x₁, x₂, x₃]
Dot Product: x · w = x₁w₁ + x₂w₂ + x₃w₃
```

### Agent Connection
Words are converted into embeddings (dense vectors). The dot product between two vectors measures their semantic similarity.

## SECTION F — MATRICES

### Intuition
A matrix is a grid of numbers. It transforms vectors.

### Agent Connection
The attention mechanism in Transformers (the architecture behind LLMs) is almost entirely matrix multiplication.

## SECTION G — FUNCTIONS AND COMPOSITION

### Formula
```text
g(f(x))
```

### Agent Connection
Software pipelines (Prompt -> LLM -> Tool) are mathematical function compositions.

## SECTION H — DERIVATIVES

### Intuition
A derivative describes how quickly a quantity changes.

### Formula
```text
f(x) = x²
f'(x) = 2x
```

## SECTION I — GRADIENTS

### Intuition
A gradient is a vector of partial derivatives for multi-variable functions.

### Agent Connection
Gradients tell a neural network how to update its weights to make fewer mistakes.

## SECTION J — BASIC OPTIMIZATION

### Formula
```text
θ_new = θ_old - η∇L
```

### What each symbol means
* `θ`: Model parameters.
* `η`: Learning rate (step size).
* `∇L`: Gradient of the Loss function.

## SECTION K — BIG-O NOTATION

### Intuition
Big-O measures how an algorithm's runtime scales as the input size grows.

### Categories
* `O(1)`: Constant time (Hash map / Registry lookup).
* `O(n)`: Linear time (Iterating a list).
* `O(n²)`: Quadratic time (Nested loops).

### Agent Connection
A tool registry must be `O(1)`. If an agent searches its memory, the algorithm dictates if it responds in milliseconds or minutes.
"""

with open(BASE_DIR / "README.md", "w") as f:
    f.write(main_readme)

with open(BASE_DIR / "10_math_for_agents" / "README.md", "w") as f:
    f.write(math_readme)

print("Main READMEs created.")
