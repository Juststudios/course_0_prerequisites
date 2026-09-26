# Note: This file serves as an educational reference. 
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
