"""
Module 11: Files and Persistent I/O — Streams, Context Managers, and Atomic Writes
===================================================================================

Every program executed by an operating system operates inside volatile RAM.
To persist data across program executions, software interacts with storage media
via files. In modern agent architectures, robust file handling is fundamental
for saving conversation history, loading prompt templates, persisting memory
checkpoints, and rotating audit logs.

This comprehensive lesson covers:
  1. The Context Manager Protocol (`with open(...)`) and Resource Cleanup
  2. Major Opening Modes (`"r"`, `"w"`, `"a"`, `"x"`) and Unicode Encoding (`utf-8`)
  3. Reading Strategies: Full Read, Chunked Read, and Memory-Safe Line Iteration
  4. Writing Strategies: `.write()`, `.writelines()`, and Flushing Buffers (`.flush()`)
  5. Navigating Streams: File Pointers, `.seek()`, and `.tell()`
  6. Binary File Operations (`"rb"`, `"wb"`) with Raw Byte Streams
  7. Modern Path Manipulation with `pathlib.Path`
  8. Resilient Atomic File Writes (`os.replace`)
  9. Real-World AI Agent Architecture: Persistent JSONL Message Store & Checkpoint Recovery
"""

import json
import os
from pathlib import Path
import tempfile
import time
from typing import Any, Dict, Generator, List, Optional, Tuple

print("=" * 75)
print("MODULE 11: FILE HANDLING AND PERSISTENT I/O IN PYTHON")
print("=" * 75)


# ==============================================================================
# SECTION 1: The Context Manager Protocol (with open(...))
# ==============================================================================
print("\n--- 1. The Context Manager Protocol and Deterministic Cleanup ---")

# When opening a file, the operating system assigns a low-level file descriptor.
# Using `with open(...) as f:` ensures `f.close()` is called automatically when
# leaving the block, even if an unhandled exception is raised!

