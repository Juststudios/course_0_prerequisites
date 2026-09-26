# Topic: Function Decorators and Closures

## What You Will Learn
In this module, you will master Python decorators—one of the language's most expressive metaprogramming patterns. You will learn:
- How Python treats functions as first-class citizens (objects that can be passed, bound, and returned).
- The concept of lexical closures: how inner functions retain access to outer scope variables even after the outer function has finished executing.
- How the `@decorator` syntax desugars into higher-order function composition (`func = decorator(func)`).
- How to write flexible wrappers using `*args` and `**kwargs` that preserve return values.
- Why naive decorators erase function metadata (`__name__`, `__doc__`, signature) and how `functools.wraps` fixes this.
- How to create parameterized decorators (decorators that accept arguments) using a three-tiered nested function architecture.
- How multiple stacked decorators behave during definition time versus execution time.
- How AI agents use decorators for tool registration (`@agent.tool`), API retry logic, rate limiting, and execution tracing.

## Prerequisites
Before tackling decorators, you should be confident with:
- Defining functions, return values, positional arguments, and keyword arguments (Module 08).
- Variable scope, closures, and the LEGB lookup rule (Module 09).
- Error handling with `try/except` blocks (Module 10).
- Dunder attributes like `__name__` and `__doc__` (Module 13).

