# Topic: Subprocesses and Shell Execution in Python

## What You Will Learn
In this module, you will learn:
- What a subprocess is and how operating systems spawn and manage child processes.
- Why legacy execution utilities like `os.system()` are obsolete and dangerous.
- How to launch external programs and CLI tools using Python's modern `subprocess.run()` function.
- How to capture standard output (`stdout`) and standard error (`stderr`) as decoded text.
- How to inspect process return codes and automatically raise exceptions on failure using `check=True` and `CalledProcessError`.
- How to prevent runaway or frozen processes using `timeout` and `TimeoutExpired`.
- The critical distinction between `shell=False` (safe list-based execution) and `shell=True` (shell injection danger).
- How to feed input into subprocesses via `stdin`.
- When and how to use `subprocess.Popen` for advanced streaming or non-blocking process supervision.
- How autonomous AI coding agents execute bash commands, run test suites (`pytest`), invoke linters, and inspect git repositories safely.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 05: Strings, encoding, and decoding.
- Module 08: Functions and keyword arguments.
- Module 10: Errors and Exception Handling (`try`, `except`, `TimeoutError`).
- Module 27: Environment Variables (process environment inheritance).

## The Problem
Python is a powerful language, but it cannot do everything inside the Python interpreter:
- What if your program needs to check the status of a Git repository (`git status`)?
- What if you need to transcode a video using `ffmpeg`?
- What if an autonomous AI coding agent needs to run a test suite (`pytest tests/`), compile a C/Rust module (`cargo build`), or format code with `ruff`?

Early Python programmers often used `os.system("ls -la")`. But `os.system()` has fatal limitations:
1. **Cannot Capture Output**: It dumps text directly to the console; your Python code cannot capture or inspect the output string!
2. **Poor Error Handling**: It returns an opaque OS bitmask rather than standard exceptions.
3. **Severe Security Vulnerabilities**: Passing user inputs to a shell opens your system to **Shell Injection Attacks**, allowing malicious users to execute arbitrary commands like `rm -rf /` or steal sensitive files.

Python's `subprocess` module solves these challenges with safe, robust, cross-platform process orchestration.

## Key Terminology
- **Process**: An independent executing instance of a program with its own dedicated memory space, resources, and Process ID (PID).
- **Subprocess (Child Process)**: A process spawned and managed by another process (the parent process, such as your Python script).
- **Exit Code / Return Code**: An integer returned by a process when it finishes. By convention, `0` indicates success; any non-zero value indicates an error.
- **Standard Streams**:
  - **`stdin` (Standard Input, fd 0)**: The stream where a process reads incoming input data.
  - **`stdout` (Standard Output, fd 1)**: The stream where a process writes normal output text.
  - **`stderr` (Standard Error, fd 2)**: The stream where a process writes diagnostics and error messages.
- **`subprocess.run()`**: The recommended, high-level synchronous API for executing a command and waiting for it to complete.
- **`CompletedProcess`**: The object returned by `subprocess.run()` containing `args`, `returncode`, `stdout`, and `stderr`.
- **`subprocess.Popen`**: The low-level interface providing fine-grained control over streaming I/O and asynchronous process management.
- **Shell Injection**: A critical security exploit where unvalidated inputs allow an attacker to inject and execute arbitrary shell commands.

## Intuition
Think of a general contractor managing a construction site:
- The contractor (the Python parent script) oversees the master blueprint.
- When electrical work is required, the contractor does not attempt to wire the building directly. Instead, the contractor hires an independent licensed electrician (spawns a subprocess).
- The contractor gives the electrician exact work specifications (`stdin` or arguments).
- The electrician performs the job independently in their own workspace.
- When finished, the electrician reports back with the completed report (`stdout`), any defect logs (`stderr`), and a sign-off status code (`returncode 0`).
- If the electrician gets stuck or takes longer than the agreed contract deadline (`timeout`), the contractor intervenes and cancels the job.

## Concept
### 1. The Anatomy of `subprocess.run()`
The standard way to execute a command in modern Python:
```python
import subprocess

result = subprocess.run(
    ["echo", "Hello, World!"],  # Command and arguments as a list
    capture_output=True,         # Capture stdout and stderr
    text=True,                   # Decode output bytes to str using UTF-8
    check=True,                  # Raise CalledProcessError if returncode != 0
    timeout=5                    # Raise TimeoutExpired if execution exceeds 5s
)
```

