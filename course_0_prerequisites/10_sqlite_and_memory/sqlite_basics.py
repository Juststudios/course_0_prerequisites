"""sqlite_basics.py - Demonstrates SQLite transactions, WAL mode, and parameterized queries.

Key concepts demonstrated:
1. Enabling WAL mode for concurrency.
2. Parameterized queries preventing SQL injection.
3. ACID transactions with automatic rollback on error.
"""

import sqlite3
import tempfile
import os
from typing import List, Tuple


def initialize_db(db_path: str) -> sqlite3.Connection:
    """Connects to SQLite and configures pragmas for high performance."""
    conn = sqlite3.connect(db_path, timeout=10.0)
    # Enable WAL mode if not in-memory
    if ":memory:" not in db_path:
        conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")

    # Create tables
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kv_memory (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    return conn


def test_acid_transactions(conn: sqlite3.Connection) -> None:
    """Proves that failed transactions roll back completely."""
    # Insert baseline item
    with conn:
        conn.execute("INSERT OR REPLACE INTO kv_memory (key, value) VALUES (?, ?)", ("state", "initial"))

    # Attempt a transaction where step 2 fails
    try:
        with conn:
            conn.execute("UPDATE kv_memory SET value = ? WHERE key = ?", ("modified", "state"))
            # Deliberately violate constraint by inserting duplicate primary key with standard INSERT
            conn.execute("INSERT INTO kv_memory (key, value) VALUES (?, ?)", ("state", "duplicate_crash"))
    except sqlite3.IntegrityError:
        pass  # Expected rollback

    # Verify state rolled back to 'initial'
    cur = conn.cursor()
    cur.execute("SELECT value FROM kv_memory WHERE key = ?", ("state",))
    val = cur.fetchone()[0]
    assert val == "initial", f"Expected rollback to 'initial', got '{val}'"
    print("[OK] Transaction rollback verified: partial state modification reverted.")


def test_sql_injection_defense(conn: sqlite3.Connection) -> None:
    """Proves that malicious input does not alter query logic."""
    malicious_key = "user_pref'; DROP TABLE kv_memory; --"
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO kv_memory (key, value) VALUES (?, ?)",
            (malicious_key, "safe_value")
        )

    cur = conn.cursor()
    cur.execute("SELECT value FROM kv_memory WHERE key = ?", (malicious_key,))
    row = cur.fetchone()
    assert row is not None and row[0] == "safe_value"

    # Verify table was NOT dropped
    cur.execute("SELECT count(*) FROM kv_memory")
    count = cur.fetchone()[0]
    assert count > 0
    print("[OK] Parameterized query successfully neutralized SQL injection attempt.")


def main() -> None:
    print("=== Module 10: SQLite Basics & ACID Transactions Demo ===")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    try:
        conn = initialize_db(db_path)
        test_acid_transactions(conn)
        test_sql_injection_defense(conn)
        conn.close()
        print("All tests in sqlite_basics.py passed successfully!\n")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
        wal_file = f"{db_path}-wal"
        shm_file = f"{db_path}-shm"
        if os.path.exists(wal_file):
            os.remove(wal_file)
        if os.path.exists(shm_file):
            os.remove(shm_file)


if __name__ == "__main__":
    main()
