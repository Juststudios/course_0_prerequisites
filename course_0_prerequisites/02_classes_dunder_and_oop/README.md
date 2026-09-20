# Module 02: Classes, Dunder Methods, and OOP Patterns for AI Agents

## 1. Learning Objectives
By the end of this module, you will be able to:
- Leverage Python double-underscore ("dunder") methods (`__repr__`, `__str__`, `__getitem__`, `__len__`, `__iter__`) to make agent data models natively serializable and inspectable.
- Implement synchronous and asynchronous context managers (`__enter__`/`__exit__` and `__aenter__`/`__aexit__`) for leak-free agent resource allocation (database transactions, temp sandboxes, HTTP sessions).
- Define formal interface contracts using Python's Abstract Base Classes (`abc.ABC` and `@abstractmethod`).
- Build polymorphic model providers (e.g., `OpenAIProvider`, `AnthropicProvider`, `MockProvider`) allowing runtime LLM swaps without touching agent orchestration code.
- Apply composition over inheritance to architect modular, testable agent cores.

---

## 2. Why AI Agent Engineers Need This
In real-world agent frameworks, hardcoding an agent to a single LLM vendor or tightly coupling prompt generation to message storage leads to brittle systems. 

Object-Oriented Programming (OOP) in Python provides the bedrock of agent architecture:
1. **Dunder methods** control how complex agent trajectories, tool calls, and message histories serialize into strings for LLM prompts and debug logs.
2. **Context managers** guarantee that expensive database connections, ephemeral docker containers, or mock fixtures are closed cleanly even when an LLM hallucination throws an unexpected error.
3. **Abstract Base Classes (ABCs)** enforce strict interface contracts across model providers and memory stores, ensuring that switching from a cloud provider to a local model (e.g., Ollama or vLLM) requires zero changes to your agent reasoning loop.

---

## 3. Structured Concept Breakdown

### Concept 1: Dunder Methods (Data Model Protocols)
- **TERM**: Dunder Methods
- **DEFINITION**: Special methods reserved by Python surrounded by double underscores (e.g., `__init__`, `__repr__`, `__getitem__`) that hook into language operations.
- **INTUITION**: Standardized electrical sockets in a home. When you plug in an appliance, the electrical system doesn't need to know what brand the appliance is—it just interacts through the standard socket protocol.
- **WHY IT EXISTS**: Without dunder methods, every developer would invent arbitrary method names (`get_item_by_index()`, `calculate_length()`, `to_display_string()`), breaking interoperability with standard Python features like `len(obj)`, `obj[key]`, or `str(obj)`.
- **HOW IT WORKS**: When you call `len(message_history)`, Python translates this internally to `type(message_history).__len__(message_history)`. Implementing `__getitem__` allows an agent message store to be queried like a dictionary or list (`history[0]` or `history["session_123"]`).
- **CODE**:
```python
class MessageStore:
    def __init__(self):
        self._messages = []

    def append(self, role: str, content: str):
        self._messages.append({"role": role, "content": content})

    def __len__(self) -> int:
        return len(self._messages)

    def __getitem__(self, index: int) -> dict:
        return self._messages[index]

    def __repr__(self) -> str:
        return f"MessageStore(count={len(self._messages)}, preview={self._messages[-1] if self._messages else None})"
```

---

### Concept 2: Context Manager
- **TERM**: Context Manager
- **DEFINITION**: An object implementing the runtime context protocol via `__enter__()` and `__exit__()` (or async `__aenter__()` and `__aexit__()`), executed using the `with` (or `async with`) statement.
- **INTUITION**: An airlock door in a spacecraft. Entering the room automatically establishes safe pressure (`__enter__`), and leaving the room automatically re-seals the chamber (`__exit__`), even if an emergency occurs while inside.
- **WHY IT EXISTS**: Autonomous agents perform operations with external side-effects: opening SQLite databases, generating ephemeral sandbox folders for code execution, and holding open network sockets. If an LLM call throws an exception, unclosed resources cause memory leaks, locked databases, and zombie processes. Context managers guarantee cleanup.
- **HOW IT WORKS**: The `with expr as target:` statement evaluates `expr`, invokes `target = expr.__enter__()`, executes the enclosed code block, and finally invokes `expr.__exit__(exc_type, exc_val, exc_tb)`. If an exception was raised, `__exit__` can inspect it and optionally suppress it by returning `True`.
- **CODE**:
```python
import os
import shutil
import tempfile

class EphemeralSandbox:
    """Creates an isolated temporary folder for agent file execution."""
    def __enter__(self) -> str:
        self.temp_dir = tempfile.mkdtemp(prefix="agent_sandbox_")
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Guaranteed cleanup on exit or failure
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        return False  # Do not suppress exceptions
```

---

