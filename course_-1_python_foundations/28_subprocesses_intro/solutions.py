"""
Module 28 Solutions: Subprocesses and Shell Execution
=====================================================

Reference implementations for all 4 exercise levels.
"""

import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Level 1: Recall Solution
# ============================================================================

def run_echo_command(text: str) -> str:
    """Executes child process and returns stripped stdout string."""
    cmd = [sys.executable, "-c", "import sys; print(sys.argv[1])", text]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


# ============================================================================
# Level 2: Modify Solution
# ============================================================================

def run_command_with_timeout(cmd_args: List[str], timeout_sec: float) -> Tuple[bool, str]:
    """Executes a command enforcing a strict timeout deadline."""
    try:
        proc = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        return True, proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, f"Timed out after {timeout_sec}s"


# ============================================================================
# Level 3: Build Solution
# ============================================================================

def pipe_text_to_process(input_data: str, py_script: str) -> Tuple[int, str, str]:
    """Feeds text to a child process's stdin and captures returncode, stdout, and stderr."""
    cmd = [sys.executable, "-c", py_script]
    proc = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


# ============================================================================
# Level 4: Debug Solution
# ============================================================================

def safe_execute_calculator(expr: str) -> str:
    """
    Safely evaluates an arithmetic expression inside a child process without shell=True,
    with decoded text mode and error capture.
    """
    code = f"import sys; print({expr})"
    cmd = [sys.executable, "-c", code]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=False
    )

    if proc.returncode == 0:
        return proc.stdout.strip()
    else:
        # Return cleanly formatted error message from stderr
        first_err_line = proc.stderr.strip().splitlines()[-1] if proc.stderr else "Unknown error"
        return f"Error: {first_err_line}"


# ============================================================================
# Verification Tests
# ============================================================================

def run_tests() -> None:
    print("Running Module 28 Verification Tests...")

    # Level 1 test
    echoed = run_echo_command("Verification Agent Active")
    assert echoed == "Verification Agent Active", f"Level 1 failed: '{echoed}'"
    print("  [✓] Level 1 (Recall: run and capture) passed.")

    # Level 2 test: success case
    ok_cmd = [sys.executable, "-c", "print('done')"]
    success, out = run_command_with_timeout(ok_cmd, 2.0)
    assert success is True and out == "done"

    # Level 2 test: timeout case
    slow_cmd = [sys.executable, "-c", "import time; time.sleep(2)"]
    timed_out, msg = run_command_with_timeout(slow_cmd, 0.1)
    assert timed_out is False
    assert "Timed out after 0.1s" in msg
    print("  [✓] Level 2 (Modify: timeout enforcement) passed.")

    # Level 3 test
    script = "import sys; lines = sys.stdin.readlines(); print(f'{len(lines)} lines')"
    ret, stdout_res, stderr_res = pipe_text_to_process("alpha\nbeta\ngamma\n", script)
    assert ret == 0
    assert stdout_res == "3 lines"
    assert stderr_res == ""
    print("  [✓] Level 3 (Build: stdin piping) passed.")

    # Level 4 test: valid math
    calc_ok = safe_execute_calculator("15 * 4 + 2")
    assert calc_ok == "62", f"Expected '62', got '{calc_ok}'"

    # Level 4 test: error handling (division by zero)
    calc_err = safe_execute_calculator("10 / 0")
    assert calc_err.startswith("Error: ZeroDivisionError")
    print("  [✓] Level 4 (Debug: safe calculator) passed.")

    print("All Module 28 exercise solutions verified successfully!\n")


def main() -> None:
    run_tests()


if __name__ == "__main__":
    main()
