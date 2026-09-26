import os

def create_module(module_dir, readme, exercises, solutions, impl_name, impl):
    os.makedirs(module_dir, exist_ok=True)
    with open(os.path.join(module_dir, "README.md"), "w") as f:
        f.write(readme)
    with open(os.path.join(module_dir, "exercises.py"), "w") as f:
        f.write(exercises)
    with open(os.path.join(module_dir, "solutions.py"), "w") as f:
        f.write(solutions)
    with open(os.path.join(module_dir, impl_name), "w") as f:
        f.write(impl)

# ================= MODULE 26 =================
mod26_dir = "/home/settings/Documents/pearl/networking/26_databases"

mod26_readme = """# Databases

## What You Will Learn
In this module, you will learn the foundational concepts of databases. You will understand why we use databases instead of just writing to files, the difference between relational (SQL) and non-relational (NoSQL) databases, and the core principles of data persistence.

## Prerequisites
- Basic understanding of data structures (lists, dictionaries).
- Familiarity with file I/O operations (reading/writing files).

## Key Terminology
- **Database (DB):** An organized collection of structured information, or data, typically stored electronically in a computer system.
- **DBMS (Database Management System):** The software that interacts with end users, applications, and the database itself to capture and analyze the data (e.g., MySQL, MongoDB).
- **Relational Database:** A type of database that stores and provides access to data points that are related to one another (using tables, rows, and columns).
- **ACID Transactions:** A set of properties (Atomicity, Consistency, Isolation, Durability) that guarantee database transactions are processed reliably.
- **Query:** A request for data or information from a database.

## The Problem
If you store application data in a plain text file or a JSON file, you will quickly run into problems as your application grows. Multiple users trying to write to the file at the same time will corrupt it. Searching through a massive file to find one specific record is incredibly slow. What happens if the server crashes while writing to the file? You lose data.

## How It Works
A Database Management System (DBMS) solves these problems. It manages the physical storage on the hard drive, uses sophisticated algorithms (like B-Trees) to index data for instant retrieval, and implements locks and transaction logs to handle concurrent access and prevent data loss during crashes.

## Intuition
Storing data in a file is like tossing receipts into a shoebox. It works when you have a few, but when tax season comes, finding one specific receipt is a nightmare. A database is like an expert filing cabinet system managed by a hyper-efficient librarian. When you need a receipt, you don't look through the cabinet yourself; you ask the librarian (via a query), who uses their indexing system to hand it to you instantly.

## Technical Explanation
Databases are broadly categorized into:
1. **Relational (SQL):** Data is organized into tables (relations). Schemas are strictly defined. Examples: PostgreSQL, MySQL, SQLite. Excellent for highly structured data where relationships matter (e.g., users and their orders).
2. **Non-Relational (NoSQL):** Data is stored in flexible formats like JSON documents, key-value pairs, or graphs. Examples: MongoDB, Redis, Cassandra. Excellent for unstructured data, rapid prototyping, or massive scale.

## Example
If you want to find all users over the age of 18:
- In a flat file: You must read every line, parse it, check the age, and keep a running list.
- In a SQL database: You write `SELECT * FROM users WHERE age > 18;`. The DB engine figures out the fastest way to get that data using indexes.

## Python Implementation
```python
import sqlite3

# SQLite is a simple, file-based relational database built into Python
def demo_sqlite():
    # Connect to an in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create a table
    cursor.execute('''
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)
    ''')
    
    # Insert data
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 17)")
    
    # Query data
    cursor.execute("SELECT name FROM users WHERE age > 18")
    adults = cursor.fetchall()
    
    print("Adults:", adults)
    
    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    demo_sqlite()
```

## What Happens Underneath
When you execute a query, the DBMS parses your SQL string, creates an execution plan, and determines whether it can use an index or if it must do a "full table scan" (reading every row on disk). Data is read from the disk into memory buffers, manipulated, and then the results are returned over a network socket to your application.

## Common Mistakes
- **Storing files in the database:** Do not store large images or videos in the DB (BLOBs). Store them in object storage (like AWS S3) and store the URL in the database.
- **N+1 Query Problem:** Running a query in a loop (e.g., fetching a user, then querying for their orders in a loop) instead of joining the tables.
- **No Backups:** A database is a single point of failure. Without automated backups, a corrupted disk means the end of your business.

## Security Considerations
- Ensure the database is not accessible from the public internet; it should only be accessible from your application servers within a private network (VPC).
- Use least-privilege principles: the application should connect with a user that only has permissions to read/write specific tables, not drop the entire database.

## Real-World Applications
- **E-commerce:** Relational databases handle inventory, users, and transactions to ensure exact consistency.
- **Caching:** In-memory databases like Redis are used to store temporary, frequently accessed data to speed up web responses.

## AI-Agent Connection
AI agents need persistent memory to remember user preferences or past conversations. A database allows the agent to recall this context efficiently. Furthermore, "Vector Databases" (like Pinecone or Milvus) are a special type of database optimized for storing and searching AI embeddings.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Write a Python script using `sqlite3` that creates a table of `books`, inserts 3 books, and then updates the title of one specific book using its ID.

## Summary
Databases are the bedrock of persistent applications. They provide safety, speed, and concurrency that plain files cannot. Choosing the right database (SQL vs NoSQL) depends on your data's structure and scaling requirements.

## What You Should Know Before Moving On
- Why a database is superior to flat files for application data.
- The high-level difference between SQL and NoSQL.
- What a DBMS is.
"""

