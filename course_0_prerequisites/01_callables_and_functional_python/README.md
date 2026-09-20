# Module 01: Callables and Functional Python for AI Agents

## 1. Learning Objectives
By the end of this module, you will be able to:
- Understand and identify all types of Python callables (functions, lambdas, classes with `__call__`).
- Construct higher-order functions and closures to maintain isolated, parameterized agent tool states.
- Author robust decorator functions utilizing `@functools.wraps` to instrument tool execution without mutating original function signatures.
- Perform runtime signature introspection using Python's `inspect` module to dynamically extract parameters, annotations, and docstrings for LLM tool calling schemas.
- Implement a centralized tool registry capable of mapping string tool names emitted by an LLM to their underlying executable callables.

---

## 2. Why AI Agent Engineers Need This
In modern autonomous agent architectures (e.g., OpenAI Function Calling, Anthropic Tool Use, LangChain, AutoGen, and Hermes-style systems), the LLM does not execute code directly. Instead, the model outputs structured text containing the name of a tool and a dictionary of arguments.

The agent runtime is responsible for:
1. **Introspecting** Python functions at startup to generate the JSON schemas sent to the LLM.
2. **Looking up** the appropriate callable when the LLM requests an action.
3. **Wrapping** tool calls with execution hooks, rate limiters, error boundaries, and telemetry.

Without mastery of callables, decorators, and introspection, agent developers rely on rigid, hardcoded dispatch switches (`if tool_name == "search": ...`) that are fragile, difficult to test, and impossible to scale dynamically.

---

## 3. Structured Concept Breakdown

### Concept 1: Callable
- **TERM**: Callable
- **DEFINITION**: Any object in Python that can be invoked using parentheses `()` and accepts optional arguments, returning an object or `None`.
- **INTUITION**: A doorbell button. Regardless of whether the doorbell is a simple mechanical chime (a function) or a digital intercom system with internal memory (a callable class instance), pressing `()` triggers an action.
- **WHY IT EXISTS**: In dynamic systems, code often needs to defer execution. Passing around executable logic as first-class objects allows runtimes to treat actions as data. Without callables, you would have to pass string names and eval them, introducing massive security and maintenance issues.
- **HOW IT WORKS**: When Python encounters `obj(*args, **kwargs)`, it checks if `callable(obj)` is True. For regular functions, it invokes their code object. For class instances, Python checks for the presence of the special method `__call__`. If defined, `obj(args)` translates directly to `type(obj).__call__(obj, args)`.
- **CODE**:
```python
# A callable class holding internal state (e.g., query counter)
class SearchTool:
    def __init__(self, index_name: str):
        self.index_name = index_name
        self.call_count = 0

    def __call__(self, query: str) -> str:
        self.call_count += 1
        return f"Results from {self.index_name} for '{query}' (Call #{self.call_count})"

# Instantiation and invocation
search = SearchTool(index_name="kb_articles")
print(callable(search))  # True
print(search("python async"))  # Results from kb_articles for 'python async' (Call #1)
```

---

### Concept 2: Higher-Order Function
- **TERM**: Higher-Order Function (HOF)
- **DEFINITION**: A function that accepts one or more functions as arguments, returns a function as its result, or both.
- **INTUITION**: An assembly line supervisor who takes a worker (a function), provides them with protective gear and instructions, and outputs an upgraded worker ready for specialized tasks.
- **WHY IT EXISTS**: Agents frequently require middleware patterns: adding retries, logging, execution timeouts, or input validation to tools. Without higher-order functions, you would have to duplicate logging and error-handling code inside every single tool implementation.
- **HOW IT WORKS**: In Python, functions are first-class objects residing in memory with a type of `function`. They can be assigned to variables, stored in dictionaries, passed into parameter lists, and returned from other functions just like numbers or strings.
- **CODE**:
```python
import time
from typing import Callable, Any

def with_retry(max_retries: int = 3) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Higher-order function that equips any tool callable with retry logic."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_err = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(0.01 * attempt)
            raise RuntimeError(f"Tool failed after {max_retries} attempts: {last_err}")
        return wrapper
    return decorator
```

---

### Concept 3: Closure
- **TERM**: Closure
- **DEFINITION**: A function object that retains bindings to variables in its enclosing lexical scope even after that enclosing scope has finished executing.
- **INTUITION**: A backpack carried by a traveling hiker. Even when the hiker leaves their hometown (the outer function finishes), they carry the items packed in their backpack (enclosed variables) wherever they go.
- **WHY IT EXISTS**: Agents often create specialized tool instances on the fly—for example, binding a specific user's API key, session ID, or sandboxed directory path to a tool without making that state global or exposing it to the LLM.
- **HOW IT WORKS**: When an inner function references a variable defined in an outer enclosing function, Python stores that variable in the inner function's `__closure__` attribute as a cell object. This prevents garbage collection of the referenced object even when the outer scope returns.
- **CODE**:
```python
def make_sandboxed_file_reader(allowed_dir: str):
    """Outer function defining the scope boundary."""
    import os

    def read_file(relative_path: str) -> str:
        # Closes over allowed_dir
        safe_path = os.path.abspath(os.path.join(allowed_dir, relative_path))
        if not safe_path.startswith(os.path.abspath(allowed_dir)):
            raise PermissionError("Access denied: path traversal detected!")
        with open(safe_path, "r", encoding="utf-8") as f:
            return f.read()

    return read_file

# sandbox_reader remembers allowed_dir="/tmp/sandbox"
# even after make_sandboxed_file_reader has finished executing.
```

