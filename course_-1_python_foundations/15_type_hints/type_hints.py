"""
Module 15: Type Hints (Companion Entry Point)
==============================================
Forwards directly to the primary lesson implementation in typing_lesson.py.
"""
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import typing_lesson

if __name__ == "__main__":
    print("Executing Module 15 via type_hints.py wrapper -> typing_lesson.py")