mod26_ex = """# Module 26: Databases - Exercises

# Tier 1: Recall
# 1. What does ACID stand for in the context of databases?
# TODO: Assign the string value to the variable.
acid_meaning = ""

# 2. SQLite is an example of a NoSQL database. (True/False)
# TODO: Assign a boolean.
is_sqlite_nosql = None

# Tier 2: Modify
import sqlite3

def get_db_version():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # TODO: Modify the query to select the sqlite version. 
    # Hint: The query string is "SELECT sqlite_version();"
    query = ""
    cursor.execute(query)
    version = cursor.fetchone()[0]
    conn.close()
    return version

# Tier 3: Build
def create_and_insert():
    # TODO: Connect to an in-memory sqlite database.
    # Create a table called 'products' with columns 'id' (INTEGER PRIMARY KEY) and 'price' (REAL).
    # Insert a product with a price of 19.99.
    # Return the connection object.
    pass

# Tier 4: Debug
def fetch_user(user_id):
    # TODO: This code has a syntax error in the SQL string. Fix it.
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    # Buggy code:
    cursor.execute(f"SELECT * FROM users WHERE id == {user_id}")
    result = cursor.fetchone()
    conn.close()
    return result
"""

mod26_sol = """# Module 26: Databases - Solutions

# Tier 1: Recall
acid_meaning = "Atomicity, Consistency, Isolation, Durability"
is_sqlite_nosql = False

# Tier 2: Modify
import sqlite3

def get_db_version():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = "SELECT sqlite_version();"
    cursor.execute(query)
    version = cursor.fetchone()[0]
    conn.close()
    return version

# Tier 3: Build
def create_and_insert():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, price REAL)")
    cursor.execute("INSERT INTO products (price) VALUES (19.99)")
    conn.commit()
    return conn

# Tier 4: Debug
def fetch_user(user_id):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    # Fix: SQL uses a single '=' for equality, not '==' like Python
    # Also, better to use parameterized queries
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result
"""

mod26_impl = """import sqlite3

def setup_database():
    \"\"\"Creates a simple file-based SQLite database for demonstration.\"\"\"
    # Connects to a file, creating it if it doesn't exist
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    cursor.execute("INSERT INTO messages (sender, content) VALUES ('Alice', 'Hello, World!')")
    
    # Save (commit) the changes
    conn.commit()
    
    # Retrieve data
    cursor.execute("SELECT * FROM messages")
    print("Messages in DB:", cursor.fetchall())
    
    conn.close()

if __name__ == "__main__":
    setup_database()
"""

create_module(mod26_dir, mod26_readme, mod26_ex, mod26_sol, "sqlite_demo.py", mod26_impl)


# ================= MODULE 27 =================
mod27_dir = "/home/settings/Documents/pearl/networking/27_postgresql"

