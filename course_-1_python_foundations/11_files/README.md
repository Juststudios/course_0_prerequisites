# File Handling and Persistent I/O in Python

## What You Will Learn
In this module, you will master file input/output (I/O) and persistent storage in Python:
- How the operating system manages files through streams and file descriptors.
- The fundamental modes of `open()`: reading (`"r"`), writing (`"w"`), appending (`"a"`), exclusive creation (`"x"`), and binary variants (`"rb"`, `"wb"`).
- Why specifying `encoding="utf-8"` is mandatory for robust cross-platform software.
- How Python's context manager protocol (`with open(...) as f:`) guarantees deterministic resource cleanup.
- Strategies for reading data: entire file reading (`.read()`), line-by-line streaming (`for line in f:`), and indexed batching.
- How to write, append, and flush data streams using `.write()`, `.writelines()`, and `.flush()`.
- Navigating file streams using `.seek()` and `.tell()`.
- Modern, object-oriented filesystem manipulation using Python's standard `pathlib.Path`.
- How to implement atomic writes to prevent data corruption during unexpected system crashes.
- How autonomous AI agents use file systems to store long-term conversational memory, load dynamic prompt templates, persist tool execution artifacts, and rotate audit logs.

## Prerequisites
Before beginning this module, you should be comfortable with:
- Module 03: Variables, strings, and string manipulation.
- Module 07: Control flow (`if/elif/else`, `for` loops, `while` loops).
- Module 08: Defining functions and parameters.
- Module 10: Handling exceptions (`try/except/finally`, `FileNotFoundError`, `PermissionError`).

## The Problem
Every variable you store in Python—whether an integer, dictionary, or agent state—lives inside volatile random-access memory (RAM). When your program terminates, or if the server reboots or crashes, all data in RAM evaporates instantly.

To build software that delivers lasting utility, data must be committed to non-volatile storage (SSDs, hard drives, or network storage). However, interacting with physical disks introduces serious software engineering challenges:
1. **Resource Exhaustion (Leaked File Descriptors)**: Operating systems restrict the number of open file handles a single process may hold (often 1024 by default). If code opens files without closing them, the process runs out of handles and crashes with `OSError: [Errno 24] Too many open files`.
2. **Accidental Data Destruction**: Opening an existing database or log file with mode `"w"` immediately truncates the file to zero bytes, obliterating all historical data before a single line of code runs.
3. **Encoding Nightmares (Mojibake & Crashes)**: On Windows, Python's default encoding may be `cp1252`, while Linux and macOS use `utf-8`. Reading a UTF-8 file containing emoji or non-English characters on Windows without explicit encoding raises `UnicodeDecodeError`.
4. **Partial Writes & File Corruption**: If an application crashes midway through writing a JSON file, the file is left half-written and corrupt. Subsequent reads fail entirely.

Python's file subsystem and context manager pattern provide the tools to solve all of these problems reliably.

## Key Terminology
- **File Handle (File Object / Stream)**: An in-memory Python object representing an active stream connection to a physical file managed by the OS kernel.
- **File Descriptor (FD)**: A low-level non-negative integer assigned by the operating system kernel to identify an open file stream in the process table.
- **Context Manager (`with` statement)**: A Python language construct that guarantees entry (`__enter__`) and exit (`__exit__`) actions, ensuring resources like files are closed even if exceptions occur.
- **Stream Position (Cursor / Offset)**: The zero-based byte or character index indicating where the next read or write operation will take place.
- **Buffer & Flushing**: An intermediate memory cache used by Python and the OS to batch I/O operations for performance. Flushing pushes buffered data from RAM directly to physical disk.
- **Atomic Write**: A file update technique that writes to a temporary file first and renames it over the destination in a single atomic filesystem operation (`os.replace`), preventing corrupted half-written files.
- **`pathlib.Path`**: Python's modern object-oriented API representing filesystem paths with cross-platform slash (`/`) operators, replacing legacy `os.path` string parsing.
- **Encoding**: The mapping rule converting characters into bytes (e.g., UTF-8, ASCII).

## Intuition
Think of working with a file like visiting a high-security document archive:
- **`open()`** is checking out a physical binder from the librarian. The librarian records that you have binder #14 (the file descriptor).
- **The Mode (`"r"`, `"w"`, `"a"`)** is the badge you wear:
  - `"r"` (Read badge): You can look at the pages, but your pen is confiscated.
  - `"w"` (Write badge): The librarian hands you the binder, but first feeds all existing pages into a paper shredder!
  - `"a"` (Append badge): You can only flip to the very last page and write new notes at the bottom.
