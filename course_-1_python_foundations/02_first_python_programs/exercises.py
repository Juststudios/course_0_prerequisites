"""
Module 02: First Python Programs — Exercises
=============================================
Complete each of the four levels below.
Each level exercises your understanding of stdout, print(), separators, and escape characters.
"""

from typing import List


# =====================================================================
# Level 1: Recall
# =====================================================================
def predict_print_output() -> str:
    """
    Recall Exercise:
    Consider the following statement:
        print("Apple", "Banana", "Cherry", sep="::", end="!")

    # TODO: Return the exact string that is emitted to stdout.
    """
    # TODO: Replace the line below with the exact string output
    raise NotImplementedError("Level 1: Complete predict_print_output() with exact stdout characters.")


# =====================================================================
# Level 2: Modify
# =====================================================================
def format_pipeline_stage(stages: List[str]) -> str:
    """
    Modify Exercise:
    Given a list of pipeline stage names (e.g. ["PLAN", "FETCH", "GENERATE", "AUDIT"]),
    construct a single string that joins the stages using " -> " as the separator,
    and wraps the entire pipeline inside brackets with a trailing newline:
    Example output: "[PLAN -> FETCH -> GENERATE -> AUDIT]\n"

    If the list is empty, return "[]\n".

    # TODO: Implement format_pipeline_stage using separator formatting logic.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 2: Implement format_pipeline_stage().")


# =====================================================================
# Level 3: Build
# =====================================================================
def build_agent_header(agent_name: str, status: str, step: int, total_steps: int) -> str:
    """
    Build Exercise:
    Construct an ASCII banner representing an agent status monitor.
    The banner must match this exact format:
    Line 1: 40 hyphens: "----------------------------------------\n"
    Line 2: "AGENT: <agent_name> | STATUS: <status>\n"
    Line 3: "PROGRESS: Step <step> of <total_steps>\n"
    Line 4: 40 hyphens: "----------------------------------------\n"

    Example for ("Scout", "SCANNING", 3, 10):
    ----------------------------------------\nAGENT: Scout | STATUS: SCANNING\nPROGRESS: Step 3 of 10\n----------------------------------------\n

    # TODO: Build and return the formatted header string.
    """
    # TODO: Replace the line below with your implementation
    raise NotImplementedError("Level 3: Implement build_agent_header().")


# =====================================================================
# Level 4: Debug
# =====================================================================
def debug_escaped_path(drive: str, folder: str, filename: str) -> str:
    r"""
    Debugging Exercise:
    A student wrote a function to construct a Windows-style file path:
        "C:\\Users\\Alice\\Documents\\data.json"
    Their original draft had severe escape sequence and quote errors:
        # BUG: unescaped backslashes caused '\U' unicode escape errors
        # BUG: string was missing proper separators
        path = drive + ":\" + folder + "\" + filename
        return path

    # TODO: Fix the bugs and return the properly escaped Windows path:
    # Format: "<drive>:\\<folder>\\<filename>"
    """
    # TODO: Fix the escaping bug and return the valid path string
    raise NotImplementedError("Level 4: Fix debug_escaped_path().")


if __name__ == "__main__":
    print("Module 02 Exercises loaded successfully.")
    print("To test your solutions, implement the functions above or run solutions.py.")
