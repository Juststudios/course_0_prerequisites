# Scope, Namespaces, and Lifetimes in Python

## What You Will Learn
In this module, you will master how Python resolves variable names and manages object lifetimes:
- The fundamental concept of namespaces as dynamic mappings from names to objects.
- How Python inspects environments at runtime using `locals()` and `globals()`.
- The LEGB resolution hierarchy: **L**ocal, **E**nclosing, **G**lobal, and **B**uilt-in scopes.
- How variable shadowing occurs and how to safeguard Python's built-in namespace.
- Why modifying global state from within a local function requires the explicit `global` keyword.
- The root cause and mechanics of Python's dreaded `UnboundLocalError`.
- How nested functions access and modify outer state using the `nonlocal` keyword.
- How closures encapsulate persistent state across function calls without global variables or classes.
- How Python tracks closed-over state inside cell objects via `__closure__`.
- How variable lifetimes, stack frames, and reference counting dictate garbage collection.
- How autonomous AI agents use scoped namespaces and closures to isolate conversational memory, manage multi-tenant sessions, and maintain stateful tool registries.

## Prerequisites
Before starting this module, you should understand:
- Module 03: Variables, primitive types, and references.
- Module 07: Control flow constructs (`if`, `for`, `while`, and indentation blocks).
- Module 08: Defining functions, parameter passing, return values, and higher-order functions.

## The Problem
When programs grow beyond trivial single-file scripts, managing variable names becomes one of computing's greatest challenges. Consider what happens when:
1. Two different functions both need an index variable named `i` or a temporary buffer named `data`. If all variables lived in a single shared global pool, one function would silently overwrite the other function's data, triggering catastrophic race conditions and corrupted calculations.
2. A programmer creates a variable named `sum = 10` or `list = [1, 2, 3]`. Suddenly, calling the built-in `sum([1, 2])` or `list("abc")` raises a cryptic `TypeError: 'int' object is not callable`.
3. A function attempts to read a global configuration counter and increment it, only to crash immediately with `UnboundLocalError: local variable 'counter' referenced before assignment`.
4. An AI agent running concurrent conversations leaks chat history from User Alice into the prompt context of User Bob because the messages were stored in a mutable module-level global list.

Without rigorous boundaries governing where names are visible, where they can be reassigned, and when they are destroyed, programs become hopelessly brittle. Python solves this through lexical scoping and namespace hierarchies.

## Key Terminology
- **Namespace**: A dictionary-like mapping from symbol names (strings) to memory references (objects). Examples include the built-in namespace, module global namespace, and function local namespace.
- **Scope**: The textual (lexical) region of a Python program where a particular namespace is directly accessible without explicit prefixing.
- **LEGB Rule**: The four-tier search sequence Python follows when resolving an unqualified variable name: Local -> Enclosing -> Global -> Built-in.
- **Shadowing**: When a variable declared in an inner scope shares the name of a variable in an outer or built-in scope, effectively hiding the outer name within the inner region.
- **Global Scope**: The top-level namespace of the currently executing module file, accessible throughout that module and inspected via `globals()`.
- **Enclosing Scope (Nonlocal)**: The namespace of an outer enclosing function wrapping an inner nested function.
- **Local Scope**: The temporary namespace created when a function is called, storing its arguments and locally assigned variables, inspected via `locals()`.
- **Built-in Scope**: The outermost preloaded Python namespace containing built-in exceptions and functions like `print()`, `len()`, `range()`, and `open()`.
- **Closure**: A function object that retains access to variables from its lexical enclosing scope even after the outer function has completed execution and returned.
- **Cell Object**: The internal Python C-level structure used to store a shared reference to a variable captured by a closure (`func.__closure__`).
- **Lifetime**: The span of time between when an object or binding is allocated in memory and when Python's garbage collector deallocates it.

