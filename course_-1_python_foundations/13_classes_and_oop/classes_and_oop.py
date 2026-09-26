"""
Module 13: Classes and Object-Oriented Programming (Companion Entry Point)
=========================================================================
Forwards directly to the primary lesson implementation in classes.py.
"""
import sys
from pathlib import Path

# Ensure local module is importable
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import classes

if __name__ == "__main__":
    print("Executing Module 13 via classes_and_oop.py wrapper -> classes.py")
