"""
Reversi / Othello Capstone Game
===============================
Game AI Capstone Project: Interactive Pygame & Headless AI Engine

Provides:
- OthelloState: Complete 8x8 game engine with flips, pass handling, and terminal detection.
- Heuristic evaluation using Piece-Square Table (PST), mobility, and corner bonus.
- Minimax with Alpha-Beta pruning (`minimax_ab`).
- Headless simulation (`play_game(ai_depth=2)`).
- Pygame graphical interface (`main()` or `run_gui()`).
"""

import sys
import os
from pathlib import Path

# Add solutions directory to path if needed
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from solutions.reversi_solution import (
    OthelloState,
    PST,
    heuristic,
    minimax_ab,
    play_game,
    play_ai_vs_ai,
    run_gui,
    EMPTY,
    BLACK,
    WHITE,
    DIRECTIONS
)


def main():
    """Entry point: runs Pygame GUI if display is detected, otherwise headless demo."""
    if "--gui" in sys.argv:
        run_gui()
    elif not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        print("No graphical display detected. Executing headless demonstration...")
        winner, scores = play_game(ai_depth=2, verbose=True)
        print(f"Result: Winner={winner}, Final Scores={scores}")
    else:
        run_gui()


if __name__ == "__main__":
    main()
