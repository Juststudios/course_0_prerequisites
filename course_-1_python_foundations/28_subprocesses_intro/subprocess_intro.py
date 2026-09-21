"""Module 28: Subprocesses Introduction"""
import subprocess, sys

# Running an external command:
result = subprocess.run(
    [sys.executable, "--version"],   # safe: list form, no shell injection
    capture_output=True,
    text=True,
    timeout=10
)
print(f"stdout: {result.stdout.strip()}")
print(f"return code: {result.returncode}")   # 0 = success

# Running Python code as a subprocess:
code = "print(2 + 2)"
result = subprocess.run(
    [sys.executable, "-c", code],
    capture_output=True, text=True, timeout=5
)
print(f"Computed: {result.stdout.strip()}")

# Security warning: NEVER do subprocess.run(user_input, shell=True)
# This allows command injection attacks.
print("\nSubprocesses lesson complete. See Course 0 Module 09 for sandboxing.")
