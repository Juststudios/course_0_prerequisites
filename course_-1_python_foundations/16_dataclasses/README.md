# Topic: Python Dataclasses

## What You Will Learn
- Why dataclasses were introduced in Python 3.7 (PEP 557) to eliminate boilerplate code.
- How `@dataclass` automatically generates `__init__`, `__repr__`, and `__eq__` methods.
- The difference between dataclasses, plain dictionaries, namedtuples, and Pydantic models.
- How to configure field behavior with `field()` and `default_factory` for mutable defaults.
- Creating immutable, hashable records using `frozen=True`.
- Performing post-init validation and computing derived attributes with `__post_init__`.
- Converting dataclasses to and from native Python dicts and JSON for AI agent payloads.

## Prerequisites
- Understanding of classes, attributes, methods, and dunder methods (Module 13).
- Understanding of Python type hints and annotations (Module 15).
- Familiarity with dictionaries and lists (Module 06).

## The Problem
In modern software—especially in AI agent architectures—a massive portion of your code consists of data containers: config objects, message envelopes, tool parameters, and telemetry records.

Writing traditional Python classes for pure data containers requires exhausting, repetitive boilerplate:
```python
class AgentMessage:
    def __init__(self, role, content, timestamp, model, tokens=0):
        self.role = role
        self.content = content
        self.timestamp = timestamp
        self.model = model
        self.tokens = tokens

    def __repr__(self):
        return f"AgentMessage(role={self.role!r}, content={self.content!r}, ...)"

    def __eq__(self, other):
        if not isinstance(other, AgentMessage):
            return False
        return (self.role, self.content, self.timestamp) == (other.role, other.content, other.timestamp)
```
If you add one new field, you have to modify `__init__`, `self.field = field`, `__repr__`, and `__eq__`.

Using a plain dictionary (`{"role": "user", "content": "..."}`) avoids the class boilerplate, but introduces severe flaws:
1. No IDE autocompletion (`msg["contnet"]` silently fails at runtime).
2. No type hints or static contract checking.
3. No object identity or custom methods.

We need the clean ergonomics of typed classes without the tedious ceremony of writing boilerplate methods. That solution is the **Dataclass**.

## Key Terminology
- **`@dataclass`**: A class decorator from the standard library `dataclasses` module that inspects type annotations and synthesizes boilerplate methods.
- **Synthesized Methods**: Methods generated automatically by Python at class definition time (such as `__init__`, `__repr__`, and `__eq__`).
- **`field()`**: A utility function allowing fine-grained control over individual field attributes (default factories, visibility in `__repr__`, inclusion in comparisons).
- **`default_factory`**: A callable (such as `list`, `dict`, or a custom function) used to generate a fresh default value for mutable fields per instance.
- **`frozen=True`**: A dataclass setting making instances immutable (read-only) and hashable.
- **`__post_init__`**: A special hook method called automatically immediately after the synthesized `__init__` finishes.
- **`asdict()`**: A standard function that recursively converts a dataclass instance into a native Python dictionary.

## Intuition
Imagine ordering custom shipping containers for a logistics fleet:
1. **The Traditional Class** is like hiring a master carpenter to hand-carve every single shipping container from raw timber. For every container, they must hand-chisel the door hinges (`__init__`), paint the identification logo (`__repr__`), and weigh it on a scale (`__eq__`).
2. **The Plain Dictionary** is a loose cardboard box with handwritten marker text. It is fast to fold, but easily ripped, mislabeled, and impossible to standardize.
3. **The Dataclass** is a modern stamped steel manufacturing mold. You specify the dimensions and features:
   - Length: 40 feet
   - Insulated: True
   - Serial Number: String
   The factory stamping machine automatically cuts the steel, rivets the hinges, applies the barcode, and calibrates the scale instantaneously.

## Concept
When Python decorates a class with `@dataclass`, it performs runtime reflection on the class's `__annotations__` dictionary:
1. It reads every annotated field in the order declared.
2. It constructs a dynamic Python function string for `__init__` accepting those fields as parameters.
3. It compiles and attaches `__init__`, `__repr__`, and `__eq__` to the class.
4. If `order=True`, it also synthesizes `__lt__`, `__le__`, `__gt__`, and `__ge__`.

