# Functions in Python

## What You Will Learn
In this module, you will master functional abstraction in Python:
- How to define, call, and document functions cleanly.
- How parameters differ from arguments, and how Python binds positional vs. keyword values.
- How default parameters work, and why the mutable default argument trap (`arg=[]`) causes subtle bugs.
- How to accept flexible, variadic inputs using `*args` and `**kwargs`.
- How to enforce clean API boundaries using keyword-only (`*`) and positional-only (`/`) parameters.
- How Python packs and unpacks multiple return values seamlessly via tuples.
- How functions behave as first-class citizens (passing them as callbacks and storing them in registries).
- How AI agents use functions as the concrete execution bridge for LLM tool calling.

## Prerequisites
Before starting this module, you should understand:
- Python control flow (`if`, `elif`, `else`, `for`, `while`) from Module 07.
- Python data structures: lists, dictionaries, tuples, and sets.
- Variable assignment and expression evaluation.

## The Problem
As programs grow beyond basic scripts, copy-pasting code leads to catastrophic fragility:
- If a token-counting calculation appears in twelve different places, fixing a bug requires changing twelve files.
- Without encapsulation, local temporary variables pollute the global namespace and inadvertently overwrite each other.
- Without functional abstractions, an AI agent cannot dynamically decide to execute a tool (like a calculator or database search) because the operations are hardcoded into an unwieldy, monolithic script.

Functions solve this by isolating units of logic behind clear input-output contracts: they accept data, transform it, and return a result without polluting the surrounding environment.

