from pathlib import Path

BASE_DIR = Path("/home/settings/Documents/pearl/course_0_prerequisites")

def write_file(path_str, content):
    p = BASE_DIR / path_str
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        f.write(content.strip() + "\n")

# --- 01 PYTHON FOUNDATIONS ---
write_file("01_python_foundations/README.md", """
# Module 0.1: Functions and Callables

## Terminology
* **Function:** A reusable block of code.
* **Parameter:** A variable defined in the function signature.
* **Argument:** The actual value passed to the function.
* **Return Value:** The output of the function.
* **Callable:** Any object that can be invoked using parentheses `()`.
* **Callback:** A function passed as an argument to be executed later.
* **First-Class Object:** In Python, functions can be assigned to variables and passed around.

## Intuition
Functions map inputs to outputs. A callable is anything that acts like a function.

## Why it Exists
Without functions, code repeats. Without callables, we cannot build dynamic systems like Tool Registries.

## How it Works / Code Walkthrough

```text
LLM
 ↓
Tool name
 ↓
Tool arguments
 ↓
Python callable
 ↓
Result
```

## Hermes / Agent Connection
A tool in an AI agent is simply represented as a callable Python function. The LLM predicts the tool name and arguments, and the agent runtime invokes the callable.
""")

write_file("01_python_foundations/functions.py", """
# Functions and Callables Example

def add(a: int, b: int) -> int:
    # 'a' and 'b' are parameters
    return a + b

# In Python, functions are first-class objects.
# We can store them in a dictionary (a registry).
tools = {
    "add": add
}

# The LLM outputs the string "add" and the arguments 2, 3.
# We fetch the callable from the registry and execute it.
result = tools["add"](2, 3)
print(f"Result of tool execution: {result}")
""")

# --- 02 TYPE HINTS ---
write_file("02_type_hints/README.md", """
# Module 0.3: Type Hints

## Terminology
* **Type Annotation:** Hints describing expected data types.
* **Return Type:** The type a function returns.
* **Optional:** A value that could be of a type, or None.
* **Any:** An untyped value.
* **Callable:** A type hint for a function.

## Intuition
Type hints act as documentation that the IDE and validation tools can read. 

## Code Walkthrough
```python
Callable[[str], int]
```
This means a function that takes a single `str` argument and returns an `int`.

## Hermes / Agent Connection
Type information helps generate API contracts and tool schemas automatically. For instance, Pydantic uses type hints to build JSON schemas sent to the LLM. Type hints do *not* enforce runtime types by themselves in standard Python.
""")

write_file("02_type_hints/examples.py", """
from typing import Optional, Any, Callable

# handler is a Callable taking a str and returning an int
def process(items: list[str], handler: Callable[[str], int]) -> dict[str, int]:
    # We iterate over items and apply the callback handler
    return {
        item: handler(item)
        for item in items
    }

def count_chars(text: str) -> int:
    return len(text)

result = process(["agent", "llm", "tool"], count_chars)
print(result)
""")

# --- 03 ASYNC PYTHON ---
write_file("03_async_python/README.md", """
# Module 0.4: Async/Await

## Terminology
* **Synchronous:** Code executes line by line, blocking execution while waiting.
* **Asynchronous:** Code can pause and yield control while waiting for I/O.
* **Coroutine:** An async function.
* **Event Loop:** The engine running coroutines.

## Mathematical Connection - Concurrency
If three independent API calls each take 2 seconds:
Sequential execution: `2 + 2 + 2 = 6 seconds`
Concurrent execution: `max(2, 2, 2) = 2 seconds`

## Agent Connection
Agents constantly make network requests to LLM APIs, databases, and external tools. Doing this synchronously freezes the runtime. Async allows an agent to process other tasks while waiting for the LLM.
""")

write_file("03_async_python/async_basics.py", """
import asyncio
import time

async def fetch_data(url: str) -> str:
    # await yields control back to the event loop while waiting
    await asyncio.sleep(0.1) 
    return f"Data from {url}"

async def main():
    start = time.time()
    # Execute concurrently
    results = await asyncio.gather(
        fetch_data("api1"),
        fetch_data("api2"),
        fetch_data("api3")
    )
    end = time.time()
    print(f"Results: {results}")
    print(f"Time taken: {end - start:.2f}s (Much less than 0.3s!)")

if __name__ == "__main__":
    asyncio.run(main())
""")

# --- 04 CONTEXT MANAGEMENT & CONTEXTVARS ---
write_file("04_context_management/README.md", """
# Module 0.5 & 0.6: Context Managers and ContextVars

## Terminology
* **Resource:** A file, database connection, or lock.
* **Context Manager:** An object defining setup (`__enter__`) and teardown (`__exit__`).
* **ContextVar:** Stores context-local state across the call chain.

## Intuition
Context managers ensure you clean up your mess (like closing files). 
ContextVars allow you to pass a "backpack" of state down a deep function chain without having to explicitly pass it as a parameter every time.

## Agent Connection
Request A might be in the profile `HERMES_HOME = profile_A`, while concurrent Request B is `profile_B`. Using global variables would cause Request B to overwrite Request A's state. ContextVars safely isolate this state per async task.
""")

write_file("04_context_management/contextvars_example.py", """
import contextvars
import asyncio

# Keep the request ID in task-local context so functions
# deeper in the call chain can access it without passing
# the ID through every function parameter.
request_id = contextvars.ContextVar("request_id", default="anonymous")

async def deep_function():
    # We access the ContextVar without it being passed to us
    print(f"Deep function running for request: {request_id.get()}")

async def handle_request(req_id: str):
    # Set the ContextVar for this specific async task
    token = request_id.set(req_id)
    await asyncio.sleep(0.1)
    await deep_function()
    request_id.reset(token)

async def main():
    # Run two requests concurrently. Notice how their state doesn't mix!
    await asyncio.gather(
        handle_request("req-123"),
        handle_request("req-456")
    )

if __name__ == "__main__":
    asyncio.run(main())
""")

print("Python modules generated.")
