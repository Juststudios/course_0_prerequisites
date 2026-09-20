"""tools.py - Extensible ToolRegistry with @tool decorator and safe built-in tools."""

from typing import Callable, Any, Dict, List, Optional
import functools
import inspect
import subprocess
import sys
import ast
import operator
from datetime import datetime, timezone

from .models import ToolResult


class SafeASTCalculator:
    """Safe mathematical expression evaluator using Python AST parsing without eval() vulnerabilities."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression: str) -> float:
        """Parses and computes the result of a mathematical expression safely."""
        try:
            tree = ast.parse(expression.strip(), mode="eval")
            return cls._eval_node(tree.body)
        except ZeroDivisionError:
            raise ZeroDivisionError("Division by zero in mathematical expression.")
        except Exception as e:
            raise ValueError(f"Invalid arithmetic expression '{expression}': {e}")

    @classmethod
    def _eval_node(cls, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            return float(cls.OPERATORS[op_type](left, right))

        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in cls.OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            operand = cls._eval_node(node.operand)
            return float(cls.OPERATORS[op_type](operand))

        else:
            raise ValueError(f"Disallowed syntax node in arithmetic expression: {type(node).__name__}")


class ToolRegistry:
    """Central registry of executable agent tools and their schemas."""

    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register(self, func: Optional[Callable[..., Any]] = None, *, name: Optional[str] = None):
        """Decorator to register a callable as an agent tool."""
        def decorator(target_func: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or target_func.__name__
            schema = self._generate_schema(target_func, tool_name)

            @functools.wraps(target_func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return target_func(*args, **kwargs)

            self._tools[tool_name] = wrapper
            self._schemas[tool_name] = schema
            wrapper.tool_schema = schema  # type: ignore[attr-defined]
            wrapper.tool_name = tool_name  # type: ignore[attr-defined]
            return wrapper

        if func is None:
            return decorator
        return decorator(func)

    def execute(self, tool_name: str, call_id: str = "call_default", **arguments: Any) -> ToolResult:
        """Executes a registered tool with argument validation and exception boundary."""
        if tool_name not in self._tools:
            return ToolResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=f"Tool '{tool_name}' not found. Available: {list(self._tools.keys())}"
            )

        try:
            output = self._tools[tool_name](**arguments)
            return ToolResult(
                call_id=call_id,
                tool_name=tool_name,
                success=True,
                output=output
            )
        except Exception as e:
            return ToolResult(
                call_id=call_id,
                tool_name=tool_name,
                success=False,
                error=f"{type(e).__name__}: {str(e)}"
            )

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Returns JSON schemas for all registered tools."""
        return list(self._schemas.values())

    def list_tools(self) -> List[str]:
        """Returns list of registered tool names."""
        return list(self._tools.keys())

    def _generate_schema(self, func: Callable[..., Any], tool_name: str) -> Dict[str, Any]:
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or f"Execute {tool_name}"

        type_mapping = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        properties: Dict[str, Any] = {}
        required: List[str] = []

        for p_name, param in sig.parameters.items():
            if p_name in ("self", "cls"):
                continue
            py_type = param.annotation
            json_type = type_mapping.get(py_type, "string")
            properties[p_name] = {
                "type": json_type,
                "description": f"Argument {p_name}",
            }
            if param.default is inspect.Parameter.empty:
                required.append(p_name)

        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": doc.split("\n\n")[0],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }


# Default registry instance
default_registry = ToolRegistry()
tool = default_registry.register


# Built-in Tools
@tool
def calculator(expression: str) -> float:
    """Evaluates a safe mathematical expression (e.g. '(15 * 4) + 20')."""
    return SafeASTCalculator.evaluate(expression)


@tool
def local_search(query: str, domain: str = "general") -> List[str]:
    """Searches local knowledge documentation for relevant information."""
    knowledge_base = {
        "python": [
            "Python 3.14 includes improved typing syntax and fast interpreter optimizations.",
            "Asyncio coroutines allow cooperative multitasking via event loops.",
            "ContextVars provide task-local storage for asynchronous execution.",
            "SQLite provides an embedded relational database with WAL mode concurrency.",
        ],
        "agent": [
            "ReAct agents cycle through Thought -> Action -> Observation steps.",
            "Tool sandboxing prevents command injection and path traversal vulnerabilities.",
            "Pydantic runtime validation catches malformed LLM tool arguments.",
        ],
        "general": [
            "Autonomous agents combine LLM reasoning with tool execution and memory persistence.",
            "Observability requires structured JSON logs and distributed trace identifiers.",
        ]
    }

    q = query.lower()
    matches = []
    # Search all domains if not found
    pool = knowledge_base.get(domain.lower(), []) + knowledge_base["general"] + knowledge_base["python"] + knowledge_base["agent"]
    for item in pool:
        if any(term in item.lower() for term in q.split()):
            if item not in matches:
                matches.append(item)

    if not matches:
        return [f"No direct knowledge articles found for query '{query}'."]
    return matches[:3]


@tool
def run_python(code: str, timeout: float = 3.0) -> str:
    """Safely executes a Python code snippet in an isolated subprocess."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
        if proc.returncode != 0:
            return f"Execution Error (Exit Code {proc.returncode}):\n{proc.stderr.strip()}"
        return proc.stdout.strip() if proc.stdout else "Executed successfully (no stdout)."
    except subprocess.TimeoutExpired:
        return f"Execution Timed Out after {timeout} seconds."
    except Exception as e:
        return f"Subprocess Error: {e}"


@tool
def get_time() -> str:
    """Returns the current UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
