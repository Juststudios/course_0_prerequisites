"""
Module 05: Strings — Exercises
===============================
Complete each of the four levels below.
Each level exercises your understanding of indexing, slicing, immutability,
f-string formatting, and text parsing algorithms.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall
# =====================================================================
def string_operations_recall() -> Dict[str, Any]:
    """
    Recall Exercise:
    Given the reference string:
        sample = "AutonomousAgent"

    Return a dictionary with the exact results of the following string operations:
        - "first_char": The first character of sample
        - "last_char": The last character of sample using negative indexing
        - "slice_auto": The first 10 characters ("Autonomous")
        - "slice_agent": The characters from index 10 to the end ("Agent")
        - "stride_two": Every second character starting from index 0
        - "reversed_str": The entire string reversed using slicing
        - "fstring_format": Formatted string using name="Agent-47" and score=0.91234
          matching exactly: "Agent: Agent-47 | Score: 91.2%"
        - "split_count": The number of items obtained from "alpha,beta,gamma,delta".split(",")

    # TODO: Return dictionary with the exact requested results.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 1: Implement string_operations_recall().")


# =====================================================================
# Level 2: Modify
# =====================================================================
def clean_user_prompt(raw_text: str) -> str:
    """
    Modify Exercise:
    Sanitizes raw user prompt text submitted to an AI agent:

    Rules:
    1. If `raw_text` is empty or only whitespace, return an empty string `""`.
    2. Strip leading and trailing whitespace.
    3. Normalize all internal whitespace (consecutive spaces, tabs, newlines) into a single space.
       (Hint: `split()` with no arguments splits on any whitespace runs).
    4. If the stripped string starts and ends with matching quotes (either single `'...'`
       or double `"..."`), remove the outer pair of quotes and strip again.
    5. Ensure the cleaned prompt ends with valid punctuation: `.`, `?`, or `!`.
       If it does not end with one of these three punctuation marks, append a period `.` to the end.

    # TODO: Implement the prompt sanitization pipeline.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement clean_user_prompt().")


# =====================================================================
# Level 3: Build
# =====================================================================
def extract_markdown_code_blocks(markdown_text: str) -> List[Tuple[str, str]]:
    """
    Build Exercise:
    Parse an arbitrary markdown document and extract all fenced code blocks.

    Fenced code blocks begin with three backticks followed by an optional language tag,
    a newline, the code content, and a closing triple backtick line:
        ```python
        print("hello")
        ```
        or
        ```
        plain text
        ```

    Requirements:
    1. Return a list of tuples: `[(language, code_body), ...]` in order of appearance.
    2. The language tag must be stripped and lowercased. If no language tag is provided
       on the opening fence line, default to `"text"`.
    3. The `code_body` must have leading and trailing whitespace stripped.
    4. If an opening fence has no matching closing fence before EOF, ignore that block.
    5. If markdown_text contains no code blocks, return an empty list `[]`.

    # TODO: Build the fenced code block extractor.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement extract_markdown_code_blocks().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def parse_agent_log_entry(raw_line: str) -> Dict[str, Any]:
    """
    Debug Exercise:
    Parses a single formatted log line from an autonomous agent execution log.

    Log format standard:
      "[TIMESTAMP] [LEVEL] [AGENT_NAME] MESSAGE (tokens=INT, latency_ms=FLOAT, status=STR)"

    Example line:
      "[2026-09-21 14:30:00] [INFO] [Agent-Alpha] Task completed (tokens=120, latency_ms=45.20, status=SUCCESS)"

    Expected return dictionary:
      {
          "timestamp": "2026-09-21 14:30:00",  # str without brackets
          "level": "INFO",                     # str without brackets
          "agent_name": "Agent-Alpha",         # str without brackets
          "message": "Task completed",         # str stripped
          "tokens": 120,                       # int
          "latency_ms": 45.20,                 # float
          "status": "SUCCESS"                  # str
      }

    Buggy implementation details:
    - Attempting raw `.split(" ")` causes the timestamp `2026-09-21 14:30:00` to be split in half!
    - Uses hardcoded slice positions which crash when agent names or messages vary in length.
    - Fails to convert `tokens` to `int` and `latency_ms` to `float`.
    - Crashes on malformed or slightly different bracket spacing.

    # TODO: Fix the bugs using robust string methods (.find, .split, .strip, etc.).
    """
    # TODO: Replace the line below with your fixed implementation
    raise NotImplementedError("Level 4: Fix parse_agent_log_entry().")


if __name__ == "__main__":
    print("Module 05 Exercises loaded successfully.")
    print("Implement the functions above or run solutions.py to verify.")
