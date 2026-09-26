"""
Module 29: Embedded Relational Databases with SQLite
====================================================

This lesson explores how to use Python's built-in `sqlite3` module to store,
query, and manage structured relational data with full ACID transactional integrity.

Unlike client-server database systems (such as PostgreSQL or MySQL), SQLite is
serverless and zero-configuration. It runs inside the application's process memory
and stores the entire database in a single file or in RAM (`:memory:`).

In autonomous AI agent systems, SQLite serves as the primary engine for:
1. Long-term episodic memory and multi-turn conversational transcripts.
2. Caching expensive LLM responses and tool execution outputs.
3. Tracking multi-step agent plans, task status, and execution dependencies.

Key Topics Covered:
-------------------
1. Connecting to in-memory (`:memory:`) and file-based databases.
2. Creating relational tables with constraints (DDL).
3. Parameterized queries (`?` placeholders) to prevent SQL Injection.
4. High-performance batch insertion using `cursor.executemany()`.
5. Accessing named columns using the `sqlite3.Row` row factory.
6. Transaction boundaries: `commit()`, `rollback()`, and ACID safety.
7. Analytical queries: filtering, sorting, aggregations (`COUNT`, `SUM`).
8. AI Agent Application: Persistent Conversation & Tool Cache Storage Engine.
"""

import datetime
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# Section 1: Creating Connections and Cursors
# ============================================================================

def demonstrate_connection_basics() -> None:
    """
    Demonstrates initializing an in-memory SQLite database connection.
    In-memory databases (:memory:) are ultra-fast, isolated, and leave no
    lingering artifacts on disk.
    """
    print("=" * 70)
    print("1. SQLITE CONNECTION & CURSOR BASICS")
    print("=" * 70)

    # Establish connection to in-memory database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Query SQLite engine version
    cursor.execute("SELECT sqlite_version()")
    version = cursor.fetchone()[0]
    print(f"Connected to SQLite engine version: {version}")

    cursor.close()
    conn.close()
    print("Connection closed cleanly.")
    print("-" * 70 + "\n")


# ============================================================================
# Section 2 & 3: Schema Definition and Parameterized Insertion
# ============================================================================

def demonstrate_schema_and_parameterization() -> None:
    """
    Demonstrates table creation (DDL) and the critical importance of
    parameterized queries to prevent SQL Injection attacks.
    """
    print("=" * 70)
    print("2 & 3. SCHEMA DDL & PARAMETERIZED QUERIES (SQL Injection Defense)")
    print("=" * 70)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Define schema with primary key and constraints
    cursor.execute("""
        CREATE TABLE agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            archetype TEXT NOT NULL,
            max_context_tokens INTEGER DEFAULT 8192,
            is_active INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    print("Table 'agents' created with schema constraints.")

    # 1. Safe Parameterized Insertion using '?' placeholders
    agent_data = ("Auditor-M5", "Forensic Auditor", 16384, 1)
    cursor.execute(
        "INSERT INTO agents (name, archetype, max_context_tokens, is_active) VALUES (?, ?, ?, ?)",
        agent_data
    )
    conn.commit()
    print(f"Inserted record with ID: {cursor.lastrowid}")

    # 2. Preventing SQL Injection
    # Malicious payload intended to inject SQL statements:
    malicious_input = "HackerAgent', 'Malicious', 99999, 1); DROP TABLE agents; --"
    
    # When passed via parameter tuple, SQLite treats the string strictly as a literal value
    cursor.execute(
        "INSERT INTO agents (name, archetype, max_context_tokens, is_active) VALUES (?, ?, ?, ?)",
        (malicious_input, "Injected", 1000, 1)
    )
    conn.commit()

    # Verify table still exists and record was stored as literal text
    cursor.execute("SELECT name FROM agents WHERE archetype = ?", ("Injected",))
    retrieved_name = cursor.fetchone()[0]
    print(f"Stored malicious string literally without executing injection:\n   '{retrieved_name}'")

    cursor.close()
    conn.close()
    print("-" * 70 + "\n")


# ============================================================================
# Section 4: Batch Operations with cursor.executemany()
# ============================================================================

def demonstrate_batch_insertion() -> None:
    """
    Demonstrates inserting multiple rows efficiently in a single operation
    using `cursor.executemany()`.
    """
    print("=" * 70)
    print("4. HIGH-PERFORMANCE BATCH INSERTION (executemany)")
    print("=" * 70)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE tool_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            category TEXT NOT NULL,
            latency_ms INTEGER NOT NULL
        )
    """)

    tools = [
        ("web_search", "information_retrieval", 120),
        ("calculator", "math", 5),
        ("code_linter", "development", 45),
        ("database_query", "data", 30),
        ("file_writer", "filesystem", 15),
    ]

    # Execute batch insertion
    cursor.executemany(
        "INSERT INTO tool_registry (tool_name, category, latency_ms) VALUES (?, ?, ?)",
        tools
    )
    conn.commit()

    print(f"Batch inserted {cursor.rowcount} tools into the registry.")

    cursor.close()
    conn.close()
    print("-" * 70 + "\n")


