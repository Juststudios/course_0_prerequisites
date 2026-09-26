# Topic: Functional Programming in Python

## What You Will Learn
- The core philosophy of functional programming (FP) and how it contrasts with imperative and object-oriented paradigms.
- The concept of first-class and higher-order functions in Python.
- Pure functions, immutability, side-effect elimination, and referential transparency.
- Anonymous functions with `lambda`: when to use them and when to avoid them.
- Transforming and filtering data collections using `map()`, `filter()`, `reduce()`, and list/dict comprehensions.
- Partial function application using `functools.partial`.
- Building declarative data processing pipelines for cleaning and formatting AI agent prompts and outputs.

## Prerequisites
- Solid foundation in Python functions: defining functions, positional/keyword arguments, return values (Module 08).
- Familiarity with collections: lists, dictionaries, tuples, and iteration (Modules 06–07).
- Understanding of basic scopes (Module 09).

## The Problem
In imperative and object-oriented programming, systems are often designed around mutating shared state across multiple steps:
```python
results = []
for message in raw_messages:
    if message["role"] == "user":
        cleaned = message["content"].strip().lower()
        results.append(cleaned)
```
While simple at first, as codebases grow, widespread mutable state creates significant engineering challenges:
1. **Hidden Side Effects**: A function called halfway through a script might quietly alter a list or dictionary that another part of the system relied on.
2. **Order Dependency**: If step C depends on step B mutating variable X, reorganizing or parallelizing steps often introduces insidious bugs that are difficult to reproduce.
3. **Difficult Testing and Concurrency**: Functions that read from or write to external mutable variables cannot be easily tested in isolation or executed across multiple threads/processes without race conditions.

Functional programming solves this by treating computation as the mathematical evaluation of pure functions without changing state or mutating data.

## Key Terminology
- **First-Class Citizen**: An entity that can be passed as an argument, returned from a function, assigned to a variable, and stored in data structures. In Python, functions are first-class citizens.
- **Higher-Order Function**: A function that takes one or more functions as arguments, returns a function, or both (e.g., `map`, `filter`, `sorted`).
- **Pure Function**: A function whose return value depends exclusively on its input parameters and produces zero observable side effects (no mutating global state, no disk I/O, no network calls).
- **Referential Transparency**: An expression that can be replaced with its corresponding value without changing the program's behavior.
- **Lambda Function**: A small, anonymous inline function defined with the `lambda` keyword containing a single expression.
- **Partial Application**: Creating a new callable from an existing function by pre-filling ("freezing") a subset of its arguments using `functools.partial`.
- **Function Composition**: Combining two or more functions where the output of one function becomes the input of the next ($f(g(x))$).

## Intuition
Think of an industrial automotive assembly line:
1. **The Imperative Way**: A single mechanic walks around a car chassis with a toolbox, adjusting a bolt here, painting a panel there, and swapping tires over time. If the mechanic forgets which step they are on, the chassis state is corrupted.
2. **The Functional Way**: The car moves along an automated conveyor belt. Station 1 (pure function A) takes raw steel and outputs stamped panels. Station 2 (pure function B) takes panels and outputs a welded chassis. Station 3 (pure function C) paints it.
   - None of the stations reach out and touch the other stations' tools.
   - Each station takes an input, transforms it without altering the original raw materials, and yields a new output.
   - If Station 2 produces a defect, you know with mathematical certainty that the bug is inside Station 2, because no other station has access to its data.

## Concept
Python is a multi-paradigm language. It does not force you to write purely functional code (like Haskell), but it incorporates powerful functional concepts.

The three pillars of functional programming in Python are:
1. **Functions as Values**:
   ```python
   def square(x): return x * x
   op = square  # Bound to variable
   print(op(5)) # 25
   ```
2. **Transformation without Mutation**:
   Instead of modifying a list in-place via `.append()` or `.pop()`, we transform inputs into new collections using comprehensions or mapping functions.
