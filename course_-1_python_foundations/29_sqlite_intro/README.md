# Topic: Embedded Relational Databases with SQLite

## What You Will Learn
In this module, you will learn:
- What SQLite is and why it is the most deployed database engine in human history.
- The fundamental difference between serverless embedded databases (SQLite) and client-server databases (PostgreSQL, MySQL).
- How to use Python's built-in `sqlite3` module with zero third-party installation or setup.
- How to create temporary in-memory databases (`:memory:`) for fast testing and persistent disk-based database files.
- How to design schemas using SQL Data Definition Language (DDL): tables, primary keys, and data types.
- How to execute CRUD queries (`INSERT`, `SELECT`, `UPDATE`, `DELETE`) with parameterized placeholders (`?`) to completely eliminate SQL Injection vulnerabilities.
- How transactions work (ACID properties) and how to commit changes or roll back upon errors.
- How to use `sqlite3.Row` as a row factory to access query results by column name like a dictionary.
- How autonomous AI agents use SQLite to store conversation histories, cache expensive LLM responses, and persist long-term memory across sessions.

## Prerequisites
Before tackling this module, you should be familiar with:
- Module 06: Collections (Tuples, Lists, and Dictionaries).
- Module 10: Errors and Exception Handling (`try`, `except`, `finally`).
- Module 11: File I/O and Context Managers (`with` statements).
- Module 26: JSON serialization and key-value mapping concepts.

## The Problem
As your AI agent or Python application grows, you must store data across restarts: user preferences, conversation transcripts, token costs, and tool execution logs.

A common beginner approach is saving everything into a JSON file (`data.json`):
```python
# Naive approach:
with open("agent_memory.json", "w") as f:
    json.dump(memory_records, f)
```
While JSON is great for data interchange, it fails as a database:
1. **No Indexed Queries**: To find one message from last Tuesday, you must read the entire 500MB JSON file from disk into RAM and loop through every single record.
2. **Catastrophic Corruption Risk**: If your computer loses power or the process crashes halfway through writing the file, the entire JSON file is corrupted and unrecoverable.
3. **No Concurrency or ACID Guarantees**: You cannot safely read and write simultaneously. Multi-step operations cannot be rolled back if an error occurs halfway through.
4. **Server Overhead**: Setting up a full PostgreSQL or MySQL server requires installing database software, managing network ports, configuring user grants, and administering server daemons.

**SQLite** provides the perfect solution: a full-featured, zero-configuration, ACID-compliant SQL relational database engine running directly inside your Python process, storing data in a single compact file on disk.

## Key Terminology
- **SQLite**: An embedded, serverless, self-contained relational database engine bundled directly inside Python.
- **Embedded / Serverless Database**: A database that runs inside the client application's memory space rather than connecting over a network to a separate database server.
- **Connection (`sqlite3.Connection`)**: The object representing an active session to a database file or in-memory store.
- **Cursor (`sqlite3.Cursor`)**: A control structure used to traverse and fetch query results from a database.
- **In-Memory Database (`:memory:`)**: A temporary SQLite database held entirely in RAM, destroyed when the connection closes.
- **Parameterized Query**: Passing query values separately from SQL text using `?` placeholders, preventing SQL Injection.
- **SQL Injection**: A severe security vulnerability where attackers inject malicious SQL commands into queries via unsanitized user inputs.
- **ACID**: Atomicity, Consistency, Isolation, Durability—the four guarantees ensuring reliable database transactions.
- **Commit**: Permanently writing transactional changes from the memory buffer to disk.
- **Rollback**: Aborting a transaction and restoring the database to its pre-transaction state.
- **Row Factory**: A callable configured on a connection that converts raw database rows into rich objects (e.g. `sqlite3.Row`).

## Intuition
Think of managing records for a medical clinic:
- **The JSON Approach** is a single massive notebook. Every time a doctor needs to check a patient's allergy, the doctor must flip through all 10,000 pages from page 1 to find the patient's name. If the doctor spills coffee on page 50, the entire notebook is ruined.
- **The SQLite Approach** is a filing cabinet with indexed drawers, alphabetical tabs, and an automated librarian. The doctor asks: *"Retrieve allergies for Patient #402"* (`SELECT allergies FROM patients WHERE id = 402`). The librarian instantly navigates to the exact tab in milliseconds. If the power goes out while updating a chart, the transaction log ensures no data is corrupted.