```
  Annotated Class Definition:
  @dataclass
  class Config:
      model: str
      timeout: float = 30.0
              |
              v (Dataclass decorator inspects annotations)
  Synthesized Methods Attached to Class:
  - def __init__(self, model: str, timeout: float = 30.0): ...
  - def __repr__(self): return f"Config(model={self.model!r}, ...)"
  - def __eq__(self, other): return (self.model, self.timeout) == ...
```

## Syntax
```python
from dataclasses import dataclass, field, asdict
from typing import Optional

# 1. Basic dataclass
@dataclass
class Point:
    x: float
    y: float

# 2. Advanced configuration with mutable defaults & secrets
@dataclass(frozen=True)
class AgentConfig:
    agent_name: str
    temperature: float = 0.7
    # Mutable collections MUST use default_factory
    tool_whitelist: list[str] = field(default_factory=list)
    # Mask secrets from logs and repr
    api_key: Optional[str] = field(default=None, repr=False)

# 3. Post-init validation hook
@dataclass
class BoundedScore:
    value: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 100.0):
            raise ValueError(f"Score {self.value} outside [0.0, 100.0]!")
```

## Example
Here is a complete, working script illustrating dataclasses modeling an AI Agent's execution step and configuration:

```python
from dataclasses import dataclass, field, asdict
import time
from typing import Any, Optional

@dataclass
class AgentThought:
    step_id: int
    thought: str
    tool_call: Optional[str] = None
    observation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def is_actionable(self) -> bool:
        """Dataclasses can have regular methods just like standard classes!"""
        return self.tool_call is not None

@dataclass(frozen=True)
class AgentProfile:
    name: str
    model: str
    role_description: str
    temperature: float = 0.5
    tags: tuple[str, ...] = field(default_factory=tuple)

if __name__ == "__main__":
    profile = AgentProfile(
        name="Hermes-ReAct",
        model="claude-3-5-sonnet",
        role_description="Autonomous coding assistant",
        tags=("coding", "testing"),
    )

    thought1 = AgentThought(
        step_id=1,
        thought="User requested mathematical verification.",
        tool_call="calculator(12 * 8)",
    )

    print("Profile (Frozen/Immutable):", profile)
    print("Thought 1:", thought1)
    print("Is thought 1 actionable?", thought1.is_actionable())

    # Serialization to standard dictionary
    thought_dict = asdict(thought1)
    print("\nSerialized asdict():", thought_dict)
```

## Line-by-Line Explanation
- `@dataclass`: Instructs Python to inspect the type hints in `AgentThought` and synthesize standard class boilerplate.
- `step_id: int`: Declares a mandatory field. Because it has no default value, it must precede any fields with default values.
- `tool_call: Optional[str] = None`: Declares an optional field with a default value of `None`.
- `timestamp: float = field(default_factory=time.time)`: Calls `time.time()` anew each time an instance is created, ensuring every thought receives its own distinct timestamp rather than sharing the time when the class was first imported!
- `@dataclass(frozen=True)`: Freezes the `AgentProfile` class. Any attempt to write `profile.temperature = 0.9` will raise a `FrozenInstanceError`.
- `thought_dict = asdict(thought1)`: Recursively converts the dataclass instance and any nested dataclasses into a standard Python dictionary.

## What Python Is Doing
1. **Dynamic Code Compilation**: Under the hood, `@dataclass` uses Python's `compile()` and `exec()` to generate pure Python bytecode for `__init__`, `__repr__`, and `__eq__`. The generated methods are identical in speed and behavior to hand-written methods.
2. **`__match_args__` Synthesis**: In Python 3.10+, `@dataclass` automatically generates `__match_args__ = ('step_id', 'thought', ...)`, enabling native structural pattern matching (`match thought: case AgentThought(step_id=1): ...`).
3. **Descriptor Generation for Frozen Classes**: When `frozen=True` is enabled, Python overrides `__setattr__` and `__delattr__` on the class to raise `FrozenInstanceError` whenever attribute mutation is attempted.