mod27_readme = """# PostgreSQL

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
"""

mod27_ex = """# Module 27: PostgreSQL - Exercises

# Tier 1: Recall
# 1. What is the default port for PostgreSQL?
# TODO: Assign the integer value.
postgres_default_port = 0

# 2. What does MVCC stand for?
# TODO: Assign the string value.
mvcc_meaning = ""

# Tier 2: Modify
def build_connection_string(user, password, host, port, dbname):
    # TODO: Modify this function to return a correctly formatted PostgreSQL connection URI.
    # Format: postgresql://user:password@host:port/dbname
    pass

# Tier 3: Build
# (Conceptual build, assuming psycopg2 is not installed in the testing environment)
def safe_insert_query():
    # TODO: Write the EXACT SQL string with psycopg2 parameter placeholders (%s)
    # to insert a name and email into a 'users' table.
    # Return the string.
    pass

# Tier 4: Debug
def process_data(conn):
    # TODO: This function opens a cursor but fails to close it if an exception occurs.
    # Fix the code using a try/finally block.
    
    cursor = conn.cursor()
    # Assume this might raise an error
    cursor.execute("SELECT * FROM some_table")
    data = cursor.fetchall()
    cursor.close()
    return data
"""

mod27_sol = """# Module 27: PostgreSQL - Solutions

# Tier 1: Recall
postgres_default_port = 5432
mvcc_meaning = "Multi-Version Concurrency Control"

# Tier 2: Modify
def build_connection_string(user, password, host, port, dbname):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Tier 3: Build
def safe_insert_query():
    return "INSERT INTO users (name, email) VALUES (%s, %s);"

# Tier 4: Debug
def process_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM some_table")
        data = cursor.fetchall()
        return data
    finally:
        cursor.close() # Ensures the cursor is always closed
"""

mod27_impl = """# Note: This file serves as an educational reference. 
# It requires `psycopg2` and a running PostgreSQL instance to execute successfully.

import os

# Stubbing psycopg2 for environments where it isn't installed
try:
    import psycopg2
except ImportError:
    class psycopg2:
        @staticmethod
        def connect(*args, **kwargs):
            raise NotImplementedError("psycopg2 is not installed.")

def execute_transaction():
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    
    try:
        # 1. Connect
        conn = psycopg2.connect(DATABASE_URL)
        
        # 2. Create cursor
        cursor = conn.cursor()
        
        # 3. Execute commands inside a transaction
        try:
            # The python driver automatically starts a transaction
            cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = %s", (1,))
            cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = %s", (2,))
            
            # Commit the transaction (make it permanent)
            conn.commit()
            print("Transaction successful.")
            
        except Exception as e:
            # If anything goes wrong, rollback all changes
            conn.rollback()
            print("Transaction failed, rolling back.", e)
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    print("Review the code in postgres_example.py to see how transactions are handled.")
"""

create_module(mod27_dir, mod27_readme, mod27_ex, mod27_sol, "postgres_example.py", mod27_impl)


# ================= MODULE 28 =================
mod28_dir = "/home/settings/Documents/pearl/networking/28_database_and_api"

