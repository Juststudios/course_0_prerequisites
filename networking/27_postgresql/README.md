# PostgreSQL

## What You Will Learn
In this module, you will dive into PostgreSQL (Postgres), one of the most popular, powerful, and open-source Relational Database Management Systems (RDBMS). You will learn how it differs from SQLite, how to connect to it via Python, and basic SQL commands.

## Prerequisites
- Completion of Module 26: Databases.
- Basic understanding of SQL syntax (SELECT, INSERT, UPDATE).

## Key Terminology
- **PostgreSQL / Postgres:** An advanced, enterprise-grade open-source relational database.
- **Client/Server Model:** Unlike SQLite (which is a file), Postgres runs as a background service (server) that accepts connections over a network from clients.
- **psycopg2 / psycopg3:** The most popular Python drivers (adapters) for PostgreSQL.
- **Connection String (URI):** A string containing all the information needed to connect to a database (e.g., `postgresql://user:password@localhost:5432/dbname`).

## The Problem
SQLite is amazing, but it is built for single-user or low-concurrency applications because it locks the entire file during writes. If you are building a web server with hundreds of concurrent users, SQLite will bottleneck. You need a database that can handle thousands of concurrent connections, enforce strict data types, and scale across multiple disks.

## How It Works
PostgreSQL runs as a daemon process (typically on port 5432). When your Python application wants data, it opens a TCP network connection to Postgres, authenticates, and sends SQL commands as text. The Postgres server executes the query, reads the data from its highly optimized storage engine, and sends the binary results back over the network.

## Intuition
If SQLite is a personal filing cabinet in your office, PostgreSQL is a massive warehouse staffed by a hundred workers. It takes a little more effort to get into the warehouse (authentication, network connections), but it can process a hundred requests simultaneously without anyone bumping into each other.

## Technical Explanation
Postgres excels at concurrency using MVCC (Multi-Version Concurrency Control). This means readers do not block writers, and writers do not block readers. When you update a row, Postgres actually creates a new version of the row and marks the old one as expired, cleaning it up later. This prevents the database from locking up during heavy read/write loads.

## Example
A standard Postgres connection string looks like this:
`postgresql://db_user:my_secret_password@db.example.com:5432/my_database`

## Python Implementation
```python
# Note: This requires pip install psycopg2-binary
import psycopg2
import os

def connect_to_postgres():
    # Use environment variables for secrets!
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    
    try:
        # Establish connection
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Execute a query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Connected to: {db_version[0]}")
        
        # Close communication
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Unable to connect to the database: {e}")

if __name__ == "__main__":
    connect_to_postgres()
```

## What Happens Underneath
When `psycopg2.connect()` is called, Python performs a DNS lookup, opens a TCP socket to port 5432, performs a TLS handshake (if configured), and then speaks the PostgreSQL wire protocol to authenticate. Once authenticated, a dedicated backend process is spawned on the Postgres server to handle that specific connection's queries.

## Common Mistakes
- **Leaking Connections:** Forgetting to call `conn.close()`. Postgres has a maximum connection limit (often 100 by default). If you leak connections, your app will eventually crash with a "too many clients" error.
- **Not Using Connection Pooling:** Creating a new TCP connection for every single HTTP request is slow. Use connection poolers like `PgBouncer` or SQLAlchemy's built-in pool.
- **String Interpolation for SQL:** Using `f"SELECT * FROM users WHERE name = '{name}'"` leads directly to SQL Injection. ALWAYS use parameter binding provided by the driver.

## Security Considerations
- Never expose port 5432 to the public internet.
- Use TLS/SSL for the database connection if the DB server is on a different physical machine than your app server.
- Rotate database passwords regularly.

## Real-World Applications
- **Backend Systems:** Postgres is the default choice for Django and Ruby on Rails applications.
- **Geospatial Data:** The PostGIS extension makes Postgres the most powerful open-source database for geographic data.

## AI-Agent Connection
Many modern LLM applications use Postgres with the `pgvector` extension to store and search vector embeddings alongside standard relational data, acting as both a primary DB and a vector DB simultaneously.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Write a function that uses `psycopg2` to insert a user securely (preventing SQL injection) into a `users` table.

## Summary
PostgreSQL is a robust, concurrent, and highly extensible relational database. By moving from SQLite to Postgres, applications gain the ability to handle massive concurrency and complex data types over a network.

## What You Should Know Before Moving On
- The architectural difference between SQLite (embedded) and PostgreSQL (client/server).
- How to construct a Postgres connection string.
- Why connection management and pooling are necessary.