### 2. Why `shell=False` is Mandatory for Safety
- **With `shell=False` (Default and Recommended)**:
  Python passes the argument list directly to the operating system's process launcher (`execve` on POSIX). The OS treats every list element as an isolated string literal. Even if a user supplies `"; rm -rf /"`, it is treated merely as a harmless file name argument!
- **With `shell=True` (Dangerous)**:
  Python spawns an intermediate system shell (`/bin/sh -c "..."`). The shell interprets meta-characters like `;`, `&`, `|`, `>`, and backticks. If untrusted user input is concatenated into the command string, attackers gain full arbitrary command execution on your host.

### 3. Piping and Standard Streams
Subprocesses communicate via pipes (in-memory OS byte buffers). Python can pipe data into a child process's `stdin` and capture its `stdout` and `stderr` streams independently.

## Syntax
### Basic Command Execution
```python
import subprocess

# 1. Simple command without output capture
subprocess.run(["python3", "--version"])

# 2. Capturing output as decoded text
res = subprocess.run(["git", "--version"], capture_output=True, text=True)
print(f"Git Version: {res.stdout.strip()} (Exit Code: {res.returncode})")

# 3. Passing input into stdin
res = subprocess.run(
    ["grep", "python"],
    input="java\npython\nrust\n",
    capture_output=True,
    text=True
)
print(f"Matched: {res.stdout.strip()}")
```

### Error and Timeout Handling
```python
import subprocess

# Raising CalledProcessError on failure
try:
    subprocess.run(["ls", "/non_existent_path_9988"], check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as err:
    print(f"Command failed with exit code {err.returncode}")
    print(f"Error output: {err.stderr.strip()}")

# Enforcing execution deadlines
try:
    subprocess.run(["sleep", "10"], timeout=1)
except subprocess.TimeoutExpired as err:
    print(f"Subprocess timed out after {err.timeout} seconds!")
```

## Example
Here is a complete, executable Python example demonstrating command execution, status checking, output parsing, and safe tool running:

```python
import subprocess
import sys
from typing import Dict, Any

def execute_cli_tool(args: list[str], timeout_sec: int = 5) -> Dict[str, Any]:
    """
    Executes an external command safely, capturing outputs, status, and errors.
    """
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False  # Inspect returncode manually
        )
        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout_sec}s",
            "timed_out": True,
        }

if __name__ == "__main__":
    # Test 1: Successful Python version query
    result = execute_cli_tool([sys.executable, "--version"])
    print(f"Version Check: success={result['success']}, output='{result['stdout']}'")

    # Test 2: Child script execution with calculation
    code = "import sys; print(sum(int(x) for x in sys.argv[1:]))"
    calc_res = execute_cli_tool([sys.executable, "-c", code, "10", "20", "30"])
    print(f"Calculation Result: {calc_res['stdout']}")
```

## Line-by-Line Explanation
1. `subprocess.run(args, ...)`: Invokes the command specified by `args` (a list of strings) synchronously.
2. `capture_output=True`: Tells Python to open pipes for `stdout` and `stderr` instead of printing directly to the terminal.
3. `text=True`: Automatically decodes the raw output bytes into standard Python strings using UTF-8.
4. `timeout=timeout_sec`: Guards against frozen commands by raising `TimeoutExpired` if the child does not terminate within the deadline.
5. `proc.returncode == 0`: Checks whether the process completed successfully according to standard POSIX conventions.
6. `sys.executable`: References the path of the exact Python interpreter currently running, ensuring child scripts execute with the same virtual environment.

## What Python Is Doing
Under the hood:
1. When `subprocess.run()` is called on Linux/POSIX systems:
   - Python invokes the low-level `fork()` (or `clone()`) system call, creating a duplicate child process.
   - In the child process, Python configures file descriptors: it binds `stdin` (fd 0), `stdout` (fd 1), and `stderr` (fd 2) to pipe endpoints created in the parent.
   - The child process calls `execve()`, which replaces its memory image with the specified executable binary.
2. In the parent process:
   - Python reads data from the pipes as the child emits output.
   - If a `timeout` is specified, Python uses `poll()` or `select()` on the file descriptors with a timer. If the timer expires before the child exits, Python sends `SIGKILL` to terminate the runaway process.
   - Python calls `waitpid()` to harvest the child's termination status, preventing "zombie processes" from lingering in the OS process table.
   - It packages the exit code and collected output buffers into a `CompletedProcess` object.