3. **Declarative Pipelines**:
   Expressing *what* you want done rather than managing loop indices, accumulators, and temporary scratchpad variables manually.

```
Raw Input Data
     |
     v
[ Filter Function ] ----> Discards non-relevant tokens
     |
     v
[ Map Function ]    ----> Normalizes & trims text strings
     |
     v
[ Reducer / Join ]  ----> Combines into final structured prompt
```

## Syntax
```python
# 1. Lambda syntax: lambda <parameters>: <single_expression>
double = lambda x: x * 2

# 2. High-order functions: map and filter
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))      # [2, 4]
squared = list(map(lambda x: x ** 2, numbers))            # [1, 4, 9, 16, 25]

# 3. Pythonic comprehensions (often preferred over raw map/filter):
squared_evens = [x ** 2 for x in numbers if x % 2 == 0]   # [4, 16]

# 4. Partial application:
from functools import partial
def power(base: int, exponent: int) -> int:
    return base ** exponent

cube = partial(power, exponent=3)
print(cube(4))  # 64
```

## Example
Here is a complete, working example illustrating a functional text preprocessing pipeline for an AI Agent prompt builder:

```python
from functools import reduce, partial
from typing import Callable, List

# Step 1: Define pure transformation functions
def strip_whitespace(text: str) -> str:
    return text.strip()

def remove_punctuation(text: str) -> str:
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
    return "".join(c for c in text if c in allowed)

def to_lower(text: str) -> str:
    return text.lower()

# Step 2: Compose functions into a processing pipeline
def compose(*functions: Callable[[str], str]) -> Callable[[str], str]:
    """Composes multiple single-argument functions left-to-right."""
    def pipeline(initial_value: str) -> str:
        return reduce(lambda val, func: func(val), functions, initial_value)
    return pipeline

# Step 3: Create reusable specialized text sanitizers
sanitize_prompt = compose(strip_whitespace, remove_punctuation, to_lower)

# Step 4: Process a collection of raw user queries immutably
raw_inputs = [
    "  Where is the Nearest Post Office?!  ",
    "How do I calibrate a LIDAR sensor??? ",
    "   Summarize 2026 AI Benchmarks...   ",
]

# Using map to apply our pure pipeline across all inputs:
cleaned_prompts = list(map(sanitize_prompt, raw_inputs))

if __name__ == "__main__":
    print("Original Inputs:")
    for item in raw_inputs:
        print(f"  {item!r}")
    print("\nCleaned Prompts (Functional Pipeline):")
    for prompt in cleaned_prompts:
        print(f"  {prompt!r}")
```

## Line-by-Line Explanation
- `def strip_whitespace(text: str) -> str:`: A pure function taking a string and returning a new trimmed string. The original input string remains unchanged in memory (strings are immutable in Python).
- `def remove_punctuation(text: str) -> str:`: Uses a generator expression inside `"".join(...)` to filter out characters not present in the allowed set.
- `def compose(*functions)`: A higher-order function that accepts an arbitrary number of callable functions (`*functions`) and returns a new function (`pipeline`).
- `reduce(lambda val, func: func(val), functions, initial_value)`: Sequentially applies each transformation in `functions`, threading the result of one function as the input to the next.
- `sanitize_prompt = compose(...)`: Creates a reusable, declarative text sanitization engine without writing repetitive `for` loops.
- `list(map(sanitize_prompt, raw_inputs))`: Applies `sanitize_prompt` to every item in `raw_inputs` immutably, preserving `raw_inputs` intact.

## What Python Is Doing
1. **First-Class Function Objects**: When you write `def to_lower(text): ...`, Python creates an instance of `types.FunctionType` with code object `__code__` containing compiled bytecode instructions.
2. **Lazy Evaluation in `map` and `filter`**: In Python 3, `map()` and `filter()` do not immediately create lists. They return iterator objects that yield transformed elements on-demand (one at a time) when consumed by a `for` loop or `list()`. This prevents memory spikes on large datasets.
3. **Closures in Function Factories**: When `compose()` returns `pipeline`, Python bundles the enclosing scope's `functions` tuple into `pipeline.__closure__`, keeping those references alive as long as `pipeline` exists.
4. **Lambda Bytecode**: A lambda compiles to the exact same bytecode instructions (`LOAD_FAST`, `BINARY_MULTIPLY`, `RETURN_VALUE`) as an equivalent standard `def` function.

