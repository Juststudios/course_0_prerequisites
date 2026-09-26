"""
Module 19: Decorators and Closures
==================================

This lesson explores function decorators in Python from first principles to
advanced agent-oriented metaprogramming patterns.

Topics covered:
  1. First-Class Functions: Passing, assigning, and returning callables
  2. Lexical Closures: Capturing state in inner functions
  3. The Basic Decorator Pattern: Manual wrapping vs `@` syntax
  4. Universal Argument Forwarding (*args, **kwargs) and Return Values
  5. Preserving Metadata with `functools.wraps`
  6. Parameterized Decorators (Decorator Factories with Arguments)
  7. Stacking Multiple Decorators and Execution Ordering
  8. AI Agent Application: Tool Registry & Network Retry Decorators
"""

import functools
import time
from typing import Any, Callable, Dict, List, Optional


# =====================================================================
# 1. First-Class Functions: Passing, Assigning, and Returning Callables
# =====================================================================
print("=" * 70)
print("1. FIRST-CLASS FUNCTIONS IN PYTHON")
print("=" * 70)

# In Python, functions are first-class citizens: they are regular objects.
def format_shout(text: str) -> str:
    """Returns text in uppercase with exclamation points."""
    return f"{text.upper()}!!!"

def format_whisper(text: str) -> str:
    """Returns text in lowercase with ellipses."""
    return f"{text.lower()}..."

# Functions can be assigned to variables:
alias_func = format_shout
print(f"Calling via variable alias: {alias_func('hello world')}")

# Functions can be passed into other functions as arguments:
def apply_formatter(formatter: Callable[[str], str], message: str) -> str:
    print(f"  Applying formatter: {formatter.__name__}")
    return formatter(message)

print(apply_formatter(format_whisper, "SYSTEM RUNNING NORMALLY"))


# =====================================================================
# 2. Lexical Closures: Capturing State in Inner Functions
# =====================================================================
print("\n" + "=" * 70)
print("2. LEXICAL CLOSURES: CAPTURING FREE VARIABLES")
print("=" * 70)

# A closure occurs when an inner function references variables from its
# enclosing scope, and that inner function is returned and used elsewhere.

def make_rate_limiter(max_calls_per_second: int):
    """
    Outer factory function. Returns an inner function that 'remembers'
    max_calls_per_second even after make_rate_limiter returns.
    """
    call_count = 0  # Captured variable stored in closure cell

    def check_limit() -> bool:
        nonlocal call_count
        call_count += 1
        print(f"  [RateLimiter] Call #{call_count} / Limit {max_calls_per_second}")
        return call_count <= max_calls_per_second

    return check_limit

limiter = make_rate_limiter(max_calls_per_second=2)
print("Testing closure invocation:")
print("  Call 1 allowed?", limiter())
print("  Call 2 allowed?", limiter())
print("  Call 3 allowed?", limiter())  # Exceeds limit


# =====================================================================
# 3. Basic Decorator: Manual Wrapping vs `@` Syntactic Sugar
# =====================================================================
print("\n" + "=" * 70)
print("3. BASIC DECORATOR: MANUAL WRAPPING VS `@` SYNTAX")
print("=" * 70)

def simple_logger(original_func: Callable) -> Callable:
    """A minimal decorator that logs before and after calling a function."""
    def wrapper():
        print(f"  >>> [LOG START] Entering {original_func.__name__}")
        original_func()
        print(f"  <<< [LOG END] Exited {original_func.__name__}")
    return wrapper

def ping_server():
    print("      [SERVER] Ping received. Status: 200 OK.")

# Approach A: Manual higher-order function reassignment
print("Approach A: Manual Reassignment:")
wrapped_ping = simple_logger(ping_server)
wrapped_ping()

# Approach B: Using Python's @ decorator syntax
print("\nApproach B: Using @ Syntactic Sugar:")
@simple_logger
def health_check():
    print("      [HEALTH] All internal subsystems operating within parameters.")

health_check()


# =====================================================================
# 4. Universal Forwarding (*args, **kwargs) and Return Values
# =====================================================================
print("\n" + "=" * 70)
print("4. UNIVERSAL ARGUMENT FORWARDING (*args, **kwargs) & RETURN VALUES")
print("=" * 70)

def audit_trail(func: Callable) -> Callable:
    """
    Universal decorator that forwards all arguments and preserves return values.
    """
    def wrapper(*args, **kwargs):
        print(f"  [AUDIT] Calling '{func.__name__}' with args={args}, kwargs={kwargs}")
        # Always store the result of calling the original function
        result = func(*args, **kwargs)
        print(f"  [AUDIT] '{func.__name__}' returned: {result}")
        # Always return the result back to the caller
        return result
    return wrapper

@audit_trail
def compute_action_score(action_name: str, confidence: float, boost: float = 1.0) -> float:
    return confidence * boost

