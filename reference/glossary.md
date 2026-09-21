# Master Terminology Glossary

A unified index of every important term used across the curriculum.
Each entry: **Term** | Definition | Example | Where it appears.

---

## Python Foundations (Course -1)

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Variable** | A name bound to a value in memory | `age = 18` | Module 3 |
| **Function** | A named, reusable block of code | `def add(a, b): return a+b` | Module 8 |
| **Callable** | Any object invokable with `()` | `add(2,3)`, `my_obj()` | Module 8, 14 |
| **Class** | Blueprint for creating objects | `class Agent: ...` | Module 13 |
| **Object / Instance** | A concrete thing created from a class | `a = Agent()` | Module 13 |
| **Attribute** | Data attached to an object | `agent.name` | Module 13 |
| **Method** | A function belonging to a class | `agent.run()` | Module 13 |
| **`self`** | Reference to the current instance | `self.name = name` | Module 13 |
| **Inheritance** | A class extending another | `class LogAgent(Agent)` | Module 13 |
| **Type Hint** | Optional label describing expected type | `name: str` | Module 15 |
| **Decorator** | A function wrapping another function | `@timer` | Module 19 |
| **Generator** | A function using `yield` to produce values lazily | `def stream(): yield token` | Module 18 |
| **Context Manager** | Object managing resource setup/teardown with `with` | `with open(f) as fh:` | Module 20 |
| **Module** | A `.py` file importable by others | `import tools` | Module 12 |
| **Package** | A directory with `__init__.py` | `from agent import tools` | Module 12 |
| **Exception** | A runtime error object | `ZeroDivisionError` | Module 10 |
| **Assertion** | `assert cond` — raises AssertionError if False | `assert result == 5` | Module 21 |
| **Dataclass** | Class with auto-generated `__init__`, `__repr__` | `@dataclass class Cfg:` | Module 16 |

---

## Agent Architecture (Course 0)

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Tool** | A callable function available to the LLM | `registry["add"]` | Course 0 Mod 1 |
| **Registry** | A mapping of tool names to implementations | `{"add": add_fn}` | Course 0 Mod 8 |
| **Facade** | A simplified interface hiding internal complexity | `AgentFacade.run()` | Course 0 Mod 8 |
| **Dependency Injection** | Passing dependencies in rather than creating them inside | `Agent(registry=reg)` | Course 0 Mod 8 |
| **Plugin** | A dynamically discovered/loaded module | `load_plugin("search")` | Course 0 Mod 8 |
| **ContextVar** | A variable with task/thread-local scope | `request_id = ContextVar(...)` | Course 0 Mod 5 |
| **Coroutine** | An `async` function that can be paused with `await` | `async def fetch():` | Course 0 Mod 4 |
| **Event Loop** | The scheduler that runs coroutines | `asyncio.run(main())` | Course 0 Mod 4 |
| **Concurrency** | Multiple tasks making progress simultaneously | `asyncio.gather(...)` | Course 0 Mod 4 |

---

## Networking

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Client** | Program initiating the request | Browser, `httpx.AsyncClient` | Course 0 Mod 6 |
| **Server** | Program responding to requests | FastAPI, nginx | Course 0 Mod 6 |
| **HTTP** | Hypertext Transfer Protocol — the web's language | `GET /api/v1/models` | Course 0 Mod 6 |
| **Endpoint** | A specific URL where an API lives | `/v1/chat/completions` | Course 0 Mod 6 |
| **Request** | A message from client to server | `POST /chat` + JSON body | Course 0 Mod 6 |
| **Response** | Server's reply | `200 OK` + JSON | Course 0 Mod 6 |
| **Status Code** | Numeric code indicating outcome | `200`, `404`, `500` | Course 0 Mod 6 |
| **JSON** | JavaScript Object Notation — lightweight data format | `{"model": "hermes"}` | Course 0 Mod 7 |
| **Header** | Key-value metadata in HTTP messages | `Authorization: Bearer sk-...` | Course 0 Mod 6 |
| **Latency** | Time between request and response | 200ms round-trip | Course 0 Mod 6 |
| **Timeout** | Max wait time before giving up | `timeout=30.0` | Course 0 Mod 6 |

---

