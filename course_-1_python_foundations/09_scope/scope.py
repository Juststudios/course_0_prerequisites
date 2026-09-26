"""
Module 09: Scope, Lifetimes, and Closures — The LEGB Rule in Python
===================================================================

Scope determines where a variable or name is accessible and visible within your code.
Lifetimes determine when that variable is created in memory and when it is destroyed.
Mastering scope prevents accidental variable overwrites, mysterious UnboundLocalErrors,
and dangerous global state leaks. Furthermore, understanding enclosing scope unlocks
*closures*, a foundational design pattern used throughout AI agent architectures.

This lesson covers:
  1. Namespaces and Name Binding (locals(), globals())
  2. The LEGB Resolution Rule (Local, Enclosing, Global, Built-in)
  3. Variable Shadowing and Protecting Built-ins
  4. The `global` Statement and the UnboundLocalError Trap
  5. The `nonlocal` Statement in Nested Functions
  6. Closures: Encapsulating State Across Function Calls
  7. Inspecting Closures via `__closure__` and Cells
  8. Variable Lifetimes and Frame Garbage Collection
  9. Real-World AI Agent State Management using Closures
"""

import builtins
from typing import Any, Callable, Dict, List, Tuple

print("=" * 70)
print("MODULE 09: SCOPE AND LIFETIMES IN PYTHON")
print("=" * 70)


# ==============================================================================
# SECTION 1: Namespaces and Name Binding
# ==============================================================================
print("\n--- 1. Namespaces and Name Binding ---")

# In Python, variables are names that point to objects. A namespace is essentially
# a Python dictionary mapping variable names (strings) to their bound objects.

module_level_symbol = "Active Agent System"

def inspect_local_namespace(param_a: int, param_b: str) -> None:
    local_temp = [1, 2, 3]
    # locals() returns a dictionary of the current local scope:
    current_locals = locals()
    print("  Inside inspect_local_namespace:")
    for k, v in current_locals.items():
        print(f"    local name '{k}': {v} (type {type(v).__name__})")

inspect_local_namespace(42, "temperature")

# globals() returns the dictionary representing the module-level namespace:
print(f"  Checking globals() for 'module_level_symbol': {'module_level_symbol' in globals()}")


# ==============================================================================
# SECTION 2: The LEGB Resolution Rule
# ==============================================================================
print("\n--- 2. The LEGB Rule (Local -> Enclosing -> Global -> Built-in) ---")

# When Python encounters a variable name, it searches four scopes in order:
#   L: Local      (inside the current function)
#   E: Enclosing  (inside any outer enclosing function bodies)
#   G: Global     (at the top level of the current module file)
#   B: Built-in   (Python preloaded names: len, range, print, etc.)

scope_tier = "GLOBAL"

def outer_enclosing() -> None:
    scope_tier = "ENCLOSING"
    
    def inner_local() -> None:
        scope_tier = "LOCAL"
        print(f"  Inner function sees scope_tier: {scope_tier} (Found in LOCAL)")

    def inner_fallback() -> None:
        # Here scope_tier is not defined locally, so Python climbs up to ENCLOSING
        print(f"  Fallback function sees scope_tier: {scope_tier} (Found in ENCLOSING)")

    inner_local()
    inner_fallback()

outer_enclosing()
print(f"  Top-level code sees scope_tier: {scope_tier} (Found in GLOBAL)")

# Built-in scope:
print(f"  Built-in 'len' function resolution: {len} (Found in BUILT-IN)")


# ==============================================================================
# SECTION 3: Shadowing and Protecting Built-ins
# ==============================================================================
print("\n--- 3. Shadowing Built-in Names ---")

# If you define a variable with the same name as a built-in, you "shadow" it,
# hiding the built-in within that scope.

def demonstrate_shadowing() -> None:
    # Shadowing the built-in `sum`
    sum = 100  # Local int variable shadows builtin sum()
    print(f"  Shadowed 'sum' value: {sum}")
    try:
        # Attempting to call the shadowed name raises TypeError: 'int' object is not callable
        sum([10, 20, 30])  # type: ignore
    except TypeError as exc:
        print(f"  Caught expected error from shadowing: {exc}")

    # You can still reach the original built-in via the `builtins` module:
    real_sum = builtins.sum([10, 20, 30])
    print(f"  Recovered builtins.sum(): {real_sum}")

demonstrate_shadowing()


# ==============================================================================
# SECTION 4: The `global` Keyword and the UnboundLocalError
# ==============================================================================
print("\n--- 4. The `global` Keyword and UnboundLocalError ---")

# Reading a global variable from inside a function is permitted without any keyword:
total_queries = 100

def read_global_queries() -> None:
    print(f"  Reading global queries: {total_queries}")

read_global_queries()

# BUT if you ASSIGN to a variable anywhere in a function, Python marks that name
# as LOCAL for the ENTIRE function during bytecode compilation.

def demonstrate_unbound_local_trap() -> None:
    counter = 50
    def broken_increment() -> None:
        try:
            # Python sees `counter = ...` on the next line and marks `counter` as LOCAL.
            # Thus, trying to evaluate `counter + 1` before assignment raises UnboundLocalError!
            print(f"Current counter: {counter}")
            # counter += 1  # Uncommenting this causes UnboundLocalError on the print above!
        except Exception as e:
            print("Error:", e)
    broken_increment()

demonstrate_unbound_local_trap()

# To explicitly write to a module-level global variable, use `global`:
agent_run_count = 0

def increment_global_run() -> None:
    global agent_run_count
    agent_run_count += 1
    print(f"  Incremented agent_run_count to: {agent_run_count}")

increment_global_run()
increment_global_run()

