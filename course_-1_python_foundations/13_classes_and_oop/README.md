# Topic: Classes and Object-Oriented Programming

## What You Will Learn
- The difference between procedural and object-oriented programming paradigms.
- How classes serve as blueprints for instantiating independent objects with state and behavior.
- The mechanics of `self` and how Python passes instance references to methods.
- The difference between instance attributes and shared class attributes (and common traps).
- Special "dunder" methods (`__init__`, `__repr__`, `__str__`, `__eq__`, `__call__`).
- Encapsulation conventions (`_protected`, `__private` name mangling) and `@property`.
- Inheritance, method overriding, `super()`, and polymorphism via duck typing.
- Why composition ("has-a") is preferred over inheritance ("is-a") in modern AI agent design.

## Prerequisites
- Solid grasp of Python data structures (dictionaries, lists, tuples) from Module 06.
- Understanding of functions, parameters, return values, and scopes from Modules 08–09.
- Basic familiarity with importing modules from Module 12.

## The Problem
In procedural programming, you store state in loose dictionaries or variables and write standalone functions that take those dictionaries as arguments. For example:
```python
agent_state = {"name": "Assistant", "memory": [], "tokens": 0}

def add_memory(state, message):
    state["memory"].append(message)

def report(state):
    return f"{state['name']} has {len(state['memory'])} memories."
```
As systems scale, this approach suffers critical flaws:
1. **Loose, Unenforced Structure**: Any function can modify any key in `agent_state`, spell a key wrong (`agent_state["memry"]`), or put invalid data into it.
2. **Scattered Logic**: Functions operating on the state are scattered across multiple files with no unified boundary.
3. **Multi-Instance Complexity**: Managing 50 concurrent agents requires passing 50 different dictionaries into dozens of global functions, resulting in fragile, unwieldy code.

We need a construct that binds state (attributes) and behavior (methods) together into a cohesive, reusable, self-protecting entity. That construct is the **Class**.

## Key Terminology
- **Class**: A user-defined blueprint defining the attributes and methods that instances of that type will possess.
- **Instance (Object)**: A concrete realization of a class created in memory with its own distinct attribute values.
- **`self`**: The explicit reference to the current instance passed automatically as the first parameter to instance methods.
- **`__init__`**: The initializer (constructor) method called immediately after a new instance is allocated.
- **Dunder Methods**: Special methods enclosed by double underscores (e.g. `__str__`, `__repr__`) that define how objects interact with Python operators and built-in functions.
- **Encapsulation**: The bundling of data and the methods that act on that data, restricting direct external access to internal state.
- **Inheritance**: The mechanism where a child class derives attributes and methods from a parent class (`class Child(Parent):`).
- **Polymorphism**: The ability of different classes to respond to the same method interface, allowing interchangeable use.
- **Composition**: Combining simple objects into complex wholes ("has-a" relationship) rather than subclassing ("is-a" relationship).

## Intuition
Consider an architectural blueprint for a modern smart home:
1. **The Blueprint** is the `Class`. It specifies that every house has walls, an address, a thermostat, and doors, as well as actions like `unlock_door()` and `set_temperature()`.
2. **The Actual Houses** on Oak Street, Maple Avenue, and Pine Road are **Instances** (objects). Changing the thermostat in the Maple Avenue house to 72°F does NOT change the temperature in the Pine Road house. Each house has its own private state.
3. **`self`** is the identity of the specific house you are standing inside. When you press the thermostat button, `self.temperature = 72` adjusts *this* house, not your neighbor's.
4. **Composition** is outfitting the house with an air conditioner, a security system, and solar panels. The house is not *a kind of* air conditioner; the house *has* an air conditioner.

## Concept
In Python, everything is an object—including numbers, strings, functions, and modules. When you define a class, you create a new user-defined type.

### The Lifecycle of an Object
1. **Creation**: When you call `agent = Agent("Atlas")`, Python invokes `__new__` to allocate the object in heap memory.
2. **Initialization**: Python calls `__init__(self, "Atlas")`, binding initial attributes to `self`.
3. **Method Dispatch**: When you call `agent.execute()`, Python translates this behind the scenes to `Agent.execute(agent)`.
4. **Destruction & Garbage Collection**: When references to `agent` drop to zero, Python's garbage collector frees the memory (optionally invoking `__del__`).