## Key Terminology
- **Function**: A reusable, named block of code that performs an isolated computation or action.
- **Parameter**: A variable listed inside the parentheses in the function definition (the blueprint's slot).
- **Argument**: The concrete value passed into the function when it is called (the physical data).
- **Positional Argument**: An argument assigned to a parameter based solely on its position in the call list.
- **Keyword Argument**: An argument passed with an explicit name (`parameter_name=value`), making call sites order-independent and self-documenting.
- **Arity**: The number of arguments or parameters a function takes.
- **First-Class Function**: A language feature where functions can be assigned to variables, passed as arguments to other functions, and returned from functions just like integers or strings.
- **Higher-Order Function**: A function that accepts another function as an argument, returns a function, or both.

## Intuition
Imagine an automated kitchen:
- A **function definition (`def`)** is a recipe card filed in a recipe box. Writing the recipe does not bake the cake; it only records how to bake it.
- **Parameters** are empty ingredient bowls labeled "flour", "sugar", and "eggs".
- A **function call** is an order placed with the chef. The physical ingredients handed to the chef are the **arguments**.
- The baked cake delivered through the kitchen window is the **return value**.
- If a chef finishes baking but delivers nothing through the window, Python assumes the chef delivered a tray containing `None`.
- **First-Class Functions** mean the recipe card itself can be handed to another chef, placed in a menu, or modified dynamically.

## Concept

### 1. Function Contracts & Return Values
Every Python function terminates when it reaches a `return` statement or reaches the end of its indented body. If no `return` expression is specified, Python silently returns `None`.

### 2. Argument Binding Order
Python binds arguments using a strict hierarchy:
1. Positional arguments are assigned to positional parameters left-to-right.
2. Keyword arguments are assigned to their matching parameter names.
3. Any excess positional arguments are collected into a tuple by `*args`.
4. Any excess keyword arguments are collected into a dictionary by `**kwargs`.
5. Unfilled parameters receive their default values; if any parameter without a default remains unfilled, Python raises `TypeError`.

### 3. The Mutable Default Trap
In Python, default parameter expressions are evaluated **once**, when the `def` statement executes (at module load time), not every time the function is called.
If a default is a mutable object (like a list `[]` or dict `{}`), all invocations that rely on that default share the exact same object in memory!

```python
# Dangerous: All calls mutate the identical list object!
def bad_add(item, target=[]):
    target.append(item)
    return target

# Idiomatic & Safe:
def good_add(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### 4. Keyword-Only and Positional-Only Markers
- `def fn(a, /, b, *, c):`
  - `a` must be passed positionally (cannot do `fn(a=1)`).
  - `b` can be passed positionally or by keyword.
  - `c` must be passed by keyword (cannot do `fn(1, 2, 3)`).

## Syntax

```python
# Standard definition with type hints and default values
def generate_summary(
    text: str,
    max_words: int = 50,
    *,
    capitalize_first: bool = True
) -> str:
    """Summarize text to a specified word limit."""
    words = text.split()[:max_words]
    summary = " ".join(words)
    return summary.capitalize() if capitalize_first else summary

# Variadic arguments (*args, **kwargs)
def log_agent_event(event_type: str, *tags: str, **metadata: Any) -> None:
    print(f"Event: {event_type} | Tags: {tags} | Meta: {metadata}")

# Multiple return values (tuple packing)
def compute_bounds(data: list[float]) -> tuple[float, float]:
    return min(data), max(data)
```

## Example

```python
from typing import Callable, Any

# Tool registry implementing first-class function dispatch
class AgentToolRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        self._handlers[name] = func

    def dispatch(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:
        if tool_name not in self._handlers:
            return {"status": "error", "error": f"Tool '{tool_name}' not available"}
        try:
            handler = self._handlers[tool_name]
            result = handler(**kwargs)
            return {"status": "success", "result": result}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

# Concrete tools
def calculate_vat(amount: float, rate: float = 0.20) -> float:
    return round(amount * rate, 2)

def generate_user_id(prefix: str, identifier: int) -> str:
    return f"{prefix}_{identifier:04d}"

# Wire into agent
registry = AgentToolRegistry()
registry.register("calc_vat", calculate_vat)
registry.register("gen_id", generate_user_id)

# Dispatching tool calls
print(registry.dispatch("calc_vat", amount=150.0, rate=0.15))
print(registry.dispatch("gen_id", prefix="USR", identifier=42))
print(registry.dispatch("non_existent_tool"))
```

## Line-by-Line Explanation
1. `class AgentToolRegistry:`: Defines an object to manage callable tool functions.
2. `self._handlers: dict[str, Callable[..., Any]] = {}`: Internal mapping storing tool names as keys and executable callables as values.
3. `self._handlers[name] = func`: Stores the function reference as a first-class citizen inside the dictionary.
4. `def dispatch(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:`: Accepts the target tool name and arbitrary keyword arguments destined for that tool.
5. `if tool_name not in self._handlers:`: Validates that the requested tool exists in the registry.
6. `handler = self._handlers[tool_name]`: Fetches the callable function object.
7. `result = handler(**kwargs)`: Unpacks the dictionary of arguments into the tool function and executes it.
8. `except Exception as exc:`: Intercepts execution crashes and converts them into structured error responses.

## What Python Is Doing
When Python compiles and executes a function:
1. **Creation Time (`def`)**: Python creates a `function` object (`PyFunctionObject`). It evaluates the default argument expressions immediately and stores them in `__defaults__` (positional defaults) and `__kwdefaults__` (keyword-only defaults). The compiled bytecode is attached to `__code__`.
2. **Call Time (`func()`)**: Python creates a new **Stack Frame** (`PyFrameObject`) on the call stack. This frame allocates a fixed-size local variable array (`fastlocals`).
3. **Parameter Binding**: Arguments are mapped into the frame's local array. Positional arguments are placed at known slot offsets; `*args` allocates a tuple; `**kwargs` allocates a dictionary.
4. **Execution & Teardown**: The Python Virtual Machine executes the frame's bytecode. When `return` executes, the result is pushed to the caller's evaluation stack, and the frame is popped and deallocated (triggering garbage collection for local variables whose reference count reaches zero).

## Common Mistakes

### 1. The Mutable Default Argument Bug
- **Bug**: `def track_step(step, history=[]):`
- **Why**: The default list is created only once. Successive calls without a second argument append to the same list.
- **Fix**: Use `history=None` and initialize `history = []` inside the function body.

### 2. Confusing `print()` with `return`
- Beginners often print inside a function and forget to return a value. When they assign the result (`res = my_func()`), `res` is `None`!

### 3. Argument Order Violations
- In parameter definitions, non-default arguments must precede default arguments:
  `def invalid(a=1, b):` raises a `SyntaxError: non-default argument follows default argument`.

### 4. Forgetting `*` or `**` During Forwarding
- Passing `args` instead of `*args` passes a single tuple instead of unpacking elements.
- Passing `kwargs` instead of `**kwargs` passes a dictionary as a single positional parameter.

## Real-World Uses
- **API Client SDKs**: Functions like `requests.get(url, params=None, headers=None, timeout=30)` rely on keyword arguments and safe defaults.
- **Data Transformation Pipelines**: Higher-order functions used in map/reduce and ETL stream processing.
- **Decorator Infrastructure**: Functions wrapping and augmenting other functions (e.g. `@retry`, `@lru_cache`, `@app.route`).

## Connection to AI Agents
In modern AI Agent architecture (such as OpenAI Tool Calling, Anthropic Tool Use, and LangChain):
1. **Tool Definition**: Every capability an AI agent possesses (reading files, executing bash commands, searching the web) is exposed as a Python function.
2. **Schema Reflection**: Frameworks inspect the function's docstring and type hints (`inspect.signature`) to generate JSON Schemas sent to the LLM.
3. **Dispatch & Dynamic Invocation**: When the LLM outputs a JSON payload like `{"name": "search", "arguments": {"query": "python"}}`, the Python agent unpacks the arguments directly into the function: `registry[call["name"]](**call["arguments"])`.

## Practice
1. Write a function `clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float` that restricts `value` to lie between `min_val` and `max_val`.
2. Write a function `summarize_scores(*scores: float) -> dict[str, float]` that returns `{"count": ..., "mean": ..., "min": ..., "max": ...}` for arbitrary score arguments.
3. Create a higher-order function `retry(fn: Callable[[], Any], times: int = 3) -> Any` that calls `fn` and retries up to `times` if it raises an exception.

## Challenge
Design an extensible tool validator:
`validate_and_call(func: Callable[..., Any], kwargs: dict[str, Any], required_keys: set[str]) -> Any`:
- Verify all `required_keys` are present in `kwargs`. If missing, raise `ValueError` listing missing parameters.
- Check if any unexpected keys are passed that `func` does not accept (unless `func` accepts `**kwargs`).
- Execute `func` and return the result.

## Summary
- Functions encapsulate logic, prevent repetition, and provide clean abstraction boundaries.
- Positional arguments match by order; keyword arguments match by parameter name.
- Default arguments must never be mutable objects (use `None` sentinel pattern).
- `*args` packs arbitrary positional arguments into a tuple; `**kwargs` packs named arguments into a dict.
- Keyword-only parameters (`*`) enforce explicit, readable call sites.
- Functions are first-class objects in Python, making dynamic registries and tool dispatch simple and powerful.

## What You Should Know Before Moving On
Before proceeding to Module 09 (Scope):
- You can explain why `def f(x, l=[]):` is dangerous and rewrite it safely.
- You can write functions that accept `*args` and `**kwargs` and unpack them.
- You understand how Python packs multiple return values into tuples.
- You can pass functions as arguments into other functions and store them in collections.
- You understand how LLMs use functions to interact with external tools and systems.
