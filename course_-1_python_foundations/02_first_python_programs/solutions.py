"""
Module 02: First Python Programs — Reference Solutions
=======================================================
Clean, working implementations for all four exercise tiers.
"""

from typing import List


# =====================================================================
# Level 1: Recall Solution
# =====================================================================
def predict_print_output() -> str:
    """
    print("Apple", "Banana", "Cherry", sep="::", end="!")
    Joins args with "::" and appends "!":
        "Apple::Banana::Cherry!"
    """
    return "Apple::Banana::Cherry!"


# =====================================================================
# Level 2: Modify Solution
# =====================================================================
def format_pipeline_stage(stages: List[str]) -> str:
    """
    Constructs "[stage1 -> stage2 -> ...]\n"
    """
    if not stages:
        return "[]\n"
    joined = " -> ".join(stages)
    return f"[{joined}]\n"


# =====================================================================
# Level 3: Build Solution
# =====================================================================
def build_agent_header(agent_name: str, status: str, step: int, total_steps: int) -> str:
    """
    Constructs a 4-line ASCII status banner.
    """
    border = "-" * 40 + "\n"
    line2 = f"AGENT: {agent_name} | STATUS: {status}\n"
    line3 = f"PROGRESS: Step {step} of {total_steps}\n"
    return border + line2 + line3 + border


# =====================================================================
# Level 4: Debug Solution
# =====================================================================
def debug_escaped_path(drive: str, folder: str, filename: str) -> str:
    """
    Correctly escapes backslashes to format: "<drive>:\\<folder>\\<filename>"
    """
    return f"{drive}:\\{folder}\\{filename}"


# =====================================================================
# Verification Runner
# =====================================================================
if __name__ == "__main__":
    # Test Level 1
    out = predict_print_output()
    assert out == "Apple::Banana::Cherry!", f"Level 1 failed: {out}"

    # Test Level 2
    stages = ["PLAN", "FETCH", "GENERATE", "AUDIT"]
    pipe_str = format_pipeline_stage(stages)
    assert pipe_str == "[PLAN -> FETCH -> GENERATE -> AUDIT]\n", f"Level 2 failed: {pipe_str}"
    assert format_pipeline_stage([]) == "[]\n"

    # Test Level 3
    hdr = build_agent_header("Scout", "SCANNING", 3, 10)
    expected_hdr = (
        "----------------------------------------\n"
        "AGENT: Scout | STATUS: SCANNING\n"
        "PROGRESS: Step 3 of 10\n"
        "----------------------------------------\n"
    )
    assert hdr == expected_hdr, f"Level 3 failed:\n{hdr}\nvs\n{expected_hdr}"

    # Test Level 4
    win_path = debug_escaped_path("C", "Users\\Alice", "report.json")
    assert win_path == "C:\\Users\\Alice\\report.json", f"Level 4 failed: {win_path}"

    print("Module 02: All Level 1-4 solutions verified successfully!")
