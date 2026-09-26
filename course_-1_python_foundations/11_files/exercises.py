"""
Module 11 Exercises: File Handling and Persistent I/O in Python
===============================================================

Complete the exercises below across the four progressive tiers:
  Level 1: Recall  — Basic file reading, line/word counting, and safe appending
  Level 2: Modify  — Dual context managers, log filtering, and chunked streaming
  Level 3: Build   — Designing an atomic conversation store and state persistence manager
  Level 4: Debug   — Diagnosing and repairing premature file truncation and handle leaks

Run your implementations against `solutions.py` to confirm correctness.
"""

from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple


# ==============================================================================
# Level 1: Recall
# ==============================================================================

def count_lines_and_words(filepath: str) -> Tuple[int, int]:
    """
    Open `filepath` using a context manager with UTF-8 encoding.
    Stream the file line-by-line and compute:
      - Total line count (int)
      - Total word count (int, split by whitespace)

    Return (line_count, word_count).
    If the file does not exist, let FileNotFoundError propagate naturally.

    Example:
        For a file containing:
            "Hello world\nWelcome to Python"
        count_lines_and_words(path) -> (2, 5)
    """
    # TODO: Open file with context manager, count lines and words without reading whole file
    raise NotImplementedError("Exercise 1.1: count_lines_and_words not implemented yet.")


def append_agent_event(filepath: str, event_text: str) -> int:
    """
    Append `event_text + "\n"` to the file at `filepath` using mode "a" and UTF-8 encoding.
    Do NOT overwrite or truncate existing content.
    Return the total size of the file in bytes after appending.

    Example:
        size = append_agent_event("events.log", "Action: Search tool called")
    """
    # TODO: Append event text with trailing newline and return new file size
    raise NotImplementedError("Exercise 1.2: append_agent_event not implemented yet.")


# ==============================================================================
# Level 2: Modify
# ==============================================================================

def safe_filter_log_entries(source_path: str, dest_path: str, keyword: str) -> int:
    """
    Modify raw manual file handling to use Python's dual context manager syntax.
    Read `source_path` line by line. If a line contains `keyword` (case-sensitive),
    write that line to `dest_path`.

    Requirements:
      - Use `with open(...) as fin, open(...) as fout:`
      - Specify UTF-8 encoding on both handles.
      - Return the count of matching lines written.

    Example:
        matches = safe_filter_log_entries("system.log", "errors.log", "ERROR")
    """
    # TODO: Implement dual context manager filtering
    raise NotImplementedError("Exercise 2.1: safe_filter_log_entries not implemented yet.")


def chunked_file_reader(filepath: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """
    Implement a memory-safe generator that yields a file in fixed-size character chunks.
    Requirements:
      - Use a context manager with UTF-8 encoding.
      - In a loop, read up to `chunk_size` characters with `f.read(chunk_size)`.
      - If read returns an empty string (EOF), terminate cleanly.
      - Yield each non-empty chunk.

    Example:
        for chunk in chunked_file_reader("huge_data.txt", chunk_size=512):
            process(chunk)
    """
    # TODO: Implement chunked generator reader
    raise NotImplementedError("Exercise 2.2: chunked_file_reader not implemented yet.")


# ==============================================================================
# Level 3: Build
# ==============================================================================

class AgentConversationStore:
    """
    Build a persistent storage manager for an AI agent workspace.
    The store maintains two persistent assets inside `directory`:
      1. `conversation.jsonl` — An append-only JSON Lines file storing message turns.
      2. `state.json` — A JSON file holding the agent's current state checkpoint,
                        saved ATOMICALLY using a temporary file and os.replace.
    """
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.history_path = self.directory / "conversation.jsonl"
        self.state_path = self.directory / "state.json"

    def append_message(self, role: str, message: str) -> None:
        """
        Append a message entry `{"role": role, "message": message}` as a single line
        of JSON followed by `\n` to `self.history_path`.
        Ensure UTF-8 encoding and flush the buffer.
        """
        # TODO: Implement append_message
        raise NotImplementedError("Exercise 3.1: append_message not implemented yet.")

    def get_history(self) -> List[Dict[str, str]]:
        """
        Read `self.history_path` line by line and return a list of message dictionaries.
        If `self.history_path` does not exist, return an empty list `[]`.
        """
        # TODO: Implement get_history
        raise NotImplementedError("Exercise 3.2: get_history not implemented yet.")

    def save_state_atomic(self, state: Dict[str, Any]) -> None:
        """
        Atomically save `state` to `self.state_path`.
        Write to a temporary file (`state.json.tmp`) in `self.directory` first,
        flush and fsync, then replace `self.state_path` using `os.replace`.
        """
        # TODO: Implement save_state_atomic
        raise NotImplementedError("Exercise 3.3: save_state_atomic not implemented yet.")

    def load_state(self) -> Dict[str, Any]:
        """
        Read and return the dictionary from `self.state_path`.
        If `self.state_path` does not exist, return an empty dictionary `{}`.
        """
        # TODO: Implement load_state
        raise NotImplementedError("Exercise 3.4: load_state not implemented yet.")


# ==============================================================================
# Level 4: Debug
# ==============================================================================

def update_config_safely(filepath: str, key: str, value: Any) -> Dict[str, Any]:
    """
    Diagnose and repair the flawed configuration update function below.

    FLAWED IMPLEMENTATION:
    -------------------------------------------------------------------------
    def update_config_safely(filepath, key, value):
        # BUG 1: Opening with "w+" immediately truncates existing file to 0 bytes!
        f = open(filepath, "w+")
        # BUG 2: json.load on empty/truncated file raises JSONDecodeError!
        # BUG 3: Missing encoding="utf-8" causes platform-dependent issues.
        # BUG 4: If JSON decode fails, file descriptor 'f' is never closed (handle leak)!
        data = json.load(f)
        data[key] = value
        f.write(json.dumps(data))
        f.close()
        return data
    -------------------------------------------------------------------------

    Requirements for the fixed version:
      1. If `filepath` exists, open it in read mode ("r") with UTF-8 encoding and parse JSON.
         If the file is empty or missing, start with an empty dictionary `{}`.
      2. Update `data[key] = value`.
      3. Write the updated dictionary back to `filepath` with UTF-8 encoding.
      4. Guarantee all file handles are closed using context managers.
      5. Return the updated dictionary.
    """
    # TODO: Implement the corrected, safe configuration update logic
    raise NotImplementedError("Exercise 4.1: update_config_safely not implemented yet.")
