"""structured_protocol.py - Demonstrates XML delimiter protocol and few-shot formatting.

Key concepts demonstrated:
1. Formatting few-shot examples in XML structure.
2. Generating a complete ReAct system prompt.
3. Parsing <thought>, <action>, and <final_answer> tags.
"""

from typing import List, Dict, Any, Optional
import re
import json


class StructuredOutputProtocol:
    """Manages few-shot prompt compilation and XML tag parsing."""

    SYSTEM_TEMPLATE = """You are an autonomous AI Agent operating under a strict ReAct protocol.

<tools>
{tools_manifest}
</tools>

<protocol_rules>
1. Always begin every step with <thought> explaining your reasoning.
2. If you need to invoke a tool, output <action>TOOL_NAME {{"arg": "val"}}</action>.
3. When you have answered the user, output <final_answer>YOUR COMPLETE ANSWER</final_answer>.
4. Do NOT output plain text outside the XML tags.
</protocol_rules>

<few_shot_examples>
{few_shot_blocks}
</few_shot_examples>
"""

    @classmethod
    def compile_system_prompt(cls, tools: List[Dict[str, str]], examples: List[Dict[str, str]]) -> str:
        """Compiles the system prompt with tool manifests and few-shot blocks."""
        tools_str = "\n".join(f"- {t['name']}: {t['description']}" for t in tools)

        example_blocks = []
        for i, ex in enumerate(examples, 1):
            block = (
                f"<example id='{i}'>\n"
                f"  <user>{ex['user']}</user>\n"
                f"  <thought>{ex['thought']}</thought>\n"
                f"  <action>{ex['action']}</action>\n"
                f"  <final_answer>{ex['final_answer']}</final_answer>\n"
                f"</example>"
            )
            example_blocks.append(block)

        examples_str = "\n".join(example_blocks)
        return cls.SYSTEM_TEMPLATE.format(
            tools_manifest=tools_str,
            few_shot_blocks=examples_str
        )

    @classmethod
    def parse_response(cls, model_output: str) -> Dict[str, Optional[str]]:
        """Parses thought, action, and final_answer from XML tags."""
        thought_match = re.search(r"<thought>(.*?)</thought>", model_output, re.DOTALL)
        action_match = re.search(r"<action>(.*?)</action>", model_output, re.DOTALL)
        final_match = re.search(r"<final_answer>(.*?)</final_answer>", model_output, re.DOTALL)

        return {
            "thought": thought_match.group(1).strip() if thought_match else None,
            "action": action_match.group(1).strip() if action_match else None,
            "final_answer": final_match.group(1).strip() if final_match else None,
        }


def main() -> None:
    print("=== Module 12: Structured Output Protocol Demo ===")

    tools = [
        {"name": "calculator", "description": "Evaluates math expressions"},
        {"name": "search", "description": "Searches internal documentation"}
    ]

    examples = [
        {
            "user": "What is 12 * 12?",
            "thought": "I will calculate 12 * 12 using the calculator tool.",
            "action": 'calculator {"expression": "12 * 12"}',
            "final_answer": "12 * 12 is 144."
        }
    ]

    prompt = StructuredOutputProtocol.compile_system_prompt(tools, examples)
    assert "<protocol_rules>" in prompt
    assert "<example id='1'>" in prompt
    assert "calculator: Evaluates math expressions" in prompt
    print("[OK] Compiled system prompt with few-shot examples verified.")

    # Test parsing a simulated model output
    sample_model_output = """
    <thought>
    The user asked for the square of 9. I should compute 9 * 9.
    </thought>
    <action>calculator {"expression": "9 * 9"}</action>
    """

    parsed = StructuredOutputProtocol.parse_response(sample_model_output)
    assert parsed["thought"] == "The user asked for the square of 9. I should compute 9 * 9."
    assert parsed["action"] == 'calculator {"expression": "9 * 9"}'
    assert parsed["final_answer"] is None
    print(f"[OK] Parsed thought: {parsed['thought']}")
    print(f"[OK] Parsed action: {parsed['action']}")

    # Test final answer output
    final_output = "<thought>Calculation returned 81.</thought><final_answer>The answer is 81.</final_answer>"
    parsed_final = StructuredOutputProtocol.parse_response(final_output)
    assert parsed_final["final_answer"] == "The answer is 81."
    assert parsed_final["action"] is None
    print(f"[OK] Parsed final answer: {parsed_final['final_answer']}")

    print("All tests in structured_protocol.py passed successfully!\n")


if __name__ == "__main__":
    main()
