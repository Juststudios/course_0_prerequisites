"""
Module 28: Subprocesses and Shell Execution in Python
=====================================================

This lesson explores how Python programs execute external operating system commands,
scripts, and CLI tools using the `subprocess` standard library module.

In modern software engineering and autonomous AI agent development, subprocesses
are the essential bridge between high-level Python logic and the host environment.
AI coding agents use subprocesses to run test suites, invoke compilers, check Git
repositories, and interact with the filesystem.

Key Topics Covered:
-------------------
1. The modern `subprocess.run()` interface and `CompletedProcess`.
2. Capturing `stdout` and `stderr` as clean UTF-8 text strings.
3. Automatic error handling with `check=True` and `CalledProcessError`.
4. Preventing infinite hangs with timeouts (`subprocess.TimeoutExpired`).
5. Security: Why `shell=False` prevents Shell Injection vulnerabilities.
6. Feeding standard input into a child process (`stdin` / `input`).
7. Real-time streaming and process management with `subprocess.Popen`.
8. AI Agent Application: Sandboxed Command Execution Engine with safety guards.
"""

import os
import shlex
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Section 1: The Modern subprocess.run() Interface
# ============================================================================

def demonstrate_basic_run() -> None:
    """
    Demonstrates executing an external command and inspecting the CompletedProcess object.
    """
    print("=" * 70)
    print("1. BASIC COMMAND EXECUTION (subprocess.run)")
    print("=" * 70)

    # We use sys.executable to run a quick Python snippet as a child process
    cmd = [sys.executable, "-c", "print('Hello from the child subprocess!')"]
    
    # Run synchronously and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(f"Executed Command:  {' '.join(cmd)}")
    print(f"Exit Code:         {result.returncode} (0 means success)")
    print(f"Captured Output:   {result.stdout.strip()}")
    print(f"Returncode == 0?   {result.returncode == 0}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 2: Differentiating stdout and stderr
# ============================================================================

def demonstrate_stdout_vs_stderr() -> None:
    """
    Demonstrates how standard output (stdout) and standard error (stderr)
    are routed to separate stream buffers.
    """
    print("=" * 70)
    print("2. SEPARATING STDOUT AND STDERR")
    print("=" * 70)

    # Script emitting both standard info and error diagnostics
    code = (
        "import sys\n"
        "sys.stdout.write('Normal operation telemetry: OK\\n')\n"
        "sys.stderr.write('Warning diagnostic: memory usage elevated\\n')\n"
    )

    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    )

    print(f"Stdout Stream (Normal Output):")
    print(f"   {proc.stdout.strip()}")
    print(f"Stderr Stream (Diagnostics/Errors):")
    print(f"   {proc.stderr.strip()}")
    print(f"Process Return Code: {proc.returncode}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 3: Automatic Error Raising with check=True
# ============================================================================

def demonstrate_error_handling() -> None:
    """
    Demonstrates how `check=True` raises `subprocess.CalledProcessError`
    when a command exits with a non-zero status code.
    """
    print("=" * 70)
    print("3. ERROR RAISING WITH check=True")
    print("=" * 70)

    # Simulated failing script
    failing_code = "import sys; sys.stderr.write('Fatal: missing config file\\n'); sys.exit(42)"

    try:
        print("Running command that exits with code 42 (check=True)...")
        subprocess.run(
            [sys.executable, "-c", failing_code],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as exc:
        print(f"Caught CalledProcessError successfully!")
        print(f"   Failing Command:     {exc.cmd}")
        print(f"   Exit Code:           {exc.returncode}")
        print(f"   Stderr Captured:     {exc.stderr.strip()}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 4: Deadlines and Timeouts
# ============================================================================

def demonstrate_timeouts() -> None:
    """
    Demonstrates guarding against frozen commands using the timeout parameter.
    """
    print("=" * 70)
    print("4. TIMEOUTS AND EXECUTION DEADLINES")
    print("=" * 70)

    # Command that attempts to sleep for 5 seconds
    sleeping_code = "import time; time.sleep(5)"

    t0 = time.perf_counter()
    try:
        print("Launching long-running command with timeout=0.2s...")
        subprocess.run(
            [sys.executable, "-c", sleeping_code],
            timeout=0.2,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - t0
        print(f"Process interrupted after {elapsed:.2f}s (timeout deadline: {exc.timeout}s)")
        print("Child process was automatically terminated by Python.")
    print("-" * 70 + "\n")


# ============================================================================
# Section 5: Security: shell=False vs shell=True (Shell Injection)
# ============================================================================

def demonstrate_shell_injection_safety() -> None:
    """
    Demonstrates why passing arguments as a list with shell=False prevents
    malicious shell injection attacks.
    """
    print("=" * 70)
    print("5. SECURITY: shell=False PREVENTS SHELL INJECTION")
    print("=" * 70)

    # Suppose an external user or untrusted input provides a filename
    untrusted_input = "notes.txt; echo 'INJECTED_ATTACK_COMMAND'"

    # 1. SAFE APPROACH: Passing a list with shell=False (default)
    # The OS treats the entire string literally as an argument to the command.
    print("Safe execution with shell=False (argument passed as list element):")
    safe_proc = subprocess.run(
        [sys.executable, "-c", "import sys; print(f'Received arg: {sys.argv[1]}')", untrusted_input],
        capture_output=True,
        text=True,
        shell=False
    )
    print(f"   Output: {safe_proc.stdout.strip()}")
    print("   Notice: The semicolon was treated as harmless literal text, NOT a command separator!")
    print("-" * 70 + "\n")


# ============================================================================
# Section 6: Supplying Standard Input (stdin)
# ============================================================================

def demonstrate_stdin_feeding() -> None:
    """
    Demonstrates piping text into the child process's standard input stream.
    """
    print("=" * 70)
    print("6. PASSING INPUT VIA STDIN")
    print("=" * 70)

    # Child script that consumes stdin and counts words
    counter_script = (
        "import sys\n"
        "lines = sys.stdin.readlines()\n"
        "total_words = sum(len(line.split()) for line in lines)\n"
        "print(f'Total lines: {len(lines)}, Total words: {total_words}')\n"
    )

    sample_text = (
        "Autonomous AI agents use subprocesses.\n"
        "Python makes subprocess management safe and reliable.\n"
        "Concurrency and clean interfaces ensure stability.\n"
    )

    proc = subprocess.run(
        [sys.executable, "-c", counter_script],
        input=sample_text,
        capture_output=True,
        text=True
    )

    print("Supplied Text to stdin:")
    print("   [3 lines of agent documentation]")
    print(f"Child Script Output:\n   {proc.stdout.strip()}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 7: Streaming and Fine Control with subprocess.Popen
# ============================================================================

def demonstrate_popen_streaming() -> None:
    """
    Demonstrates using subprocess.Popen for fine-grained process control
    and reading outputs via .communicate().
    """
    print("=" * 70)
    print("7. FINE-GRAINED CONTROL WITH subprocess.Popen")
    print("=" * 70)

    countdown_code = (
        "import sys, time\n"
        "for i in range(3, 0, -1):\n"
        "    print(f'T-minus {i}...', flush=True)\n"
        "    time.sleep(0.02)\n"
        "print('Liftoff!', flush=True)\n"
    )

    process = subprocess.Popen(
        [sys.executable, "-c", countdown_code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print(f"Child process launched with PID: {process.pid}")
    
    # communicate() reads all data until EOF and waits for process completion
    stdout_data, stderr_data = process.communicate()

    print(f"Process complete with exit code: {process.returncode}")
    print("Collected Stream Output:")
    for line in stdout_data.strip().splitlines():
        print(f"   {line}")
    print("-" * 70 + "\n")


# ============================================================================
# Section 8: AI Agent Command Execution Engine
# ============================================================================

class AgentCommandRunner:
    """
    A secure command execution wrapper designed for AI coding agents.
    Enforces argument tokenization, forbidden command blacklists, working directory
    isolation, and execution timeouts.
    """
    FORBIDDEN_BINARIES = {"rm", "shutdown", "reboot", "dd", "mkfs"}

    def __init__(self, default_timeout: float = 5.0, work_dir: Optional[str] = None):
        self.default_timeout = default_timeout
        self.work_dir = work_dir or os.getcwd()

    def run_tool_command(self, command_line: str) -> Dict[str, Any]:
        """
        Safely tokenizes and executes a CLI command string.
        """
        # 1. Safely tokenize command string into an argument list
        try:
            tokens = shlex.split(command_line)
        except ValueError as e:
            return {"success": False, "returncode": -1, "stdout": "", "stderr": f"Syntax error: {e}"}

        if not tokens:
            return {"success": False, "returncode": -1, "stdout": "", "stderr": "Empty command"}

        # 2. Security validation: check against forbidden executable binaries
        binary_name = os.path.basename(tokens[0])
        if binary_name in self.FORBIDDEN_BINARIES:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Security Violation: Command '{binary_name}' is forbidden.",
            }

        # 3. Execute safely without shell=True
        try:
            res = subprocess.run(
                tokens,
                capture_output=True,
                text=True,
                timeout=self.default_timeout,
                cwd=self.work_dir,
                shell=False
            )
            return {
                "success": res.returncode == 0,
                "returncode": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Execution timed out after {self.default_timeout} seconds",
            }
        except FileNotFoundError:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Executable not found: '{tokens[0]}'",
            }


def demonstrate_agent_command_engine() -> None:
    """
    Demonstrates the AI agent command runner in action.
    """
    print("=" * 70)
    print("8. AI AGENT COMMAND EXECUTION ENGINE")
    print("=" * 70)

    runner = AgentCommandRunner(default_timeout=3.0)

    # 1. Valid command execution
    res1 = runner.run_tool_command(f"{sys.executable} -c \"print('Agent verification complete')\"")
    print(f"Safe Command Result: success={res1['success']}, output='{res1['stdout'].strip()}'")

    # 2. Blocked forbidden command
    res2 = runner.run_tool_command("rm -rf /some/directory")
    print(f"Blocked Command Result: success={res2['success']}, error='{res2['stderr']}'")
    print("-" * 70 + "\n")


# ============================================================================
# Main Entry Point
# ============================================================================

def main() -> None:
    print("Starting Module 28: Subprocesses and Shell Execution in Python\n")
    demonstrate_basic_run()
    demonstrate_stdout_vs_stderr()
    demonstrate_error_handling()
    demonstrate_timeouts()
    demonstrate_shell_injection_safety()
    demonstrate_stdin_feeding()
    demonstrate_popen_streaming()
    demonstrate_agent_command_engine()
    print("Module 28 demonstration completed successfully!")


if __name__ == "__main__":
    main()
