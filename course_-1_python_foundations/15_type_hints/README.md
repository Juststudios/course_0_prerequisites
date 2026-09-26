# Topic: Type Hints and Static Type Checking in Python

## What You Will Learn
- What type hints (annotations) are and how Python uses gradual typing (PEP 484).
- The critical distinction between static type checking (via mypy/pyright) and runtime execution.
- How to annotate variables, function parameters, and return types.
- Annotating container collections using modern built-in generics (`list[str]`, `dict[str, Any]`, `tuple[int, ...]`).
- Advanced types from the `typing` module: `Union` (`|`), `Optional`, `Literal`, `Callable`, and `TypeVar`.
- Structural subtyping with `Protocol` (static duck typing) and schema definitions with `TypedDict`.
- How modern AI agent frameworks inspect type hints to automatically generate JSON schemas for LLM tool calling.

## Prerequisites
- Proficiency in Python functions, parameters, and return statements (Module 08).
- Understanding of Python data collections: lists, dicts, tuples (Module 06).
- Familiarity with classes and object-oriented programming (Module 13).

## The Problem
Python is dynamically typed. You can pass an integer where a string was expected, or `None` where a list was expected, and Python will not complain until the code is actually running and crashes with a runtime error:
```python
def generate_summary(text, max_tokens):
    return text[:max_tokens] + f" (Total tokens: {max_tokens})"

# What if another developer calls this?
generate_summary(None, 50)  # TypeError: 'NoneType' object is not subscriptable at RUNTIME!
```
In small scripts, you can keep all variable types in your head. But in production systems, large teams, and complex AI agent architectures:
1. **Silent Contract Violations**: You cannot tell what a function expects or returns without reading its entire implementation or writing paragraphs of outdated docstrings.
2. **Missing IDE Autocomplete**: Your editor cannot suggest methods because it does not know what type of object a variable holds.
3. **Runtime Crashes in Production**: Type mismatches are only caught when a user or AI agent triggers that specific line of code at 2 AM.

We need a way to declare unambiguous type contracts directly in code that automated tools and IDEs can verify *before* code is ever deployed.

## Key Terminology
- **Dynamic Typing**: Types are associated with values at runtime, not variables. Variables can hold any type of object.
- **Gradual Typing**: A typing system where parts of a program can be dynamically typed while other parts are statically annotated.
- **Type Hint / Annotation**: Metadata attached to variables, parameters, or return types declaring the expected type.
- **`__annotations__`**: A special dictionary attribute on functions, classes, and modules where Python stores type hints at runtime.
- **Static Type Checker (mypy / pyright)**: An external analysis tool that reads your code without running it to verify that all operations obey declared type contracts.
- **`Optional[T]` / `T | None`**: Indicates that a value can either be of type `T` or `None`.
- **`Callable[[ArgTypes], ReturnType]`**: Type annotation representing a callable function or method.
- **`Literal`**: Constrains a value to specific literal strings, numbers, or booleans.
- **`Protocol`**: Defines an interface using structural subtyping (compile-time duck typing).

## Intuition
Think of electrical plugs and wall outlets:
1. **Pure Dynamic Typing** is like having identical two-prong wall outlets for everything—phone chargers, microwave ovens, industrial laser cutters, and 240V arc welders. If you plug a 50-amp welder into a 10-amp lamp outlet, the outlet melts or sparks fly (a runtime crash).
2. **Type Hints** are color-coded, labeled matching sockets.
   - The socket says: `"Accepts: 120V 15A Plug"`.
   - The plug says: `"Provides: 120V 15A Plug"`.
3. **The Static Type Checker (mypy)** is the electrical safety inspector who walks through the building with a blueprint *before* turning on the master power breaker. If they spot an industrial welder wired to a toaster socket, they flag the violation immediately.
4. **Runtime Python** is electricity itself: it doesn't read the labels by default; it just flows through whatever wire you connected.