- **`encoding="utf-8"`** is agreeing on the alphabet and language before opening the book, ensuring characters aren't misinterpreted as gibberish.
- **`with open(...) as f:`** is an automatic vault door with an alarm clock. No matter what happens inside—even if you faint (`raise Exception`)—the vault door closes and returns the binder to the shelf automatically.
- **`f.close()`** is walking back to the counter manually. If you forget or get distracted, the binder stays checked out forever until the library closes.

## Concept

### 1. Opening Modes Breakdown
The `open(file, mode="r", encoding=None)` built-in function supports several standard mode strings:

| Mode | Operation | If File Exists | If File Missing | Pointer Start |
|------|-----------|----------------|-----------------|---------------|
| `"r"` | Read text | Opens file | Raises `FileNotFoundError` | Beginning (0) |
| `"w"` | Write text | **Truncates to 0 bytes** | Creates new file | Beginning (0) |
| `"a"` | Append text | Preserves data | Creates new file | End of file |
| `"x"` | Exclusive create | Raises `FileExistsError` | Creates new file | Beginning (0) |
| `"r+"` | Read and Write | Preserves data | Raises `FileNotFoundError` | Beginning (0) |
| `"rb"` | Read binary | Preserves data | Raises `FileNotFoundError` | Beginning (0) |
| `"wb"` | Write binary | Truncates to 0 bytes | Creates new file | Beginning (0) |

Always include `b` when working with images, audio, PDFs, pickled models, or raw bytes to prevent Python from attempting Unicode text decoding.

### 2. Reading Strategies: Memory Efficiency
Beginners often use `content = f.read()` or `lines = f.readlines()`. While fine for small files, both load the **entire file into RAM simultaneously**. If an AI agent attempts to read a 12GB dataset or web scrape dump with `f.read()`, the machine runs out of memory (OOM) and the operating system terminates the process.

**Memory-Safe Streaming**:
```python
# Iterating directly over the file object streams line-by-line:
with open("large_dataset.log", "r", encoding="utf-8") as f:
    for line in f:
        process_line(line)  # Uses minimal RAM (one line buffer at a time)
```

### 3. Modern Filesystem Manipulation with `pathlib`
Python 3.4 introduced `pathlib`, providing object-oriented path handling that eliminates awkward string concatenations:
```python
from pathlib import Path

base_dir = Path("/home/user/agent_workspace")
log_file = base_dir / "logs" / "agent.jsonl"  # Clean division operator

log_file.parent.mkdir(parents=True, exist_ok=True)  # Creates missing directories
log_file.write_text("initial log entry", encoding="utf-8")  # Quick one-liner
```

## Syntax

```python
from pathlib import Path

# 1. Standard Safe Read with Context Manager
with open("config.json", "r", encoding="utf-8") as f:
    config_text = f.read()

# 2. Line-by-Line Streaming
with open("telemetry.csv", "r", encoding="utf-8") as f:
    for line in f:
        row = line.strip().split(",")

# 3. Safe Appending
with open("audit.log", "a", encoding="utf-8") as f:
    f.write(f"Agent action executed at {timestamp}\n")

# 4. Stream Navigation (Seeking)
with open("binary.dat", "rb") as f:
    header = f.read(16)        # Read first 16 bytes
    f.seek(0)                  # Rewind pointer back to beginning
    full_data = f.read()

# 5. Atomic File Writing Pattern
import os
import tempfile

def atomic_save(filepath: Path, content: str) -> None:
    # Write to a temporary file in the same directory first
    temp_file = filepath.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())  # Force OS to write to physical media
    # Atomically replace destination (instantaneous on POSIX/NTFS)
    os.replace(temp_file, filepath)
```

## Example