## Intuition
Imagine a student sitting in a classroom inside a university building:
- **Local Scope (Desk)**: You have a notepad on your desk. When you need a pencil, you check your desk first. Everything on your desk belongs to you, and when you leave the room at the end of class, your desk is cleared.
- **Enclosing Scope (Classroom Whiteboard)**: If you need an assignment formula not on your desk, you look up at the whiteboard in your room. Everyone in this room can see it, but people in other rooms cannot.
- **Global Scope (Building Bulletin Board)**: If you need the academic calendar, you step into the hallway and check the building's central bulletin board. Any classroom in the building can read this board.
- **Built-in Scope (The Laws of Physics & Math)**: Fundamental constants (like $\pi$) or standard dictionary definitions apply universally everywhere on Earth without needing to be posted on any board.

When looking for an answer, you search from the most immediate to the most universal: **Desk -> Classroom -> Building -> Universal Laws** (LEGB). You never start at the universal laws if the answer is right on your desk!

## Concept

### 1. The LEGB Resolution Pipeline
When Python encounters an expression like `result = x + 1`, it must locate what object `x` refers to. It searches four distinct tiers in strict order:
1. **L (Local)**: Python checks the local execution frame of the active function. If `x` was assigned inside this function, that local object is used.
2. **E (Enclosing)**: If not found in Local and this function is nested inside another function, Python inspects the enclosing function's namespace. If nested multiple levels deep, Python climbs outward frame by frame.
3. **G (Global)**: If not found in any enclosing scope, Python inspects the module-level namespace (the file where the function was defined).
4. **B (Built-in)**: If not found globally, Python checks the `builtins` module. If `x` is still not found, Python raises a `NameError: name 'x' is not defined`.

```
+-------------------------------------------------------------+
| BUILT-IN SCOPE (len, range, print, Exception, int, dict...)  |
|  +-------------------------------------------------------+  |
|  | GLOBAL SCOPE (Module-level constants, classes, funcs)  |  |
|  |  +-------------------------------------------------+  |  |
|  |  | ENCLOSING SCOPE (Outer function enclosing variables) |  |
|  |  |  +-------------------------------------------+  |  |  |
|  |  |  | LOCAL SCOPE (Inner function variables)     |  |  |  |
|  |  |  +-------------------------------------------+  |  |  |
|  |  +-------------------------------------------------+  |  |
|  +-------------------------------------------------------+  |
+-------------------------------------------------------------+
   Resolution Search Order: Local -> Enclosing -> Global -> Built-in
```

### 2. Name Binding and the Read vs. Write Asymmetry
In Python, **reading** a variable climbs up the LEGB chain automatically. However, **writing (assigning)** a variable defaults strictly to the current **Local** scope!
- If you assign `x = 5` inside a function, Python treats `x` as a brand-new local variable, even if an `x` exists globally.
- If you intend to modify an existing global variable from inside a function, you must declare `global x`.
- If you intend to modify an enclosing variable from inside a nested function, you must declare `nonlocal x`.

### 3. The Mechanics of Closures
When an outer function defines a local variable and returns an inner function that references that variable, a **closure** is formed. Even though the outer function has finished executing and its stack frame has been destroyed, Python moves the referenced variable into a heap-allocated **cell object**. The inner function keeps a reference to this cell in its `__closure__` attribute, allowing it to remember and update state across repeated invocations.

## Syntax

```python
# 1. Inspecting Namespaces
current_locals = locals()    # Dictionary of local scope bindings
module_globals = globals()   # Dictionary of module global scope bindings

# 2. Reading vs Writing Global Scope
app_config = {"version": "1.0", "mode": "production"}
request_counter = 0

def log_request():
    # Reading global dictionary: No keyword required (dictionary is mutated in place)
    app_config["last_accessed"] = "2026-09-21"
    
    # Rebinding global integer: Requires explicit 'global' keyword
    global request_counter
    request_counter += 1

# 3. Enclosing Scope & 'nonlocal'
def make_counter(start: int = 0):
    count = start  # Enclosing variable
    
    def step(increment: int = 1) -> int:
        nonlocal count  # Binds 'count' to the enclosing scope variable
        count += increment
        return count
        
    return step

# 4. Closures with Encapsulated State
counter_a = make_counter(10)
counter_b = make_counter(100)
print(counter_a())  # 11
print(counter_b())  # 101 (completely independent state!)
```