## Common Mistakes
1. **Using Mutable Default Arguments Directly**:
   ```python
   @dataclass
   class Agent:
       history: list[str] = []  # ValueError: mutable default <class 'list'> is not allowed!
   ```
   Python protects you from the shared mutable trap by raising an explicit `ValueError`.
   *Fix*: Always use `field(default_factory=list)` or `field(default_factory=dict)`.
2. **Field Ordering Violations**:
   ```python
   @dataclass
   class Config:
       timeout: float = 30.0    # Field with default
       api_key: str             # Non-default field! SyntaxError in generated __init__
   ```
   *Fix*: All non-default fields must come before fields with default values.
3. **Assuming Dataclasses Validate Types at Runtime**:
   Writing `p = Point(x="hello", y=[1, 2])` will NOT crash at runtime. Dataclasses use type hints for code generation, not runtime type validation. If strict runtime type validation is required, perform checks inside `__post_init__` or use Pydantic.
4. **Mutating Frozen Dataclasses**:
   Attempting to modify fields on a `frozen=True` instance.
   *Fix*: Use `dataclasses.replace(instance, field=new_value)` to generate a new modified instance immutably.

## Real-World Uses
- **API Payloads & DTOs (Data Transfer Objects)**: Structuring responses from REST APIs, database queries, and microservice RPCs.
- **Application Configuration**: Loading `.env` or YAML configurations into strongly typed, autocompleting configuration objects.
- **Machine Learning Hyperparameters**: Storing experiment settings (batch size, learning rate, optimizer parameters, model architecture).

## Connection to AI Agents
Dataclasses are the standard building blocks for AI Agent architectures:
- **Conversation State & Messages**: Modern LLM libraries structure messages as dataclasses (`ChatMessage(role='user', content='...', metadata={})`), guaranteeing consistent serialization across agent pipelines.
- **Tool Call Requests and Responses**: When an agent executes a tool, the invocation parameters and the return data are wrapped in dataclasses (`ToolCall(name='search', arguments={})`), preventing loose unstructured dictionary errors.
- **Agent Configuration & Telemetry**: Dataclasses hold hyperparameter settings and telemetry logs cleanly across distributed agent nodes.

## Practice
1. Create a dataclass `Coordinates` with `lat: float` and `lon: float`. Verify that comparing two instances with identical numbers evaluates to `True` using `==`.
2. Create an `AgentCredentials` dataclass with `username: str` and `api_secret: str`. Configure `api_secret` with `repr=False` and confirm that printing the credentials does not display the secret.
3. Test using `dataclasses.asdict()` on a nested dataclass to observe automatic recursive dictionary serialization.

## Challenge
Design a `ValidatedAgentConfig` dataclass:
- Fields: `agent_id: str`, `max_steps: int = 20`, `temperature: float = 0.7`, `tools: list[str] = field(default_factory=list)`.
- Use `__post_init__` to enforce domain rules:
  - `agent_id` must not be empty.
  - `max_steps` must be strictly positive ($> 0$).
  - `temperature` must be between 0.0 and 2.0 inclusive.
- If any validation fails, raise an informative `ValueError`.
- Test both valid instantiation and each failure case.

## Summary
- `@dataclass` automates the creation of standard boilerplate methods (`__init__`, `__repr__`, `__eq__`).
- Mutable defaults must use `field(default_factory=...)` to avoid shared instance contamination.
- `frozen=True` produces immutable, hashable instances suitable for dictionary keys.
- `__post_init__` provides a clean hook for runtime validation and derived field computation.
- Dataclasses deliver the perfect balance of developer ergonomics, type hints, and performance for AI agent state containers.

## What You Should Know Before Moving On
- How to define a dataclass with typed fields and default values.
- Why mutable defaults require `field(default_factory=...)`.
- How to implement `__post_init__` for data validation.
- How to create immutable data structures with `frozen=True`.
- How to convert dataclasses to native dictionaries using `asdict()`.
