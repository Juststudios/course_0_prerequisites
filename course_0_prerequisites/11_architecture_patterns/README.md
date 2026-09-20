# Module 11: Architecture Patterns: Pipelines, State Machines, and Dependency Injection

## 1. Learning Objectives
By the end of this module, you will be able to:
- Structure multi-step agent execution workflows using the Pipeline / Chain of Responsibility pattern.
- Model autonomous agent lifecycles as a deterministic Finite State Machine (FSM) with explicit states (`IDLE`, `PLANNING`, `EXECUTING_TOOL`, `EVALUATING`, `ERROR`, `FINISHED`).
- Implement state transition guards and step counters to definitively prevent infinite reasoning loops.
- Apply Dependency Injection (DI) and Inversion of Control to decouple agent orchestration from specific model providers, tools, and databases.
- Write hermetic, easily mockable unit tests for complex agent state transitions.

---

## 2. Why AI Agent Engineers Need This
Early prototypes of AI agents are frequently implemented as unstructured `while True:` loops. As complexity grows (adding tool error recovery, human-in-the-loop approvals, branching logic, and rate limiting), naive loops degenerate into unmaintainable spaghetti code:
1. **Infinite Loops**: An agent fails to progress on a task and loops 100 times calling the same failing tool, racking up massive API bills.
2. **Untestable State**: When an agent instantiates its own database and model clients inside methods, testing specific error scenarios without hitting live APIs becomes impossible.
3. **Fragile Orchestration**: Modifying the prompt construction step breaks the action execution step because components are tightly coupled.

Industrial-grade agent frameworks (like LangGraph, AutoGen, and Temporal) model agents as **State Machines** and **Pipelines** powered by **Dependency Injection**.

---

## 3. Structured Concept Breakdown

### Concept 1: Pipeline Pattern (Chain of Responsibility)
- **TERM**: Pipeline Pattern
- **DEFINITION**: A design pattern where data flows sequentially through a chain of discrete, decoupled processing stages, where the output of stage $N$ serves as the input to stage $N+1$.
- **INTUITION**: An automotive assembly line. Chassis $\rightarrow$ Engine installation $\rightarrow$ Wiring $\rightarrow$ Painting $\rightarrow$ Inspection. Each technician performs one focused task and passes the car to the next station.
- **WHY IT EXISTS**: Separates concerns. Input sanitization, prompt compilation, LLM inference, JSON parsing, and tool dispatch should not be entangled in one giant function.
- **HOW IT WORKS**: Each pipeline stage implements a common interface (`def process(self, context: Context) -> Context:`). The pipeline runner loops through the stages in order, passing the accumulated context.
- **CODE**:
```python
class PipelineStage:
    def process(self, data: dict) -> dict:
        raise NotImplementedError

class SanitizerStage(PipelineStage):
    def process(self, data: dict) -> dict:
        data["query"] = data["query"].strip()
        return data

class Pipeline:
    def __init__(self, stages: list[PipelineStage]):
        self.stages = stages

    def execute(self, initial_data: dict) -> dict:
        ctx = initial_data
        for stage in self.stages:
            ctx = stage.process(ctx)
        return ctx
```

---

### Concept 2: Finite State Machine (FSM)
- **TERM**: Finite State Machine (FSM)
- **DEFINITION**: A mathematical model of computation consisting of a finite set of discrete states, a set of inputs/events, and transition functions that map current states to next states.
- **INTUITION**: A traffic light. It can only be in one of three states: RED, YELLOW, or GREEN. It cannot be RED and GREEN simultaneously. Transitions occur in an exact, predictable sequence according to timer events.
- **WHY IT EXISTS**: Agents operate in distinct phases: reading user input, planning, executing a tool, evaluating tool output, or waiting for human approval. An FSM makes legal and illegal transitions explicit, preventing impossible states (e.g. executing a tool before planning).
- **HOW IT WORKS**: The agent tracks `self.state = AgentState.IDLE`. When an event occurs (e.g. `user_prompt_received`), the state updates to `AgentState.PLANNING`. Attempting a transition not in the allowed transition table raises `IllegalStateTransitionError`.
- **CODE**:
```python
from enum import Enum, auto

class AgentState(Enum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    FINISHED = auto()
    ERROR = auto()

class SimpleFSM:
    ALLOWED_TRANSITIONS = {
        AgentState.IDLE: {AgentState.PLANNING},
        AgentState.PLANNING: {AgentState.EXECUTING, AgentState.FINISHED, AgentState.ERROR},
        AgentState.EXECUTING: {AgentState.PLANNING, AgentState.ERROR},
    }
```

