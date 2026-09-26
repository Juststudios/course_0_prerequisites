# Topic: Basic Software Architecture

Welcome to the architectural threshold of Python development. Up to this point in your programming journey, you have learned the individual building blocks of Python: variables, collections, control flow, functions, object-oriented classes, exceptions, and file I/O. But knowing how to lay individual bricks does not automatically mean you know how to design a skyscraper. 

Software architecture is the art and science of organizing code so that as a project grows from 50 lines to 50,000 lines, it remains clean, easy to understand, testable, and adaptable to change. In this module, you will learn the foundational architectural patterns that professional engineers and AI agent developers use to build maintainable systems.

---

## What You Will Learn

- **Separation of Concerns (SoC)**: Why dividing a program into distinct sections with specific responsibilities prevents chaos.
- **Loose Coupling vs. Tight Coupling**: How to design components that can change independently without breaking the rest of your system.
- **Dependency Injection (DI)**: The technique of providing dependencies from the outside rather than hardcoding them inside classes.
- **The Registry Pattern**: How to build dynamic lookup systems that map names to callable functions or tools—the exact mechanism powering AI agent toolkits.
- **The Facade Pattern**: How to provide a simple, friendly interface over complex internal subsystems.
- **The Adapter Pattern**: How to standardize incompatible external components into a consistent, uniform interface.

---

## Prerequisites

Before diving into this module, you should be comfortable with:
- **Python Functions & Callables**: Defining functions, passing functions as arguments, and using `*args` and `**kwargs` (Module 08).
- **Classes and Object-Oriented Programming**: Creating classes, `__init__` constructors, instance methods, and attributes (Module 13).
- **Type Hints**: Reading and writing basic type annotations such as `dict[str, Any]` and `Callable` (Module 15).
- **Dictionaries**: Adding, retrieving, and iterating over key-value pairs (Module 06).

---

## The Problem

Imagine you are building an AI agent assistant that fetches weather reports, executes math calculations, and saves user notes. 

When beginners write this, they typically put everything inside a single monolithic class:
```python
class MonolithicAgent:
    def __init__(self):
        # Hardcoded database connection
        self.db = sqlite3.connect("production.db")
        # Hardcoded credentials and output sinks
        self.api_key = "secret_key"
        self.log_file = open("agent.log", "a")

    def handle_request(self, command, data):
        # 500 lines of entangled if/elif logic mixing SQL, HTTP, and math!
        if command == "calc":
            ...
        elif command == "weather":
            ...
```

Now consider what happens when:
1. **You want to test the agent**: You cannot run a unit test without accidentally writing to the real production database and hitting a real paid API.
2. **You want to add a new tool**: You have to edit the massive `handle_request` method, risking breaking existing features.
3. **A tool fails**: An error in the weather tool crashes the entire agent because everything is glued together in a single tangled mess.

This is called **spaghetti code** characterized by **tight coupling** and **violation of Single Responsibility**. Basic software architecture solves this problem completely.

---

## Key Terminology

- **Architecture**: The high-level structure of a software system, defining the components, their responsibilities, and how they communicate.
- **Separation of Concerns (SoC)**: A design principle stating that each module or class should address one distinct aspect of the problem domain (e.g., storage vs. presentation vs. business logic).
- **Tight Coupling**: A condition where software components are deeply interdependent. Changing one component inevitably forces changes in others.
- **Loose Coupling**: A condition where components interact through well-defined, minimal interfaces. One component can be swapped or modified without affecting the other.
- **Dependency Injection (DI)**: A pattern where an object receives its dependencies (collaborators) from an external caller, rather than creating them internally.
- **Registry Pattern**: A centralized catalog or directory where objects or functions are registered under unique keys and retrieved on demand.
- **Facade Pattern**: A structural pattern that provides a simplified, higher-level interface to a complex subsystem.
- **Adapter Pattern**: A structural pattern that allows objects with incompatible interfaces to collaborate by wrapping one inside a translating layer.

