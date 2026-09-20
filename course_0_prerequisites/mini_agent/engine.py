"""engine.py - Deterministic ReAct reasoning engine without external API dependencies."""

from typing import List, Dict, Any, Optional, Tuple
import re
import uuid

from .models import AgentStep, ToolCall


class DeterministicReActEngine:
    """Simulates an LLM ReAct reasoning loop (Thought -> Action -> Observation -> Final Answer)."""

    def __init__(self, agent_name: str = "MiniAgent") -> None:
        self.agent_name = agent_name

    def plan_next_step(
        self,
        query: str,
        history: List[Dict[str, Any]],
        steps: List[AgentStep],
        available_tools: List[str]
    ) -> Tuple[str, Optional[ToolCall], Optional[str]]:
        """Determines the next action in the ReAct loop.

        Returns:
            Tuple of (thought, tool_call, final_answer)
            - If final_answer is not None, the task is finished.
            - If tool_call is not None, the agent must execute this tool.
        """
        step_idx = len(steps) + 1
        q_lower = query.lower()

        # Check if the last observation had an error and needs self-correction
        if steps and steps[-1].observation and ("error" in steps[-1].observation.lower() or "exception" in steps[-1].observation.lower()):
            last_obs = steps[-1].observation
            thought = f"Previous attempt failed with error: '{last_obs}'. Formulating corrected approach."
            # Attempt correction if it was calculator syntax
            if steps[-1].tool_call and steps[-1].tool_call.tool_name == "calculator":
                # Fix expression if possible
                corrected_expr = "10 + 20"
                tool_call = ToolCall(
                    id=f"call_{uuid.uuid4().hex[:8]}",
                    tool_name="calculator",
                    arguments={"expression": corrected_expr}
                )
                return thought, tool_call, None

        # 1. Information Retrieval / Search Queries (prioritized when explicitly asked to search)
        if q_lower.startswith("search") or "search for" in q_lower or any(k in q_lower for k in ["find articles", "lookup in docs"]):
            if "local_search" in available_tools:
                if not steps:
                    search_q = query.replace("search for", "").replace("Search for", "").replace("search", "").replace("Search", "").strip()
                    thought = f"The user is looking for information. I will search the local knowledge base for '{search_q}'."
                    tool_call = ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        tool_name="local_search",
                        arguments={"query": search_q, "domain": "python"}
                    )
                    return thought, tool_call, None
                else:
                    obs = steps[-1].observation
                    thought = f"Retrieved knowledge results: {obs}. Formulating comprehensive response."
                    final_answer = f"Based on local documentation:\n{obs}"
                    return thought, None, final_answer

        # 2. Python Code Execution Queries
        if any(keyword in q_lower for keyword in ["python", "script", "run code", "execute"]):
            if "run_python" in available_tools:
                if not steps:
                    code_snippet = self._extract_or_generate_python(query)
                    thought = f"The user requested Python code execution. Running safe subprocess with code:\n{code_snippet}"
                    tool_call = ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        tool_name="run_python",
                        arguments={"code": code_snippet, "timeout": 3.0}
                    )
                    return thought, tool_call, None
                else:
                    obs = steps[-1].observation
                    thought = f"Code execution output received: {obs}. Returning result to user."
                    final_answer = f"Python Execution Output:\n{obs}"
                    return thought, None, final_answer

        # 2. Time / Date Queries
        if any(keyword in q_lower for keyword in ["time", "date", "clock", "timestamp"]):
            if "get_time" in available_tools:
                if not steps:
                    thought = "User inquired about the current time. Invoking get_time tool."
                    tool_call = ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        tool_name="get_time",
                        arguments={}
                    )
                    return thought, tool_call, None
                else:
                    obs = steps[-1].observation
                    thought = f"Current timestamp is {obs}. Returning answer."
                    final_answer = f"The current system time is {obs}."
                    return thought, None, final_answer

        # 3. Information Retrieval / Search Queries
        if any(keyword in q_lower for keyword in ["search", "find", "lookup", "tell me about", "what are", "how does"]):
            if "local_search" in available_tools:
                if not steps:
                    search_q = query.replace("search for", "").replace("search", "").strip()
                    thought = f"The user is looking for information. I will search the local knowledge base for '{search_q}'."
                    tool_call = ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        tool_name="local_search",
                        arguments={"query": search_q, "domain": "python"}
                    )
                    return thought, tool_call, None
                else:
                    obs = steps[-1].observation
                    thought = f"Retrieved knowledge results: {obs}. Formulating comprehensive response."
                    final_answer = f"Based on local documentation:\n{obs}"
                    return thought, None, final_answer

        # 4. Math / Arithmetic Queries
        if any(keyword in q_lower for keyword in ["calculate", "math", "+", "-", "*", "/", "%", "**"]) or (
            "what is" in q_lower and any(op in query for op in ["+", "-", "*", "/", "%", "**"])
        ):
            math_expr = self._extract_math_expression(query)
            if math_expr and "calculator" in available_tools:
                if not steps:
                    thought = f"The user wants to evaluate an arithmetic expression. I will use the calculator tool to compute: '{math_expr}'."
                    tool_call = ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        tool_name="calculator",
                        arguments={"expression": math_expr}
                    )
                    return thought, tool_call, None
                else:
                    obs = steps[-1].observation
                    thought = f"Calculation yielded: {obs}. I have sufficient information to answer the user."
                    final_answer = f"The result of {math_expr} is {obs}."
                    return thought, None, final_answer

        # 5. Default General Response (No tool needed)
        thought = "Direct response is suitable without invoking additional tools."
        final_answer = f"Hello! I am {self.agent_name}. I received your query: '{query}'. How can I assist you further?"
        return thought, None, final_answer

    @staticmethod
    def _extract_math_expression(query: str) -> Optional[str]:
        # Look for parenthesized or arithmetic math substrings
        # e.g. "What is (25 * 4) + (100 / 5)?" -> "(25 * 4) + (100 / 5)"
        match = re.search(r"[\d\(\)\s\+\-\*\/\.\%]{3,}", query)
        if match:
            candidate = match.group(0).strip().rstrip("?").strip()
            # Verify candidate has digits
            if any(c.isdigit() for c in candidate):
                return candidate
        return "2 + 2"

    @staticmethod
    def _extract_or_generate_python(query: str) -> str:
        if "squares" in query.lower():
            return "print([x**2 for x in range(1, 6)])"
        if "hello" in query.lower():
            return "print('Hello World from MiniAgent!')"
        return "import sys; print('Python executable:', sys.version.split()[0])"
