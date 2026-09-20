"""message_store.py - Persistent relational message store and tool audit logger for AI agents.

Key concepts demonstrated:
1. Multi-table relational schema: sessions, messages, and tool_audit.
2. Chronological sliding window history retrieval with LIMIT.
3. Structured JSON storage for tool call arguments and results.
"""

from typing import List, Dict, Any, Optional
import sqlite3
import json
import time


class AgentMessageStore:
    """Manages persistent session messages and tool audit logs."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        if db_path != ":memory:":
            self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._create_schema()

    def _create_schema(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at REAL NOT NULL,
                    metadata_json TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tool_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    arguments_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    duration_ms REAL NOT NULL,
                    timestamp REAL NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)

    def ensure_session(self, session_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Creates session record if it doesn't already exist."""
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, created_at, metadata_json) VALUES (?, ?, ?)",
                (session_id, time.time(), json.dumps(metadata or {}))
            )

    def add_message(self, session_id: str, role: str, content: str) -> int:
        """Appends a conversational turn."""
        self.ensure_session(session_id)
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, role, content, time.time())
            )
            return cur.lastrowid or 0

    def get_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves the most recent messages in chronological order."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT role, content, timestamp FROM messages
            WHERE session_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (session_id, limit)
        )
        rows = cur.fetchall()
        # Reverse to chronological order (oldest to newest)
        return [
            {"role": r[0], "content": r[1], "timestamp": r[2]}
            for r in reversed(rows)
        ]

    def log_tool_audit(
        self,
        session_id: str,
        trace_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
        result: Dict[str, Any],
        success: bool,
        duration_ms: float
    ) -> None:
        """Records an immutable audit entry for tool execution."""
        self.ensure_session(session_id)
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO tool_audit (
                    session_id, trace_id, tool_name, arguments_json, result_json,
                    success, duration_ms, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    trace_id,
                    tool_name,
                    json.dumps(arguments),
                    json.dumps(result),
                    1 if success else 0,
                    duration_ms,
                    time.time()
                )
            )

    def get_audit_trail(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves audit trail entries for a session."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT trace_id, tool_name, arguments_json, result_json, success, duration_ms
            FROM tool_audit WHERE session_id = ? ORDER BY id ASC
            """,
            (session_id,)
        )
        rows = cur.fetchall()
        return [
            {
                "trace_id": r[0],
                "tool_name": r[1],
                "arguments": json.loads(r[2]),
                "result": json.loads(r[3]),
                "success": bool(r[4]),
                "duration_ms": r[5]
            }
            for r in rows
        ]


def main() -> None:
    print("=== Module 10: Persistent Agent Message Store Demo ===")

    store = AgentMessageStore(":memory:")
    session = "session_user_42"

    # 1. Add conversation messages
    store.add_message(session, "system", "You are an autonomous engineering assistant.")
    store.add_message(session, "user", "What is the capital of France?")
    store.add_message(session, "assistant", "The capital of France is Paris.")
    store.add_message(session, "user", "What is its population?")
    store.add_message(session, "assistant", "Approximately 2.1 million within city limits.")

    # 2. Test sliding window history retrieval
    recent_3 = store.get_history(session, limit=3)
    assert len(recent_3) == 3
    # Chronological order check:
    assert recent_3[0]["content"] == "The capital of France is Paris."
    assert recent_3[1]["content"] == "What is its population?"
    assert recent_3[2]["content"] == "Approximately 2.1 million within city limits."
    print(f"[OK] Sliding window retrieved 3 recent messages in chronological order.")

    # 3. Log tool audit entry
    store.log_tool_audit(
        session_id=session,
        trace_id="trace_tool_001",
        tool_name="search_population",
        arguments={"city": "Paris", "year": 2024},
        result={"population": 2102650},
        success=True,
        duration_ms=45.2
    )

    audit_logs = store.get_audit_trail(session)
    assert len(audit_logs) == 1
    assert audit_logs[0]["tool_name"] == "search_population"
    assert audit_logs[0]["arguments"]["city"] == "Paris"
    assert audit_logs[0]["success"] is True
    print(f"[OK] Tool audit entry recorded and retrieved: {audit_logs[0]['tool_name']} in {audit_logs[0]['duration_ms']}ms")

    print("All tests in message_store.py completed successfully!\n")


if __name__ == "__main__":
    main()
