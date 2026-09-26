"""
Module 16: Python Dataclasses
==============================
A deep, practical exploration of dataclasses in modern Python: boilerplate
elimination, automatic dunder generation, field customization, default_factory,
frozen immutability, post-init validation hooks, serialization, and AI agent
state modeling.

Run this script directly:
    python3 dataclasses_lesson.py
"""

from dataclasses import asdict, astuple, dataclass, field, replace
import json
import time
from typing import Any, Dict, List, Optional, Tuple


def banner(title: str) -> None:
    """Formats section headers for clear terminal output."""
    print("\n" + "=" * 75)
    print(f"  {title.upper()}")
    print("=" * 75)


# =============================================================================
# Section 1: The Problem Dataclasses Solve (Boilerplate Elimination)
# =============================================================================
banner("Section 1: The Boilerplate Problem")

# Without dataclasses, creating a typed data container requires writing
# repetitive __init__, __repr__, and __eq__ methods by hand.
# With @dataclass, Python synthesizes all of these methods automatically!

@dataclass
class Coordinate2D:
    x: float
    y: float

# Instantiate and inspect:
coord1 = Coordinate2D(10.5, 20.0)
coord2 = Coordinate2D(10.5, 20.0)
coord3 = Coordinate2D(0.0, 0.0)

print(f"coord1 __repr__: {coord1}")
print(f"coord1 == coord2: {coord1 == coord2} (Value equality synthesized automatically!)")
print(f"coord1 == coord3: {coord1 == coord3}")
print(f"coord1 is coord2: {coord1 is coord2} (Distinct objects in memory)")


# =============================================================================
# Section 2: Default Values and Field Ordering Rules
# =============================================================================
banner("Section 2: Default Values and Field Ordering")

# Rule: Fields without default values MUST appear before fields with default values.

@dataclass
class LLMModelConfig:
    model_name: str                  # Non-default: required
    provider: str = "anthropic"      # Default: optional
    max_tokens: int = 4096           # Default: optional
    temperature: float = 0.7         # Default: optional

default_cfg = LLMModelConfig("claude-3-5-sonnet")
custom_cfg = LLMModelConfig("gpt-4o", provider="openai", temperature=0.2)

print(f"Default config: {default_cfg}")
print(f"Custom config:  {custom_cfg}")


# =============================================================================
# Section 3: Fine-Grained Field Customization with field()
# =============================================================================
banner("Section 3: Field Customization and default_factory")

# WARNING: Never use mutable defaults directly!
# list_param: list = []  <- Raises ValueError: mutable default is not allowed!
# Always use field(default_factory=list) or field(default_factory=dict).

@dataclass
class AgentWorkspace:
    workspace_id: str
    # 1. default_factory creates a fresh list/dict for EACH instance:
    active_tasks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # 2. repr=False masks sensitive values from print() and logs:
    api_secret: str = field(default="sk-DEFAULT-SECRET", repr=False)
    # 3. compare=False excludes field from == equality comparisons:
    created_at: float = field(default_factory=time.time, compare=False)

ws1 = AgentWorkspace("ws-001")
ws2 = AgentWorkspace("ws-001")

ws1.active_tasks.append("Analyze logs")
print(f"Workspace 1 tasks: {ws1.active_tasks}")
print(f"Workspace 2 tasks: {ws2.active_tasks} (Clean, separate list instance!)")
print(f"Workspace 1 repr (api_secret hidden): {ws1}")
print(f"ws1 == ws2: {ws1 == ws2} (True because created_at is excluded from comparison!)")


# =============================================================================
# Section 4: Immutable Dataclasses (frozen=True)
# =============================================================================
banner("Section 4: Immutable Dataclasses (frozen=True)")

# When frozen=True is specified:
# 1. Instances cannot be modified after initialization (attributes are read-only).
# 2. Instances are automatically hashable, meaning they can be stored in sets
#    or used as dictionary keys!

@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    rate_limit_per_min: int = 60

search_tool = ToolDefinition("web_search", "Queries external search engine", 30)
print(f"Frozen tool definition: {search_tool}")
print(f"Hash of frozen tool:    {hash(search_tool)}")

# Frozen instances can be dictionary keys:
tool_permissions: Dict[ToolDefinition, bool] = {search_tool: True}
print(f"Permission lookup: {tool_permissions[search_tool]}")

# If we want a modified copy of a frozen instance, use dataclasses.replace():
upgraded_tool = replace(search_tool, rate_limit_per_min=120)
print(f"Upgraded tool (immutable copy): {upgraded_tool}")