## Concept
In Python, type hints are purely annotations. Python's runtime interpreter intentionally **ignores** type hints when executing code:
```python
x: int = "This is a string, not an int!"  # Runs with NO runtime error in Python!
```
Type hints exist for:
1. **Static Analysis Tools (mypy, pyright, Ruff)**: Catch bugs before running tests.
2. **Developer Tooling (VS Code, PyCharm)**: Powering instant autocompletion, parameter hints, and automated refactoring.
3. **Runtime Reflection Libraries (Pydantic, FastAPI, Instructor)**: Inspecting `__annotations__` to automatically validate HTTP payloads or convert Python functions into OpenAI/Anthropic tool schemas.

```
+----------------------------------------------------------------+
|  def calculate_tax(subtotal: float, rate: float = 0.08) -> float|
+----------------------------------------------------------------+
         |                                           |
         v                                           v
[ Static Type Checkers ]                    [ LLM Tool Converters ]
  (mypy / pyright)                           (Pydantic / Instructor)
  Verifies subtotal is float                 Extracts:
  Flags: calculate_tax("100")                  - subtotal (type: number)
  Before code runs!                            - rate (type: number)
                                               Generates JSON Schema!
```

## Syntax
```python
# 1. Variable and collection annotations
username: str = "Alice"
retry_count: int = 3
temperature: float = 0.7
is_active: bool = True

# Python 3.9+ built-in container generics
allowed_roles: list[str] = ["admin", "agent", "user"]
user_scores: dict[str, float] = {"Alice": 98.5, "Bob": 84.0}
coordinate: tuple[float, float] = (37.7749, -122.4194)

# 2. Modern Union syntax (Python 3.10+): T1 | T2
user_id: int | str = "USR-4091"

# 3. Optional values: str | None
nickname: str | None = None

# 4. Function signatures with parameter and return annotations
def format_prompt(template: str, variables: dict[str, str]) -> str:
    return template.format(**variables)

# 5. Callable signature: Callable[[arg1_type, arg2_type], return_type]
from typing import Callable
ToolFunc = Callable[[str, int], bool]
```

## Example
Here is a complete, working script demonstrating type annotations across an AI Agent tool runner with introspection:

```python
from typing import Callable, Any, Literal, TypedDict
import inspect

class ToolMetadata(TypedDict):
    name: str
    description: str
    category: Literal["web", "compute", "database"]
    timeout_sec: float

def execute_agent_tool(
    name: str,
    tool_fn: Callable[[str], str],
    argument: str,
    metadata: ToolMetadata,
) -> str:
    """Executes a tool obeying type contracts."""
    print(f"Executing [{metadata['category'].upper()}] tool '{name}' (timeout {metadata['timeout_sec']}s)...")
    return tool_fn(argument)

# Implementation of a concrete tool adhering to Callable[[str], str]
def reverse_text(input_text: str) -> str:
    return input_text[::-1]

if __name__ == "__main__":
    meta: ToolMetadata = {
        "name": "reverser",
        "description": "Reverses a string",
        "category": "compute",
        "timeout_sec": 5.0,
    }

    result = execute_agent_tool("reverser", reverse_text, "Autonomous Agent", meta)
    print("Execution output:", result)

    # Inspecting type annotations at runtime:
    sig = inspect.signature(execute_agent_tool)
    print("\nRuntime Type Signature of execute_agent_tool:")
    for param_name, param in sig.parameters.items():
        print(f"  {param_name}: {param.annotation}")
    print(f"  Returns: {sig.return_annotation}")
```

## Line-by-Line Explanation
- `class ToolMetadata(TypedDict):`: Defines a typed dictionary specifying exact keys and value types. Static type checkers flag any dictionary missing a required key or using the wrong type.
- `category: Literal["web", "compute", "database"]`: Restricts `category` to one of three exact string literals.
- `tool_fn: Callable[[str], str]`: Specifies that `tool_fn` must be a function taking exactly one `str` parameter and returning a `str`.
- `metadata: ToolMetadata`: Enforces that `metadata` adheres to the `ToolMetadata` dictionary contract.
- `def reverse_text(input_text: str) -> str:`: Satisfies the `Callable[[str], str]` contract.
- `inspect.signature(...)`: Demonstrates that Python preserves type hints in runtime metadata via `inspect` or `__annotations__`.

## What Python Is Doing
1. **Annotation Storage**: When a function is defined, Python compiles its code and populates its `__annotations__` dictionary with the evaluated type objects:
   ```python
   execute_agent_tool.__annotations__
   # {'name': <class 'str'>, 'tool_fn': typing.Callable[[str], str], ...}
   ```