## Concept
### 1. The Connection and Cursor Lifecycle
1. Open a connection: `conn = sqlite3.connect("agent_memory.db")`
2. Create a cursor: `cursor = conn.cursor()`
3. Execute SQL commands: `cursor.execute("CREATE TABLE ...")`
4. Commit transactional changes: `conn.commit()`
5. Close resources: `conn.close()` (or use `with conn:` context manager).

### 2. Parameterization vs SQL Injection
**The Fatal Vulnerability (String Concatenation / f-strings)**:
```python
# NEVER DO THIS! CRITICAL SECURITY HOLE!
user_input = "Alice'; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE name = '{user_input}'"
cursor.execute(query)  # Drops the entire users table!
```
**The Secure Standard (Parameterized Queries)**:
```python
# SECURE: Values passed as tuple to placeholder '?'
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```
When parameterized, SQLite treats the input string purely as literal data; it can never be interpreted as SQL syntax commands.

### 3. Named Columns with `sqlite3.Row`
By default, SQLite returns rows as tuples: `row[0]`, `row[1]`. Setting `conn.row_factory = sqlite3.Row` allows accessing columns by name: `row["name"]`, `row["created_at"]`.

## Syntax
### Creating Tables and Inserting Data
```python
import sqlite3

# 1. Connect to in-memory or disk database
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row  # Enable dictionary-like column access
cursor = conn.cursor()

# 2. Define schema (DDL)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL,
        token_count INTEGER DEFAULT 0
    )
""")

# 3. Insert records using parameterized queries
cursor.execute(
    "INSERT INTO agents (name, role, token_count) VALUES (?, ?, ?)",
    ("ResearchAgent", "Researcher", 1250)
)

# 4. Batch insertion
agents_batch = [
    ("CoderAgent", "Developer", 4500),
    ("ReviewerAgent", "Auditor", 800),
]
cursor.executemany(
    "INSERT INTO agents (name, role, token_count) VALUES (?, ?, ?)",
    agents_batch
)
conn.commit()
```

### Querying Data
```python
# Query multiple rows
cursor.execute("SELECT * FROM agents WHERE token_count > ? ORDER BY token_count DESC", (1000,))
rows = cursor.fetchall()
for row in rows:
    print(f"Agent {row['name']} ({row['role']}): {row['token_count']} tokens")

# Query a single row
cursor.execute("SELECT * FROM agents WHERE name = ?", ("CoderAgent",))
agent = cursor.fetchone()
if agent:
    print(f"Found: {agent['name']} with ID {agent['id']}")

conn.close()
```

## Example
Here is a complete, executable Python example demonstrating schema creation, transactions, rollback on error, and indexed querying:

```python
import sqlite3
from typing import List, Tuple

def demonstrate_sqlite_workflow() -> None:
    # Use an in-memory database for isolated, high-speed execution
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Insert messages in a transaction
    messages = [
        ("sess_01", "user", "What is the capital of France?"),
        ("sess_01", "assistant", "The capital of France is Paris."),
        ("sess_02", "user", "Explain SQLite in Python."),
    ]
    cursor.executemany(
        "INSERT INTO chat_messages (session_id, sender, content) VALUES (?, ?, ?)",
        messages
    )
    conn.commit()

    # Query messages for sess_01
    cursor.execute(
        "SELECT sender, content FROM chat_messages WHERE session_id = ? ORDER BY id",
        ("sess_01",)
    )
    results = cursor.fetchall()
    print(f"Retrieved {len(results)} messages for session 'sess_01':")
    for r in results:
        print(f"   [{r['sender']}]: {r['content']}")

    conn.close()

if __name__ == "__main__":
    demonstrate_sqlite_workflow()
```

## Line-by-Line Explanation
1. `conn = sqlite3.connect(":memory:")`: Connects to an ephemeral in-memory database that leaves zero artifacts on disk.
2. `conn.row_factory = sqlite3.Row`: Configures row mapping so records can be indexed by column name (`r['sender']`) rather than numerical index (`r[0]`).
3. `CREATE TABLE chat_messages (...)`: Defines a relational schema with a primary key that auto-increments with each inserted row.
4. `cursor.executemany(sql, messages)`: Efficiently inserts multiple records in a single database transaction.
5. `conn.commit()`: Flushes the write log and commits the transaction permanently.
6. `cursor.execute("... WHERE session_id = ?", ("sess_01",))`: Queries matching rows securely with parameter binding.