## Common Mistakes
1. **Passing a Single String Without `shell=True`**:
   `subprocess.run("ls -la")` produces `FileNotFoundError: [Errno 2] No such file or directory: 'ls -la'`. Python looks for an executable literally named `"ls -la"`. Pass a list: `subprocess.run(["ls", "-la"])`.
2. **Enabling `shell=True` with Untrusted Inputs**:
   Writing `subprocess.run(f"cat {user_file}", shell=True)` allows users to submit `"file.txt; rm -rf /"`. Never use `shell=True` when inputs come from users or remote LLMs!
3. **Forgetting `text=True`**:
   Without `text=True`, `proc.stdout` is a raw `bytes` object (e.g. `b'hello\n'`). String methods like `.strip()` or `in` searches will fail or behave unexpectedly.
4. **Hanging Indefinitely on Interactive Commands**:
   Running a command that prompts for interactive user confirmation (e.g. `rm -i` or `apt-get install` without `-y`) will hang forever if no `timeout` or `stdin` is supplied.
5. **Deadlocking `Popen` with Raw Pipes**:
   When using `subprocess.Popen`, reading directly from `proc.stdout.read()` before the process exits can deadlock if the OS pipe buffer fills up. Always use `proc.communicate()`.

## Real-World Uses
- **Autonomous AI Coding Agents**: Agents inspecting source repositories (`git diff`, `git log`), executing test suites (`pytest`), and linting code (`ruff`, `mypy`).
- **Build Systems and CI/CD Runners**: Jenkins, GitHub Actions, and custom build scripts driving compilers (`gcc`, `cargo`, `tsc`).
- **Data Engineering Pipelines**: Invoking CLI utilities for data compression (`gzip`, `tar`), audio/video processing (`ffmpeg`), or database backups (`pg_dump`).
- **System Administration**: Managing system services, checking disk space (`df -h`), and querying hardware telemetry.

## Connection to AI Agents
Modern AI coding agents (such as AutoGPT, SWE-bench solvers, and Anthropic Claude Computer Use) operate primarily through subprocess execution:
- **The `run_command` Tool**: The primary tool of any software engineering agent is a subprocess wrapper that runs bash commands on the user's behalf.
- **Safety Sandboxing**: Agents use subprocess parameters (such as `cwd`, restricted `env`, and `preexec_fn` resource limits) to sandbox tool executions.
- **Deadlines and Cancellation**: Autonomous agents run tests with strict timeouts (e.g. 30 seconds) to prevent infinite loops in student code or generated scripts.
- **Parsing Structured Tool Outputs**: Agents execute commands like `git status --porcelain` or `pytest --json-report` via subprocess, parse the output, and reason over the results.

## Practice
1. Use `subprocess.run()` to execute `python3 -c "print(40 + 2)"` and capture the output.
2. Check that the return code is 0 and assert that the output stripped equals `"42"`.
3. Try executing an invalid command like `["false"]` with `check=True` inside a `try/except` block and catch `CalledProcessError`.
4. Test timeout behavior by executing `["sleep", "3"]` with `timeout=1`.

## Challenge
Can you build an AI agent Command Execution Engine that executes commands safely, enforces strict execution timeouts, captures stdout/stderr independently, injects custom environment variables, and rejects dangerous shell patterns? (We will build this in `exercises.py`!)

## Summary
- `subprocess.run()` is the standard modern API for executing external programs in Python.
- Always pass arguments as a list of strings (`["cmd", "arg1", "arg2"]`) with `shell=False` to prevent shell injection.
- Use `capture_output=True` and `text=True` to capture clean string outputs.
- Use `timeout` to prevent child processes from hanging indefinitely.
- AI coding agents rely on subprocesses as their primary interface to the host operating system.

## What You Should Know Before Moving On
- How to execute external commands and capture their output using `subprocess.run()`.
- The difference between `stdout`, `stderr`, and `returncode`.
- Why `shell=True` is dangerous and how to avoid shell injection vulnerabilities.
- How to handle `CalledProcessError` and `TimeoutExpired` exceptions.
- How AI agents use subprocesses to run compilers, linters, and test suites.
