"""memory.py - Persistent SQLite memory manager with WAL mode, sessions, and audit logs."""

from typing import List, Dict, Any, Optional
import sqlite3
import json
import time


class SQLiteMemory:
    """Persistent SQLite-backed memory store for agent conversation turns and tool audit logs."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10.0)

        # Enable WAL mode for high concurrency if file-based
        if ":memory:" not in db_path:
            self.conn.execute("PRAGMA journal_mode = WAL;")
        self.conn.execute("PRAGMA synchronous = NORMAL;")
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self._init_tables()

    def _init_tables(self) -> None:
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
                    args_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    duration_ms REAL NOT NULL,
                    timestamp REAL NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
                );
            """)

    def ensure_session(self, session_id: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Creates session record if missing."""
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, created_at, metadata_json) VALUES (?, ?, ?)",
                (session_id, time.time(), json.dumps(metadata or {}))
            )

    def add_message(self, session_id: str, role: str, content: str) -> int:
        """Stores a conversational turn in chronological history."""
        self.ensure_session(session_id)
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, role, content, time.time())
            )
            return cur.lastrowid or 0

    def get_history(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves recent conversation messages in chronological order."""
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
        # Reverse to chronological order
        return [
            {"role": r[0], "content": r[1], "timestamp": r[2]}
            for r in reversed(rows)
        ]

    def log_tool_call(
        self,
        session_id: str,
        trace_id: str,
        tool_name: str,
        args: Dict[str, Any],
        result: Any,
        success: bool,
        duration_ms: float,
    ) -> None:
        """Records an immutable tool execution entry."""
        self.ensure_session(session_id)
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO tool_audit (
                    session_id, trace_id, tool_name, args_json, result_json,
                    success, duration_ms, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    trace_id,
                    tool_name,
                    json.dumps(args),
                    json.dumps(result if isinstance(result, (dict, list, str, int, float, bool, type(None))) else str(result)),
                    1 if success else 0,
                    duration_ms,
                    time.time()
                )
            )

    def get_audit_logs(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves all tool execution audit entries for a session."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT trace_id, tool_name, args_json, result_json, success, duration_ms, timestamp
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
                "duration_ms": r[5],
                "timestamp": r[6],
            }
            for r in rows
        ]

    def clear_history(self, session_id: str) -> None:
        """Deletes all messages and tool audits for a session."""
        with self.conn:
            self.conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            self.conn.execute("DELETE FROM tool_audit WHERE session_id = ?", (session_id,))

    def close(self) -> None:
        """Closes the underlying database connection."""
        self.conn.close()