## Mathematics (Engineering Mathematics)

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Scalar** | A single number | `5.0` | Linear Algebra |
| **Vector** | An ordered list of numbers | `[1, 2, 3]` | Linear Algebra |
| **Matrix** | A 2D grid of numbers | `[[1,2],[3,4]]` | Linear Algebra |
| **Dot Product** | Sum of element-wise products | `[1,2]·[3,4] = 11` | Linear Algebra |
| **Eigenvalue** | How much a matrix stretches a vector | `Av = λv` | Linear Algebra |
| **Derivative** | Rate of change at a point | `d/dx x² = 2x` | Calculus |
| **Gradient** | Vector of partial derivatives | `∇L = [∂L/∂w₁, ∂L/∂w₂]` | Calculus |
| **Integral** | Area under a curve | `∫ v(t)dt = s(t)` | Calculus |
| **Probability** | Likelihood of an event (0 to 1) | `P(rain) = 0.3` | Probability |
| **Expected Value** | Probability-weighted average | `E[X] = Σ x·P(x)` | Probability |
| **Normal Distribution** | Bell curve distribution | `X ~ N(μ, σ²)` | Probability |
| **Radian** | Angle unit: 2π = full circle | `π/4 = 45°` | Trigonometry |
| **sin(θ)** | Opposite / hypotenuse | `sin(30°) = 0.5` | Trigonometry |
| **cos(θ)** | Adjacent / hypotenuse | `cos(60°) = 0.5` | Trigonometry |
| **tan(θ)** | sin(θ) / cos(θ) | `tan(45°) = 1` | Trigonometry |

---

## Machine Learning

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Feature** | Input variable for a model | `temperature = 22.5` | ML Fundamentals |
| **Target** | Value the model predicts | `fault = True` | ML Fundamentals |
| **Training** | Adjusting model parameters using data | `model.fit(X, y)` | ML Fundamentals |
| **Loss Function** | Measures how wrong predictions are | `MSE = mean((y-ŷ)²)` | ML / Deep Learning |
| **Gradient Descent** | Optimization by moving against gradient | `w = w - α·∇L` | ML / Calculus |
| **Overfitting** | Memorizing training data, not generalizing | Low train error, high test error | Module 6 |
| **Regularization** | Penalty term to prevent overfitting | Ridge: `L + λ‖w‖²` | Module 3 |
| **Cross-Validation** | Using multiple train/test splits for evaluation | K-Fold CV | Module 6 |

---

## Deep Learning

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Tensor** | N-dimensional array | `torch.tensor([[1,2],[3,4]])` | Module 7 |
| **Activation Function** | Non-linear transformation applied after linear layer | `ReLU(x) = max(0,x)` | Module 9 |
| **Backpropagation** | Chain rule applied to compute gradients | `loss.backward()` | Module 7 |
| **Epoch** | One full pass through the training data | `for epoch in range(100):` | Module 8 |
| **Batch** | Subset of training data processed together | `batch_size=32` | Module 8 |
| **Attention** | Mechanism to weight relevant parts of input | `softmax(QKᵀ/√d)·V` | Module 11 |
| **Transformer** | Architecture using attention, no RNNs | GPT, BERT | Module 11 |
| **Embedding** | Dense vector representation of discrete tokens | `[0.2, -0.5, 0.8, ...]` | Module 11 |

---

## NEAT (NeuroEvolution)

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Genome** | Encoded representation of a neural network | Node + connection genes | NEAT Module 3 |
| **Fitness** | Score measuring solution quality | `F(genome) → 3.95` | NEAT Module 1 |
| **Mutation** | Random change to a genome | Add node, change weight | NEAT Module 5 |
| **Crossover** | Combining two parent genomes | Disjoint/excess gene handling | NEAT Module 5 |
| **Species** | Group of genetically similar genomes | Protects innovation | NEAT Module 4 |
| **Population** | All genomes in one generation | `pop_size = 150` | NEAT Module 4 |
| **Innovation Number** | Unique ID for each new gene | Enables crossover alignment | NEAT Module 4 |

---

## Game AI

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **State** | The current condition of the game | Board position | Game AI |
| **Minimax** | Optimal strategy in zero-sum games | `minimax(state, depth)` | Game AI |
| **Alpha-Beta Pruning** | Minimax with branch pruning | Skips dominated moves | Game AI |
| **MCTS** | Monte Carlo Tree Search | AlphaGo | Game AI |
| **Heuristic** | Rule-of-thumb evaluation function | Piece count advantage | Game AI |
| **Policy** | Mapping from state to action | `π(s) → action` | RL / MCTS |
| **Reward** | Signal indicating quality of an action | `+1` for win, `-1` for loss | RL |

---

## Software Architecture

| Term | Definition | Example | Appears In |
|------|-----------|---------|-----------|
| **Registry** | Mapping names to implementations | `tools = {"add": add_fn}` | Course 0 Mod 8 |
| **Facade** | Simple interface hiding complexity | `agent.run(input)` | Course 0 Mod 8 |
| **Dependency Injection** | Passing deps from outside rather than creating them | `Agent(registry=reg)` | Course 0 Mod 8 |
| **Separation of Concerns** | Each module has one job | `tools.py`, `memory.py` | Module 31 |
| **Composition** | Object containing other objects | `Agent` has-a `ToolRegistry` | Module 13 |
| **Interface** | Agreed-upon contract between components | `Callable[[str], Any]` | Course 0 |