### Concept 3: Abstract Base Class (ABC)
- **TERM**: Abstract Base Class (ABC)
- **DEFINITION**: A class derived from `abc.ABC` containing one or more methods decorated with `@abc.abstractmethod` that cannot be directly instantiated and mandates implementation by concrete subclasses.
- **INTUITION**: An architectural blueprint for a house. You cannot sleep in a blueprint (you cannot instantiate an ABC), but it guarantees that any actual house built from it will have a front door, a roof, and water pipes.
- **WHY IT EXISTS**: Large agent applications rely on interchangeable services (e.g. Model Providers, Memory Stores, Vector DBs). Without ABCs, a developer might implement `OpenAIClient.chat()` and `AnthropicClient.generate()`, creating an incompatible interface mess that breaks the central agent runner.
- **HOW IT WORKS**: When Python creates a class inheriting from `ABC`, its metaclass checks if any `@abstractmethod` remains un-overridden. If so, calling `Class()` raises `TypeError: Can't instantiate abstract class ... with abstract methods ...`.
- **CODE**:
```python
import abc
from typing import List, Dict, Any

class BaseLLMProvider(abc.ABC):
    """Formal interface contract for all LLM backends in the agent."""

    @abc.abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        """Subclasses MUST implement this method."""
        pass
```

---

### Concept 4: Polymorphism
- **TERM**: Polymorphism
- **DEFINITION**: The ability of different classes to expose the same interface method signature while providing distinct internal implementations.
- **INTUITION**: The universal power plug. A wall socket supplies power identically whether you plug in a laptop, a lamp, or a vacuum cleaner.
- **WHY IT EXISTS**: In unit tests and offline evaluation, you want to run your agent without calling expensive real LLMs or incurring latency. Polymorphism lets you swap `OpenAIProvider` with `MockProvider` seamlessly—the agent runner calls `provider.generate(messages)` without knowing or caring which provider is active.
- **HOW IT WORKS**: Python uses dynamic dispatch (duck typing). When `provider.generate()` is called, Python looks up the `generate` attribute on the runtime instance, invoking the concrete subclass's method.
- **CODE**:
```python
class MockProvider(BaseLLMProvider):
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        return "Deterministic simulated agent response."

class RuleBasedProvider(BaseLLMProvider):
    def generate(self, messages: List[Dict[str, str]], **kwargs: Any) -> str:
        last_msg = messages[-1]["content"].lower()
        if "weather" in last_msg:
            return '{"tool": "get_weather", "city": "London"}'
        return "Acknowledged."
```

---

### Concept 5: Composition over Inheritance
- **TERM**: Composition over Inheritance
- **DEFINITION**: Designing systems by assembling objects of different classes that hold references to one another ("has-a" relationship) rather than building deep class inheritance hierarchies ("is-a" relationship).
- **INTUITION**: A smartphone. Instead of inheriting from a camera, a telephone, and a game console, a smartphone *has* a camera module, *has* a cellular modem, and *has* a GPU chip.
- **WHY IT EXISTS**: Inheritance creates tight coupling. An `Agent` inheriting from `SQLiteDatabase` and `OpenAIClient` is impossible to refactor. With composition, an `Agent` *has* a `memory` and *has* a `provider`, which can be injected and swapped independently.
- **HOW IT WORKS**: The agent's `__init__` takes instances of `BaseLLMProvider`, `BaseMemory`, and `ToolRegistry`, storing them as instance attributes (`self.provider = provider`).
- **CODE**:
```python
class Agent:
    def __init__(self, provider: BaseLLMProvider, memory: MessageStore):
        self.provider = provider
        self.memory = memory

    def step(self, user_prompt: str) -> str:
        self.memory.append("user", user_prompt)
        response = self.provider.generate(list(self.memory._messages))
        self.memory.append("assistant", response)
        return response
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Unhandled Context Leaks in Tool Sandboxes
- **The Bug**: An agent tool writes temporary files into `/tmp/agent/` without using a context manager. If a code execution tool crashes or times out, the files remain on disk.
- **The Consequence**: Disk exhaustion on agent servers after running thousands of autonomous steps, resulting in total server crash.
- **The Fix**: Always manage temp directories using context managers (`with tempfile.TemporaryDirectory() as tmp_dir:`).

### Anti-Pattern 2: God Class Inheritance
- **The Bug**: Creating an `Agent` base class that inherits from `PromptManager`, `DatabaseConnector`, `LLMClient`, and `ToolRunner`.
- **The Consequence**: Massive tight coupling, impossible unit testing, diamond inheritance bugs (`super()` resolution failures), and an inability to mock out individual services.
- **The Fix**: Use Dependency Injection and Composition. Pass dependencies into the agent's constructor.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. Which dunder method is called when an object is printed with `repr(obj)`?
2. What arguments does `__exit__` receive when an exception is raised inside a `with` block?
3. What exception is raised when attempting to instantiate an ABC that still has un-implemented abstract methods?

### Tier 2 (Debugging)
Find the flaw in this context manager:
```python
class DatabaseSession:
    def __enter__(self):
        self.conn = connect_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True  # What is the danger of returning True here?
```
*Hint*: Returning `True` silently swallows ALL exceptions, including syntax errors, assertions, and catastrophic failures!

### Tier 3 (Application)
Write a context manager `TraceSpan(name: str)` that records the start time upon entry, prints the elapsed duration on exit, and records whether the block exited cleanly or with an error.

### Tier 4 (Challenge)
Design an abstract class `BaseMemory(abc.ABC)` with abstract methods `save_message(role, content)` and `get_history(limit)`. Implement two concrete classes: `InMemoryMessageStore` (list-backed) and `FileBackedMessageStore` (JSONL-backed). Demonstrate swapping them inside an agent class without modifying any agent code.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/02_classes_dunder_and_oop/dunder_patterns.py
python3 course_0_prerequisites/02_classes_dunder_and_oop/abstract_providers.py
```
