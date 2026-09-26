"""
Module 15: Type Hints and Modern Python Typing
===============================================
A comprehensive guide to static typing in Python: primitive and container
annotations, Optional/Union types, Callable contracts, TypeVar generics,
Protocols, and runtime schema reflection for autonomous AI agent tool calling.

Run this script directly:
    python3 typing_lesson.py
"""

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    TypedDict,
    Union,
)
import inspect


def banner(title: str) -> None:
    """Formats section headers for clear terminal output."""
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


# =============================================================================
# Section 1: Basic Variable Annotations & Runtime Introspection
# =============================================================================
banner("Section 1: Basic Annotations and __annotations__")

# In Python 3.6+, variables can be annotated with their expected type.
# Python does NOT enforce these types at runtime; it stores them in __annotations__.

agent_name: str = "Hermes"
step_budget: int = 15
temperature: float = 0.7
is_active: bool = True

print(f"Agent '{agent_name}' (Budget: {step_budget}, Temp: {temperature}, Active: {is_active})")

# Notice how Python stores annotations in module or function __annotations__:
print("Module-level annotations sample:")
for k, v in list(globals().get("__annotations__", {}).items())[:4]:
    print(f"  {k}: {v}")


# =============================================================================
# Section 2: Function Signatures — Parameters and Return Values
# =============================================================================
banner("Section 2: Annotating Function Signatures")

def calculate_token_cost(prompt_tokens: int, completion_tokens: int, cost_per_k: float = 0.002) -> float:
    """Computes total USD cost for an LLM inference call."""
    total_tokens = prompt_tokens + completion_tokens
    return (total_tokens / 1000.0) * cost_per_k

cost = calculate_token_cost(prompt_tokens=1500, completion_tokens=350, cost_per_k=0.003)
print(f"Calculated Inference Cost: ${cost:.5f}")

# Introspecting function type annotations at runtime:
print(f"Function annotations for calculate_token_cost: {calculate_token_cost.__annotations__}")


# =============================================================================
# Section 3: Modern Built-in Generics (Collections)
# =============================================================================
banner("Section 3: Modern Built-in Container Generics")

# In Python 3.9+, standard collections (list, dict, tuple, set) accept type parameters:
# list[T]         -> homogeneous list of elements of type T
# dict[K, V]      -> mapping of keys of type K to values of type V
# tuple[T1, T2]   -> fixed-length heterogeneous tuple
# tuple[T, ...]   -> arbitrary-length homogeneous tuple
# set[T]          -> unique set of elements of type T

active_tools: list[str] = ["web_search", "calculator", "sqlite_query"]
tool_execution_counts: dict[str, int] = {"web_search": 12, "calculator": 5}
agent_coordinate: tuple[float, float] = (37.7749, -122.4194)
supported_encodings: set[str] = {"utf-8", "ascii"}

print(f"Active tools list[str]: {active_tools}")
print(f"Execution counts dict[str, int]: {tool_execution_counts}")
print(f"Coordinate tuple[float, float]: {agent_coordinate}")


# =============================================================================
# Section 4: Union Types and Optional Values
# =============================================================================
banner("Section 4: Unions and Optional (Nullable) Types")

# Modern Python (3.10+) uses the pipe operator `|` for Unions:
# int | str is equivalent to Union[int, str]
# str | None is equivalent to Optional[str]

def query_agent_memory(query: str, limit: int | None = None) -> list[str]:
    """Retrieves memories, optionally capping results if limit is provided."""
    mock_db = ["User asked for weather", "User asked for stock price", "Agent answered 42"]
    if limit is not None:
        return mock_db[:limit]
    return mock_db

print("Memories (limit=None):", query_agent_memory("weather"))
print("Memories (limit=1):   ", query_agent_memory("weather", limit=1))


# =============================================================================
# Section 5: Callable Types — The Foundation of Agent Tool Registries
# =============================================================================
banner("Section 5: Callable Types for Tools & Callbacks")

# Callable[[Arg1Type, Arg2Type, ...], ReturnType]
# Represents functions, lambdas, or objects implementing __call__.

