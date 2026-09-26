"""
Module 08: Functions — Definition, Parameterization, and Functional Abstraction
==============================================================================

Functions are the fundamental unit of abstraction, code reuse, and modularity in Python.
A function bundles a sequence of statements into a callable object that accepts inputs
(parameters), executes logic, and yields an output (return value). In modern software
and AI systems, functions form the bridge between raw LLM reasoning and real-world execution
(known as "Tool Calling" or "Function Calling").

This lesson covers:
  1. Function Anatomy and the `return` Statement
  2. Positional vs. Keyword Arguments
  3. Default Parameters and the Dangerous Mutable Default Trap
  4. Variadic Positional Arguments (*args)
  5. Variadic Keyword Arguments (**kwargs)
  6. Keyword-Only and Positional-Only Parameters (*, /)
  7. Multiple Return Values via Tuple Packing/Unpacking
  8. Type Annotations and Docstrings (PEP 257)
  9. Functions as First-Class Citizens (Passing & Returning Functions)
  10. Practical AI Tool-Registry & Dispatch Engine
"""

from typing import Any, Callable, Dict, List, Optional, Tuple

print("=" * 70)
print("MODULE 08: FUNCTIONS IN PYTHON")
print("=" * 70)


# ==============================================================================
# SECTION 1: Function Anatomy and Return Values
# ==============================================================================
print("\n--- 1. Function Anatomy and Return Values ---")

# Every function is declared using `def <name>(<parameters>):`
# If no `return` statement is explicitly reached, Python returns `None`.

def greet_agent(name: str) -> str:
    """Construct a formal greeting for an autonomous agent."""
    return f"Greetings, Agent '{name}'. System ready."

def log_heartbeat(status: str) -> None:
    """Demonstrate a function with no return value (implicitly returns None)."""
    print(f"  [Heartbeat Log]: {status}")

greeting_result = greet_agent("Orchestrator-01")
print("Calling greet_agent():", greeting_result)

heartbeat_result = log_heartbeat("OK - 200")
print("Calling log_heartbeat() return value:", heartbeat_result)
print("Is return value None?:", heartbeat_result is None)


# ==============================================================================
# SECTION 2: Positional vs. Keyword Arguments
# ==============================================================================
print("\n--- 2. Positional vs. Keyword Arguments ---")

def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model_name: str) -> float:
    """Calculate USD cost given token counts and model pricing."""
    rates = {
        "gpt-4o": (5.00 / 1_000_000, 15.00 / 1_000_000),
        "claude-3-5": (3.00 / 1_000_000, 15.00 / 1_000_000),
        "default": (1.00 / 1_000_000, 2.00 / 1_000_000)
    }
    input_rate, output_rate = rates.get(model_name, rates["default"])
    total_cost = (prompt_tokens * input_rate) + (completion_tokens * output_rate)
    return total_cost

# Calling with positional arguments (order matters):
cost_pos = calculate_token_cost(1000, 500, "gpt-4o")
print(f"Positional call cost: ${cost_pos:.6f}")

# Calling with keyword arguments (order does not matter, self-documenting):
cost_kw = calculate_token_cost(model_name="claude-3-5", completion_tokens=800, prompt_tokens=2000)
print(f"Keyword call cost:    ${cost_kw:.6f}")


# ==============================================================================
# SECTION 3: Default Arguments and the Mutable Default Trap
# ==============================================================================
print("\n--- 3. Default Arguments & The Mutable Default Trap ---")

# Default arguments provide fallback values if the caller omits them:
def configure_llm(model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 2048) -> Dict[str, Any]:
    return {"model": model, "temperature": temperature, "max_tokens": max_tokens}

print("Using defaults:    ", configure_llm())
print("Overriding partial:", configure_llm(temperature=0.2))

# THE DANGEROUS PITFALL: Never use mutable objects ([], {}) as default arguments!
# Python evaluates default arguments ONCE at function definition time, NOT at invocation time.
# Every call that uses the default shares the EXACT same instance.

def dangerous_append(event: str, history: List[str] = []) -> List[str]:  # ANTIPATTERN!
    history.append(event)
    return history

print("\nDemonstrating Mutable Default Trap (Antipattern):")
list_a = dangerous_append("login")
print("  Call 1:", list_a)
list_b = dangerous_append("query")
print("  Call 2:", list_b)
print("  Notice how Call 2 corrupted Call 1 history! list_a is list_b:", list_a is list_b)

# THE CORRECT IDIOMATIC PATTERN: Default to None and instantiate inside the function:
def safe_append(event: str, history: Optional[List[str]] = None) -> List[str]:
    if history is None:
        history = []
    history.append(event)
    return history

print("\nDemonstrating Idiomatic Safe Default:")
clean_a = safe_append("login")
print("  Call 1:", clean_a)
clean_b = safe_append("query")
print("  Call 2:", clean_b)
print("  clean_a is clean_b?:", clean_a is clean_b)


# ==============================================================================
# SECTION 4: Variadic Positional Arguments (*args)
# ==============================================================================
print("\n--- 4. Variadic Positional Arguments (*args) ---")

# `*args` packs any number of positional arguments into a tuple:
def combine_context_strings(*chunks: str) -> str:
    """Concatenate an arbitrary number of text chunks into a unified prompt context."""
    print(f"  Received chunks tuple (type={type(chunks).__name__}, len={len(chunks)})")
    return "\n---\n".join(chunks)

combined = combine_context_strings(
    "System: You are an autonomous coding assistant.",
    "User: Refactor the auth module.",
    "Context: Active file auth.py has 200 lines."
)
print("Combined output:\n" + combined)