## Example

```python
"""
Real-world AI Agent Token Budget Tracker utilizing LEGB resolution and closures.
"""
from typing import Callable, Dict, Tuple

# Global Scope: Default configuration for all agent runs
DEFAULT_MODEL = "claude-3-5-sonnet"
GLOBAL_AUDIT_LOG: list[str] = []


def create_token_guard(max_budget: int) -> Tuple[Callable[[int, str], bool], Callable[[], Dict[str, int]]]:
    """
    Creates an agent token guard that encapsulates token usage without global variables.
    Demonstrates Enclosing scope, 'nonlocal' rebinding, and closure state isolation.
    """
    # Enclosing Scope variables
    consumed_tokens = 0
    call_count = 0

    def consume(tokens: int, operation_name: str) -> bool:
        nonlocal consumed_tokens, call_count  # Rebinds enclosing variables
        
        # Accessing Global Scope (GLOBAL_AUDIT_LOG is read/mutated via reference)
        GLOBAL_AUDIT_LOG.append(f"Operation '{operation_name}' requested {tokens} tokens.")
        
        # Check against enclosing budget
        if consumed_tokens + tokens > max_budget:
            GLOBAL_AUDIT_LOG.append(f"REJECTED: Budget exceeded ({consumed_tokens + tokens} > {max_budget})")
            return False
            
        consumed_tokens += tokens
        call_count += 1
        return True

    def get_metrics() -> Dict[str, int]:
        # Reads enclosing scope variables without mutating them (no nonlocal needed)
        return {
            "consumed": consumed_tokens,
            "remaining": max_budget - consumed_tokens,
            "total_calls": call_count
        }

    return consume, get_metrics


# Demonstration
print("=== Initializing Agent Guards ===")
guard_agent_1, stats_agent_1 = create_token_guard(max_budget=500)
guard_agent_2, stats_agent_2 = create_token_guard(max_budget=200)

# Agent 1 operations
success_1 = guard_agent_1(150, "Retrieve Context Documents")
success_2 = guard_agent_1(300, "Generate Multi-Step Plan")
success_3 = guard_agent_1(100, "Execute Tool Call")  # Exceeds budget (450 + 100 > 500)

print(f"Agent 1 Op 1 approved: {success_1}")
print(f"Agent 1 Op 2 approved: {success_2}")
print(f"Agent 1 Op 3 approved: {success_3} (Exceeded budget)")
print(f"Agent 1 Stats: {stats_agent_1()}")

# Agent 2 operations (Independent closure state!)
guard_agent_2(120, "Summarize User Query")
print(f"Agent 2 Stats: {stats_agent_2()}")
print(f"Audit log entries recorded: {len(GLOBAL_AUDIT_LOG)}")
```

