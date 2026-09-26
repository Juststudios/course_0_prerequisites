import sqlite3

def setup_database():
    """Creates a simple file-based SQLite database for demonstration."""
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