mod28_readme = """# Database and API Integration

## What You Will Learn
In this module, you will learn how to integrate a database into an API backend. You will learn the architectural pattern of combining HTTP routing with database operations, how to manage database connections in a web server, and the basics of ORMs (Object-Relational Mappers).

## Prerequisites
- Completion of Module 27: PostgreSQL.
- Understanding of HTTP servers and frameworks (like Flask or FastAPI).

## Key Terminology
- **ORM (Object-Relational Mapper):** A tool that allows you to interact with a relational database using object-oriented code instead of raw SQL (e.g., SQLAlchemy, Django ORM).
- **CRUD:** Create, Read, Update, Delete. The four basic operations for persistent storage, which map cleanly to HTTP methods (POST, GET, PUT, DELETE).
- **Connection Pool:** A cache of database connections maintained so that connections can be reused when future requests to the database are required.
- **Dependency Injection:** A design pattern used heavily in modern frameworks (like FastAPI) to provide the database connection to the route handler.

## The Problem
A database on its own is inaccessible to the outside world (for good security reasons). An API without a database has amnesia—it forgets everything when it restarts. To build a useful web application, you must connect the two: the API serves as the gatekeeper and translator, receiving HTTP requests from clients and translating them into SQL queries for the database.

## How It Works
When an HTTP request hits the API:
1. The web framework routes the request to a specific function.
2. The function checks out a database connection from the Connection Pool.
3. The function uses an ORM or raw SQL to execute a CRUD operation based on the request body/parameters.
4. The database returns the data.
5. The API formats the data as JSON and sends the HTTP response back to the client.
6. The database connection is returned to the pool.

## Intuition
Think of a restaurant. The Database is the kitchen/pantry where all the food (data) is stored. The API is the waiter. Customers (clients) cannot go into the kitchen. They hand their orders (HTTP requests) to the waiter, who goes to the kitchen, gets the food (SQL query), plates it nicely (JSON formatting), and brings it back to the customer's table.

## Technical Explanation
In modern Python APIs (like FastAPI), integrating a database usually involves SQLAlchemy (an ORM). 
Instead of writing `SELECT * FROM users;`, you write `session.query(User).all()`. The ORM translates the Python code into SQL.
Because opening a TCP connection to Postgres takes time, web servers use connection pooling. When the server starts, it opens 10-20 connections and keeps them open. Route handlers borrow a connection for a few milliseconds to run their query, then return it.

## Example
Mapping HTTP methods to DB operations (CRUD):
- `POST /users` -> `INSERT INTO users...`
- `GET /users/1` -> `SELECT * FROM users WHERE id=1`
- `PUT /users/1` -> `UPDATE users SET...`
- `DELETE /users/1` -> `DELETE FROM users WHERE id=1`

## Python Implementation
```python
# A conceptual example combining a web framework and a database
from dataclasses import dataclass
import sqlite3

# Dummy web framework decorators
class MockApp:
    def get(self, path): return lambda f: f
    def post(self, path): return lambda f: f

app = MockApp()

def get_db_connection():
    # In production, this would be a connection pool
    conn = sqlite3.connect('api.db')
    conn.row_factory = sqlite3.Row # Returns dict-like rows
    return conn

@app.get("/users/{user_id}")
def read_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        return {"error": "Not Found"}, 404
        
    return dict(user)

@app.post("/users")
def create_user(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {"id": new_id, "name": name}, 201
```

## What Happens Underneath
1. **Network Layer:** Client sends HTTP POST over TCP.
2. **Web Server:** Gunicorn/Uvicorn parses HTTP bytes into Python objects.
3. **Application Logic:** Your function executes.
4. **Database Driver:** Serializes the SQL query and parameters into the PostgreSQL wire protocol over another TCP connection.
5. **Database Server:** Executes the write, syncs to disk (fsync).
6. **Return Trip:** Data flows back up the stack, ultimately serialized into JSON bytes sent over the HTTP TCP socket.

## Common Mistakes
- **Doing heavy computation while holding a DB connection:** Retrieve the data, release the connection back to the pool, THEN do your heavy math.
- **N+1 Queries in APIs:** Designing an API endpoint that loops through database queries, causing extreme latency.
- **Returning DB Models directly:** Always map DB rows to specific API schemas (DTOs). Don't accidentally expose password hashes because you serialized the whole User table row.

## Security Considerations
- Validate all incoming API data BEFORE sending it to the database to prevent SQL injection and logic errors.
- Never expose internal database IDs if they can be guessed (consider UUIDs).
- Ensure your API handles database connection failures gracefully (returning a 503 Service Unavailable instead of crashing).

## Real-World Applications
- **RESTful APIs:** The backbone of the modern web, serving React/Vue frontends and mobile apps.
- **Microservices:** Each microservice typically has its own API and its own separate database to maintain loose coupling.

## AI-Agent Connection
When building an AI agent that takes actions, the tools you provide to the LLM are usually API endpoints. The LLM decides to call `POST /orders`, and your API executes the database insertion. The API enforces the business rules so the LLM cannot corrupt the database.

## Exercises
Complete the exercises in `exercises.py`.

## Challenge
Write a small script using `sqlite3` and Python's built-in `http.server` that serves a GET endpoint `/items` returning a JSON list of items from the database.

## Summary
Combining APIs and databases allows you to build persistent, secure, and useful web services. By mapping HTTP verbs to CRUD operations and utilizing connection pooling and ORMs, you bridge the gap between network clients and persistent storage.

## What You Should Know Before Moving On
- What CRUD stands for and how it maps to HTTP methods.
- The role of an ORM.
- Why connection pooling is critical for web APIs.
"""