# A Tool function that accepts a string input and returns a string result:
AgentTool = Callable[[str], str]

def web_search(query: str) -> str:
    return f"Search results for: '{query}' -> Found 3 articles."

def calculator(expression: str) -> str:
    return f"Evaluated '{expression}' -> 42.0"

# A higher-order dispatcher taking an AgentTool:
def execute_tool_safely(tool_name: str, tool_func: AgentTool, argument: str) -> str:
    print(f"  [Dispatcher] Invoking tool '{tool_name}'...")
    return tool_func(argument)

print(execute_tool_safely("search", web_search, "latest tech news"))
print(execute_tool_safely("math", calculator, "100 * 2.5"))


# =============================================================================
# Section 6: Literal Types and TypedDict for Structured Contracts
# =============================================================================
banner("Section 6: Literal and TypedDict for Structured Schemas")

# Literal restricts a variable to specific fixed values:
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

# TypedDict defines a dictionary with exact string keys and value types:
class AgentStepRecord(TypedDict):
    step_id: int
    action: str
    status: Literal["SUCCESS", "FAILED", "PENDING"]
    output: str

step: AgentStepRecord = {
    "step_id": 1,
    "action": "execute_query",
    "status": "SUCCESS",
    "output": "Table queried successfully.",
}
print(f"TypedDict step record: {step}")


# =============================================================================
# Section 7: TypeVar and Generics
# =============================================================================
banner("Section 7: TypeVar and Generic Classes")

# TypeVar allows creating functions and classes that preserve type relationships
# across inputs and outputs without having to use loose `Any`.

T = TypeVar("T")

class Stack(Generic[T]):
    """A generic LIFO stack data structure preserving element types."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

string_stack: Stack[str] = Stack[str]()
string_stack.push("Thought 1: Planning")
string_stack.push("Thought 2: Execution")
print(f"Popped from Stack[str]: '{string_stack.pop()}' (Preserved string type!)")


# =============================================================================
# Section 8: Protocols — Static Duck Typing (Structural Subtyping)
# =============================================================================
banner("Section 8: Protocols (Structural Subtyping)")

# Protocols allow static type checkers to verify that an object has certain
# methods without requiring explicit class inheritance!

class Summarizable(Protocol):
    def summarize(self) -> str:
        ...

class ConversationHistory:
    def summarize(self) -> str:
        return "Conversation contains 5 user messages and 5 agent responses."

class DocumentChunk:
    def summarize(self) -> str:
        return "Document chunk: Section 4.2 Machine Learning Architecture."

def print_summary(item: Summarizable) -> None:
    """Accepts ANY object as long as it provides a summarize() method."""
    print("  [Summary Protocol]", item.summarize())

# Neither class inherits from a shared parent, but both satisfy Summarizable!
print_summary(ConversationHistory())
print_summary(DocumentChunk())


# =============================================================================
# Section 9: Real-World AI Agent — Generating JSON Tool Schemas
# =============================================================================
banner("Section 9: Generating LLM Tool Schemas from Python Type Hints")

# When OpenAI or Anthropic tool-calling APIs request tools, agent frameworks
# reflect over Python function type hints to generate JSON Schema definitions!

def generate_tool_schema(func: Callable[..., Any]) -> dict[str, Any]:
    """Inspects a Python function's type hints and docstrings to build a JSON Schema."""
    sig = inspect.signature(func)
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
    }

    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        py_type = param.annotation
        json_type = type_map.get(py_type, "string")
        properties[name] = {
            "type": json_type,
            "description": f"Parameter {name}",
        }
        if param.default is inspect.Parameter.empty:
            required.append(name)

    return {
        "name": func.__name__,
        "description": inspect.getdoc(func) or "",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }

# A real agent tool with explicit type hints:
def fetch_weather(city: str, units: str = "metric") -> str:
    """Retrieves current weather condition and temperature for a given city."""
    return f"Weather in {city}: 22C, sunny ({units})"

schema = generate_tool_schema(fetch_weather)
print(f"Generated JSON Schema for '{schema['name']}':")
import json
print(json.dumps(schema, indent=2))

banner("Module 15 Lesson Complete")
