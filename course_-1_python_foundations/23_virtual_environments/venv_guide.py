"""Module 23: Virtual Environments"""
# This module is mostly conceptual — run the shell commands below.
print("""
Creating a virtual environment:
  python3 -m venv .venv

Activating it:
  source .venv/bin/activate   (Linux/Mac)
  .venv\\Scripts\\activate      (Windows)

Installing packages:
  pip install httpx pydantic

Saving dependencies:
  pip freeze > requirements.txt

Installing from requirements.txt:
  pip install -r requirements.txt

Why this matters:
  Different projects need different package versions.
  Virtual environments keep them isolated.
""")
