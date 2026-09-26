"""
Module 28 Exercises: Subprocesses and Shell Execution
=====================================================

Practice running external commands, capturing output streams, handling timeouts,
piping stdin, and securing command execution against shell injection attacks.

Follow the instructions for each level. Replace `raise NotImplementedError`
with your solution.
"""

import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall
# ============================================================================

def run_echo_command(text: str) -> str:
    """
    Recall how to execute a command and capture its standard output as text.

    Requirements:
    1. Run `[sys.executable, "-c", "import sys; print(sys.argv[1])", text]`.
    2. Set `capture_output=True` and `text=True`.
    3. Return the stripped `stdout` string.
    """
    # TODO: Execute command using subprocess.run and return stripped stdout.
    raise NotImplementedError("Level 1: Implement run_echo_command")


# ============================================================================
# Level 2: Modify
# ============================================================================

def run_command_with_timeout(cmd_args: List[str], timeout_sec: float) -> Tuple[bool, str]:
    """
    Modify command execution to enforce a strict timeout deadline.

    Requirements:
    1. Execute `cmd_args` using `subprocess.run()` with the specified `timeout=timeout_sec`.
    2. Set `capture_output=True` and `text=True`.
    3. If the process finishes within the deadline, return `(True, result.stdout.strip())`.
    4. If `subprocess.TimeoutExpired` is raised, return `(False, f"Timed out after {timeout_sec}s")`.
    """
    # TODO: Execute command with timeout and handle TimeoutExpired.
    raise NotImplementedError("Level 2: Implement run_command_with_timeout")


# ============================================================================
# Level 3: Build
# ============================================================================

def pipe_text_to_process(input_data: str, py_script: str) -> Tuple[int, str, str]:
    """
    Build a pipeline that pipes text into a child Python script's stdin.

    Requirements:
    1. Launch a child Python process executing `py_script` with `[sys.executable, "-c", py_script]`.
    2. Pass `input_data` into the process's standard input via the `input` parameter of `subprocess.run()`.
    3. Set `capture_output=True` and `text=True`.
    4. Return a tuple of:
       - returncode (int)
       - stripped stdout (str)
       - stripped stderr (str)
    """
    # TODO: Build stdin piping execution pipeline.
    raise NotImplementedError("Level 3: Implement pipe_text_to_process")


# ============================================================================
# Level 4: Debug
# ============================================================================

def safe_execute_calculator(expr: str) -> str:
    """
    DEBUG CHALLENGE:
    The following function is supposed to evaluate an arithmetic expression
    inside an isolated child Python process and return the computed result string.

    However, the buggy implementation has multiple flaws:
    1. It uses `shell=True` and string concatenation, making it vulnerable to shell injection.
    2. It forgets `text=True`, leaving `proc.stdout` as raw `bytes`.
    3. If the child process raises an error (e.g. division by zero or syntax error),
       it crashes or returns raw unhandled output.

    Fix the implementation:
    - Pass arguments as a list with `shell=False`.
    - Use `capture_output=True` and `text=True`.
    - If `proc.returncode == 0`, return `proc.stdout.strip()`.
    - If `proc.returncode != 0`, return `f"Error: {proc.stderr.strip()}"`.
    """
    # BUGGY CODE:
    # command_str = f"python3 -c 'print({expr})'"
    # proc = subprocess.run(command_str, shell=True, capture_output=True) # BUG: shell=True & bytes!
    # return proc.stdout.strip()  # BUG: bytes has no string strip if not decoded!

    # TODO: Fix shell=False, text=True, and error handling.
    raise NotImplementedError("Level 4: Debug safe_execute_calculator")