```
  +--------------------------------------------------------+
  |                      Class: Agent                      |
  |  - class_attribute: model_family = "gpt-4"             |
  |  - methods: __init__(), add_memory(), execute()        |
  +--------------------------------------------------------+
                       /                 \
                      / (instantiate)     \ (instantiate)
                     v                     v
  +---------------------------+   +---------------------------+
  |  Instance A (agent_1)     |   |  Instance B (agent_2)     |
  |  self.name = "Hermes"     |   |  self.name = "Apollo"     |
  |  self.memory = ["msg 1"]  |   |  self.memory = []         |
  +---------------------------+   +---------------------------+
```

## Syntax
```python
class Agent:
    # Class attribute (shared by all instances)
    DEFAULT_TEMPERATURE: float = 0.7

    def __init__(self, name: str, role: str) -> None:
        # Instance attributes (unique to each instance)
        self.name: str = name
        self.role: str = role
        self._history: list[str] = []  # protected attribute convention

    def add_thought(self, thought: str) -> None:
        """Instance method operating on self."""
        self._history.append(thought)

    @property
    def thought_count(self) -> int:
        """Property getter for computed or encapsulated values."""
        return len(self._history)

    def __repr__(self) -> str:
        """Developer-friendly unambiguous string representation."""
        return f"Agent(name={self.name!r}, role={self.role!r})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name} [{self.role}]"
```

## Example
Here is a complete, working OOP implementation modeling an AI Agent with a pluggable Memory and Tool execution engine:

```python
from typing import Callable, Any

class MemoryStore:
    """Encapsulates short-term memory buffer for an agent."""
    def __init__(self, max_items: int = 5) -> None:
        self.max_items = max_items
        self._buffer: list[str] = []

    def save(self, message: str) -> None:
        self._buffer.append(message)
        if len(self._buffer) > self.max_items:
            self._buffer.pop(0)  # Evict oldest memory

    def retrieve_all(self) -> list[str]:
        return list(self._buffer)


class AutonomousAgent:
    """An autonomous agent utilizing composition for tools and memory."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.memory = MemoryStore(max_items=3)  # Composition: "has-a" memory
        self._tools: dict[str, Callable[..., Any]] = {}

    def register_tool(self, name: str, func: Callable[..., Any]) -> None:
        self._tools[name] = func

    def act(self, tool_name: str, *args, **kwargs) -> str:
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' not available.")
        
        # Execute tool
        result = self._tools[tool_name](*args, **kwargs)
        self.memory.save(f"Executed {tool_name} -> {result}")
        return str(result)

    def __repr__(self) -> str:
        return f"AutonomousAgent(name={self.name!r}, tools={list(self._tools.keys())})"


if __name__ == "__main__":
    agent = AutonomousAgent("Atlas")
    agent.register_tool("add", lambda a, b: a + b)
    agent.register_tool("greet", lambda user: f"Hello, {user}!")

    print(agent)
    print("Action 1:", agent.act("add", 10, 25))
    print("Action 2:", agent.act("greet", "Ada"))
    print("Memory Buffer:", agent.memory.retrieve_all())
```

## Line-by-Line Explanation
- `class MemoryStore:`: Declares a class representing a bounded memory buffer.
- `def __init__(self, max_items: int = 5) -> None:`: Constructor accepting configuration; binds `max_items` and initializes `_buffer` on the current instance.
- `self._buffer.pop(0)`: Keeps the buffer within `max_items`, encapsulating memory truncation logic inside the `MemoryStore`.
- `class AutonomousAgent:`: Declares the agent orchestrator class.
- `self.memory = MemoryStore(max_items=3)`: Demonstrates **composition**. The agent holds an instance of `MemoryStore`. If we later swap `MemoryStore` for `SQLiteMemoryStore`, the agent's core reasoning logic remains untouched.
- `self._tools[tool_name] = func`: Stores tool callables in the instance's private dictionary.
- `agent.act(...)`: Looks up the tool, invokes it, saves the interaction to memory, and returns the result.

## What Python Is Doing
1. **Class Creation**: When Python encounters `class Agent:`, it creates a code block namespace, executes the body, and constructs a `type` object named `Agent`.
2. **The `__dict__` attribute**: Every object in Python has an internal dictionary `__dict__` where its attributes live. When you write `self.name = "Atlas"`, Python sets `self.__dict__['name'] = "Atlas"`.
3. **Attribute Lookup Chain (MRO - Method Resolution Order)**:
   - When you access `agent.act()`, Python first checks `agent.__dict__`.
   - If not found, it checks `agent.__class__.__dict__` (`AutonomousAgent`).
   - If not found, it checks parent classes in `AutonomousAgent.__mro__`.
   - If still not found, it calls `__getattr__` or raises `AttributeError`.
