"""
Module 14: Functional Programming in Python
============================================
A comprehensive guide to functional paradigms in Python: first-class functions,
pure functions, immutability, lambdas, map/filter/reduce, partial application,
function composition, and declarative pipelines for AI agent prompt engineering.

Run this script directly:
    python3 functional.py
"""

from functools import partial, reduce
from typing import Any, Callable, Dict, List, Optional, Tuple


def banner(title: str) -> None:
    """Formats section headers for clear terminal output."""
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


# =============================================================================
# Section 1: First-Class Functions — Functions as Values
# =============================================================================
banner("Section 1: First-Class and Higher-Order Functions")

# In Python, functions are first-class citizens:
# 1. They can be assigned to variables.
# 2. They can be passed as arguments to other functions.
# 3. They can be returned from other functions.
# 4. They can be stored in collections (lists, dicts).

def greet_formal(name: str) -> str:
    return f"Good day, esteemed agent {name}."

def greet_casual(name: str) -> str:
    return f"Hey {name}!"

# Functions assigned to variables:
greeter: Callable[[str], str] = greet_formal
print(f"Calling greeter variable: {greeter('Atlas')}")

# Passing functions as arguments (Higher-Order Function):
def format_greeting(name: str, formatter: Callable[[str], str]) -> str:
    """Takes a function as an argument and executes it."""
    return formatter(name)

print("Higher-order format (casual):", format_greeting("Atlas", greet_casual))
print("Higher-order format (formal):", format_greeting("Atlas", greet_formal))

# Returning functions from functions (Function Factory):
def make_multiplier(factor: int) -> Callable[[int], int]:
    """Returns a new specialized multiplier function."""
    def multiply(x: int) -> int:
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(f"Factory double(10) = {double(10)}")
print(f"Factory triple(10) = {triple(10)}")


# =============================================================================
# Section 2: Pure Functions vs Side Effects
# =============================================================================
banner("Section 2: Pure Functions and Side-Effect Elimination")

# A Pure Function has two fundamental properties:
# 1. Determinism: Identical inputs always produce the identical output.
# 2. No Side Effects: It does not alter global variables, mutate input arguments,
#    or perform hidden I/O.

# IMPURE FUNCTION: Mutates external state
global_call_count = 0
def impure_tax_calc(amount: float) -> float:
    global global_call_count
    global_call_count += 1  # Side effect!
    return amount * 1.15

# PURE FUNCTION: Pure mathematical transformation
def pure_tax_calc(amount: float, tax_rate: float = 0.15) -> float:
    return amount * (1.0 + tax_rate)

print(f"Pure calc 1: {pure_tax_calc(100.0):.2f}")
print(f"Pure calc 2: {pure_tax_calc(100.0):.2f}")
print("Pure functions guarantee zero unexpected state corruption across execution steps.")


# =============================================================================
# Section 3: Anonymous Functions — The 'lambda' Keyword
# =============================================================================
banner("Section 3: Anonymous Functions (Lambdas)")

# Lambdas are short, inline functions defined with: lambda <args>: <expression>
# They are best used for throwaway operations, such as sorting keys or quick filters.

add = lambda a, b: a + b
print(f"Lambda add(7, 8) = {add(7, 8)}")

# Sorting structured agent records with a lambda key:
agent_candidates = [
    {"name": "Agent-C", "latency_ms": 120, "accuracy": 0.94},
    {"name": "Agent-A", "latency_ms": 45,  "accuracy": 0.88},
    {"name": "Agent-B", "latency_ms": 80,  "accuracy": 0.99},
]

# Sort by lowest latency:
by_latency = sorted(agent_candidates, key=lambda a: a["latency_ms"])
print("\nAgents sorted by lowest latency:")
for ag in by_latency:
    print(f"  {ag['name']}: {ag['latency_ms']}ms")

# Sort by highest accuracy:
by_accuracy = sorted(agent_candidates, key=lambda a: a["accuracy"], reverse=True)
print("\nAgents sorted by highest accuracy:")
for ag in by_accuracy:
    print(f"  {ag['name']}: {ag['accuracy'] * 100:.1f}%")


# =============================================================================
# Section 4: Map, Filter, and Reduce
# =============================================================================
banner("Section 4: The Functional Trio: map(), filter(), reduce()")

raw_scores = [45, 82, 91, 55, 67, 100, 38, 74]
print(f"Original scores: {raw_scores}")

# 1. filter(): Retain elements matching a predicate (returns lazy iterator)
passing_scores = list(filter(lambda s: s >= 70, raw_scores))
print(f"Filter (passing >= 70): {passing_scores}")

# 2. map(): Transform every element with a function (returns lazy iterator)
curved_scores = list(map(lambda s: min(100, s + 5), passing_scores))
print(f"Map (curve +5 points, capped at 100): {curved_scores}")