final_score = compute_action_score("inspect_code", confidence=0.85, boost=1.2)
print(f"Final score received by caller: {final_score:.4f}")


# =====================================================================
# 5. Preserving Metadata with `functools.wraps`
# =====================================================================
print("\n" + "=" * 70)
print("5. PRESERVING METADATA WITH `functools.wraps`")
print("=" * 70)

# Without @functools.wraps, functions lose their __name__ and __doc__.
def naive_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@naive_decorator
def calculate_pi_approximation() -> float:
    """Approximates pi using Gregory-Leibniz series."""
    return 3.14159

print("Without functools.wraps:")
print(f"  Function name: {calculate_pi_approximation.__name__} (Lost original name!)")
print(f"  Docstring:     {calculate_pi_approximation.__doc__} (Lost original docstring!)")

# With @functools.wraps:
def proper_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@proper_decorator
def calculate_euler_approximation() -> float:
    """Approximates Euler's number e."""
    return 2.71828

print("\nWith functools.wraps:")
print(f"  Function name: {calculate_euler_approximation.__name__} (Preserved!)")
print(f"  Docstring:     {calculate_euler_approximation.__doc__} (Preserved!)")


# =====================================================================
# 6. Parameterized Decorators (Decorator Factories)
# =====================================================================
print("\n" + "=" * 70)
print("6. PARAMETERIZED DECORATORS (DECORATOR FACTORIES)")
print("=" * 70)

# When a decorator accepts its own arguments, we need a 3-layer nested structure:
# Layer 1: Factory that accepts configuration parameters
# Layer 2: Decorator that accepts the target function
# Layer 3: Wrapper that intercepts runtime invocations

def repeat_action(times: int):
    """
    Decorator factory: Runs a function `times` times and returns the final result.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_result = None
            for iteration in range(1, times + 1):
                print(f"  [REPEAT] Iteration {iteration}/{times} of {func.__name__}...")
                last_result = func(*args, **kwargs)
            return last_result
        return wrapper
    return decorator

@repeat_action(times=3)
def send_heartbeat():
    print("    -> Heartbeat ping sent to central coordinator.")
    return "HEARTBEAT_ACK"

result = send_heartbeat()
print(f"Repeated execution result: {result}")


# =====================================================================
# 7. Stacking Multiple Decorators and Execution Ordering
# =====================================================================
print("\n" + "=" * 70)
print("7. STACKING MULTIPLE DECORATORS: EXECUTION ORDER")
print("=" * 70)

def tag_bold(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def tag_italic(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

# Stacking order:
#   @tag_bold
#   @tag_italic
# is equivalent to: greeting = tag_bold(tag_italic(greeting))
@tag_bold
@tag_italic
def render_greeting(name: str) -> str:
    return f"Hello, {name}!"

rendered = render_greeting("Agent-007")
print(f"Stacked decorator output: {rendered}")


# =====================================================================
# 8. AI Agent Application: Tool Registry & Retry Logic
# =====================================================================
print("\n" + "=" * 70)
print("8. AI AGENT APPLICATION: TOOL REGISTRY & RETRY LOGIC")
print("=" * 70)

AGENT_TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def agent_tool(name: str, description: str):
    """Registers an agent tool with metadata and provides execution logging."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            print(f"  [TOOL EXEC] Invoking '{name}' with args={args}")
            res = func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            print(f"  [TOOL EXEC] '{name}' finished in {elapsed_ms:.2f}ms")
            return res

        AGENT_TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "callable": wrapper,
        }
        return wrapper
    return decorator

def retry_on_failure(max_retries: int = 2):
    """Retries an operation if it raises an exception."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    print(f"    [RETRY] Attempt {attempt} failed ({exc}). Retrying...")
                    if attempt == max_retries:
                        raise
        return wrapper
    return decorator

# Applying both decorators to an agent tool
@agent_tool(name="fetch_web_data", description="Fetches web documents via URL")
@retry_on_failure(max_retries=3)
def fetch_web_data(url: str, fail_count: int = 1) -> str:
    """Simulates an intermittently failing web request."""
    # Using function attribute as a call counter
    if not hasattr(fetch_web_data, "_calls"):
        fetch_web_data._calls = 0
    fetch_web_data._calls += 1

    if fetch_web_data._calls <= fail_count:
        raise ConnectionResetError(f"Temporary socket drop for {url}")
    return f"<html>Content of {url}</html>"

print("Registered Tools in Agent System:")
for tool_key, tool_info in AGENT_TOOL_REGISTRY.items():
    print(f"  * {tool_key}: {tool_info['description']}")

print("\nInvoking registered tool with simulated transient failure:")
tool_fn = AGENT_TOOL_REGISTRY["fetch_web_data"]["callable"]
content = tool_fn("https://api.agentic.ai/docs", fail_count=1)
print(f"Tool execution returned: {content}")

print("\n" + "=" * 70)
print("Module 19 lesson completed successfully!")
print("=" * 70)