# =============================================================================
# Section 5: The Post-Initialization Hook (__post_init__)
# =============================================================================
banner("Section 5: Post-Initialization Hook (__post_init__)")

# __post_init__ runs immediately after synthesized __init__ completes.
# Perfect for:
#   1. Enforcing business logic and domain validation invariants.
#   2. Computing derived or cached attributes.

@dataclass
class BoundedPrompt:
    text: str
    max_length: int = 100
    # Derived attribute calculated in __post_init__:
    char_count: int = field(init=False)
    is_truncated: bool = field(init=False)

    def __post_init__(self) -> None:
        # Validation
        if self.max_length <= 0:
            raise ValueError("max_length must be strictly positive!")

        cleaned = self.text.strip()
        self.char_count = len(cleaned)
        if len(cleaned) > self.max_length:
            self.text = cleaned[:self.max_length - 3] + "..."
            self.is_truncated = True
        else:
            self.text = cleaned
            self.is_truncated = False

p1 = BoundedPrompt("Short command", max_length=50)
p2 = BoundedPrompt("This prompt is extraordinarily long and exceeds the declared character budget!", max_length=35)

print(f"Prompt 1: '{p1.text}' (Truncated: {p1.is_truncated}, Length: {p1.char_count})")
print(f"Prompt 2: '{p2.text}' (Truncated: {p2.is_truncated}, Length: {p2.char_count})")


# =============================================================================
# Section 6: Inheritance in Dataclasses
# =============================================================================
banner("Section 6: Inheritance in Dataclasses")

@dataclass
class BaseMessage:
    role: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class ToolResultMessage(BaseMessage):
    # Child fields are appended to parent fields in synthesized __init__:
    tool_name: str = ""
    result_data: str = ""
    execution_time_sec: float = 0.0

msg = ToolResultMessage(
    role="tool",
    tool_name="database_query",
    result_data="Fetched 42 records",
    execution_time_sec=0.12
)
print(f"Inherited dataclass message: {msg}")


# =============================================================================
# Section 7: Serialization — asdict() and astuple()
# =============================================================================
banner("Section 7: Serialization (asdict, astuple, JSON)")

# Dataclasses easily serialize into standard Python structures:
data_dict = asdict(msg)
data_tuple = astuple(coord1)

print(f"asdict() representation:\n  {data_dict}")
print(f"astuple() representation:\n  {data_tuple}")

# Converting to formatted JSON string:
json_string = json.dumps(data_dict, indent=2)
print(f"Exported JSON string:\n{json_string}")


# =============================================================================
# Section 8: Real-World AI Agent State Architecture
# =============================================================================
banner("Section 8: Real-World AI Agent Telemetry Pipeline")

# Autonomous AI agents use structured dataclasses to track each step of a ReAct loop:
# 1. Thought -> 2. Action (Tool Call) -> 3. Observation (Result)

@dataclass
class ToolCall:
    tool: str
    params: Dict[str, Any]

@dataclass
class StepTelemetry:
    step_number: int
    thought: str
    tool_call: Optional[ToolCall] = None
    observation: Optional[str] = None
    duration_sec: float = 0.0

@dataclass
class AgentTrajectory:
    agent_id: str
    goal: str
    steps: List[StepTelemetry] = field(default_factory=list)

    def record_step(self, thought: str, tool_call: Optional[ToolCall] = None, observation: Optional[str] = None, duration: float = 0.0) -> None:
        step = StepTelemetry(
            step_number=len(self.steps) + 1,
            thought=thought,
            tool_call=tool_call,
            observation=observation,
            duration_sec=duration
        )
        self.steps.append(step)

# Simulate trajectory recording:
trajectory = AgentTrajectory(agent_id="agent-hermes-01", goal="Query customer balance and notify.")

trajectory.record_step(
    thought="Querying database for customer ID 1048.",
    tool_call=ToolCall("sql_query", {"query": "SELECT balance FROM customers WHERE id=1048"}),
    observation="Balance: $4,250.00",
    duration=0.08
)

trajectory.record_step(
    thought="Balance retrieved. Emitting notification to user.",
    tool_call=ToolCall("send_notification", {"user_id": 1048, "text": "Balance is $4,250.00"}),
    observation="Notification dispatched (Status 200).",
    duration=0.15
)

print(f"Recorded Agent Trajectory with {len(trajectory.steps)} steps:")
for s in trajectory.steps:
    tool_str = f" -> Tool: {s.tool_call.tool}" if s.tool_call else ""
    print(f"  [Step {s.step_number}] ({s.duration_sec}s) {s.thought}{tool_str}")

banner("Module 16 Lesson Complete")