## What Python Is Doing
Under the hood:
1. When `sqlite3.connect()` is called, Python's C extension initializes a native SQLite engine instance and opens a C-level database handle (`sqlite3*`).
2. When you execute DDL (`CREATE TABLE`), SQLite parses the statement, generates bytecode, and formats database storage pages (typically 4096-byte blocks) backed by B-trees.
3. When executing parameterized queries (`?`), SQLite compiles the SQL statement into an internal Virtual Database Engine (VDBE) bytecode program once. It then safely binds your parameter values into the bytecode registers using functions like `sqlite3_bind_text()` and `sqlite3_bind_int64()`. No text interpolation ever occurs!
4. Transactions operate via a Write-Ahead Log (WAL) or rollback journal. All mutations write to the journal first; only when `commit()` is called is the transaction marked as atomic and finalized.

## Common Mistakes
1. **SQL Injection via String Formatting**:
   Writing `cursor.execute(f"SELECT * FROM items WHERE id = {user_id}")`. Never use f-strings for SQL queries! Always use `?` placeholders.
2. **Forgetting the Trailing Comma in Single-Element Tuples**:
   Writing `cursor.execute("SELECT * FROM t WHERE id = ?", (my_id))` without a comma passes `my_id` as a grouped expression rather than a tuple, causing `TypeError: parameters are of unsupported type`. Write `(my_id,)`.
3. **Forgetting to Call `conn.commit()`**:
   Performing `INSERT`, `UPDATE`, or `DELETE` statements without calling `conn.commit()`. When the connection closes, uncommitted changes are rolled back and permanently lost!
4. **Hardcoding Tuple Indices**:
   Using `row[3]` in application logic. If schema columns are reordered or a new column is added, your code silently reads the wrong data. Always use `conn.row_factory = sqlite3.Row`.
5. **Cross-Thread Connection Sharing**:
   SQLite connections cannot be shared across multiple threads by default (`sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread`). Use a connection pool or open connections per thread.

## Real-World Uses
- **Autonomous AI Agent Memory**: Storing conversational chat histories, episodic memories, and tool invocation traces.
- **Mobile Applications**: Every iOS and Android device runs hundreds of SQLite databases storing contacts, SMS messages, and application state.
- **Web Browsers**: Google Chrome, Firefox, and Safari store browsing histories, cookies, and bookmarks in SQLite databases.
- **Desktop Software**: Applications like Apple Photos, Lightroom, and VSCode use SQLite for cataloging and configuration storage.

## Connection to AI Agents
SQLite is the premier embedded database for AI agents:
- **Episodic & Chat Memory**: Storing conversational turns with session IDs, timestamps, token counts, and roles. When an agent restarts, it queries SQLite to rebuild its context window.
- **LLM Response Caching**: Storing model prompts and completions keyed by prompt hash. If an agent executes the same tool or query twice, it retrieves the cached response instantly, saving money and latency.
- **Task and Goal Tracking**: Tracking task status (`pending`, `in_progress`, `completed`, `failed`), retry counters, and intermediate tool outputs.
- **Vector & Embeddings Indexing**: Storing embedding vectors and metadata alongside text chunks using extensions like `sqlite-vss` or raw vector tables.

## Practice
1. Create an in-memory SQLite database and define a table `tasks` with columns `id`, `description`, `priority`, and `is_done`.
2. Insert 3 tasks using parameterized queries.
3. Query all tasks where `priority > 2` and print their descriptions using `sqlite3.Row`.
4. Update one task's `is_done` status to `1` and verify the change with another query.

## Challenge
Can you build an AI Agent Memory Manager that stores conversation turns, supports multi-turn session queries, calculates total token usage per session, and implements an atomic transaction rollback test? (We will build this in `exercises.py`!)

## Summary
- SQLite is an embedded, serverless relational database engine included with Python's standard library.
- Parameterized queries (`?`) are mandatory to prevent SQL injection vulnerabilities.
- Use `sqlite3.Row` to access query columns by name rather than arbitrary tuple indices.
- All modifications (`INSERT`, `UPDATE`, `DELETE`) require `conn.commit()` to persist.
- AI agents use SQLite for persistent memory, chat history, and tool caching.

## What You Should Know Before Moving On
- How to create tables and execute queries using Python's `sqlite3` module.
- Why parameterized queries prevent SQL injection and how to write them with `(val,)`.
- How to use `conn.commit()` and `conn.rollback()` to manage database transactions.
- How to configure `conn.row_factory = sqlite3.Row` for dictionary-like column access.
- How an autonomous AI agent leverages SQLite for conversation history and state persistence.