---

### Concept 3: State Transition Guards & Loop Cutoffs
- **TERM**: Transition Guard
- **DEFINITION**: A boolean condition that must evaluate to `True` before a state transition is permitted, preventing invalid transitions or runaway iteration counts.
- **INTUITION**: A security checkpoint before boarding an airplane. Having a ticket is necessary, but the guard also checks that your passport is valid and your luggage meets weight limits.
- **WHY IT EXISTS**: Agents can enter cyclical reasoning loops (e.g. Tool A fails $\rightarrow$ retry Tool A $\rightarrow$ fail $\rightarrow$ repeat). A step counter guard enforces `current_steps < max_steps`, transitioning the agent to `AgentState.ERROR` or `AgentState.FINISHED` when exceeded.
- **HOW IT WORKS**: Inside `transition_to(next_state)`, the machine evaluates guard predicates:
  ```python
  if next_state == AgentState.EXECUTING and self.step_count >= self.max_steps:
      return self.transition_to(AgentState.ERROR, reason="Max steps exceeded")
  ```
- **CODE**:
```python
def check_step_guard(current_steps: int, max_steps: int) -> bool:
    if current_steps >= max_steps:
        raise RuntimeError(f"Loop guard triggered: exceeded {max_steps} steps.")
    return True
```

---

### Concept 4: Dependency Injection (DI) & Inversion of Control
- **TERM**: Dependency Injection (DI)
- **DEFINITION**: A software engineering pattern where an object receives its collaborating dependencies (database, tool registry, LLM provider) from an external caller rather than instantiating them internally.
- **INTUITION**: A race car driver. The driver does not forge the engine or refine the gasoline themselves; the pit crew injects the prepared car and fuel, allowing the driver to focus exclusively on driving.
- **WHY IT EXISTS**: If an `Agent` runs `self.db = sqlite3.connect("prod.db")` inside `__init__`, you cannot run unit tests without modifying production data. With DI, you inject `SQLiteMemory(":memory:")` for tests and `SQLiteMemory("prod.db")` in production.
- **HOW IT WORKS**: All dependencies are declared as constructor parameters, typed using abstract interfaces (Module 02).
- **CODE**:
```python
class AutonomousAgent:
    def __init__(self, provider: BaseLLMProvider, memory: BaseMemory, tools: ToolRegistry):
        # Injected dependencies
        self.provider = provider
        self.memory = memory
        self.tools = tools
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Unbounded "While True" ReAct Loops
- **The Bug**: `while True: action = get_action(); if action == "done": break`.
- **The Consequence**: If the LLM enters an infinite hallucination loop or tool returns a persistent error, the loop runs forever, draining compute resources and API balances.
- **The Fix**: Model the loop with an explicit FSM enforcing `step_count <= max_steps`.

### Anti-Pattern 2: Hardcoding Global Singletons
- **The Bug**: Tools accessing a global `GLOBAL_DB_CONNECTION` directly.
- **The Consequence**: Tests cannot run in parallel; tests pollute each other's state; impossible to configure different databases for different tenants.
- **The Fix**: Pass the database instance into tools or registries via Dependency Injection.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. In a Finite State Machine, what is a "transition guard"?
2. Why does Dependency Injection make unit testing easier?
3. What design pattern chains sequential stages where each stage's output feeds the next?

### Tier 2 (Debugging)
Find the flaw in this agent loop:
```python
state = "PLANNING"
while state != "DONE":
    if state == "PLANNING":
        action = plan()
        state = "EXECUTING"
    elif state == "EXECUTING":
        res = execute(action)
        state = "PLANNING"
```
*Hint*: There is no step limit or error state! If `plan()` never returns `"done"`, the loop never terminates.

### Tier 3 (Application)
Write a 3-stage `PromptPipeline`:
1. `VariableInjectionStage`: replaces placeholders like `{query}`.
2. `LengthCheckStage`: asserts total characters $\le 4000$.
3. `XMLDelimiterStage`: wraps the prompt in `<system>` and `<user>` tags.

### Tier 4 (Challenge)
Build a complete `AgentStateMachine` with:
- States: `IDLE`, `PLANNING`, `EXECUTING`, `EVALUATING`, `FINISHED`, `ERROR`.
- Guards on maximum iterations and illegal state transitions.
- A trace history of all state transitions and timestamps.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/11_architecture_patterns/state_machine.py
python3 course_0_prerequisites/11_architecture_patterns/dependency_injection.py
```
