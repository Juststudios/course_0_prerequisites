"""repair_malformed_json.py - Heuristic extraction, repair, and bracket balancing for LLM outputs.

Key concepts demonstrated:
1. Stripping markdown code fences (```json ... ```) and conversational preamble/postscript.
2. Replacing Python single-quotes, booleans, and None with JSON equivalents.
3. Removing trailing commas before closing braces/brackets.
4. Stack-based bracket balancing for truncated JSON responses.
"""

from typing import Dict, Any, Optional
import re
import json


class LLMJSONRepair:
    """Production utility to sanitize and recover JSON from malformed LLM completions."""

    @classmethod
    def extract_and_repair(cls, raw_llm_text: str) -> Dict[str, Any]:
        """Extracts JSON substring, heals common syntax errors, and parses into a Python dict."""
        cleaned = cls.strip_markdown_fences(raw_llm_text)
        healed = cls.repair_syntax(cleaned)
        balanced = cls.balance_brackets(healed)

        try:
            return json.loads(balanced)
        except json.JSONDecodeError as err:
            raise ValueError(
                f"Failed to recover valid JSON after repair pipeline.\n"
                f"Original: {raw_llm_text!r}\n"
                f"Repaired: {balanced!r}\n"
                f"Error: {err}"
            )

    @staticmethod
    def strip_markdown_fences(text: str) -> str:
        """Strips conversational intro and ```json ... ``` code fences."""
        text = text.strip()
        # Look for explicit ```json ... ``` blocks
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if fence_match:
            return fence_match.group(1).strip()

        # If no fences, find boundary between first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1].strip()

        # Or between first '[' and last ']'
        start_arr = text.find("[")
        end_arr = text.rfind("]")
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            return text[start_arr : end_arr + 1].strip()

        return text

    @staticmethod
    def repair_syntax(text: str) -> str:
        """Heuristic fixes for trailing commas, single quotes, and Python literals."""
        # 1. Replace single quotes used for JSON keys and values with double quotes
        # (Preserve internal apostrophes like "it's" if possible)
        text = re.sub(r"(?<=[{\[,:\s])'([^'\n\r]+?)'(?=[\s,\]}:])", r'"\1"', text)

        # 2. Replace Python literals with JSON literals
        text = re.sub(r"\bTrue\b", "true", text)
        text = re.sub(r"\bFalse\b", "false", text)
        text = re.sub(r"\bNone\b", "null", text)

        # 3. Strip trailing commas before closing braces/brackets
        text = re.sub(r",\s*([\]}])", r"\1", text)

        return text

    @staticmethod
    def balance_brackets(text: str) -> str:
        """Uses a stack to append missing closing quotes, braces, and brackets for truncated responses."""
        stack = []
        in_string = False
        escape = False

        for char in text:
            if char == '"' and not escape:
                in_string = not in_string
            elif not in_string:
                if char == "{":
                    stack.append("}")
                elif char == "[":
                    stack.append("]")
                elif char in ("}", "]"):
                    if stack and stack[-1] == char:
                        stack.pop()
            escape = (char == "\\" and not escape)

        # Close open string quote
        if in_string:
            text += '"'

        # Append missing closing brackets in reverse order
        while stack:
            text += stack.pop()

        return text


def main() -> None:
    print("=== Module 07: Malformed LLM JSON Repair Demo ===")

    # Test Case 1: Markdown code fence with conversational preamble
    case1 = """
    Certainly! Here is the tool call you requested:
    ```json
    {
        "action": "web_search",
        "query": "python contextvars"
    }
    ```
    I hope this helps!
    """
    res1 = LLMJSONRepair.extract_and_repair(case1)
    assert res1["action"] == "web_search"
    assert res1["query"] == "python contextvars"
    print("[OK] Case 1: Stripped markdown fences and preamble successfully.")

    # Test Case 2: Trailing commas and single quotes
    case2 = "{'action': 'calculator', 'expression': '2 + 2',}"
    res2 = LLMJSONRepair.extract_and_repair(case2)
    assert res2["action"] == "calculator"
    assert res2["expression"] == "2 + 2"
    print("[OK] Case 2: Fixed single quotes and trailing commas successfully.")

    # Test Case 3: Python literals (True, False, None)
    case3 = '{"is_active": True, "details": None, "flags": [False,]}'
    res3 = LLMJSONRepair.extract_and_repair(case3)
    assert res3["is_active"] is True
    assert res3["details"] is None
    assert res3["flags"] == [False]
    print("[OK] Case 3: Replaced Python literals (True/False/None) successfully.")

    # Test Case 4: Truncated JSON stream (missing closing brackets)
    case4 = '{"status": "in_progress", "results": [{"id": 1, "title": "First"'
    res4 = LLMJSONRepair.extract_and_repair(case4)
    assert res4["status"] == "in_progress"
    assert res4["results"][0]["id"] == 1
    print("[OK] Case 4: Balanced truncated brackets successfully.")

    print("All tests in repair_malformed_json.py passed successfully!\n")


if __name__ == "__main__":
    main()