with tempfile.TemporaryDirectory() as demo_dir:
    base_path = Path(demo_dir)
    sample_file = base_path / "greeting.txt"

    # Writing using with statement
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("Hello, Autonomous AI World!\nWelcome to persistent storage.")

    # Verifying file status after the with-block
    print(f"  Created file: {sample_file.name}")
    print(f"  Is file closed after with-block? {f.closed}")  # True!

    # Reading file back
    with open(sample_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  Read content:\n{content}")


# ==============================================================================
# SECTION 2: Major Opening Modes ("r", "w", "a", "x") & Encodings
# ==============================================================================
print("\n--- 2. File Opening Modes and UTF-8 Encoding ---")

with tempfile.TemporaryDirectory() as demo_dir:
    mode_file = Path(demo_dir) / "modes_demo.txt"

    # Mode "w" (Write): Creates a new file, or TRUNCATES existing file to 0 bytes
    with open(mode_file, "w", encoding="utf-8") as f:
        f.write("First line of text.\n")
    print(f"  After 'w' mode, file size: {mode_file.stat().st_size} bytes")

    # Mode "a" (Append): Adds content to the end without truncating
    with open(mode_file, "a", encoding="utf-8") as f:
        f.write("Second line appended at the end.\n")
        f.write("Non-ASCII UTF-8 characters: 🤖 Autonomous Agent 🚀\n")
    print(f"  After 'a' mode, file size: {mode_file.stat().st_size} bytes")

    # Mode "x" (Exclusive Creation): Fails if file already exists
    try:
        with open(mode_file, "x", encoding="utf-8") as f:
            f.write("This will fail because file already exists!")
    except FileExistsError:
        print("  [Handled] Caught expected FileExistsError on mode 'x'")

    # Reading back the UTF-8 content
    with open(mode_file, "r", encoding="utf-8") as f:
        print("  Contents with UTF-8 symbols:")
        for line in f:
            print(f"    | {line.rstrip()}")


# ==============================================================================
# SECTION 3: Reading Strategies (Full vs. Line Streaming)
# ==============================================================================
print("\n--- 3. Memory-Safe Reading Strategies ---")

# Beginners often read whole files into memory with .read() or .readlines().
# For large multi-gigabyte logs, streaming line-by-line is essential to prevent OOM.

with tempfile.TemporaryDirectory() as demo_dir:
    large_log = Path(demo_dir) / "server.log"
    with open(large_log, "w", encoding="utf-8") as f:
        for i in range(1, 6):
            f.write(f"2026-09-21 12:0{i}:00 INFO Agent step {i} completed successfully\n")

    # Strategy A: f.read() — Entire content into single string
    with open(large_log, "r", encoding="utf-8") as f:
        full_text = f.read()
    print(f"  Strategy A (.read()): {len(full_text)} characters read at once.")

    # Strategy B: Line-by-line streaming — Constant memory consumption (O(1))
    print("  Strategy B (Direct iterator for line in f):")
    with open(large_log, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            print(f"    Line {idx}: {line.strip()[:45]}...")


# ==============================================================================
# SECTION 4: Writing Strategies and Buffer Flushing
# ==============================================================================
print("\n--- 4. Writing Lists of Lines and Buffer Flushing ---")

with tempfile.TemporaryDirectory() as demo_dir:
    target_path = Path(demo_dir) / "prompts.txt"

    prompts = [
        "System: You are an autonomous coding assistant.\n",
        "User: Explain how context managers close files.\n",
        "Assistant: Context managers use the __exit__ dunder method.\n"
    ]

    # writelines() writes an iterable of strings
    with open(target_path, "w", encoding="utf-8") as f:
        f.writelines(prompts)
        f.flush()  # Manually forces the Python buffer to write out to the OS buffer
        print(f"  Wrote {len(prompts)} prompt blocks with writelines() and flushed.")

    with open(target_path, "r", encoding="utf-8") as f:
        print(f"  Read back:\n{f.read()}")


# ==============================================================================
# SECTION 5: Stream Seeking and Pointer Inspection (seek and tell)
# ==============================================================================
print("\n--- 5. Stream Position Navigation (.seek() and .tell()) ---")

with tempfile.TemporaryDirectory() as demo_dir:
    seek_file = Path(demo_dir) / "seek_test.txt"
    with open(seek_file, "w+", encoding="utf-8") as f:
        f.write("0123456789ABCDEF")
        print(f"  Current stream position after write (.tell()): {f.tell()}")

        # Reposition pointer back to start
        f.seek(0)
        print(f"  Position after f.seek(0): {f.tell()}")
        first_four = f.read(4)
        print(f"  Read first 4 characters: '{first_four}'")
        print(f"  Position now: {f.tell()}")

        # Jump to position 10
        f.seek(10)
        remainder = f.read()
        print(f"  Read from position 10 to EOF: '{remainder}'")


# ==============================================================================
# SECTION 6: Binary Mode ("rb", "wb")
# ==============================================================================
print("\n--- 6. Binary Mode Operations ---")

# Binary mode works with raw bytes objects (b"...") without encoding/decoding.
# Essential for model weights, images, audio, and compressed data.

with tempfile.TemporaryDirectory() as demo_dir:
    bin_file = Path(demo_dir) / "weights.bin"

    raw_bytes = bytes([0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x02, 0x03, 0x04])
    with open(bin_file, "wb") as f:
        f.write(raw_bytes)
    print(f"  Wrote {len(raw_bytes)} raw bytes in binary mode.")

    with open(bin_file, "rb") as f:
        loaded_bytes = f.read()
    print(f"  Read binary data: {loaded_bytes.hex().upper()}")
    print(f"  Matches original? {loaded_bytes == raw_bytes}")


# ==============================================================================
# SECTION 7: Modern Filesystem Operations with pathlib.Path
# ==============================================================================
print("\n--- 7. Modern Path Manipulation with pathlib ---")

with tempfile.TemporaryDirectory() as demo_dir:
    root = Path(demo_dir)
    agent_dir = root / "workspace" / "telemetry"
    agent_dir.mkdir(parents=True, exist_ok=True)  # Recursive directory creation

    file1 = agent_dir / "step_1.log"
    file2 = agent_dir / "step_2.log"
    file1.write_text("Step 1 ok", encoding="utf-8")
    file2.write_text("Step 2 ok", encoding="utf-8")

    print(f"  Created directory: {agent_dir}")
    print(f"  File exists? {file1.exists()}")
    print(f"  Is directory? {agent_dir.is_dir()}")

    # Globbing pattern matching
    print("  Globbing for *.log files:")
    for log_path in sorted(agent_dir.glob("*.log")):
        print(f"    Found: {log_path.name} ({log_path.stat().st_size} bytes)")


# ==============================================================================
# SECTION 8: Resilient Atomic File Writes
# ==============================================================================
print("\n--- 8. Resilient Atomic File Writes ---")

# An atomic write prevents leaving a half-written corrupted file if the program
# or operating system crashes during a write operation.

def write_atomic(dest_path: Path, data: str) -> None:
    """
    Writes data to a temporary file in the target directory and atomically
    renames it over the destination using os.replace.
    """
    temp_path = dest_path.with_suffix(".tmp")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())  # Force OS write cache to physical disk

    # Atomic rename in filesystem metadata table
    os.replace(temp_path, dest_path)

with tempfile.TemporaryDirectory() as demo_dir:
    config_file = Path(demo_dir) / "agent_config.json"
    initial_config = json.dumps({"agent": "SearchBot", "max_steps": 10}, indent=2)
    write_atomic(config_file, initial_config)

    # Overwrite atomically with updated configuration
    updated_config = json.dumps({"agent": "SearchBot", "max_steps": 25, "active": True}, indent=2)
    write_atomic(config_file, updated_config)

    print("  Atomic write successfully executed.")
    print(f"  Resulting file content:\n{config_file.read_text(encoding='utf-8')}")


# ==============================================================================
# SECTION 9: AI Agent Architecture: Persistent JSONL & Checkpoint Store
# ==============================================================================
print("\n--- 9. AI Agent Architecture: Persistent Conversation Store ---")

class PersistentAgentLog:
    """
    Production-grade agent conversation logger utilizing JSON Lines (.jsonl)
    for append-only turn recording and atomic JSON checkpoints.
    """
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.log_file = self.workspace / "turns.jsonl"
        self.state_file = self.workspace / "state.json"

    def record_turn(self, role: str, content: str, tool_name: Optional[str] = None) -> None:
        """Appends a single turn record to the JSON Lines file."""
        record = {
            "timestamp": time.time(),
            "role": role,
            "content": content,
            "tool": tool_name
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()

    def stream_turns(self) -> Generator[Dict[str, Any], None, None]:
        """Iterates lazily through turns without loading the full file into memory."""
        if not self.log_file.exists():
            return
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    yield json.loads(stripped)

    def save_checkpoint(self, checkpoint_data: Dict[str, Any]) -> None:
        """Atomically saves checkpoint state."""
        temp_file = self.workspace / "state.json.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, self.state_file)

    def load_checkpoint(self) -> Dict[str, Any]:
        """Loads the current checkpoint state."""
        if not self.state_file.exists():
            return {}
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

with tempfile.TemporaryDirectory() as demo_dir:
    agent_store = PersistentAgentLog(Path(demo_dir))

    # Record dialogue
    agent_store.record_turn("user", "What is the weather in San Francisco?")
    agent_store.record_turn("assistant", "Calling weather API", tool_name="get_weather")
    agent_store.record_turn("system", "Temperature 65F, Clear skies", tool_name="get_weather")
    agent_store.record_turn("assistant", "The weather in San Francisco is 65F and clear.")

    # Stream turns
    print("  Streaming recorded agent turns:")
    for turn in agent_store.stream_turns():
        tool_str = f" [Tool: {turn['tool']}]" if turn["tool"] else ""
        print(f"    - {turn['role'].upper()}{tool_str}: {turn['content']}")

    # Save and restore checkpoint
    state = {"turn_count": 4, "last_tool": "get_weather", "status": "idle"}
    agent_store.save_checkpoint(state)
    loaded = agent_store.load_checkpoint()
    print(f"  Checkpoint successfully restored: {loaded}")

print("\n" + "=" * 75)
print("MODULE 11 COMPLETE: ALL FILE LESSON DEMONSTRATIONS EXECUTED CLEANLY")
print("=" * 75)
