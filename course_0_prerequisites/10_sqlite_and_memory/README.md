# Module 10: SQLite, Transactions, In-Memory DBs, and Agent Memory Persistence

## 1. Learning Objectives
By the end of this module, you will be able to:
- Explain why SQLite is the premier choice for embedded, zero-dependency, transactional agent persistence.
- Manage database connections, cursors, and ACID transactions with automatic rollback on failure.
- Prevent SQL injection vulnerabilities using strictly parameterized queries (`?`).
- Optimize SQLite concurrency using Write-Ahead Logging (`PRAGMA journal_mode=WAL;`).
- Design relational schemas for agent memory: session indices, conversational message logs, and tool execution audit trails.
- Implement sliding-window history retrieval to keep prompts within LLM context token windows.

---

## 2. Why AI Agent Engineers Need This
Autonomous agents require state that survives restarts and crashes:
- Multi-turn conversation history across distinct user sessions.
- Audit trails recording every tool called, its parameters, and the returned output.
- Long-term memory notes and key-value preferences.

Storing agent history in volatile Python lists (`self.messages = []`) causes total data loss if the server restarts. Storing in flat text files risks file corruption during concurrent writes. SQLite provides an ACID-compliant, zero-configuration relational database engine embedded directly inside Python without needing to run an external database server (like PostgreSQL).

---

## 3. Structured Concept Breakdown

### Concept 1: SQLite Architecture & In-Memory Databases (`:memory:`)
- **TERM**: SQLite & In-Memory Database (`:memory:`)
- **DEFINITION**: A self-contained, serverless SQL database engine stored either as a single cross-platform disk file or completely in RAM (`:memory:`).
- **INTUITION**: A notebook vs a filing cabinet. An external DB (Postgres) is a dedicated records room down the hall requiring a security guard and network cables. SQLite is a bound notebook in your desk drawer; `:memory:` is a whiteboard erased when the meeting ends.
- **WHY IT EXISTS**: In unit tests and ephemeral agent runs, writing to disk creates cleanup headaches and slow I/O. An `:memory:` SQLite database offers sub-millisecond query latency with full SQL support and zero disk footprint.
- **HOW IT WORKS**: Passing `sqlite3.connect(":memory:")` allocates a private B-tree database structure in process memory. Closing the connection instantly reclaims the RAM.
- **CODE**:
```python
import sqlite3

# Ephemeral fast in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT);")
cursor.execute("INSERT INTO test (val) VALUES ('in-memory-agent-state');")
conn.commit()
```

---

### Concept 2: Parameterized Queries vs SQL Injection
- **TERM**: Parameterized Queries
- **DEFINITION**: Passing SQL statements with placeholder markers (`?` in SQLite) alongside a separate tuple of values, delegating data escaping and typing to the database engine.
- **INTUITION**: An envelope for money. Handing a sealed envelope marked "Deposit" to the cashier ensures the money is credited to your account; writing instructions on the back of a napkin allows someone to forge instructions.
- **WHY IT EXISTS**: Autonomous agents often store raw text from untrusted web pages or LLM outputs into memory. If you format strings: `f"INSERT INTO msgs VALUES ('{content}')"`, a prompt like `"Robert'); DROP TABLE msgs;--"` deletes your database (SQL Injection).
- **HOW IT WORKS**: The SQLite parser compiles the SQL query plan *before* substituting parameter values. Parameter values are treated strictly as literal data, never as executable SQL commands.
- **CODE**:
```python
# VULNERABLE: DO NOT DO THIS
# cursor.execute(f"INSERT INTO messages (content) VALUES ('{user_msg}')")

# SECURE: Always use parameterized queries
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
conn.commit()
```

---

### Concept 3: ACID Transactions & Rollback
- **TERM**: ACID Transactions & Rollback
- **DEFINITION**: A sequence of database operations executed as a single atomic unit of work: either all changes commit successfully, or all changes are rolled back on error.
- **INTUITION**: A bank transfer. Moving $100 from Account A to Account B requires two steps: deducting from A and adding to B. If the computer crashes halfway, the transaction rolls back so money doesn't vanish into thin air.
- **WHY IT EXISTS**: An agent turn involves multiple related operations: inserting the user message, logging the tool call, and updating token counts. If logging fails midway, the database must not be left in a corrupted, half-updated state.
- **HOW IT WORKS**: SQLite begins a transaction automatically before the first DML statement (`INSERT`/`UPDATE`). Calling `conn.commit()` writes changes permanently; calling `conn.rollback()` restores the database to its pre-transaction state.
- **CODE**:
```python
try:
    with conn:  # Context manager automatically commits on clean exit or rolls back on exception
        conn.execute("INSERT INTO messages ...")
        conn.execute("INSERT INTO tool_audit ...")
except Exception as e:
    print(f"Transaction failed, database rolled back: {e}")
```

