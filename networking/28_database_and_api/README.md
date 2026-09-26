# Database and API Integration

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
