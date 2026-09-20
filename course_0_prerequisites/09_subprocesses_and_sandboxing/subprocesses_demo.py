"""subprocesses_demo.py - Demonstrates safe CLI execution, stdout/stderr capture, and timeouts.

Key concepts demonstrated:
1. Safe subprocess invocation using argument lists (shell=False).
2. Capturing and isolating stdout, stderr, and return codes.
3. Timeout handling to prevent runaway processes.
"""

import subprocess
import sys
from typing import Dict, Any


def run_command_safe(args: list[str], timeout: float = 3.0) -> Dict[str, Any]:
    """Executes a command safely without shell interpretation."""
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False  # Crucial security guarantee
        )
        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": e.stdout.decode() if e.stdout else "",
            "stderr": f"Process timed out after {timeout} seconds",
            "timed_out": True,
        }


def main() -> None:
    print("=== Module 09: Subprocesses & Safe Execution Demo ===")

    # 1. Successful execution
    res1 = run_command_safe([sys.executable, "-c", "print('Hello from isolated Python!')"])
    assert res1["success"] is True
    assert res1["exit_code"] == 0
    assert "Hello from isolated Python!" in res1["stdout"]
    print(f"[OK] Normal execution succeeded: stdout={res1['stdout'].strip()!r}")

    # 2. Execution with non-zero exit code and stderr capture
    res2 = run_command_safe([sys.executable, "-c", "import sys; sys.stderr.write('Fatal Error'); sys.exit(42)"])
    assert res2["success"] is False
    assert res2["exit_code"] == 42
    assert "Fatal Error" in res2["stderr"]
    print(f"[OK] Failure captured correctly: exit_code={res2['exit_code']}, stderr={res2['stderr']!r}")

    # 3. Timeout handling
    res3 = run_command_safe([sys.executable, "-c", "import time; time.sleep(10)"], timeout=0.2)
    assert res3["timed_out"] is True
    assert res3["success"] is False
    print(f"[OK] Timeout captured correctly: {res3['stderr']}")

    # 4. Command injection resistance verification
    # An attacker tries to execute a second command using a semicolon
    malicious_arg = "hello; echo 'HACKED'"
    res4 = run_command_safe(["echo", malicious_arg])
    assert res4["success"] is True
    # The semicolon and echo 'HACKED' should be printed literally as a single argument, NOT executed!
    assert "hello; echo 'HACKED'" in res4["stdout"]
    print("[OK] Injection test verified: argument was treated as literal text, not evaluated.")

    print("All tests in subprocesses_demo.py passed successfully!\n")


if __name__ == "__main__":
    main()