# 3. reduce(): Aggregate a sequence into a single cumulative value
total_score = reduce(lambda acc, val: acc + val, curved_scores, 0)
average_score = total_score / len(curved_scores) if curved_scores else 0
print(f"Reduce (cumulative sum): {total_score}, Average: {average_score:.1f}")


# =============================================================================
# Section 5: Pythonic Comprehensions as Functional Transformations
# =============================================================================
banner("Section 5: Comprehensions as Preferred Pythonic FP")

# In Python, list/dict/set comprehensions are generally faster and more readable
# than raw map() and filter() combinations.

token_counts = [12, 450, 89, 1200, 340, 2048, 55]

# Equivalent of filter + map:
large_tokens_normalized = [t / 1000.0 for t in token_counts if t > 100]
print(f"Comprehension filtered & normalized (>100 tokens): {large_tokens_normalized}")

# Dictionary comprehension (immutable key-value transformation):
tool_latencies = {"search": 230, "calculator": 15, "database": 85, "python": 40}
fast_tools = {name: ms for name, ms in tool_latencies.items() if ms < 100}
print(f"Fast tools dict comprehension (<100ms): {fast_tools}")


# =============================================================================
# Section 6: Partial Function Application with functools.partial
# =============================================================================
banner("Section 6: Partial Function Application")

# functools.partial allows freezing a certain number of arguments of a function,
# resulting in a new object with a simplified signature.

def log_message(level: str, source: str, message: str) -> str:
    return f"[{level.upper()}] [{source}] {message}"

# Create specialized loggers with pre-filled level and source:
agent_info_logger = partial(log_message, "INFO", "AgentRuntime")
agent_error_logger = partial(log_message, "ERROR", "AgentRuntime")

print(agent_info_logger("Initializing planning scratchpad..."))
print(agent_error_logger("Tool API returned HTTP 503!"))


# =============================================================================
# Section 7: Function Composition & Processing Pipelines
# =============================================================================
banner("Section 7: Function Composition & Data Pipelines")

# Composition means piping the output of one function directly into another:
# h(x) = f(g(x))

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chains multiple functions left-to-right."""
    def composed_fn(arg: Any) -> Any:
        return reduce(lambda val, fn: fn(val), funcs, arg)
    return composed_fn

# Individual pure transforms:
strip_spaces = lambda text: text.strip()
clean_linebreaks = lambda text: " ".join(text.splitlines())
truncate_text = lambda text: text[:60] + "..." if len(text) > 60 else text
add_agent_prefix = lambda text: f"USER_PROMPT >> {text}"

# Construct a declarative pipeline:
prompt_pipeline = compose(strip_spaces, clean_linebreaks, truncate_text, add_agent_prefix)

raw_prompt = """
    Please analyze this quarterly report for fiscal year 2026,
    including the gross margin and operational expenditures.
"""

cleaned = prompt_pipeline(raw_prompt)
print(f"Pipelined result:\n{cleaned}")


# =============================================================================
# Section 8: Real-World AI Agent Functional Pipeline
# =============================================================================
banner("Section 8: Real-World AI Agent Functional Data Processing")

# Autonomous agents constantly process incoming streams of tool execution logs.
# A functional pipeline allows filtering noise, masking secrets, and extracting
# structured observations without modifying the raw audit logs.

raw_telemetry_logs = [
    {"step": 1, "type": "THINK", "content": "Analyzing user query", "duration": 0.05},
    {"step": 2, "type": "TOOL",  "content": "api_key=sk-SECRET123; search('Paris weather')", "duration": 0.85},
    {"step": 3, "type": "DEBUG", "content": "Cache miss in memory chunk 4", "duration": 0.01},
    {"step": 4, "type": "TOOL",  "content": "calculator('15 * 4')", "duration": 0.02},
    {"step": 5, "type": "ANSWER","content": "The weather in Paris is 18C.", "duration": 0.12},
]

def mask_secrets(log: Dict[str, Any]) -> Dict[str, Any]:
    """Pure function returning a new sanitized log dictionary."""
    content = log["content"]
    if "api_key=" in content:
        # Immutably replace secret
        import re
        content = re.sub(r"api_key=[^;\s]+", "api_key=***MASKED***", content)
    # Return a brand new dictionary (no mutation)
    return {**log, "content": content}

# Functional pipeline:
# 1. Filter out low-level DEBUG events
# 2. Mask secrets immutably
# 3. Compute total runtime of non-debug steps
production_logs = list(
    map(mask_secrets, filter(lambda log: log["type"] != "DEBUG", raw_telemetry_logs))
)

total_runtime = reduce(lambda acc, log: acc + log["duration"], production_logs, 0.0)

print("Sanitized Agent Production Logs:")
for log in production_logs:
    print(f"  [Step {log['step']}] [{log['type']:<6}] ({log['duration']:.2f}s) -> {log['content']}")
print(f"\nTotal Pipeline Execution Time: {total_runtime:.2f}s")

banner("Module 14 Lesson Complete")
