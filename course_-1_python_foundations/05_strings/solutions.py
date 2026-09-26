"""
Module 05: Strings — Reference Solutions
========================================
Complete, verified implementations for all four exercise tiers.
"""

from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def string_operations_recall() -> Dict[str, Any]:
    """
    Evaluates requested string operations.
    """
    sample = "AutonomousAgent"
    name = "Agent-47"
    score = 0.91234

    return {
        "first_char": sample[0],
        "last_char": sample[-1],
        "slice_auto": sample[:10],
        "slice_agent": sample[10:],
        "stride_two": sample[::2],
        "reversed_str": sample[::-1],
        "fstring_format": f"Agent: {name} | Score: {score:.1%}",
        "split_count": len("alpha,beta,gamma,delta".split(",")),
    }


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def clean_user_prompt(raw_text: str) -> str:
    """
    Sanitizes raw user prompt text submitted to an AI agent.
    """
    if not raw_text or not raw_text.strip():
        return ""

    # 1. Normalize internal whitespace by splitting and rejoining
    tokens = raw_text.split()
    normalized = " ".join(tokens).strip()

    if not normalized:
        return ""

    # 2. Check for matching outer quotes
    if len(normalized) >= 2:
        if (normalized.startswith('"') and normalized.endswith('"')) or \
           (normalized.startswith("'") and normalized.endswith("'")):
            normalized = normalized[1:-1].strip()

    if not normalized:
        return ""

    # 3. Ensure valid terminal punctuation
    if not normalized.endswith((".", "?", "!")):
        normalized += "."

    return normalized


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def extract_markdown_code_blocks(markdown_text: str) -> List[Tuple[str, str]]:
    """
    Extracts all fenced code blocks from markdown text.
    """
    blocks: List[Tuple[str, str]] = []
    pos = 0
    fence = "```"

    while True:
        start_idx = markdown_text.find(fence, pos)
        if start_idx == -1:
            break

        # Find the end of the opening fence line to get language identifier
        line_break_idx = markdown_text.find("\n", start_idx + len(fence))
        if line_break_idx == -1:
            # No newline after fence, cannot be a valid code block
            break

        raw_lang = markdown_text[start_idx + len(fence):line_break_idx].strip()
        lang = raw_lang.lower() if raw_lang else "text"

        code_start = line_break_idx + 1

        # Search for closing fence
        end_idx = markdown_text.find(fence, code_start)
        if end_idx == -1:
            # Unclosed fence, ignore
            break

        code_body = markdown_text[code_start:end_idx].strip()
        blocks.append((lang, code_body))

        # Advance pointer past closing fence
        pos = end_idx + len(fence)

    return blocks


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def parse_agent_log_entry(raw_line: str) -> Dict[str, Any]:
    """
    Parses a single formatted log line from an autonomous agent execution log.
    Format: [TIMESTAMP] [LEVEL] [AGENT_NAME] MESSAGE (tokens=INT, latency_ms=FLOAT, status=STR)
    """
    line = raw_line.strip()

    # Extract bracketed tokens
    # Find bracket 1: timestamp
    t_start = line.find("[")
    t_end = line.find("]", t_start)
    if t_start == -1 or t_end == -1:
        raise ValueError("Log line missing timestamp brackets")
    timestamp = line[t_start + 1:t_end].strip()

    # Find bracket 2: level
    l_start = line.find("[", t_end)
    l_end = line.find("]", l_start)
    if l_start == -1 or l_end == -1:
        raise ValueError("Log line missing level brackets")
    level = line[l_start + 1:l_end].strip()

    # Find bracket 3: agent name
    a_start = line.find("[", l_end)
    a_end = line.find("]", a_start)
    if a_start == -1 or a_end == -1:
        raise ValueError("Log line missing agent_name brackets")
    agent_name = line[a_start + 1:a_end].strip()

    # Remaining string after 3rd closing bracket
    remainder = line[a_end + 1:].strip()

    # Check for metadata in parentheses at the end
    p_start = remainder.rfind("(")
    p_end = remainder.rfind(")")

    if p_start != -1 and p_end != -1 and p_end > p_start:
        message = remainder[:p_start].strip()
        meta_str = remainder[p_start + 1:p_end].strip()
    else:
        message = remainder
        meta_str = ""

    tokens = 0
    latency_ms = 0.0
    status = "UNKNOWN"

    if meta_str:
        # Key-value pairs separated by commas
        for item in meta_str.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                k = k.strip().lower()
                v = v.strip()
                if k == "tokens":
                    tokens = int(v)
                elif k == "latency_ms":
                    latency_ms = float(v)
                elif k == "status":
                    status = v

    return {
        "timestamp": timestamp,
        "level": level,
        "agent_name": agent_name,
        "message": message,
        "tokens": tokens,
        "latency_ms": latency_ms,
        "status": status,
    }


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    recall = string_operations_recall()
    assert recall["first_char"] == "A"
    assert recall["last_char"] == "t"
    assert recall["slice_auto"] == "Autonomous"
    assert recall["slice_agent"] == "Agent"
    assert recall["stride_two"] == "AtnmuAet"
    assert recall["reversed_str"] == "tnegAsuomonotuA"
    assert recall["fstring_format"] == "Agent: Agent-47 | Score: 91.2%"
    assert recall["split_count"] == 4

    # Test Level 2
    assert clean_user_prompt("   hello  world   ") == "hello world."
    assert clean_user_prompt('"What is the weather?"') == "What is the weather?"
    assert clean_user_prompt("'Execute immediately!'") == "Execute immediately!"
    assert clean_user_prompt("   ") == ""
    assert clean_user_prompt("Line1\n\nLine2\tLine3") == "Line1 Line2 Line3."

    # Test Level 3
    sample_md = """
    Intro text
    ```python
    x = 10
    print(x)
    ```
    Middle text
    ```
    plain unformatted
    text
    ```
    Outro
    """
    blocks = extract_markdown_code_blocks(sample_md)
    assert len(blocks) == 2
    assert blocks[0] == ("python", "x = 10\n    print(x)")
    assert blocks[1] == ("text", "plain unformatted\n    text")

    # Empty check
    assert extract_markdown_code_blocks("No code here") == []

    # Test Level 4
    log_line = "[2026-09-21 14:30:00] [INFO] [Agent-Alpha] Task completed (tokens=120, latency_ms=45.20, status=SUCCESS)"
    parsed = parse_agent_log_entry(log_line)
    assert parsed["timestamp"] == "2026-09-21 14:30:00"
    assert parsed["level"] == "INFO"
    assert parsed["agent_name"] == "Agent-Alpha"
    assert parsed["message"] == "Task completed"
    assert parsed["tokens"] == 120
    assert abs(parsed["latency_ms"] - 45.20) < 1e-5
    assert parsed["status"] == "SUCCESS"

    print("Module 05: All Level 1-4 solutions verified successfully!")