4. **Self Binding**: Python methods are descriptor objects. When retrieved via an instance (`agent.act`), Python returns a **bound method** which automatically binds `agent` as the first argument (`self`).

## Common Mistakes
1. **Mutable Class Attributes**:
   ```python
   class Agent:
       tools = []  # DANGER! Shared by EVERY instance!
   ```
   If `agent_1.tools.append("search")` runs, `agent_2.tools` will ALSO contain `"search"`.
   *Fix*: Always initialize mutable collections (lists, dicts, sets) inside `__init__` on `self`: `self.tools = []`.
2. **Forgetting `self` in Method Signatures**:
   ```python
   def speak():  # WRONG
       return "hello"
   ```
   Calling `agent.speak()` crashes with `TypeError: speak() takes 0 positional arguments but 1 was given`.
   *Fix*: Always provide `self` as the first parameter for instance methods.
3. **Deep, Brittle Inheritance Trees**: Creating `Agent` -> `ToolAgent` -> `WebToolAgent` -> `ScrapingWebToolAgent`. Deep inheritance hierarchies become rigid, difficult to refactor, and tightly coupled.
   *Fix*: Favor composition. Give a single `Agent` class a list of `Tool` objects.
4. **Overwriting Dunder Methods incorrectly**: Implementing `__eq__` without checking `isinstance`, leading to crashes when comparing with `None` or unrelated objects.

## Real-World Uses
- **PyTorch & Neural Networks**: `torch.nn.Module` subclasses define network layers, forward passes, and parameter tracking via OOP.
- **Database ORMs (SQLAlchemy, Django)**: Database tables are modeled as Python classes, and table rows are instances.
- **GUI Frameworks (Qt, Tkinter)**: Windows, buttons, and dialogs inherit from base widget classes.
- **Web Servers (FastAPI, Flask)**: Request handlers, dependency injection containers, and routers are structured around classes.

## Connection to AI Agents
Object-Oriented Programming is the foundational architecture of all modern AI Agent systems:
- **Agent State Containers**: An agent must maintain state across multi-turn reasoning steps: conversation history, scratchpad thoughts, tool results, and execution budget. Classes provide the exact boundary required to encapsulate this state safely.
- **Polymorphic Tool Interfaces**: In frameworks like LangChain or AutoGen, all tools adhere to a common interface: `Tool.run(query: str) -> ToolResult`. The agent orchestrator calls `.run()` without needing to know whether the tool is a web searcher, a Python code runner, or a calculator.
- **Memory & Storage Abstraction**: Agents use polymorphic memory classes (`InMemoryStore`, `SQLiteStore`, `ChromaVectorStore`) that all implement `.add(text)` and `.search(query)`.

## Practice
1. Open a Python shell and define a simple class `Counter` with methods `increment()` and `reset()`. Create two instances `c1` and `c2`. Increment `c1` three times and verify that `c2` remains at 0.
2. Add a `__repr__` method to `Counter` so that printing `c1` outputs `<Counter count=3>`.
3. Add a property `@property` called `is_zero` that returns `True` if count is 0, otherwise `False`.
4. Inspect `c1.__dict__` to see how Python stores instance attributes under the hood.

## Challenge
Design an object-oriented `RateLimiter` class that can be attached to an AI Agent's API caller:
- It tracks the number of calls made within a rolling window of seconds (e.g., maximum 5 calls per 10 seconds).
- It provides a method `can_call() -> bool` and `record_call() -> None`.
- If the limit is exceeded, `record_call()` raises a custom `RateLimitExceededError`.
- Test it with a mock agent calling an imaginary LLM.

## Summary
- Classes bundle state (attributes) and behavior (methods) into reusable abstractions.
- `self` explicitly references the individual instance, ensuring state changes affect only that object.
- Mutable attributes must be instantiated inside `__init__`, never as class-level defaults.
- Dunder methods (`__repr__`, `__str__`, `__eq__`, `__len__`) integrate classes smoothly into Python's native operators.
- Modern software design and AI agent engineering strongly favor **composition** over deep inheritance trees.

## What You Should Know Before Moving On
- How to define a class with `__init__` and instance methods using `self`.
- The difference between instance attributes (`self.x`) and class attributes (`Class.x`).
- How to write meaningful `__repr__` and `__str__` dunder methods for debugging.
- How to structure a class using composition to delegate responsibilities to helper objects.
- Why polymorphic interfaces make AI agent tool dispatching clean, extensible, and robust.