```python
"""
Real-world AI Agent Persistent Conversation Memory & Audit Logger.
Demonstrates structured file operations, JSONL streaming, and atomic state saves.
"""
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict, Generator, List, Optional


class AgentMemoryManager:
    """
    Manages persistent conversational state and append-only audit trails
    for an autonomous AI agent using robust file operations.
    """
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.storage_dir / "conversation_history.jsonl"
        self.state_file = self.storage_dir / "agent_checkpoint.json"

    def append_message(self, role: str, content: str, tokens: int) -> None:
        """Appends a new turn to the conversation history using JSON Lines format."""
        entry = {
            "role": role,
            "content": content,
            "tokens": tokens
        }
        # Mode "a" ensures append-only without truncating prior history
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
            f.flush()  # Ensure data is pushed from Python buffer to OS buffer

    def stream_messages(self) -> Generator[Dict[str, Any], None, None]:
        """Memory-efficient generator yielding one conversation turn at a time."""
        if not self.history_file.exists():
            return

        with open(self.history_file, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    yield json.loads(clean_line)
                except json.JSONDecodeError as err:
                    print(f"Warning: Corrupted record at line {line_no}: {err}")

    def save_checkpoint_atomic(self, state: Dict[str, Any]) -> None:
        """Atomically saves the agent's full working memory checkpoint."""
        temp_target = self.storage_dir / "checkpoint.tmp"
        
        # Phase 1: Write to temporary file
        with open(temp_target, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
            f.flush()
            os.fsync(f.fileno())  # Flush to disk hardware

        # Phase 2: Atomic rename over final target
        os.replace(temp_target, self.state_file)

    def load_checkpoint(self) -> Dict[str, Any]:
        """Loads the last valid checkpoint, returning empty state if missing."""
        if not self.state_file.exists():
            return {}
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)


# Demonstration
with tempfile.TemporaryDirectory() as tmp_dir:
    manager = AgentMemoryManager(Path(tmp_dir))

    # 1. Append message turns
    manager.append_message("system", "You are an autonomous engineering assistant.", 12)
    manager.append_message("user", "Summarize the findings in the security report.", 10)
    manager.append_message("assistant", "The security report highlights 3 high-severity CVEs.", 14)

    # 2. Stream messages line by line
    print("--- Streamed Conversation Turns ---")
    total_tokens = 0
    for turn in manager.stream_messages():
        print(f"  [{turn['role'].upper()}]: {turn['content']} ({turn['tokens']} tokens)")
        total_tokens += turn["tokens"]
    print(f"Total session tokens consumed: {total_tokens}\n")

    # 3. Save atomic checkpoint
    checkpoint_payload = {
        "agent_name": "Auditor-01",
        "current_step": 3,
        "active_goal": "Security audit",
        "total_tokens": total_tokens
    }
    manager.save_checkpoint_atomic(checkpoint_payload)

    # 4. Reload and verify
    recovered_state = manager.load_checkpoint()
    print("--- Recovered Checkpoint ---")
    print(f"  Agent Name:  {recovered_state.get('agent_name')}")
    print(f"  Active Goal: {recovered_state.get('active_goal')}")
    print(f"  Tokens:      {recovered_state.get('total_tokens')}")
```

## Line-by-Line Explanation
1. `class AgentMemoryManager:`: Defines an abstraction layer encapsulating file operations.
2. `self.storage_dir.mkdir(parents=True, exist_ok=True)`: Creates the target directory and any intermediate folders if they do not exist, without raising errors if they do.
3. `self.history_file = self.storage_dir / "conversation_history.jsonl"`: Uses `pathlib.Path` slash syntax to form a clean, cross-platform file path.
4. `with open(self.history_file, "a", encoding="utf-8") as f:`: Opens the file in append mode (`"a"`). If the file exists, the write pointer moves to EOF; if not, the file is created. Explicit `utf-8` prevents encoding corruption.
5. `f.write(json.dumps(entry) + "\n")`: Serializes the dictionary to a single JSON line followed by a newline delimiter.
6. `f.flush()`: Explicitly commands Python's internal runtime buffer to flush accumulated bytes to the operating system buffer.
7. `for line_no, line in enumerate(f, start=1):`: Reads from disk lazily. Only one line is pulled into memory at any instant, guaranteeing low RAM overhead regardless of log size.
8. `yield json.loads(clean_line)`: Turns `stream_messages` into a memory-efficient generator.
9. `os.fsync(f.fileno())`: Bypasses OS kernel buffers and forces the storage controller to commit bytes directly to physical non-volatile media.
10. `os.replace(temp_target, self.state_file)`: Atomic filesystem rename. At no instant will an external process see an empty or corrupted checkpoint file.

## What Python Is Doing
When you interact with files, Python operates as a layer above the operating system kernel:
1. **The System Call Pipeline**: Calling `open("file.txt", "w")` invokes the OS kernel system call (`open()` in POSIX, `CreateFileW()` on Windows). The OS allocates a file descriptor (an integer like `3` or `5`) in the process table.
2. **CPython's I/O Hierarchy**:
   - `open()` returns a wrapper object from the `io` standard library module:
     - Text mode returns a `_io.TextIOWrapper` (handling character encoding/decoding and newline translation `\r\n` <-> `\n`).
     - Binary mode returns a `_io.BufferedReader` or `_io.BufferedWriter` (handling raw byte streams).
     - At the lowest level sits `_io.FileIO`, which interacts directly with OS file descriptors.
3. **The Context Manager Protocol**:
   - The `with open(...) as f:` statement calls `f.__enter__()`, binding `f` to the stream.
   - When the block exits (normally or via an unhandled exception), Python invokes `f.__exit__(exc_type, exc_val, exc_tb)`.
   - `__exit__` immediately calls `f.close()`, which calls the POSIX `close(fd)` system call. This releases the OS file descriptor back to the kernel pool even if an unhandled error occurred!

## Common Mistakes