---

## Intuition

Think of software architecture like the design of a professional kitchen:
- **Tightly coupled kitchen**: The chef personally grows the vegetables out back, butchers the meat in the dining room, cooks the meal, washes the dishes, and delivers the food to the customer's table. If the chef gets sick, the entire restaurant shuts down.
- **Architected kitchen**:
  - The **Pantry (Storage)** holds ingredients.
  - The **Prep Cook (Adapter)** cleans and chops ingredients into standard sizes.
  - The **Head Chef (Core Logic)** cooks using whichever ingredients are handed to them.
  - The **Waiter (Facade)** takes the customer's order and delivers the plate, hiding all kitchen chaos from the diner.
  - The **Recipe Board (Registry)** lists every dish the kitchen knows how to make and maps each dish name to its cooking procedure.

If you want to replace the dishwasher or switch vegetable suppliers, the chef doesn't have to change how they cook. The boundaries protect each part of the system.

---

## Concept

Modern software systems are built from four fundamental architectural tenets:

### 1. Single Responsibility Principle (SRP)
Every class and function should have one, and only one, reason to change. A class that computes math should not also write to an SQLite database. A class that handles user commands should not be responsible for formatting HTTP requests.

### 2. Dependency Inversion & Injection
High-level policy (what your program *does*) should not depend directly on low-level details (which specific database or file format is used). Both should depend on abstractions. Instead of:
```python
# TIGHT COUPLING: Class creates its own dependency
class Service:
    def __init__(self):
        self.db = SQLiteDatabase("data.db")
```
We inject the dependency through the constructor:
```python
# LOOSE COUPLING: Dependency is passed in from outside
class Service:
    def __init__(self, db: DatabaseInterface):
        self.db = db
```
Now, in your automated tests, you can pass an `InMemoryDatabase()`, and in production you can pass a `PostgreSQLDatabase()`, without changing a single line of `Service`!

### 3. The Registry Pattern for Extensibility
Instead of large `if/elif/else` ladders, a Registry maintains a dictionary of name-to-callable mappings:
```python
registry = {}
def register(name):
    def decorator(fn):
        registry[name] = fn
        return fn
    return decorator
```
New capabilities can be added dynamically just by registering a new function.

### 4. The Facade Pattern for Usability
When an application consists of many moving parts (a parser, a registry, an audit logger, and a memory store), external clients should not need to coordinate all of them manually. A `Facade` exposes a simple, elegant method like `agent.chat(prompt)` that coordinates the subsystems internally.

---

## Syntax

### Dependency Injection via Constructors
```python
class Consumer:
    def __init__(self, dependency: DependencyType):
        self._dependency = dependency  # Injected from outside
```

### Simple Registry Class
```python
from typing import Callable, Any

class Registry:
    def __init__(self) -> None:
        self._storage: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._storage[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._storage:
            raise KeyError(f"Item {name!r} not found in registry")
        return self._storage[name]
```

### Facade Interface
```python
class SystemFacade:
    def __init__(self, sub_a: SubsystemA, sub_b: SubsystemB):
        self._a = sub_a
        self._b = sub_b

    def perform_action(self, data: str) -> str:
        # Coordinates internal subsystems cleanly
        cleaned = self._a.clean(data)
        return self._b.process(cleaned)
```

---

## Example

Here is a complete, runnable demonstration contrasting tightly coupled architecture with decoupled, pattern-driven architecture:

