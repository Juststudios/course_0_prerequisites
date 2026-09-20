"""agent.py - MiniAgent async coordinator with ContextVars, SQLite memory, and ReAct loop."""

from typing import Optional, List
import asyncio
import contextvars
import time
import uuid

from .config import AgentConfig
from .models import AgentStep, AgentResponse, MessageRole
from .memory import SQLiteMemory
from .tools import ToolRegistry
from .engine import DeterministicReActEngine

# Context variables for tracing
trace_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("mini_agent_trace_id", default="untraced")
session_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("mini_agent_session_id", default="default")


class MiniAgent:
    """Modular autonomous agent coordinating async execution, SQLite memory, and tool invocation."""

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        memory: Optional[SQLiteMemory] = None,
        tools: Optional[ToolRegistry] = None,
        engine: Optional[DeterministicReActEngine] = None,
    ) -> None:
        self.config = config or AgentConfig()
        self.memory = memory or SQLiteMemory(db_path=self.config.db_path)
        self.tools = tools or ToolRegistry()
        self.engine = engine or DeterministicReActEngine(agent_name=self.config.agent_name)

    async def run(self, prompt: str, session_id: str = "default") -> AgentResponse:
        """Executes a multi-step reasoning task asynchronously."""
        start_time = time.perf_counter()
        trace_id = f"trace_{uuid.uuid4().hex[:10]}"

        # Bind context variables for this execution
        t_tok = trace_id_ctx.set(trace_id)
        s_tok = session_id_ctx.set(session_id)

        try:
            # Wrap entire run in timeout
            return await asyncio.wait_for(
                self._execute_react_loop(prompt, session_id, trace_id, start_time),
                timeout=self.config.timeout_seconds
            )
        except asyncio.TimeoutError:
            duration_ms = (time.perf_counter() - start_time) * 1000.0
            return AgentResponse(
                session_id=session_id,
                trace_id=trace_id,
                query=prompt,
                final_answer="Operation timed out before completion.",
                steps=[],
                success=False,
                error=f"Timeout exceeded {self.config.timeout_seconds}s",
                total_duration_ms=round(duration_ms, 2)
            )
        finally:
            trace_id_ctx.reset(t_tok)
            session_id_ctx.reset(s_tok)

    async def _execute_react_loop(
        self,
        prompt: str,
        session_id: str,
        trace_id: str,
        start_time: float
    ) -> AgentResponse:
        """Core ReAct loop implementation."""
        # 1. Record user message in memory
        self.memory.add_message(session_id, MessageRole.USER.value, prompt)

        steps: List[AgentStep] = []
        available_tool_names = self.tools.list_tools()

        if self.config.verbose:
            print(f"\n[{self.config.agent_name}] Trace: {trace_id} | Session: {session_id}")
            print(f"[{self.config.agent_name}] User Prompt: '{prompt}'")

        # 2. Iterate reasoning steps up to max_steps
        for step_num in range(1, self.config.max_steps + 1):
            history = self.memory.get_history(session_id, limit=10)

            # Consult engine for next action
            thought, tool_call, final_answer = self.engine.plan_next_step(
                query=prompt,
                history=history,
                steps=steps,
                available_tools=available_tool_names
            )

            if self.config.verbose:
                print(f"\n--- Step {step_num} ---")
                print(f"Thought: {thought}")

            # Check if task reached completion
            if final_answer is not None:
                # Save assistant response to memory
                self.memory.add_message(session_id, MessageRole.ASSISTANT.value, final_answer)
                duration_ms = (time.perf_counter() - start_time) * 1000.0

                if self.config.verbose:
                    print(f"Final Answer: {final_answer}")

                return AgentResponse(
                    session_id=session_id,
                    trace_id=trace_id,
                    query=prompt,
                    final_answer=final_answer,
                    steps=steps,
                    success=True,
                    total_duration_ms=round(duration_ms, 2)
                )

            # Execute tool call
            if tool_call is not None:
                if self.config.verbose:
                    print(f"Action: {tool_call.tool_name}({tool_call.arguments})")

                tool_start = time.perf_counter()
                tool_res = self.tools.execute(
                    tool_call.tool_name,
                    call_id=tool_call.id,
                    **tool_call.arguments
                )
                tool_dur_ms = (time.perf_counter() - tool_start) * 1000.0

                # Formulate observation string
                observation_str = str(tool_res.output) if tool_res.success else f"Error: {tool_res.error}"
                if self.config.verbose:
                    print(f"Observation: {observation_str}")

                # Log tool execution to persistent SQLite audit trail
                self.memory.log_tool_call(
                    session_id=session_id,
                    trace_id=trace_id,
                    tool_name=tool_call.tool_name,
                    args=tool_call.arguments,
                    result=tool_res.output if tool_res.success else tool_res.error,
                    success=tool_res.success,
                    duration_ms=round(tool_dur_ms, 2)
                )

                # Record step
                step = AgentStep(
                    step_number=step_num,
                    thought=thought,
                    tool_call=tool_call,
                    observation=observation_str
                )
                steps.append(step)

        # Reached max steps without final answer
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return AgentResponse(
            session_id=session_id,
            trace_id=trace_id,
            query=prompt,
            final_answer="Task could not be completed within step limits.",
            steps=steps,
            success=False,
            error=f"Max steps ({self.config.max_steps}) exceeded.",
            total_duration_ms=round(duration_ms, 2)
        )