## Line-by-Line Explanation
1. `DEFAULT_MODEL = "claude-3-5-sonnet"`: Declares a string literal in the module's **Global** scope namespace.
2. `GLOBAL_AUDIT_LOG: list[str] = []`: Creates a mutable list object in the module's **Global** namespace.
3. `def create_token_guard(max_budget: int) -> ...`: Defines a factory function. When called, a new local frame is created.
4. `consumed_tokens = 0` and `call_count = 0`: Variables bound inside `create_token_guard`'s local scope.
5. `def consume(tokens: int, operation_name: str) -> bool:`: Defines an inner function nested inside `create_token_guard`.
6. `nonlocal consumed_tokens, call_count`: Tells Python that assignments to these two names inside `consume` refer to the variables in the **Enclosing** scope (`create_token_guard`), rather than creating new local variables.
7. `GLOBAL_AUDIT_LOG.append(...)`: Python uses the LEGB rule: `GLOBAL_AUDIT_LOG` is not found locally or enclosingly, so it finds it in the **Global** scope and invokes its `.append()` method.
8. `if consumed_tokens + tokens > max_budget:`: Python reads `consumed_tokens` and `max_budget` from the **Enclosing** scope.
9. `def get_metrics() -> Dict[str, int]:`: Defines a second inner function sharing the same enclosing lexical environment.
10. `return consume, get_metrics`: Returns the two inner function objects as a tuple. Although `create_token_guard` completes here, Python preserves `consumed_tokens`, `call_count`, and `max_budget` inside heap-allocated cell objects attached to both returned functions.
11. `guard_agent_1, stats_agent_1 = create_token_guard(500)`: Creates closure instance 1 with its own unique cell objects.
12. `guard_agent_2, stats_agent_2 = create_token_guard(200)`: Creates closure instance 2 with completely separate, isolated cell objects.

## What Python Is Doing
Under the hood, Python resolves names using a combination of compile-time static analysis and runtime bytecode instructions:
1. **Compile-Time Scope Classification**: When Python compiles a function body into a code object (`PyCodeObject`), it analyzes every assignment statement.
   - If a name is assigned anywhere in the function (and not declared `global` or `nonlocal`), Python marks that name as **LOCAL** in the code object's symbol table.
   - Local variables are assigned fast fixed-array indices accessed via the high-speed bytecode instruction `LOAD_FAST <index>` and `STORE_FAST <index>`.
   - Global variables use dictionary lookups via `LOAD_GLOBAL <name_index>` and `STORE_GLOBAL <name_index>`.
2. **The UnboundLocalError Trap**: Because local classification happens at compile time across the whole function body, if you write:
   ```python
   x = 10
   def func():
       print(x)  # Compile-time analysis saw 'x = 20' below!
       x = 20
   ```
   Python compiles the entire function knowing `x` is local. At line 3, it attempts `LOAD_FAST` for `x`. Because line 4 hasn't executed yet, the local slot is empty (NULL pointer in CPython), and Python immediately raises `UnboundLocalError: local variable 'x' referenced before assignment`. It does **not** fall back to global `x = 10`!
3. **Closures and Cell Objects**: When a variable is accessed across enclosing scopes, CPython wraps the variable inside a `PyCellObject`.
   - When the inner function executes, it uses `LOAD_DEREF` and `STORE_DEREF` to dereference the pointer inside the cell.
   - You can inspect this directly in Python: `func.__closure__[0].cell_contents`.

## Common Mistakes

### 1. The UnboundLocalError Rebinding Trap
- **Bad**:
  ```python
  counter = 0
  def increment():
      counter += 1  # Expands to counter = counter + 1
  ```
- **Why**: Python sees assignment `counter = ...`, categorizes `counter` as local, but evaluates the right-hand side `counter + 1` before the assignment has happened.
- **Fix**: Declare `global counter` or wrap in a state object/closure.

### 2. Shadowing Python Built-in Names
- **Bad**:
  ```python
  def calculate_stats(list, max):
      sum = 0
      for item in list:
          sum += item
      return sum, max
  ```
- **Why**: Naming variables `list`, `max`, or `sum` shadows Python's built-in constructors and functions. Subsequent calls to `list()` or `sum()` in that scope will crash.
- **Fix**: Use descriptive, non-colliding names: `items`, `maximum_val`, `total_sum`.

### 3. Loop Variable Leaks in Global/Function Scope
- In Python, `for` loops do **not** create their own local scope!
  ```python
  for i in range(5):
      pass
  print(i)  # Prints 4! Variable 'i' leaked into the outer namespace.
  ```
- In functions or modules, loop variables persist after loop completion. If you reuse `i` later without re-initializing, stale state can cause logic bugs.

