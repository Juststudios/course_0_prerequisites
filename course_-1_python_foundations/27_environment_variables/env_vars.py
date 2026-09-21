"""Module 27: Environment Variables"""
import os

# Environment variables are key-value pairs set in the shell.
# They are the standard way to pass secrets to programs.

api_key = os.environ.get("OPENAI_API_KEY", "not-set")
print(f"API key: {api_key!r}")

# Why NOT hardcode secrets:
# BAD:  api_key = "sk-abc123"   ← visible in git history, logs, etc.
# GOOD: api_key = os.environ.get("OPENAI_API_KEY")

# Setting an env var (temporary, current process only):
os.environ["DEMO_KEY"] = "demo_value"
print(f"Demo key: {os.environ.get('DEMO_KEY')}")

# In production: use a .env file with python-dotenv (see Course 0 Module 05).
print("\nEnvironment variables lesson complete.")