# ============================================================================
# Section 5: Accessing Named Columns with sqlite3.Row
# ============================================================================

def demonstrate_row_factory() -> None:
    """
    Demonstrates configuring `conn.row_factory = sqlite3.Row` to access
    query result columns by name instead of numeric indices.
    """
    print("=" * 70)
    print("5. ACCESSING COLUMNS BY NAME (sqlite3.Row)")
    print("=" * 70)

    conn = sqlite3.connect(":memory:")
    # Enable the dictionary-like row factory
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            title TEXT,
            status TEXT,
            priority INTEGER
        )
    """)

    cursor.execute("INSERT INTO projects VALUES (1, 'Course -1 Rewrite', 'IN_PROGRESS', 10)")
    conn.commit()

    cursor.execute("SELECT id, title, status, priority FROM projects WHERE id = 1")
    row = cursor.fetchone()

    print("Retrieved row via sqlite3.Row:")
    print(f"   Row title:    {row['title']}")
    print(f"   Row status:   {row['status']}")
    print(f"   Row priority: {row['priority']}")
    print(f"   Available column names: {row.keys()}")

    cursor.close()
    conn.close()
    print("-" * 70 + "\n")


# ============================================================================
# Section 6: Transactions and Rollback Mechanics
# ============================================================================

def demonstrate_transactions_and_rollback() -> None:
    """
    Demonstrates atomicity: rolling back a transaction when an error occurs,
    ensuring the database is never left in a corrupted or partial state.
    """
    print("=" * 70)
    print("6. TRANSACTIONS & ROLLBACK (ACID Atomicity)")
    print("=" * 70)

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE bank_accounts (
            account_id TEXT PRIMARY KEY,
            balance INTEGER NOT NULL CHECK(balance >= 0)
        )
    """)

    cursor.execute("INSERT INTO bank_accounts VALUES ('Agent_A', 1000)")
    cursor.execute("INSERT INTO bank_accounts VALUES ('Agent_B', 500)")
    conn.commit()
    print("Initial Balances: Agent_A = $1000, Agent_B = $500")

    # Attempt a transfer that violates the balance constraint (overdraft)
    transfer_amount = 1500  # More than Agent_A possesses!

    try:
        # Step 1: Debit Agent_A (this succeeds)
        cursor.execute(
            "UPDATE bank_accounts SET balance = balance - ? WHERE account_id = 'Agent_A'",
            (transfer_amount,)
        )
        # Step 2: Credit Agent_B
        cursor.execute(
            "UPDATE bank_accounts SET balance = balance + ? WHERE account_id = 'Agent_B'",
            (transfer_amount,)
        )
        conn.commit()
    except sqlite3.IntegrityError as err:
        # CHECK constraint violated! Roll back entire transaction.
        print(f"Transaction failed due to constraint violation: {err}")
        conn.rollback()
        print("Rolled back all intermediate operations.")

    # Check balances after aborted transaction
    cursor.execute("SELECT account_id, balance FROM bank_accounts ORDER BY account_id")
    for acc, bal in cursor.fetchall():
        print(f"   Account: {acc:<10} Balance: ${bal}")
    print("Notice: Balances remained completely unchanged because of rollback!")

    cursor.close()
    conn.close()
    print("-" * 70 + "\n")


# ============================================================================
# Section 7: Filtering, Sorting, and Aggregations
# ============================================================================

