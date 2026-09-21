"""Module 29: SQLite Introduction"""
import sqlite3

# SQLite: a lightweight SQL database stored in a single file.
# We use :memory: for demos (no file created).
conn = sqlite3.connect(":memory:")

# Create a table:
conn.execute("""
    CREATE TABLE messages (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        role    TEXT NOT NULL,
        content TEXT NOT NULL
    )
""")

# Insert rows using parameterized queries (NEVER format strings with user input):
conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", "Hello!"))
conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("agent", "Hi there!"))
conn.commit()

# Query:
for row in conn.execute("SELECT * FROM messages"):
    print(row)

# Update and delete:
conn.execute("UPDATE messages SET content=? WHERE role=?", ("Greetings!", "agent"))
conn.execute("DELETE FROM messages WHERE id=1")
conn.commit()
print("\nAfter update/delete:")
for row in conn.execute("SELECT * FROM messages"):
    print(row)

conn.close()
print("\nSQLite lesson complete. See Course 0 Module 10 for full message store.")
