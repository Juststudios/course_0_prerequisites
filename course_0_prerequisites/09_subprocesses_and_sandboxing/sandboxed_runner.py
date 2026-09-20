"""sandboxed_runner.py - Secure command runner enforcing directory sandboxing and path traversal checks.

Key concepts demonstrated:
1. Path canonicalization with os.path.realpath.
2. Preventing directory traversal attempts (e.g. '../../etc/passwd').
3. Whitelisting allowed executables for agent tool execution.
4. Ephemeral directory sandboxing.
"""

from typing import Dict, Any, List
import os
import subprocess
import tempfile
import sys


class SandboxedToolRunner:
    """Restricts agent tool actions to a designated sandbox directory and whitelist of commands."""

    def __init__(self, sandbox_dir: str, allowed_commands: List[str]) -> None:
        self.sandbox_dir = os.path.realpath(sandbox_dir)
        self.allowed_commands = set(allowed_commands)
        os.makedirs(self.sandbox_dir, exist_ok=True)

    def resolve_safe_path(self, relative_path: str) -> str:
        """Ensures the target path does not escape the sandbox root."""
        full_path = os.path.realpath(os.path.join(self.sandbox_dir, relative_path))
        # Check that full_path starts with sandbox_dir
        if full_path != self.sandbox_dir and not full_path.startswith(self.sandbox_dir + os.sep):
            raise PermissionError(
                f"Path traversal detected! Path '{relative_path}' resolves outside sandbox."
            )
        return full_path

    def write_file(self, relative_path: str, content: str) -> str:
        """Safely writes a file within the sandbox."""
        safe_path = self.resolve_safe_path(relative_path)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written successfully: {relative_path}"

    def read_file(self, relative_path: str) -> str:
        """Safely reads a file within the sandbox."""
        safe_path = self.resolve_safe_path(relative_path)
        if not os.path.exists(safe_path):
            raise FileNotFoundError(f"File '{relative_path}' does not exist in sandbox.")
        with open(safe_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self, cmd_name: str, args: List[str], timeout: float = 3.0) -> Dict[str, Any]:
        """Executes a whitelisted command inside the sandbox directory."""
        if cmd_name not in self.allowed_commands:
            raise PermissionError(f"Command '{cmd_name}' is not in allowed whitelist: {sorted(self.allowed_commands)}")

        try:
            full_cmd = [cmd_name] + args
            proc = subprocess.run(
                full_cmd,
                cwd=self.sandbox_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False
            )
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout}s",
                "exit_code": -1,
            }


def main() -> None:
    print("=== Module 09: Sandboxed Tool Runner Demo ===")

    with tempfile.TemporaryDirectory(prefix="agent_sandbox_test_") as tmp_dir:
        runner = SandboxedToolRunner(
            sandbox_dir=tmp_dir,
            allowed_commands=[sys.executable, "ls", "grep"]
        )

        # 1. Safe file writing and reading
        runner.write_file("script.py", "print('Executed safely in sandbox!')\n")
        content = runner.read_file("script.py")
        assert "Executed safely in sandbox!" in content
        print("[OK] Safe file write/read inside sandbox verified.")

        # 2. Prevent path traversal attack
        try:
            runner.read_file("../../../etc/passwd")
            raise AssertionError("Path traversal should have been blocked!")
        except PermissionError as err:
            print(f"[OK] Path traversal blocked: {err}")

        # 3. Prevent unwhitelisted command execution
        try:
            runner.execute("curl", ["https://evil.com"])
            raise AssertionError("Unwhitelisted command should have been blocked!")
        except PermissionError as err:
            print(f"[OK] Unwhitelisted command blocked: {err}")

        # 4. Safe whitelisted execution inside sandbox
        exec_res = runner.execute(sys.executable, ["script.py"])
        assert exec_res["success"] is True
        assert "Executed safely in sandbox!" in exec_res["stdout"]
        print(f"[OK] Whitelisted execution succeeded: {exec_res['stdout'].strip()}")

    print("All tests in sandboxed_runner.py passed successfully!\n")


if __name__ == "__main__":
    main()