---

### Concept 4: Decorator
- **TERM**: Decorator
- **DEFINITION**: A syntactic sugar construct (`@decorator_name`) that passes the immediately following function or class into a callable and replaces it with the returned value.
- **INTUITION**: Gift wrapping. The present inside (the function) remains identical, but the wrapping adds ribbons, a greeting card, and protective cushioning (metadata, logging, validation).
- **WHY IT EXISTS**: Eliminates manual boilerplate. Instead of writing `my_func = register_tool(log_tool(validate_tool(my_func)))`, the `@tool` decorator allows clean, declarative registration of tools directly above their definition.
- **HOW IT WORKS**:
  Writing:
  ```python
  @tool
  def search(q: str): ...
  ```
  is strictly transformed by the Python compiler into:
  ```python
  def search(q: str): ...
  search = tool(search)
  ```
  Using `functools.wraps(func)` inside the decorator copies `__name__`, `__doc__`, `__annotations__`, and `__module__` from the target function onto the wrapper so introspection remains accurate.
- **CODE**:
```python
import functools
from typing import Callable, Any

def audit_log(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"[AUDIT] Invoking {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[AUDIT] {func.__name__} completed successfully.")
        return result
    return wrapper

@audit_log
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
```

---

### Concept 5: Function Introspection
- **TERM**: Function Introspection
- **DEFINITION**: Programmatic examination of a function's type annotations, parameter names, default values, and docstrings at runtime via the `inspect` standard library.
- **INTUITION**: An X-ray scanner for code. Without calling the function, the scanner reads its blueprint: what inputs it requires, what types it accepts, and how it documents itself.
- **WHY IT EXISTS**: AI models require JSON Schemas specifying parameter names, types, descriptions, and required fields. Writing these JSON schemas manually for every tool is error-prone and causes synchronization drift between docs and code. Introspection automatically generates accurate schemas directly from Python type hints and docstrings.
- **HOW IT WORKS**: `inspect.signature(func)` queries the `__annotations__` dictionary and code object flags of `func`, returning a `Signature` object containing ordered `Parameter` objects with `kind`, `default`, and `annotation`.
- **CODE**:
```python
import inspect

def calculate_mortgage(principal: float, annual_rate: float, years: int = 30) -> float:
    """Calculates monthly mortgage payment."""
    pass

sig = inspect.signature(calculate_mortgage)
for name, param in sig.parameters.items():
    print(f"Param: {name}, Annotation: {param.annotation}, Default: {param.default}")
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Missing `@functools.wraps` Breaking Tool Schemas
- **The Bug**: Writing a decorator without `@functools.wraps(func)`. The wrapper function replaces the original function's `__name__` with `"wrapper"` and obliterates the original docstring and annotations.
- **The Consequence**: The LLM schema generator registers every tool with the name `"wrapper"` and an empty description. The LLM cannot distinguish tools and hallucinations skyrocket.
- **The Fix**: Always decorate inner wrapper functions with `@functools.wraps(func)`.

### Anti-Pattern 2: Dynamic `eval()` Dispatch
- **The Bug**: Resolving LLM tool requests via `eval(f"{tool_name}(**args)")`.
- **The Consequence**: Arbitrary code execution vulnerability. If an adversary injects `__import__('os').system('rm -rf /')` as the tool name or argument, the host is compromised.
- **The Fix**: Use an explicit dictionary-based `ToolRegistry` that only permits invocation of pre-registered, validated callables.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What built-in Python function returns `True` if an object can be called with parentheses?
2. Which magic method must a class implement to allow instances of that class to be called like functions?
3. What attribute on a wrapper function is preserved when using `@functools.wraps(func)`?

### Tier 2 (Debugging)
Find the flaw in this tool registration decorator:
```python
def register_tool(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    registry[func.__name__] = inner
    return inner
```
*Hint*: What happens when an introspection tool inspects `registry["my_tool"].__doc__` or signature?

### Tier 3 (Application)
Write a Python decorator `@timed_tool` that measures the execution time of any decorated callable in milliseconds and stores the last execution latency in an attribute on the function object (`func.last_duration_ms`).

### Tier 4 (Challenge)
Build a `DynamicToolRegistry` class that:
1. Allows registering callables via `@registry.register`.
2. Inspects their docstring and type hints to automatically produce an OpenAI-compatible JSON schema.
3. Provides an `execute(tool_name: str, arguments: dict)` method that validates parameter presence before dispatching.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module to verify your understanding:
```bash
python3 course_0_prerequisites/01_callables_and_functional_python/callables_demo.py
python3 course_0_prerequisites/01_callables_and_functional_python/tool_decorator.py
```