### 1. Opening with `"w"` When Intending to Append
- **Bad**: `with open("agent_events.log", "w") as f: f.write(event)`
- **Why**: Mode `"w"` immediately clears all prior file content to 0 bytes!
- **Fix**: Use `"a"` to append to the end of existing logs.

### 2. Omitting `encoding="utf-8"`
- **Bad**: `with open("prompt.txt", "r") as f:`
- **Why**: Python falls back to `locale.getpreferredencoding()`. On Windows, this defaults to `cp1252`. When a user submits an emoji like 🤖 or a non-English string like `"你好"`, Python crashes with `UnicodeDecodeError`.
- **Fix**: Always specify `encoding="utf-8"`.

### 3. Manual `open()` and `close()` Without `with`
- **Bad**:
  ```python
  f = open("data.csv", "r")
  data = parse(f.read())  # If parse() raises ValueError, f.close() never runs!
  f.close()
  ```
- **Why**: Any exception raised between `open` and `close` permanently leaks the open file handle. In server applications or loops, this causes `OSError: Too many open files`.
- **Fix**: Always wrap files in a `with` statement.

### 4. Reading Huge Files with `.readlines()` or `.read()`
- **Bad**: `lines = f.readlines()` on a 5GB file loads 5GB into RAM, crashing the Python interpreter.
- **Fix**: Iterate directly over the file handle: `for line in f:`.

## Real-World Uses
- **JSON Lines (JSONL) Data Logging**: High-throughput loggers append JSON-serialized records line by line, allowing easy parsing with standard Unix tools (`grep`, `jq`, `wc`).
- **Configuration Loading**: Reading YAML/JSON/TOML application configs on startup and validating system settings.
- **Data Science Pipelines**: Streaming gigabyte-scale CSVs or Parquet datasets in chunks without exhausting RAM.
- **Safe File Replacement**: Upgrading configuration files or database snapshots using atomic rename strategies.

## Connection to AI Agents
File handling is the primary mechanism AI agents use for non-volatile persistence:
1. **Session & History Persistence**: Autonomous agents save dialogue history to `.jsonl` files on disk. When an agent restarts or crashes, it reconstructs its context window by streaming past turns.
2. **Dynamic Prompt & Schema Loading**: Production agents keep system prompts and JSON schema specifications in external Markdown and JSON files. This allows prompt engineers to update agent behavior without modifying Python source code.
3. **Tool Execution Artifacts**: When tools generate charts, CSV summaries, or download PDFs, they write them to a sandboxed artifact directory and return file URIs to the user.
4. **Log Rotation**: Agents log thought processes and LLM raw completions to rotating log files, preventing disk exhaustion while preserving telemetry for debugging.

## Practice
1. Write a function `count_lines_and_words(filepath: Path) -> Tuple[int, int]` that streams a text file line-by-line and returns the total line count and word count without calling `.read()` or `.readlines()`.
2. Write a script that opens a file in exclusive creation mode (`"x"`) and catches `FileExistsError` to prevent overwriting an existing configuration file.
3. Use `pathlib.Path` to find and print all `.py` files inside a directory and its subdirectories using `.glob("**/*.py")`.

## Challenge
Implement a thread-safe, atomic log rotator `RotatingFileLogger(base_path: Path, max_bytes: int = 1024, max_backups: int = 3)`:
- Allows writing message strings.
- Before each write, inspects current file size. If writing the new message exceeds `max_bytes`, triggers log rotation:
  - Rotates `log.2` -> `log.3` (dropping oldest if exceeding `max_backups`), `log.1` -> `log.2`, `log` -> `log.1`.
  - Creates a fresh empty `log` file.
- Appends the new message with a timestamp.
- Ensure all file operations handle edge cases (missing intermediate backup files, clean stream closures).

## Summary
- Files bridge volatile RAM to persistent disk storage.
- Modes govern read/write permissions and starting pointer position (`"r"`, `"w"`, `"a"`, `"x"`).
- Always supply `encoding="utf-8"` to prevent platform-dependent encoding crashes.
- The `with open(...)` context manager guarantees file closure regardless of exceptions.
- Stream large files line by line (`for line in f:`) rather than loading everything with `.read()`.
- Use `pathlib.Path` for modern, cross-platform path manipulation.
- Atomic file writes (`os.replace`) prevent corrupted half-written files during system crashes.

## What You Should Know Before Moving On
Before advancing to Module 12 (Modules and Packages), ensure you can:
- Correctly choose between `"r"`, `"w"`, `"a"`, and binary modes.
- Confidently use `with open(..., encoding="utf-8")` in all file operations.
- Process large files with low memory consumption using line generators.
- Use `pathlib.Path` methods (`exists()`, `mkdir()`, `/`, `glob()`) to navigate filesystems.
- Explain what happens to file descriptors when context managers exit.