```python
from typing import Callable, Any

# 1. Dependency Injection: An abstract storage contract
class InMemoryStorage:
    def __init__(self):
        self._data = {}

    def save(self, key: str, value: str) -> None:
        self._data[key] = value

    def load(self, key: str) -> str:
        return self._data.get(key, "")

# 2. Registry Pattern: Managing callable tools
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, name: str, tool_func: Callable) -> None:
        self._tools[name] = tool_func

    def execute(self, name: str, *args, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name](*args, **kwargs)

# 3. Facade Pattern: Simple agent interface coordinating registry and storage
class SimpleAgentFacade:
    def __init__(self, registry: ToolRegistry, storage: InMemoryStorage):
        self._registry = registry
        self._storage = storage

    def run_and_save(self, tool_name: str, key: str, *args, **kwargs) -> str:
        result = self._registry.execute(tool_name, *args, **kwargs)
        self._storage.save(key, str(result))
        return f"Executed {tool_name} -> {result} (saved to {key})"

# Assembly & Usage
registry = ToolRegistry()
registry.register("add", lambda a, b: a + b)
registry.register("shout", lambda text: text.upper() + "!")

storage = InMemoryStorage()
agent = SimpleAgentFacade(registry, storage)

print(agent.run_and_save("add", "sum_result", a=10, b=25))
print(agent.run_and_save("shout", "greeting", text="hello architecture"))
print("Saved sum:", storage.load("sum_result"))
```

---

## Line-by-Line Explanation

- **Lines 4–12 (`InMemoryStorage`)**: Implements a dedicated storage layer using a standard dictionary. Notice this class knows *nothing* about agents or tools. It only knows how to store and retrieve data.
- **Lines 15–25 (`ToolRegistry`)**: Maintains an internal dictionary `_tools`. The `register` method adds a function to the dictionary, and `execute` retrieves and runs it. If an unknown name is requested, it raises a clean `KeyError`.
- **Lines 28–36 (`SimpleAgentFacade`)**: The Facade class constructor accepts `registry` and `storage` via Dependency Injection. It does *not* create them itself.
- **Lines 34–36 (`run_and_save`)**: Coordinates the registry execution and the storage write in two clean lines, presenting a single cohesive operation to the outside caller.
- **Lines 39–44**: Assembles the application at the entry point (the "composition root"). Here we instantiate the parts and pass them into the facade.
- **Lines 46–48**: The client interacts exclusively with `agent.run_and_save(...)` without needing to manipulate the internal registry dictionary directly.

---

## What Python Is Doing

When you write architecturally decoupled code in Python, several runtime mechanisms come into play:

1. **First-Class Functions**: In Python, functions are objects. You can store a function reference inside a dictionary (`self._tools["add"] = lambda a, b: a + b`), pass it as an argument, and call it later using parentheses `()`. This makes the Registry pattern native and lightweight in Python without requiring cumbersome abstract factory boilerplate.
2. **Object References in Constructors**: When you pass `registry` into `SimpleAgentFacade(registry, storage)`, Python passes the reference by value. Both the composition root and the facade point to the exact same registry object in heap memory.
3. **Encapsulation with Underscores**: By prefixing internal variables with a single underscore (like `self._tools` or `self._storage`), Python conventions signal that these attributes are private implementation details. The Facade method provides the public API, preventing callers from corrupting internal state.

---

## Common Mistakes

### 1. Hardcoding Instantiations Inside Classes (Hidden Dependencies)
```python
# BAD: Impossible to unit test with mock storage
class Agent:
    def __init__(self):
        self.storage = SQLiteDatabase("prod.db")

# GOOD: Injected dependency can be swapped for testing
class Agent:
    def __init__(self, storage):
        self.storage = storage
```

### 2. God Objects (Violating Single Responsibility)
Creating a single `Agent` class that handles HTTP networking, SQLite serialization, prompt parsing, logging, and error recovery in 1,000 lines. Break these down into separate, focused classes.

### 3. Registry Mutation Without Validation
Allowing registration of items that are not callable, leading to cryptic `TypeError: 'str' object is not callable` exceptions later during runtime execution. Always validate `callable(func)` before registering.

### 4. Leaking Abstractions Through the Facade
A facade is supposed to shield the caller from complexity. If the caller still has to configure three internal subsystems before calling the facade, the facade has failed its purpose.

---

## Real-World Uses

