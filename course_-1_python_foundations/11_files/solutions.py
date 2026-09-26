"""
Module 11 Solutions: File Handling and Persistent I/O in Python
===============================================================

Reference solutions for all progressive exercises in Module 11.
Includes complete self-verification test suite under `if __name__ == "__main__":`.
"""

import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict, Generator, List, Optional, Tuple


# ==============================================================================
# Level 1: Recall Solutions
# ==============================================================================

def count_lines_and_words(filepath: str) -> Tuple[int, int]:
    """Count lines and whitespace-separated words line by line."""
    line_count = 0
    word_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            word_count += len(line.split())
    return line_count, word_count


def append_agent_event(filepath: str, event_text: str) -> int:
    """Safely append an event line and return new file size."""
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(event_text + "\n")
        f.flush()
    return Path(filepath).stat().st_size


# ==============================================================================
# Level 2: Modify Solutions
# ==============================================================================

def safe_filter_log_entries(source_path: str, dest_path: str, keyword: str) -> int:
    """Filter lines containing keyword using dual context managers."""
    matched = 0
    with open(source_path, "r", encoding="utf-8") as fin, open(dest_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if keyword in line:
                fout.write(line)
                matched += 1
    return matched


def chunked_file_reader(filepath: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """Yield file content in fixed-size character chunks."""
    with open(filepath, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


# ==============================================================================
# Level 3: Build Solutions
# ==============================================================================

class AgentConversationStore:
    """Persistent storage manager with JSONL turns and atomic checkpoints."""
    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.history_path = self.directory / "conversation.jsonl"
        self.state_path = self.directory / "state.json"

    def append_message(self, role: str, message: str) -> None:
        """Append a JSON line with role and message."""
        entry = {"role": role, "message": message}
        with open(self.history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
            f.flush()

    def get_history(self) -> List[Dict[str, str]]:
        """Read all messages from conversation.jsonl."""
        if not self.history_path.exists():
            return []
        history = []
        with open(self.history_path, "r", encoding="utf-8") as f:
            for line in f:
                clean = line.strip()
                if clean:
                    history.append(json.loads(clean))
        return history

    def save_state_atomic(self, state: Dict[str, Any]) -> None:
        """Atomically persist state dictionary using temporary file and rename."""
        temp_target = self.directory / "state.json.tmp"
        with open(temp_target, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_target, self.state_path)

    def load_state(self) -> Dict[str, Any]:
        """Load state dictionary from state.json, or empty dict if missing."""
        if not self.state_path.exists():
            return {}
        with open(self.state_path, "r", encoding="utf-8") as f:
            return json.load(f)


# ==============================================================================
# Level 4: Debug Solution
# ==============================================================================

def update_config_safely(filepath: str, key: str, value: Any) -> Dict[str, Any]:
    """Safely update JSON config without premature truncation or leaks."""
    path = Path(filepath)
    data: Dict[str, Any] = {}

    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    data = json.loads(text)
        except (json.JSONDecodeError, OSError):
            data = {}

    data[key] = value

    # Write updated config back atomically / safely
    temp_target = path.with_suffix(".tmp")
    with open(temp_target, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_target, path)

    return data


# ==============================================================================
# Self-Verification Test Suite
# ==============================================================================

def run_all_tests() -> None:
    print("Testing Module 11 Solutions...")

    with tempfile.TemporaryDirectory() as test_dir:
        base = Path(test_dir)

        # Level 1 Tests
        doc_path = base / "sample_doc.txt"
        doc_path.write_text("The quick brown fox\njumps over the lazy dog\nPython persistent storage", encoding="utf-8")
        lines, words = count_lines_and_words(str(doc_path))
        assert lines == 3, f"Expected 3 lines, got {lines}"
        assert words == 12, f"Expected 12 words, got {words}"

        # Level 1 Append Test
        events_path = base / "events.log"
        size1 = append_agent_event(str(events_path), "INIT_SYSTEM")
        assert size1 > 0
        size2 = append_agent_event(str(events_path), "STEP_1_COMPLETE")
        assert size2 > size1
        content = events_path.read_text(encoding="utf-8")
        assert "INIT_SYSTEM\nSTEP_1_COMPLETE\n" == content

        # Level 2 Tests: safe_filter_log_entries
        full_log = base / "server.log"
        error_log = base / "errors_only.log"
        full_log.write_text(
            "INFO: Start\nERROR: Database timeout\nDEBUG: cache miss\nERROR: Connection reset\nINFO: End\n",
            encoding="utf-8"
        )
        match_count = safe_filter_log_entries(str(full_log), str(error_log), "ERROR:")
        assert match_count == 2
        filtered_lines = error_log.read_text(encoding="utf-8").strip().splitlines()
        assert len(filtered_lines) == 2
        assert "ERROR: Database timeout" in filtered_lines[0]
        assert "ERROR: Connection reset" in filtered_lines[1]

        # Level 2 Tests: chunked_file_reader
        chunk_file = base / "chunk_data.txt"
        chunk_file.write_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", encoding="utf-8")
        chunks = list(chunked_file_reader(str(chunk_file), chunk_size=10))
        assert chunks == ["ABCDEFGHIJ", "KLMNOPQRST", "UVWXYZ"]

        # Level 3 Tests: AgentConversationStore
        agent_dir = base / "agent_workspace"
        store = AgentConversationStore(str(agent_dir))
        assert store.get_history() == []
        assert store.load_state() == {}

        store.append_message("user", "Hello agent!")
        store.append_message("assistant", "How can I help you?")
        history = store.get_history()
        assert len(history) == 2
        assert history[0] == {"role": "user", "message": "Hello agent!"}
        assert history[1] == {"role": "assistant", "message": "How can I help you?"}

        # Check atomic state
        initial_state = {"step": 1, "status": "running"}
        store.save_state_atomic(initial_state)
        assert store.load_state() == initial_state

        updated_state = {"step": 2, "status": "finished", "output": "Done"}
        store.save_state_atomic(updated_state)
        assert store.load_state() == updated_state

        # Level 4 Tests: update_config_safely
        config_path = base / "app_config.json"
        # 1. Update on non-existent file creates it
        res1 = update_config_safely(str(config_path), "retries", 3)
        assert res1 == {"retries": 3}
        assert config_path.exists()

        # 2. Subsequent updates preserve existing keys
        res2 = update_config_safely(str(config_path), "model", "claude-3-5-sonnet")
        assert res2 == {"retries": 3, "model": "claude-3-5-sonnet"}

        # 3. Update existing key
        res3 = update_config_safely(str(config_path), "retries", 5)
        assert res3 == {"retries": 5, "model": "claude-3-5-sonnet"}

    print("All Module 11 solutions verified successfully!")


if __name__ == "__main__":
    run_all_tests()
