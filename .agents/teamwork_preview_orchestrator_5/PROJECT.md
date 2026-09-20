# Project: Educational Curriculum Expansion (Course 0, Engineering Math Bridges, NEAT Redesign)

## Architecture
- **Curriculum Architecture**:
  - `course_0_prerequisites/`: 15 progressive modules bridging basic Python to AI agent engineering + `mini_agent/` capstone project.
  - `engineering-mathematics/`: Classical engineering math enhanced with AI/ML bridges in Linear Algebra, Calculus, and Probability, plus full package structural integrity (`ml_bridge/`, `reference/`, `assessments/`).
  - `neat/`: Pure-Python zero-dependency `neat_engine/`, 6 progressive modules, Matplotlib visualizers, Project 1 (XOR evolution), Project 2 (Cart-Pole dynamical balancing).
  - `tests/e2e/`: Comprehensive opaque-box and multi-tier verification test suites.
- **Pedagogical Format**: Every instructional markdown file strictly adheres to:
  `TERM -> DEFINITION -> INTUITION -> WHY IT EXISTS -> HOW IT WORKS -> CODE`.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | C0-M01 Callables & Functional Python | Callables, closures, `@tool` decorator, introspection | M1 | survey_c0 | IMPLEMENTED |
| 2 | C0-M02 Classes, Dunder & OOP | `__repr__`, context managers, ABCs, polymorphic providers | M1 | survey_c0 | IMPLEMENTED |
| 3 | C0-M03 Type Hints & Pydantic | Pydantic v2 models, field constraints, schema generation | M1 | survey_c0 | IMPLEMENTED |
| 4 | C0-M04 Async/Await & Event Loops | Coroutines, `asyncio.gather`, semaphores, timeout protection | M1 | survey_c0 | IMPLEMENTED |
| 5 | C0-M05 ContextVars & Scoped State | `ContextVar`, task-local storage, tenant/trace isolation | M1 | survey_c0 | IMPLEMENTED |
| 6 | C0-M06 HTTP & REST APIs | Async HTTP client, headers, connection pooling, retries/backoff | M1 | survey_c0 | IMPLEMENTED |
| 7 | C0-M07 JSON & Schema Validation | JSON repair heuristics, code fence stripping, validation | M1 | survey_c0 | IMPLEMENTED |
| 8 | C0-M08 Config Management | Env vars, `.env`, `pydantic-settings`, `SecretStr` masking | M1 | survey_c0 | IMPLEMENTED |
| 9 | C0-M09 Subprocesses & Sandboxing | Safe CLI exec, timeouts, stdout/stderr capture, path safety | M1 | survey_c0 | IMPLEMENTED |
| 10 | C0-M10 SQLite & Agent Memory | ACID transactions, `:memory:`, WAL mode, message store schema | M1 | survey_c0 | IMPLEMENTED |
| 11 | C0-M11 Architecture Patterns | Pipeline pattern, FSM agent states, Dependency Injection | M1 | survey_c0 | IMPLEMENTED |
| 12 | C0-M12 Prompt Templating | Prompt templates, XML delimiters, few-shot, structured outputs | M1 | survey_c0 | IMPLEMENTED |
| 13 | C0-M13 Logging & Observability | Structured JSON logging, trace/span IDs, token tracking | M1 | survey_c0 | IMPLEMENTED |
| 14 | C0-M14 Streaming & SSE | Async generators, SSE protocols, token streaming, delta parsing | M1 | survey_c0 | IMPLEMENTED |
| 15 | C0-M15 Math Bridges for Agents | Vector embeddings, cosine similarity, loss gradients, softmax | M1 | survey_c0 | IMPLEMENTED |
| 16 | C0-MiniAgent Skeleton Project | Async runtime + SQLite memory + Tool registry + ReAct engine | M1 | survey_c0 | IMPLEMENTED |
| 17 | C0-Exercises & Solutions | 4-tier exercises and reference solutions for Course 0 | M1 | survey_c0 | IMPLEMENTED |
| 18 | Math-Structure Package Remedy | Root README, `ml_bridge/`, `reference/` (4 cheatsheets), `assessments/`, fix capstone link | M2 | survey_math | VERIFIED |
| 19 | Math-LA AI/ML Bridge | High-D embeddings, orthogonal projection, SVD/LoRA, Attention math | M2 | survey_math | VERIFIED |
| 20 | Math-Calc AI/ML Bridge | Multivariable gradients, Jacobians, Hessians, backprop, Adam | M2 | survey_math | VERIFIED |
| 21 | Math-Prob AI/ML Bridge | Continuous Bayes, Entropy/KL, uncertainty, agent sampling (Temp/Top-p) | M2 | survey_math | VERIFIED |
| 22 | Math-Runnable Bridge Scripts | Python/NumPy and MATLAB scripts for LA, Calc, and Prob bridges | M2 | survey_math | VERIFIED |
| 23 | NEAT-Engine Core | Pure-Python `gene.py`, `genome.py`, `innovation.py`, `species.py`, `population.py`, `network.py` | M3 | survey_neat | IMPLEMENTED |
| 24 | NEAT-Curriculum Modules 1-6 | 6 progressive modules from EC basics to phenotype activation | M3 | survey_neat | IMPLEMENTED |
| 25 | NEAT-Visualizations | Pure Matplotlib `plot_fitness`, `plot_species`, `plot_network` | M3 | survey_neat | IMPLEMENTED |
| 26 | NEAT-Project 1 (XOR) | Self-contained XOR trainer evolving solving network + verification | M3 | survey_neat | IMPLEMENTED |
| 27 | NEAT-Project 2 (Cart-Pole) | Pure-Python cart-pole dynamical simulator + evolved controller | M3 | survey_neat | IMPLEMENTED |
| 28 | NEAT-Exercises & Solutions | 4-tier exercises and reference solutions for NEAT | M3 | survey_neat | IMPLEMENTED |
| 29 | E2E Testing Suite | Comprehensive multi-tier test suite validating Course 0, Math, and NEAT | M4 | E2E track | IMPLEMENTED |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Course 0 Prerequisites | 15 modules, ~30 runnable scripts, `mini_agent`, exercises/solutions | none | IN_PROGRESS (verifying) |
| M2 | Engineering Mathematics AI Bridges | Structural package fixes, 3 AI bridges, runnable scripts, cheatsheets | none | DONE (157/157 checks passed, 45/45 pytest) |
| M3 | NEAT Curriculum Redesign | `neat_engine/`, 6 modules, XOR project, Cart-Pole project, visualizers | none | IN_PROGRESS (verifying) |
| M4 | E2E Testing Track | Independent requirement-driven test suite, publishes TEST_READY.md | none (parallel) | DONE (TEST_READY.md published) |
| M5 | Final E2E Pass & Verification | 100% test pass, Reviewer approval, Challenger check, Forensic audit | M1, M2, M3, M4 | PLANNED |