- **FastAPI & Flask**: Route decorators (`@app.get("/items")`) are concrete implementations of the Registry pattern, mapping URL endpoints to view functions.
- **Pytest**: Pytest fixtures are a world-class implementation of Dependency Injection, injecting database connections, mock clients, and temporary directories into test functions based on parameter names.
- **Database ORMs (SQLAlchemy, Django ORM)**: Provide Facades over raw SQL dialects, connection pools, transaction managers, and cursors.
- **Plugin Systems**: Operating systems, web browsers, and IDEs (like VS Code) use registries to dynamically load user plugins without altering core engine source code.

---

## Connection to AI Agents

Software architecture is not an academic exercise—it is the foundational skeleton of all modern AI Agent frameworks (such as LangChain, AutoGen, CrewAI, and Semantic Kernel):

1. **Tool Registries**: An AI agent does not have tools hardcoded in `if/elif` statements. Instead, an agent maintains a `ToolRegistry`. When an LLM outputs `{"action": "search", "query": "Python 3.12 release"}`, the agent queries its registry, looks up `registry.get("search")`, and executes the tool.
2. **Pluggable LLM Backends**: Using Dependency Injection, an agent can be configured with an `OpenAIClient`, an `AnthropicClient`, or a local `OllamaClient` without changing the agent's core reasoning loop.
3. **Memory Adapters**: Agents swap memory backends (ephemeral in-memory lists, SQLite databases, or vector databases like ChromaDB/Pinecone) by relying on common storage interfaces.
4. **Agent Facades**: To the end user or frontend API, an agent is just a facade: `agent.chat(user_message) -> agent_reply`. Behind that simple call, dozens of architectural components (memory retrieval, tool execution, safety filters, context compaction) operate in concert.

---

## Practice

1. Write a `MathRegistry` that registers functions for `add`, `subtract`, `multiply`, and `divide`. Add a method `list_tools()` that returns all registered operation names.
2. Create an `Agent` class that accepts a `MathRegistry` via dependency injection and executes requested mathematical operations safely, returning an error message if the tool does not exist.
3. Create a `MockStorage` class and a `FileStorage` class that both implement `save(key, val)` and `get(key)`. Inject both into your agent to observe how the agent behaves identically regardless of the storage medium.

---

## Challenge

Design and implement an **Audited Tool Runner**:
1. Implement a `ToolRegistry` with input validation that checks that registered tools are callable and have docstrings.
2. Implement an `AuditLogger` interface with both an `InMemoryAuditLogger` and a `ConsoleAuditLogger`.
3. Build an `AuditedAgentFacade` that takes the registry and the logger via dependency injection.
4. When `facade.execute(tool_name, **kwargs)` is called, it:
   - Records the timestamp and tool name in the audit logger.
   - Executes the tool and records the result or any exception raised.
   - Returns a structured dictionary containing status, result, and execution metadata.
5. Write a test demonstrating running a calculation tool and inspecting the audit trail.

---

## Summary

- **Architecture creates sustainability**: Good architecture prevents software from collapsing under its own weight as features grow.
- **Single Responsibility**: Give every class one clear, well-bounded purpose.
- **Dependency Injection**: Pass dependencies into constructors to achieve loose coupling and effortless testing.
- **Registries**: Replace brittle `if/elif` blocks with dynamic, extensible lookup tables for callables.
- **Facades**: Shield callers from subsystem complexity by offering clean, intuitive high-level APIs.

---

## What You Should Know Before Moving On

Before advancing to Module 31, verify that you can:
- Explain why hardcoding `sqlite3.connect()` inside a class constructor makes unit testing difficult.
- Implement a basic `Registry` class with `register`, `get`, and error handling for missing keys.
- Explain how Dependency Injection allows swapping an in-memory test database for a production database without modifying the consumer class.
- Describe how an AI agent uses the Tool Registry pattern to dynamically call tools determined by an LLM.