## The Problem
Suppose you are engineering an autonomous AI agent that calls external APIs: search engines, code execution sandboxes, and LLM endpoints.
You notice that these network calls sometimes fail due to rate limits or transient network dropouts. You want to add automatic retry logic with exponential backoff to your search function:
```python
def web_search(query: str):
    # network request logic...
```
You can write a retry loop directly inside `web_search`. But what happens tomorrow when you add `calculate_math()`, `fetch_weather()`, `query_database()`, and 20 other tools?
If you copy-paste the retry logic into every single tool function:
1. You violate the DRY (Don't Repeat Yourself) principle.
2. If you decide to change the retry policy (e.g. from 3 retries to 5, or log errors to a database), you must edit 20 separate functions.
3. Your core business logic becomes obscured by boilerplate networking code.

You need a way to wrap cross-cutting concerns (logging, timing, caching, retries, input validation, permissions) cleanly around existing functions without altering their internal code. This is the exact problem decorators solve.

## Key Terminology
- **First-Class Function**: In Python, functions are first-class objects. They can be assigned to variables, stored in data structures, passed as arguments to other functions, and returned from functions.
- **Higher-Order Function**: A function that accepts one or more functions as arguments, returns a function, or both.
- **Closure**: A function object that retains bindings to free variables existing in its enclosing lexical scope at the time of creation, even if the enclosing scope has terminated.
- **Decorator**: A callable that takes a function (or class) as an argument and returns an augmented function (or class).
- **`@` Syntactic Sugar**: The pie-syntax prefix placed directly above a function definition that instructs Python to pass the function through the decorator.
- **`functools.wraps`**: A helper decorator from Python's standard library that copies original function attributes (`__name__`, `__doc__`, `__module__`, `__annotations__`) onto the wrapper function.
- **Decorator Factory**: A higher-order function that takes configuration parameters and returns a decorator function (the 3-level pattern).
- **Cross-Cutting Concern**: Functionality that applies across many parts of a codebase (such as logging, timing, authentication, and caching) rather than belonging to a single domain entity.

## Intuition
Think of a function as a gift: a handcrafted wooden toy.
- The gift does what it was built to do: roll across the floor.
- A **decorator** is gift wrap and bubble wrap.
- You take the toy, put it inside bubble wrap for shock protection (retry logic), wrap it in festive paper with a label (logging), and seal it.
- When the recipient opens the package, they still play with the toy, but it arrived safely without damage, and everyone knows who sent it.
- The original toy was never modified or cut apart. It was simply enclosed inside an outer protective shell.

## Concept
Understanding decorators requires mastering three core building blocks:

### 1. Functions as Values
```python
def say_hello():
    return "Hello"

greet = say_hello  # Assign function object to another variable
greet()            # Calls say_hello()
```

### 2. Inner Functions and Closures
```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor  # 'factor' is captured from outer scope!
    return multiply

double = make_multiplier(2)
double(5)  # Returns 10
```

### 3. The Decorator Transformation
When you write:
```python
@my_decorator
def my_func():
    pass
```
Python converts this at definition time into:
```python
def my_func():
    pass
my_func = my_decorator(my_func)
```
The original `my_func` name is rebound to whatever callable `my_decorator` returns (usually an inner `wrapper` function).

## Syntax
### 1. Standard Decorator Pattern with `functools.wraps`
```python
import functools

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} finished")
        return result
    return wrapper

@log_execution
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
```

### 2. Parameterized Decorator (Decorator Factory)
When a decorator takes its own parameters (like `@retry(max_attempts=3)`), you need three levels of functions:
```python
def retry(max_attempts: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if attempt == max_attempts:
                        raise
            return None
        return wrapper
    return decorator

@retry(max_attempts=5)
def unstable_api_call():
    pass
```

### 3. Stacking Decorators
```python
@decorator_one
@decorator_two
def action():
    pass
# Equivalent to: action = decorator_one(decorator_two(action))
```

## Example
Here is a complete, runnable example showcasing an AI Agent Tool Registry with metadata preservation and execution timing:

```python
import functools
import time
from typing import Callable, Dict, Any

# Tool Registry storage
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def tool(name: str, description: str):
    """Decorator factory to register agent tools with metadata."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            print(f"[AGENT] Invoking tool '{name}'...")
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            print(f"[AGENT] Tool '{name}' completed in {duration:.2f}ms")
            return result

        # Register tool metadata in central registry
        TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "callable": wrapper,
            "original_name": func.__name__,
        }
        return wrapper
    return decorator

@tool(name="web_search", description="Performs a real-time web query")
def search(query: str) -> str:
    """Simulates a fast web search."""
    return f"Search results for: {query}"

@tool(name="calculator", description="Computes mathematical expressions")
def calculate(expression: str) -> float:
    """Simulates expression calculation."""
    return float(eval(expression))

# Demonstration of execution
print("Registered Agent Tools:")
for tool_name, meta in TOOL_REGISTRY.items():
    print(f"  - {tool_name}: {meta['description']}")

search_result = search("Python decorators")
calc_result = calculate("40 + 2")
print("Search Result:", search_result)
print("Calc Result:", calc_result)
```

## Line-by-Line Explanation
Let's trace how the `@tool` decorator factory operates:
1. `def tool(name: str, description: str):`: Defines the outermost function. It accepts configuration parameters (`name`, `description`) and returns a decorator.
2. `def decorator(func: Callable):`: The actual decorator. It receives the target function `func` when Python applies `@tool(...)`.
3. `@functools.wraps(func)`: Essential built-in decorator that updates `wrapper` to copy `func`'s `__name__`, `__doc__`, and `__annotations__`. Without this, `search.__name__` would be `"wrapper"`, confusing introspection and documentation generators.
4. `def wrapper(*args, **kwargs):`: The inner function that replaces `func`. It uses `*args` and `**kwargs` to accept any argument signature without hardcoding parameters.
5. `start = time.perf_counter()`: Captures high-precision timestamp before calling the wrapped function.
6. `result = func(*args, **kwargs)`: Executes the original target function with all arguments forwarded intact.
7. `TOOL_REGISTRY[name] = {...}`: Side effect executed at module import/definition time. Storing the tool in the agent dictionary makes it discoverable by LLM reasoning engines.
8. `return wrapper`: The decorator returns the wrapped function to replace the original name.
9. `return decorator`: The factory returns the decorator configured with `name` and `description`.

## What Python Is Doing
At the CPython bytecode and interpreter level:
1. **Definition Time Binding**: When CPython encounters `def search(...)` decorated with `@tool(...)`:
   - It evaluates the expression `tool(name="web_search", description=...)`, which returns the `decorator` function.
   - It creates the code object for `search` and creates the `function` object.
   - It calls `decorator(function_object)` and stores the returned callable in the module namespace under the key `"search"`.
   - All decorator execution occurs **once**, when the module is imported or read!
2. **Closures and Free Variables**:
   - The returned `wrapper` function possesses a `__closure__` attribute containing a tuple of `cell` objects.
   - Each cell holds a pointer to a free variable from the outer scope (`func`, `name`, `description`).
   - Even when the outer functions `tool` and `decorator` have returned and their call frames have been popped from the C stack, the cells remain allocated on the heap as long as `wrapper` is referenced.
3. **Execution Time**: When `search("Python decorators")` is called, the CPython interpreter executes the bytecode of `wrapper`, which dereferences `func` via its closure cell and invokes it.

## Common Mistakes
### 1. Forgetting to Return the Result
```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs) # BUG: Forgot to return the result!
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

res = add(2, 3) # res is None!
```
**Fix**: Always capture `result = func(*args, **kwargs)` and `return result`.

### 2. Forgetting `@functools.wraps`
Without `functools.wraps`, decorated functions lose their identity:
```python
def naive_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@naive_decorator
def calculate_tax(amount):
    """Calculates state tax."""
    return amount * 0.08

print(calculate_tax.__name__)  # Prints 'wrapper'!
print(calculate_tax.__doc__)   # Prints None!
```
**Fix**: Always add `@functools.wraps(func)` directly on the inner `wrapper`.

### 3. Missing Parentheses on Decorator Factories
If a decorator is defined to accept parameters (`def retry(attempts=3): ...`), decorating with `@retry` (without parentheses) passes the function as `attempts`, causing a runtime `TypeError`.
**Fix**: Call the factory: `@retry()` or `@retry(attempts=5)`.

### 4. Incorrect Order in Stacking
Decorators are applied from bottom to top:
```python
@auth_required
@cache_result
def get_user_data():
    pass
# get_user_data = auth_required(cache_result(get_user_data))
```
If `cache_result` is placed above `auth_required`, cached results might bypass authentication! Order matters.

## Real-World Uses
- **Web Framework Routing**: Flask (`@app.route("/api")`) and FastAPI (`@app.get("/users")`) map URL routes to handler functions.
- **Caching and Memoization**: `functools.lru_cache(maxsize=128)` caches expensive function results based on arguments.
- **Authentication & Authorization**: Checking user roles or JWT tokens before granting access to endpoint handlers.
- **Instrumentation & APM**: Datadog, New Relic, and Prometheus use decorators to measure function latency, error rates, and CPU consumption.

## Connection to AI Agents
Decorators are the primary design pattern for building modern AI agent frameworks:
- **`@agent.tool`**: Frameworks like LangChain, CrewAI, AutoGen, and Semantic Kernel use decorators to turn standard Python functions into LLM-callable tools, extracting JSON schemas from type hints and docstrings.
- **Rate-Limiting & Exponential Backoff**: Guarding against OpenAI/Anthropic `RateLimitError` (HTTP 429) using retry decorators with randomized jitter.
- **Context Injection**: Automatically injecting conversation IDs, user session tokens, or DB sessions into agent task handlers.
- **Agent Action Tracing**: Wrapping tool executions with OpenTelemetry or LangSmith spans to record agent thoughts, inputs, and outputs in an observability trace.

## Practice
Solidify your understanding with these practice steps:
1. Write a simple `@timer` decorator that measures and prints the execution duration of a function using `time.perf_counter()`.
2. Inspect the `__name__` and `__doc__` of your decorated function with and without `@functools.wraps(func)`.
3. Build a decorator `@count_calls` that increments and prints an invocation counter each time the target function is called.
4. Create a parameterized decorator `@repeat(num_times=3)` that runs the decorated function multiple times and returns the result of the final run.

## Challenge
Design an `@agent_guardrail(max_execution_time=2.0, max_retries=2, fallback_value="GUARDRAIL_TRIGGERED")` decorator. It should:
1. Enforce that if the wrapped function takes longer than `max_execution_time` seconds or raises an unhandled exception, it retries up to `max_retries` times.
2. If all retries fail or time out, it cleanly returns the `fallback_value` instead of crashing the agent runtime.
3. Preserve the wrapped function's original metadata using `functools.wraps`.

## Summary
- A decorator is a function that takes another function, wraps it with enhanced behavior, and returns the wrapper.
- The `@decorator` syntax is syntactic sugar for `func = decorator(func)`.
- Always use `*args, **kwargs` to forward arguments transparently and return the function's result.
- Always decorate your wrapper with `@functools.wraps(func)` to preserve function metadata.
- Parameterized decorators require three nested functions: outer factory, middle decorator, inner wrapper.
- AI agent systems rely on decorators for tool registration, retry policies, and execution observability.

## What You Should Know Before Moving On
Before advancing to Module 20 (Context Managers), ensure you can:
- Explain what happens when Python executes `@my_decorator` above a function.
- Write a complete decorator with `*args`, `**kwargs`, and `@functools.wraps`.
- Explain what a closure is and where its captured variables are stored in Python memory.
- Implement a decorator factory that takes arguments.
- Articulate why decorators are the standard pattern for registering tools in AI agent systems.
