"""state_machine.py - Deterministic Finite State Machine (FSM) for AI agent reasoning loops.

Key concepts demonstrated:
1. Explicit states: IDLE, PLANNING, EXECUTING, EVALUATING, FINISHED, ERROR.
2. State transition guards enforcing legal transitions and step limits.
3. Transition history tracking for observability.
"""

from enum import Enum, auto
from typing import Set, Dict, List, Tuple
import time


class AgentState(Enum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    EVALUATING = auto()
    FINISHED = auto()
    ERROR = auto()


class AgentStateMachine:
    """Manages legal agent state transitions with step guards."""

    ALLOWED_TRANSITIONS: Dict[AgentState, Set[AgentState]] = {
        AgentState.IDLE: {AgentState.PLANNING, AgentState.ERROR},
        AgentState.PLANNING: {AgentState.EXECUTING, AgentState.FINISHED, AgentState.ERROR},
        AgentState.EXECUTING: {AgentState.EVALUATING, AgentState.ERROR},
        AgentState.EVALUATING: {AgentState.PLANNING, AgentState.FINISHED, AgentState.ERROR},
        AgentState.FINISHED: set(),  # Terminal state
        AgentState.ERROR: set(),     # Terminal state
    }

    def __init__(self, max_steps: int = 5) -> None:
        self.state = AgentState.IDLE
        self.max_steps = max_steps
        self.current_step = 0
        self.history: List[Tuple[AgentState, AgentState, float]] = []

    def transition(self, target_state: AgentState, reason: str = "") -> None:
        """Transitions to the target state if permitted by rules and guards."""
        # 1. Guard against step exhaustion before planning new actions
        if target_state == AgentState.PLANNING and self.current_step >= self.max_steps:
            print(f"[GUARD] Max step limit ({self.max_steps}) reached. Diverting to ERROR.")
            self._apply_transition(AgentState.ERROR, f"Exceeded max steps ({self.max_steps})")
            return

        # 2. Check transition legality
        allowed = self.ALLOWED_TRANSITIONS.get(self.state, set())
        if target_state not in allowed:
            err_msg = f"Illegal transition: Cannot move from {self.state.name} to {target_state.name}"
            self._apply_transition(AgentState.ERROR, err_msg)
            raise ValueError(err_msg)

        if target_state == AgentState.PLANNING:
            self.current_step += 1

        self._apply_transition(target_state, reason)

    def _apply_transition(self, new_state: AgentState, reason: str) -> None:
        old_state = self.state
        self.state = new_state
        self.history.append((old_state, new_state, time.time()))
        print(f"[FSM] {old_state.name} -> {new_state.name} (Step {self.current_step}/{self.max_steps}) {reason}")

    @property
    def is_terminal(self) -> bool:
        return self.state in (AgentState.FINISHED, AgentState.ERROR)


def simulate_agent_task(max_steps: int, steps_needed: int) -> AgentStateMachine:
    """Runs a simulated FSM agent execution."""
    fsm = AgentStateMachine(max_steps=max_steps)
    fsm.transition(AgentState.PLANNING, reason="User query received")

    while not fsm.is_terminal:
        if fsm.state == AgentState.PLANNING:
            if fsm.current_step >= steps_needed:
                fsm.transition(AgentState.FINISHED, reason="Task completed")
            else:
                fsm.transition(AgentState.EXECUTING, reason="Executing planned tool")
        elif fsm.state == AgentState.EXECUTING:
            fsm.transition(AgentState.EVALUATING, reason="Tool execution finished")
        elif fsm.state == AgentState.EVALUATING:
            fsm.transition(AgentState.PLANNING, reason="Evaluating observation, replanning")

    return fsm


def main() -> None:
    print("=== Module 11: Agent State Machine (FSM) Demo ===")

    # Scenario 1: Normal task completing within step budget
    print("--- Scenario 1: Task finishes within limit ---")
    fsm1 = simulate_agent_task(max_steps=5, steps_needed=3)
    assert fsm1.state == AgentState.FINISHED
    assert fsm1.current_step == 3
    print(f"[OK] Scenario 1 completed in FINISHED state after {fsm1.current_step} steps.")

    # Scenario 2: Runaway task hitting step guard
    print("\n--- Scenario 2: Runaway task hits step guard ---")
    fsm2 = simulate_agent_task(max_steps=3, steps_needed=10)
    assert fsm2.state == AgentState.ERROR
    assert fsm2.current_step == 3
    print(f"[OK] Scenario 2 halted cleanly in ERROR state due to step guard.")

    # Scenario 3: Illegal transition detection
    print("\n--- Scenario 3: Illegal transition check ---")
    fsm3 = AgentStateMachine()
    try:
        # Cannot jump from IDLE directly to EXECUTING
        fsm3.transition(AgentState.EXECUTING)
        raise AssertionError("Should have raised ValueError")
    except ValueError as err:
        assert fsm3.state == AgentState.ERROR
        print(f"[OK] Caught illegal transition: {err}")

    print("\nAll tests in state_machine.py passed successfully!\n")


if __name__ == "__main__":
    main()