## Interface Contracts
### Course 0 `mini_agent` Public Interface
- `MiniAgent(config: AgentConfig, memory: SQLiteMemory, tools: ToolRegistry, engine: DeterministicReActEngine)`
- `async run(prompt: str, session_id: str = "default") -> AgentResponse`
- CLI Entrypoint: `python3 -m course_0_prerequisites.mini_agent.main`

### NEAT Engine Public Interface
- `neat_engine.Population(config: NEATConfig)`
- `population.run(fitness_func, max_generations: int, fitness_threshold: float) -> Tuple[Genome, Dict]`
- `FeedForwardNetwork.create(genome: Genome) -> FeedForwardNetwork`
- `FeedForwardNetwork.activate(inputs: List[float]) -> List[float]`

### Engineering Mathematics Validation
- `python3 scripts/verify_package.py` -> 157/157 passed, 0 errors, status SUCCESS.
- All bridge scripts runnable standalone with NumPy without MATLAB dependency.

## Code Layout
- `course_0_prerequisites/`: Modules `01_callables_and_functional_python` through `15_math_bridges`, `mini_agent/`, `exercises/`, `solutions/`
- `engineering-mathematics/`: `linear_algebra/`, `calculus/`, `probability/`, `ml_bridge/`, `reference/`, `assessments/`, `capstone/`
- `neat/`: `neat_engine/`, `01_evolutionary_computation` through `06_phenotype_network_activation`, `visualizations/`, `projects/01_xor/`, `projects/02_cartpole/`, `exercises/`, `solutions/`, `tests/`
- `tests/e2e/`: E2E test suites for Course 0, Engineering Math, and NEAT.