# ==============================================================================
# SECTION 5: Variadic Keyword Arguments (**kwargs)
# ==============================================================================
print("\n--- 5. Variadic Keyword Arguments (**kwargs) ---")

# `**kwargs` packs arbitrary named arguments into a dictionary:
def create_agent_payload(agent_id: str, role: str, **metadata: Any) -> Dict[str, Any]:
    payload = {
        "agent_id": agent_id,
        "role": role,
        "parameters": metadata
    }
    return payload

agent_meta = create_agent_payload(
    "agent-42",
    "qa_reviewer",
    environment="production",
    timeout_seconds=30,
    retry_count=3,
    debug_mode=False
)
print("Agent payload generated via **kwargs:")
for k, v in agent_meta.items():
    print(f"  {k}: {v}")


# ==============================================================================
# SECTION 6: Keyword-Only and Positional-Only Arguments
# ==============================================================================
print("\n--- 6. Keyword-Only and Positional-Only Parameters ---")

# Syntax:
#   def func(pos_only, /, standard, *, kw_only):
#       - Before `/`: MUST be positional
#       - Between `/` and `*`: Either positional or keyword
#       - After `*`: MUST be keyword

def execute_sql_query(query: str, /, timeout: int = 30, *, read_only: bool = True) -> str:
    return f"Executing '{query}' [timeout={timeout}s, read_only={read_only}]"

# Correct call:
result_sql = execute_sql_query("SELECT * FROM users", 10, read_only=True)
print("SQL Execution string:", result_sql)

# Calling with read_only positionally would raise:
# TypeError: execute_sql_query() takes from 1 to 2 positional arguments but 3 were given


# ==============================================================================
# SECTION 7: Multiple Return Values via Tuple Unpacking
# ==============================================================================
print("\n--- 7. Multiple Return Values (Tuple Packing) ---")

def analyze_prompt_metrics(text: str) -> Tuple[int, int, float]:
    """Return character count, word count, and estimated tokens."""
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    estimated_tokens = round(char_count / 4.0, 1)  # Heuristic ~4 chars per token
    return char_count, word_count, estimated_tokens  # Returns a 3-element tuple

sample_text = "Autonomous agents perceive their environment, reason, and take actions."
chars, words, tokens = analyze_prompt_metrics(sample_text)
print(f"Prompt Analysis: {chars} chars | {words} words | ~{tokens} tokens")


# ==============================================================================
# SECTION 8: Functions as First-Class Citizens
# ==============================================================================
print("\n--- 8. Functions as First-Class Citizens ---")

# In Python, functions are regular objects! You can:
# 1. Store them in variables or data structures
# 2. Pass them as arguments into other functions (callbacks)
# 3. Return them from other functions

def tool_add(x: float, y: float) -> float:
    return x + y

def tool_multiply(x: float, y: float) -> float:
    return x * y

# Storing functions inside a dictionary:
math_tools: Dict[str, Callable[[float, float], float]] = {
    "add": tool_add,
    "multiply": tool_multiply
}

op_name = "multiply"
operation = math_tools[op_name]
print(f"Executing math_tools['{op_name}'](4.0, 5.0): {operation(4.0, 5.0)}")

# Passing a function as a callback:
def transform_stream(data: List[int], transformer: Callable[[int], int]) -> List[int]:
    return [transformer(item) for item in data]

doubled = transform_stream([1, 2, 3, 4], lambda n: n * 2)
print("Transformed stream via callback:", doubled)


# ==============================================================================
# SECTION 9: Real-World AI Agent Tool Dispatcher
# ==============================================================================
print("\n--- 9. Production-Style AI Agent Tool Registry & Dispatcher ---")

class ToolRegistry:
    """Registry managing tool schemas and callable execution for an AI agent."""
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._schemas: Dict[str, str] = {}

    def register(self, name: str, description: str, func: Callable[..., Any]) -> None:
        self._tools[name] = func
        self._schemas[name] = description
        print(f"  [Registry] Registered tool '{name}'")

    def execute(self, tool_name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Dispatch tool dynamically with safety handling."""
        if tool_name not in self._tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' is not registered in agent catalog."
            }
        
        target_func = self._tools[tool_name]
        try:
            result = target_func(*args, **kwargs)
            return {"success": True, "result": result}
        except Exception as exc:
            return {"success": False, "error": f"Execution failed: {str(exc)}"}


# Define actual agent tools
def search_docs(query: str, max_results: int = 3) -> List[str]:
    return [f"Doc matching '{query}' - result #{i+1}" for i in range(max_results)]

def get_system_load() -> Dict[str, float]:
    return {"cpu_percent": 24.5, "memory_gb": 3.8}

# Set up and dispatch through registry
registry = ToolRegistry()
registry.register("search_docs", "Search engineering documentation", search_docs)
registry.register("get_system_load", "Get CPU and memory metrics", get_system_load)

# Simulate dynamic LLM tool calls:
print("\nExecuting Tool 1 (search_docs):")
res1 = registry.execute("search_docs", query="asyncio", max_results=2)
print("  Outcome:", res1)

print("\nExecuting Tool 2 (get_system_load):")
res2 = registry.execute("get_system_load")
print("  Outcome:", res2)

print("\nExecuting Tool 3 (unknown tool):")
res3 = registry.execute("delete_database", db_name="prod")
print("  Outcome:", res3)

print("\n" + "=" * 70)
print("MODULE 08 LESSON COMPLETE — ALL FUNCTION EXAMPLES EXECUTED SUCCESSFULLY")
print("=" * 70)
