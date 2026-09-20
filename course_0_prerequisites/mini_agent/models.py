"""models.py - Pydantic data schemas for messages, tool calls, and agent steps."""

from typing import List, Dict, Any, Optional
from enum import Enum
import time
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message sender role enumeration."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ToolCall(BaseModel):
    """Schema representing an agent's request to execute a tool."""
    id: str = Field(..., description="Unique call identifier.")
    tool_name: str = Field(..., description="The registered name of the tool.")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Dictionary of keyword arguments.")


class ToolResult(BaseModel):
    """Schema representing the outcome of a tool execution."""
    call_id: str = Field(..., description="Corresponding ToolCall identifier.")
    tool_name: str = Field(..., description="Name of the invoked tool.")
    success: bool = Field(..., description="Whether the tool completed without exception.")
    output: Any = Field(default=None, description="Returned payload or return value.")
    error: Optional[str] = Field(default=None, description="Error message if execution failed.")


class AgentStep(BaseModel):
    """A single discrete step in the ReAct reasoning trajectory."""
    step_number: int = Field(..., description="1-indexed step count.")
    thought: str = Field(..., description="Analytical reasoning for this step.")
    tool_call: Optional[ToolCall] = Field(default=None, description="Tool invoked, if any.")
    observation: Optional[str] = Field(default=None, description="Tool execution outcome observed.")


class Message(BaseModel):
    """A conversational turn persisted in memory."""
    role: MessageRole = Field(..., description="Sender role.")
    content: str = Field(..., description="Text content of the message.")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Associated tool invocations.")
    tool_results: List[ToolResult] = Field(default_factory=list, description="Associated tool results.")
    timestamp: float = Field(default_factory=time.time, description="Unix epoch timestamp.")


class AgentResponse(BaseModel):
    """Final response returned by MiniAgent.run()."""
    session_id: str = Field(..., description="Session identifier.")
    trace_id: str = Field(..., description="Distributed tracing identifier.")
    query: str = Field(..., description="Original user prompt.")
    final_answer: str = Field(..., description="Final synthesized response to the user.")
    steps: List[AgentStep] = Field(default_factory=list, description="Complete trajectory of reasoning steps.")
    success: bool = Field(default=True, description="Whether the agent achieved a final answer.")
    error: Optional[str] = Field(default=None, description="Error explanation if unsuccessful.")
    total_duration_ms: float = Field(default=0.0, description="Total execution duration in milliseconds.")
