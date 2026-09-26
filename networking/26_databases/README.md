# Databases

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