---

### Concept 4: Write-Ahead Logging (`WAL` Mode)
- **TERM**: Write-Ahead Logging (WAL)
- **DEFINITION**: A journaling mode where changes are appended to a separate `.wal` file before merging into the main database, enabling concurrent readers alongside a concurrent writer.
- **INTUITION**: A restaurant waitstaff order pad. Instead of every waiter locking the kitchen door while placing an order (standard rollback journal locking), waiters quickly jot orders on a shared clip pad (WAL file). Readers (cooks) read continuously while one writer appends.
- **WHY IT EXISTS**: In standard SQLite rollback mode, a write operation locks the entire database file, causing `sqlite3.OperationalError: database is locked` in concurrent agent web services. WAL mode dramatically increases concurrency.
- **HOW IT WORKS**: Setting `PRAGMA journal_mode = WAL;` switches the database engine to write to a `-wal` companion file. Readers read the main file plus the WAL log concurrently without waiting for write locks.
- **CODE**:
```python
conn = sqlite3.connect("agent_memory.db")
conn.execute("PRAGMA journal_mode = WAL;")
conn.execute("PRAGMA synchronous = NORMAL;")
```

---

### Concept 5: Agent Message Store Schema & Sliding Window
- **TERM**: Agent Relational Memory Schema
- **DEFINITION**: A normalized SQL schema storing sessions, message turns, tool calls, and token counts, queried with `ORDER BY timestamp DESC LIMIT N` to fit within token context windows.
- **INTUITION**: A chat history window. Even if a user has exchanged 10,000 messages with an agent over 6 months, the LLM prompt only receives the system prompt plus the most recent 10 messages (sliding window) to prevent context exhaustion.
- **WHY IT EXISTS**: LLM context windows are bounded (e.g. 8k to 128k tokens) and cost money per token. The agent database retains the complete persistent history on disk while querying only the active window for inference.
- **HOW IT WORKS**:
  ```sql
  SELECT role, content FROM messages
  WHERE session_id = ?
  ORDER BY id DESC LIMIT ?
  ```
  The retrieved rows are reversed to chronological order before being injected into the prompt.
- **CODE**:
```python
def get_recent_history(conn, session_id: str, limit: int = 5):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )
    rows = cursor.fetchall()
    return list(reversed(rows))  # Return chronological order
```

---

## 4. Real-World Failure Modes & Anti-Patterns in Agents

### Anti-Pattern 1: Database Locking Under Concurrency
- **The Bug**: Opening multiple SQLite connections across concurrent async tasks without WAL mode enabled.
- **The Consequence**: Frequent `sqlite3.OperationalError: database is locked` errors during multi-agent parallel runs.
- **The Fix**: Execute `PRAGMA journal_mode=WAL;` and set a connection timeout: `sqlite3.connect("agent.db", timeout=10.0)`.

### Anti-Pattern 2: Dynamic SQL String Formatting
- **The Bug**: Constructing queries with f-strings: `f"SELECT * FROM messages WHERE session_id = '{session_id}'"`.
- **The Consequence**: Instant SQL injection vulnerability.
- **The Fix**: Always use query parameterization: `conn.execute("SELECT ... WHERE session_id = ?", (session_id,))`.

---

## 5. Progressive Exercises

### Tier 1 (Recall)
1. What special URI string opens an in-memory SQLite database?
2. Which PRAGMA command enables concurrent reads and writes in SQLite?
3. What happens to uncommitted changes if an exception occurs inside a `with conn:` block?

### Tier 2 (Debugging)
Find the vulnerability and error in this agent persistence function:
```python
def save_agent_step(conn, session, role, msg):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO history VALUES ('{session}', '{role}', '{msg}')")
    # What crucial call is missing here for changes to persist on disk?
```
*Hint*: SQL injection vulnerability and missing `conn.commit()`!

### Tier 3 (Application)
Write a class `SQLiteAuditLog` with methods:
- `log_tool_invocation(session_id: str, tool_name: str, args_json: str, result_json: str, success: bool)`
- `get_failed_tools(session_id: str) -> list[dict]`
Use parameterized queries and transactional commits.

### Tier 4 (Challenge)
Build a complete `PersistentAgentMemory` manager with:
- Schema supporting `sessions`, `messages`, and `key_value_store`.
- WAL mode enabled.
- Method `get_context_window(session_id: str, max_messages: int) -> list[dict]` returning the system prompt plus the last `N` messages in chronological order.
- Method `set_user_preference(user_id: str, key: str, value: str)` storing long-term memory.

---

## 6. Verification & Runnable Scripts
Run the standalone demonstration scripts included in this module:
```bash
python3 course_0_prerequisites/10_sqlite_and_memory/sqlite_basics.py
python3 course_0_prerequisites/10_sqlite_and_memory/message_store.py
```