mod28_ex = """# Module 28: Database and API - Exercises

# Tier 1: Recall
# 1. What does ORM stand for?
# TODO: Assign the string value.
orm_meaning = ""

# 2. Which HTTP method is conventionally used for the 'Update' operation in CRUD?
# TODO: Assign the string value.
update_http_method = ""

# Tier 2: Modify
def get_user_data(user_id):
    # TODO: This mock API handler returns the entire database row.
    # Modify it to only return the 'id' and 'username', explicitly EXCLUDING the 'password_hash'.
    
    db_row = {"id": 1, "username": "admin", "password_hash": "bcrypt_xyz123", "is_active": True}
    return db_row

# Tier 3: Build
def map_crud_to_http():
    # TODO: Return a dictionary mapping the 4 CRUD operations to their standard HTTP methods.
    # Example format: {"Create": "POST", ...}
    pass

# Tier 4: Debug
def handle_request(db_pool):
    # TODO: This handler checks out a connection but crashes before returning it if there's an error.
    # Fix it using a try/finally block so the connection is always released.
    
    conn = db_pool.get_connection()
    # Buggy code:
    data = run_dangerous_query(conn) # This might throw an exception!
    db_pool.release(conn)
    return data

def run_dangerous_query(conn):
    raise ValueError("DB Crash!")
"""

mod28_sol = """# Module 28: Database and API - Solutions

# Tier 1: Recall
orm_meaning = "Object-Relational Mapper"
update_http_method = "PUT" # (or PATCH)

# Tier 2: Modify
def get_user_data(user_id):
    db_row = {"id": 1, "username": "admin", "password_hash": "bcrypt_xyz123", "is_active": True}
    # Fix: Selectively build the response dictionary (DTO)
    return {
        "id": db_row["id"],
        "username": db_row["username"]
    }

# Tier 3: Build
def map_crud_to_http():
    return {
        "Create": "POST",
        "Read": "GET",
        "Update": "PUT", # or PATCH
        "Delete": "DELETE"
    }

# Tier 4: Debug
def handle_request(db_pool):
    conn = db_pool.get_connection()
    try:
        data = run_dangerous_query(conn)
        return data
    finally:
        # Fix: Ensure the connection is released back to the pool even if an error occurs
        db_pool.release(conn)

def run_dangerous_query(conn):
    raise ValueError("DB Crash!")
"""

mod28_impl = """import sqlite3
import json

def init_db():
    conn = sqlite3.connect('todo_api.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Mocking a simple API layer
class TodoAPI:
    def __init__(self):
        init_db()
        
    def _get_conn(self):
        conn = sqlite3.connect('todo_api.db')
        conn.row_factory = sqlite3.Row
        return conn

    # POST /todos
    def create_todo(self, request_body: str):
        data = json.loads(request_body)
        task = data.get("task")
        
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return {"status": 201, "body": {"id": new_id, "task": task, "completed": False}}

    # GET /todos
    def get_todos(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        conn.close()
        
        todos = [dict(row) for row in rows]
        # SQLite stores booleans as 0/1, convert back for the API
        for t in todos:
            t['completed'] = bool(t['completed'])
            
        return {"status": 200, "body": todos}

if __name__ == "__main__":
    api = TodoAPI()
    print("API Initialized.")
    
    print("\\nSimulating: POST /todos")
    resp1 = api.create_todo('{"task": "Learn API Integration"}')
    print(resp1)
    
    print("\\nSimulating: GET /todos")
    resp2 = api.get_todos()
    print(resp2)
"""

create_module(mod28_dir, mod28_readme, mod28_ex, mod28_sol, "api_db_integration.py", mod28_impl)

print("Modules 26, 27, and 28 generated successfully.")