2. **Zero Runtime Overhead During Calls**: When `execute_agent_tool(...)` is invoked, Python performs zero type checking at the C-level bytecode interpreter. The argument values are pushed directly onto the stack. This ensures type hints introduce negligible runtime performance cost.
3. **PEP 563 & Postponed Evaluation**: In modern Python (or when using `from __future__ import annotations`), annotations are stored as strings rather than evaluated immediately, resolving forward reference problems (referencing a class before it is defined).

## Common Mistakes
1. **Expecting Python to Enforce Types at Runtime**: Assuming that declaring `age: int` prevents someone from passing `age = "thirty"`. Python will not stop them; you must use a tool like Pydantic or manual `isinstance` checks if runtime enforcement is required.
2. **Overusing `Any`**: Declaring `data: Any` or `def process(x: Any) -> Any:` whenever a type is complex. Overusing `Any` disables type checking completely, forfeiting all benefits of static typing.
3. **Confusing `Optional[T]` with Default Arguments**:
   `def query(limit: int = None):` has a default of `None`, but its type hint claims it is strictly an `int`! The correct annotation is `limit: int | None = None` (or `Optional[int] = None`).
4. **Using Lowercase `callable` vs `Callable` in older Python**: In Python 3.9+, use `from typing import Callable` for parameter types: `Callable[[int], str]`.

## Real-World Uses
- **FastAPI**: Inspects function parameter type hints (`query: str, limit: int = 10`) to automatically validate incoming JSON request bodies and generate interactive OpenAPI documentation.
- **Pydantic**: Validates nested configuration and data transfer objects across microservices based on field type annotations.
- **Refactoring Massive Codebases**: Running `mypy` across a million-line codebase allows renaming a method or changing a return type with complete confidence that every caller is updated.

## Connection to AI Agents
Type hints are the engine behind modern LLM Tool Calling:
- **Automatic Schema Generation**: When you give a Python function to an LLM agent (in OpenAI function calling, Anthropic tool use, or LangChain), the framework does not inspect the code logic; it inspects the **type hints** and **docstring** to construct the JSON schema sent to the model:
  ```json
  {
    "name": "search_database",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {"type": "string"},
        "limit": {"type": "integer"}
      },
      "required": ["query"]
    }
  }
  ```
- **Guarding Agent Outputs**: LLM text output is notoriously unstructured. Agent systems use type hints and Pydantic models to force LLMs to respond with guaranteed structured JSON objects.

## Practice
1. Open a terminal and write a function `format_user(name: str, age: int, is_admin: bool = False) -> str`. Inspect its `.__annotations__` attribute in the Python interactive shell.
2. Define a type alias `Coordinates = tuple[float, float]` and annotate a distance calculation function using it.
3. Annotate a function that takes a callback `on_complete: Callable[[str, int], None]` and executes it with a test string and number.

## Challenge
Design a typed Tool Definition decorator `@agent_tool`:
- It decorates a Python function.
- It inspects the decorated function's `__annotations__` to generate a lightweight dictionary representing its schema:
  `{"function": name, "params": {param_name: type_name}, "return": return_type_name}`.
- Attach this schema dictionary as an attribute `_agent_schema` on the decorated function, and verify it with a sample calculation tool.

## Summary
- Type hints bring clarity, IDE autocompletion, and static verification to Python without sacrificing dynamic flexibility.
- Python stores type hints in `__annotations__` without enforcing them at runtime by default.
- Modern Python uses built-in generics (`list[str]`, `dict[str, int]`) and the pipe union operator (`str | None`).
- `Callable`, `Literal`, and `TypedDict` enable strict behavioral and structural contracts.
- AI Agent frameworks leverage type annotations to dynamically translate Python functions into LLM tool calling schemas.

## What You Should Know Before Moving On
- How to annotate variables, function parameters, and return types.
- How to represent nullable or optional values using `str | None` or `Optional[str]`.
- How to annotate callbacks and tool functions using `Callable[[Args], Return]`.
- Why static type checkers (like mypy) are used alongside Python's dynamic runtime.
- How type annotations empower AI agent tool schema generation.