## Common Mistakes
1. **Overusing Complex Lambdas**: Writing multi-line logic or complex conditions inside a single `lambda`. If an expression cannot be understood in 3 seconds, use a standard named `def` function with a descriptive name and docstring.
2. **Unnecessary `map`/`filter` over Comprehensions**: Writing `list(map(lambda x: x.upper(), filter(lambda x: len(x) > 3, words)))` when Python's list comprehension `[w.upper() for w in words if len(w) > 3]` is far more readable and faster in Python.
3. **Accidental Mutation Inside Pure Functions**: Modifying a passed list using `.sort()` or `.append()` inside a function intended to be pure. Always create a new collection (e.g. `sorted(items)` or `items + [new_item]`).
4. **Consuming Iterators Twice**: Forgetting that `map()` and `filter()` return single-pass iterators. If you loop over `result = map(...)` once, a second loop over `result` will be empty.

## Real-World Uses
- **Data Engineering (PySpark, Pandas)**: Applying vectorized transforms across millions of records using `.map()` and `.apply()`.
- **Event Streaming & WebSockets**: Filtering, mapping, and aggregating incoming telemetry packets in real-time pipelines.
- **Middleware & Web Handlers**: Chaining authentication, rate-limiting, and compression middleware functions in modern web frameworks (FastAPI, Starlette).

## Connection to AI Agents
Functional programming principles are indispensable for reliable autonomous AI agents:
- **Prompt Preprocessing Pipelines**: An LLM agent takes raw multi-turn user messages and runs them through a pipeline of pure sanitization, token truncation, and template formatting functions.
- **Deterministic Tool Filtering**: When an agent selects candidate tools from a registry of 50 tools, it filters tools declaratively based on capability tags, permissions, and token budgets.
- **Immutable State Snapshots**: In multi-agent consensus loops (e.g., debate or tree-of-thought search), an agent branches new thought paths. Functional transformations guarantee that branch A cannot inadvertently corrupt the state of branch B.

## Practice
1. Open a terminal and use `sorted()` with a custom `key=lambda ...` function to sort a list of agent dictionaries by their `"score"` field in descending order.
2. Use `functools.partial` to create a pre-configured logging function `log_warning = partial(print, "[WARNING]")`. Test calling `log_warning("Disk usage above 90%!")`.
3. Write a list comprehension that takes a list of integers and produces a list of strings `"EVEN"` or `"ODD"` for each number.

## Challenge
Implement a functional query pipeline `query_tool_registry`:
- Given a list of tool metadata dictionaries: `[{"name": "calc", "tags": ["math", "utility"], "latency_ms": 15}, ...]`.
- Use functional techniques (`filter`, `sorted`, list comprehensions) to write a function that finds all tools matching a given tag, filtered to only those with `latency_ms <= max_latency`, sorted from lowest latency to highest latency.

## Summary
- Functional programming emphasizes pure functions, immutability, and declarative data transformation.
- In Python, functions are first-class objects that can be stored, passed, and returned.
- Pure functions eliminate side effects, making code deterministic, parallelizable, and easy to test.
- Comprehensions provide idiomatic, highly optimized replacements for many `map` and `filter` operations.
- Modern AI agent pipelines rely on functional chaining for robust prompt formatting and tool filtering.

## What You Should Know Before Moving On
- How to define and pass higher-order functions in Python.
- When to use a `lambda` expression versus a standard `def` function.
- The difference between in-place mutation and immutable transformation.
- How to use `functools.partial` to bind default arguments.
- How functional data processing pipelines safeguard agent state against side-effect bugs.