# ARCHITECTURAL NOTE:
# Overusing `global` makes code difficult to test, impossible to run concurrently,
# and vulnerable to race conditions. Prefer passing state explicitly or using closures!


# ==============================================================================
# SECTION 5: The `nonlocal` Keyword
# ==============================================================================
print("\n--- 5. The `nonlocal` Keyword in Nested Functions ---")

# `nonlocal` allows an inner function to rebind a variable that belongs to an
# outer enclosing function (not global).

def create_rate_limiter(max_calls: int) -> Callable[[], bool]:
    calls_made = 0  # Enclosing variable

    def allow_request() -> bool:
        nonlocal calls_made  # Binds to outer `calls_made`
        if calls_made < max_calls:
            calls_made += 1
            print(f"  [RateLimiter] Request permitted ({calls_made}/{max_calls})")
            return True
        else:
            print(f"  [RateLimiter] Rate limit exceeded ({calls_made}/{max_calls})!")
            return False

    return allow_request

limiter = create_rate_limiter(max_calls=2)
print("Testing limiter:")
limiter()
limiter()
limiter()  # Should fail


# ==============================================================================
# SECTION 6: Closures and Free Variables
# ==============================================================================
print("\n--- 6. Closures: Encapsulating State Across Calls ---")

# A CLOSURE is a function that retains access to variables from its lexical
# enclosing scope even after the outer function has finished executing and returned.

def make_prompt_formatter(prefix: str) -> Callable[[str], str]:
    """Factory creating customized prompt formatters."""
    # `prefix` is a 'free variable' captured by the inner function
    def formatter(content: str) -> str:
        return f"[{prefix.upper()}] {content.strip()}"
    return formatter

system_fmt = make_prompt_formatter("system")
user_fmt = make_prompt_formatter("user")

print(system_fmt("You are a helpful coding assistant."))
print(user_fmt("Explain the LEGB rule in Python."))


# ==============================================================================
# SECTION 7: Inspecting Closures via `__closure__`
# ==============================================================================
print("\n--- 7. Inspecting Closure Cells ---")

# Python stores captured variables in `__closure__` as a tuple of `cell` objects.
print("Inspecting system_fmt closure:")
if system_fmt.__closure__:
    for cell in system_fmt.__closure__:
        print(f"  Closure cell contents: {cell.cell_contents!r} (type: {type(cell.cell_contents).__name__})")
        print(f"  Free variable names in code object: {system_fmt.__code__.co_freevars}")


# ==============================================================================
# SECTION 8: Variable Lifetimes and Frame Teardown
# ==============================================================================
print("\n--- 8. Variable Lifetimes & Stack Frames ---")

# Local variables live only as long as the function execution frame is active.
# When a function returns, its frame is destroyed, and local objects are deallocated
# unless a closure or outer reference holds a reference to them.

class ResourceSentinel:
    def __init__(self, tag: str) -> None:
        self.tag = tag
        print(f"  [ALLOCATED] Resource: {self.tag}")

    def __del__(self) -> None:
        print(f"  [FREED] Resource: {self.tag}")

def temporary_scope_lifecycle() -> None:
    print("  Entering temporary function...")
    res = ResourceSentinel("TempDatabaseConnection")
    print(f"  Using resource: {res.tag}")
    print("  Exiting temporary function (frame will be popped)...")

temporary_scope_lifecycle()
print("  Now back in global scope: resource was cleaned up automatically.")


# ==============================================================================
# SECTION 9: Real-World AI Agent State Management using Closures
# ==============================================================================
print("\n--- 9. Production AI Agent Session State Manager ---")

# Instead of leaking session data into global variables, we use a closure
# to build an isolated, stateful agent session tracker.

def create_agent_session(session_id: str, max_token_budget: int) -> Dict[str, Callable[..., Any]]:
    """Create an isolated, stateful session manager for an AI agent conversation."""
    messages: List[Dict[str, str]] = []
    tokens_consumed: int = 0
    turns: int = 0

    def add_message(role: str, content: str, tokens: int) -> bool:
        nonlocal tokens_consumed, turns
        if tokens_consumed + tokens > max_token_budget:
            print(f"  [Session {session_id}] REJECTED: Budget exceeded ({tokens_consumed + tokens}/{max_token_budget})")
            return False
        
        messages.append({"role": role, "content": content})
        tokens_consumed += tokens
        turns += 1
        print(f"  [Session {session_id}] Added {role} turn ({tokens} toks). Total: {tokens_consumed}/{max_token_budget}")
        return True

    def get_history() -> List[Dict[str, str]]:
        # Return shallow copy to prevent external mutation
        return list(messages)

    def get_stats() -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "turns": turns,
            "tokens_consumed": tokens_consumed,
            "remaining_budget": max_token_budget - tokens_consumed
        }

    return {
        "add_message": add_message,
        "get_history": get_history,
        "get_stats": get_stats
    }

# Create two completely independent agent sessions:
session_alpha = create_agent_session("alpha", max_token_budget=100)
session_beta = create_agent_session("beta", max_token_budget=50)

print("\nOperating on Session Alpha:")
session_alpha["add_message"]("user", "Hello agent!", 30)
session_alpha["add_message"]("assistant", "How can I help you?", 40)
session_alpha["add_message"]("user", "Write a long essay", 50)  # Exceeds 100 budget!

print("\nOperating on Session Beta (Completely isolated state):")
session_beta["add_message"]("user", "Short ping", 10)

print("\nAlpha stats:", session_alpha["get_stats"]())
print("Beta stats: ", session_beta["get_stats"]())

print("\n" + "=" * 70)
print("MODULE 09 LESSON COMPLETE — ALL SCOPE SAMPLES EXECUTED SUCCESSFULLY")
print("=" * 70)