### 4. Late Binding in Closures (The Lambda in Loop Bug)
- **Bad**:
  ```python
  handlers = [lambda: i for i in range(3)]
  print([h() for h in handlers])  # Prints [2, 2, 2], NOT [0, 1, 2]!
  ```
- **Why**: The lambda functions capture the variable `i`, not the value of `i` at the moment of creation. When the lambdas are called later, `i` has resolved to its final value `2`.
- **Fix**: Use default argument binding to freeze the value: `lambda i=i: i`.

## Real-World Uses
- **Factory Functions**: Creating customized worker functions configured with specific API keys, rate limits, or base URLs without constructing full object-oriented classes.
- **Function Decorators**: Capturing wrapped functions and measuring execution latency, retrying failed operations, or authenticating requests.
- **Multi-Tenant State Isolation**: In web applications and SaaS backends, closures ensure session state or request metadata cannot leak between concurrent client requests.
- **Plugin Registries**: Safe plugin systems that provide third-party extensions with restricted, sandboxed namespaces rather than direct access to system internals.

## Connection to AI Agents
1. **Autonomous Tool Sandboxing**: When an AI agent executes generated Python code or calls external tools, it runs them in an isolated namespace using `exec(code, sandboxed_globals, local_namespace)`. This prevents untrusted LLM-generated code from overwriting system globals, importing unauthorized modules, or corrupting agent state.
2. **Conversation Session Management**: Agent runtimes use factory functions and closures to instantiate session listeners. Each user conversation gets its own closure capturing message history, avoiding global memory contamination across users.
3. **Dynamic Prompt Context Formatting**: Agents often dynamically bind system instructions and available tool schemas into closure functions, allowing prompt compilers to format queries without maintaining bulky global configuration objects.

## Practice
1. Inspect your Python environment by printing the keys of `locals()` inside a small function and comparing them to `globals().keys()`.
2. Write an outer function `make_multiplier(n: int)` that returns an inner function that multiplies its argument by `n`. Inspect the inner function's `__closure__` attribute to observe the cell object holding `n`.
3. Create a function with a nested function where the inner function modifies a counter in the outer function using `nonlocal`. Verify that calling the inner function multiple times increments the counter correctly.

## Challenge
Implement an autonomous agent rate limiter closure `create_rate_limiter(max_calls: int, window_seconds: float)`:
- The closure must track the timestamps of all tool calls made by an agent.
- On each call, it prunes timestamps older than `current_time - window_seconds`.
- If the count of active calls in the window exceeds `max_calls`, it returns `(False, retry_after_seconds)`.
- Otherwise, it records the new call timestamp and returns `(True, 0.0)`.
- Ensure all tracking state is strictly encapsulated in enclosing scope variables with no global variables or external class dependencies.

## Summary
- Namespaces are dynamic mappings connecting symbol names to Python objects.
- Python resolves unqualified names using the LEGB hierarchy: Local -> Enclosing -> Global -> Built-in.
- Assignment defaults to creating or modifying a name in the current Local scope.
- Use `global <name>` to rebind a module-level variable inside a function.
- Use `nonlocal <name>` to rebind an outer function's variable inside a nested function.
- Closures bind inner functions to variables in their enclosing lexical environment, storing references in heap-allocated cell objects (`__closure__`).
- For loops do not introduce new scopes; variables bound in loops persist in the enclosing function or module namespace.

## What You Should Know Before Moving On
Before advancing to Module 10 (Errors and Exceptions), ensure you can:
- Mentally trace the resolution of any variable using the LEGB rule without executing Python.
- Explain precisely why `UnboundLocalError` occurs and how to fix it cleanly.
- Choose appropriately between `global`, `nonlocal`, and closure patterns without relying on global state.
- Inspect and explain how closures retain state across calls using Python's cell objects.
- Avoid variable shadowing bugs that hide Python built-in names like `list`, `dict`, and `sum`.
