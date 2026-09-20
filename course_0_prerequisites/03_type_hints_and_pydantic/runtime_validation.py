"""runtime_validation.py - Demonstrates catching ValidationError and generating LLM self-correction feedback.

Key concepts demonstrated:
1. Catching and decomposing Pydantic ValidationError objects.
2. Generating structured error prompts for LLM self-correction.
3. Simulating an autonomous error-recovery retry loop.
"""

from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field, ValidationError


class CalculatorInput(BaseModel):
    """Input parameters for mathematical calculations."""
    expression: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="A clean arithmetic expression without variables (e.g. '12 * 8')."
    )
    precision: int = Field(
        default=2,
        ge=0,
        le=6,
        description="Decimal places for rounding the result (0-6)."
    )


def format_validation_feedback(error: ValidationError, original_payload: Dict[str, Any]) -> str:
    """Transforms a Pydantic ValidationError into a corrective prompt for an LLM."""
    lines = [
        "TOOL INVOCATION FAILED: The arguments provided did not match the required schema.",
        f"Original Payload: {original_payload}",
        "Specific Violations:"
    ]
    for issue in error.errors():
        field_path = ".".join(str(p) for p in issue["loc"])
        msg = issue["msg"]
        err_type = issue["type"]
        lines.append(f"  - Field '{field_path}': {msg} (Error type: {err_type})")
    lines.append("Please adjust the arguments to strictly satisfy the schema constraints and try again.")
    return "\n".join(lines)


def simulate_agent_tool_invocation(raw_payloads: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """Simulates an agent attempting tool execution across successive turns."""
    for turn, payload in enumerate(raw_payloads, start=1):
        print(f"\n--- Turn {turn}: Attempting tool validation with payload: {payload} ---")
        try:
            validated_args = CalculatorInput.model_validate(payload)
            print(f"Validation SUCCESS on Turn {turn}!")
            # Execute calculation
            # Safe evaluation for demo purposes
            result = round(eval(validated_args.expression, {"__builtins__": None}, {}), validated_args.precision)
            return True, f"Calculation result: {result}"
        except ValidationError as e:
            feedback = format_validation_feedback(e, payload)
            print(f"Validation FAILED on Turn {turn}. Generated LLM feedback:\n{feedback}")
        except Exception as e:
            return False, f"Execution failed: {e}"

    return False, "Max retries exceeded without valid tool call."


def main() -> None:
    print("=== Module 03: Runtime Validation & Self-Correction Demo ===")

    # Scenario:
    # Turn 1: LLM outputs an invalid payload (precision = 10 exceeds max 6, empty expression)
    # Turn 2: LLM adjusts based on feedback, provides valid expression but precision is still -1
    # Turn 3: LLM corrects all fields and successfully executes
    trajectories = [
        {"expression": "", "precision": 10},
        {"expression": "45 * 2.5", "precision": -1},
        {"expression": "45 * 2.5", "precision": 2},
    ]

    success, message = simulate_agent_tool_invocation(trajectories)
    assert success is True, "Expected eventual success after self-correction"
    assert "112.5" in message
    print(f"\n[FINAL OUTCOME]: {message}")
    print("All tests in runtime_validation.py completed successfully!\n")


if __name__ == "__main__":
    main()