def demonstrate_aggregations() -> None:
    """
    Demonstrates analytical SQL queries: COUNT, SUM, AVG, GROUP BY, and ORDER BY.
    """
    print("=" * 70)
    print("7. SQL AGGREGATIONS & ANALYTICAL QUERIES")
    print("=" * 70)

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE tool_invocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            tool_name TEXT,
            tokens_used INTEGER,
            latency_ms REAL
        )
    """)

    invocations = [
        ("Agent-1", "web_search", 450, 110.5),
        ("Agent-1", "web_search", 520, 135.2),
        ("Agent-1", "calculator", 25, 2.1),
        ("Agent-2", "web_search", 400, 95.0),
        ("Agent-2", "code_linter", 80, 42.0),
        ("Agent-2", "calculator", 30, 2.5),
    ]

    cursor.executemany(
        "INSERT INTO tool_invocations (agent_id, tool_name, tokens_used, latency_ms) VALUES (?, ?, ?, ?)",
        invocations
    )
    conn.commit()

    # Run analytical aggregation query
    cursor.execute("""
        SELECT 
            agent_id,
            COUNT(*) as total_calls,
            SUM(tokens_used) as total_tokens,
            ROUND(AVG(latency_ms), 1) as avg_latency
        FROM tool_invocations
        GROUP BY agent_id
        ORDER BY total_tokens DESC
    """)

    print("Agent Usage Summary (Aggregated from SQLite):")
    for row in cursor.fetchall():
        print(f"   Agent: {row['agent_id']:<8} Calls: {row['total_calls']:<3} Tokens: {row['total_tokens']:<5} Avg Latency: {row['avg_latency']}ms")

    cursor.close()
    conn.close()
    print("-" * 70 + "\n")


# ============================================================================
# Section 8: AI Agent Episodic Memory Storage Engine
# ============================================================================

class AgentMemoryStore:
    """
    A persistent SQLite-backed conversation and episodic memory store
    for autonomous AI agents.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._initialize_tables()

    def _initialize_tables(self) -> None:
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session 
                ON conversation_history (session_id)
            """)

    def record_turn(self, session_id: str, role: str, message: str) -> int:
        """Appends a conversation message to the session transcript."""
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO conversation_history (session_id, role, message) VALUES (?, ?, ?)",
                (session_id, role, message)
            )
            return cursor.lastrowid

    def get_transcript(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves the recent conversation history for a given session."""
        cursor = self.conn.execute(
            """SELECT role, message, created_at 
               FROM conversation_history 
               WHERE session_id = ? 
               ORDER BY id ASC 
               LIMIT ?""",
            (session_id, limit)
        )
        return [{"role": r["role"], "message": r["message"], "time": r["created_at"]} for r in cursor.fetchall()]

    def close(self) -> None:
        self.conn.close()


def demonstrate_agent_memory() -> None:
    """
    Demonstrates recording and retrieving conversation turns with AgentMemoryStore.
    """
    print("=" * 70)
    print("8. AI AGENT EPISODIC MEMORY ENGINE")
    print("=" * 70)

    memory = AgentMemoryStore()
    sess = "sess_autonomous_881"

    memory.record_turn(sess, "system", "You are an AI code optimization specialist.")
    memory.record_turn(sess, "user", "How can I speed up SQLite batch writes?")
    memory.record_turn(sess, "assistant", "Use cursor.executemany and wrap writes in a single transaction!")

    transcript = memory.get_transcript(sess)
    print(f"Retrieved {len(transcript)} messages for session '{sess}':")
    for msg in transcript:
        print(f"   [{msg['role'].upper()}]: {msg['message']}")

    memory.close()
    print("-" * 70 + "\n")


# ============================================================================
# Main Demonstration Runner
# ============================================================================

def main() -> None:
    print("Starting Module 29: Embedded Relational Databases with SQLite\n")
    demonstrate_connection_basics()
    demonstrate_schema_and_parameterization()
    demonstrate_batch_insertion()
    demonstrate_row_factory()
    demonstrate_transactions_and_rollback()
    demonstrate_aggregations()
    demonstrate_agent_memory()
    print("Module 29 demonstration completed successfully!")


if __name__ == "__main__":
    main()
