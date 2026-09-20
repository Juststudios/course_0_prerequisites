"""
MCTS: Tournament Benchmarks & Interactive Play
==============================================
Demonstrates and validates Monte Carlo Tree Search across two classic games:
  1. Tic-Tac-Toe:
     - MCTS vs Random: Validates strategic dominance (win+draw rate >= 95%)
     - MCTS vs Perfect Minimax: Validates convergence to optimal play (draws against Minimax)
  2. Connect Four:
     - MCTS vs Random: Demonstrates deep planning in high-branching factor environments
"""

import sys
import random
import time
from pathlib import Path

# Add sibling game directories to sys.path
GAME_AI_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GAME_AI_ROOT / "03_tic_tac_toe"))
sys.path.insert(0, str(GAME_AI_ROOT / "04_minimax"))
sys.path.insert(0, str(GAME_AI_ROOT / "07_connect_four"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tic_tac_toe import TicTacToeState
from connect_four import ConnectFourState
from mcts import MCTS
import minimax as minimax_module


def render_ttt_board(board):
    symbols = {0: ' ', 1: 'X', 2: 'O'}
    lines = []
    for r in range(3):
        row = [symbols[board[r * 3 + c]] for c in range(3)]
        lines.append(" " + " | ".join(row) + " ")
        if r < 2:
            lines.append("---+---+---")
    return "\n".join(lines)


def run_tictactoe_vs_random(num_games=20, num_simulations=300):
    """Benchmark MCTS vs Random on Tic-Tac-Toe."""
    print("=" * 65)
    print(f"BENCHMARK 1: Tic-Tac-Toe — MCTS vs Random ({num_games} games)")
    print(f"MCTS Simulations per move: {num_simulations}")
    print("=" * 65)

    mcts = MCTS()
    mcts_wins = 0
    random_wins = 0
    draws = 0

    for g in range(1, num_games + 1):
        # Alternate who plays first
        mcts_player = 1 if g % 2 == 1 else 2
        state = TicTacToeState()

        while not state.is_terminal:
            if state.current_player == mcts_player:
                move = mcts.get_best_move(state, num_simulations=num_simulations)
            else:
                move = random.choice(state.get_legal_moves())
            state = state.make_move(move)

        if state.winner == mcts_player:
            mcts_wins += 1
        elif state.winner == 0:
            draws += 1
        else:
            random_wins += 1

    win_draw_rate = (mcts_wins + draws) / num_games * 100
    print(f"Results over {num_games} games:")
    print(f"  MCTS Wins:     {mcts_wins} ({mcts_wins / num_games * 100:.1f}%)")
    print(f"  Random Wins:   {random_wins} ({random_wins / num_games * 100:.1f}%)")
    print(f"  Draws:         {draws} ({draws / num_games * 100:.1f}%)")
    print(f"  MCTS Win+Draw: {win_draw_rate:.1f}%")
    print("=" * 65)

    assert win_draw_rate >= 95.0, f"MCTS performance below threshold: {win_draw_rate}%"
    return mcts_wins, random_wins, draws


def run_tictactoe_vs_minimax(num_games=10, num_simulations=600):
    """Benchmark MCTS vs Perfect Minimax on Tic-Tac-Toe."""
    random.seed(42)
    print("\n" + "=" * 65)
    print(f"BENCHMARK 2: Tic-Tac-Toe — MCTS vs Perfect Minimax ({num_games} games)")
    print(f"MCTS Simulations per move: {num_simulations}")
    print("=" * 65)

    mcts = MCTS()
    mcts_wins = 0
    minimax_wins = 0
    draws = 0

    for g in range(1, num_games + 1):
        mcts_player = 1 if g % 2 == 1 else 2
        state = TicTacToeState()

        while not state.is_terminal:
            if state.current_player == mcts_player:
                move = mcts.get_best_move(state, num_simulations=num_simulations)
            else:
                move = minimax_module.get_best_move(state)
            state = state.make_move(move)

        if state.winner == mcts_player:
            mcts_wins += 1
        elif state.winner == 0:
            draws += 1
        else:
            minimax_wins += 1

    print(f"Results over {num_games} games:")
    print(f"  MCTS Wins:     {mcts_wins}")
    print(f"  Minimax Wins:  {minimax_wins}")
    print(f"  Draws:         {draws} ({draws / num_games * 100:.1f}%)")
    print("=" * 65)

    # In solved game Tic-Tac-Toe with perfect play, optimal outcome is a Draw.
    # Minimax cannot lose. MCTS with sufficient simulations should draw almost always.
    mcts_losses = minimax_wins
    assert mcts_losses <= 2, f"MCTS failed to consistently hold Minimax to a draw! Losses: {mcts_losses}"
    return mcts_wins, minimax_wins, draws


def run_connect_four_vs_random(num_games=5, num_simulations=400):
    """Benchmark MCTS vs Random on Connect Four (6x7 grid)."""
    print("\n" + "=" * 65)
    print(f"BENCHMARK 3: Connect Four — MCTS vs Random ({num_games} games)")
    print(f"MCTS Simulations per move: {num_simulations}")
    print("=" * 65)

    mcts = MCTS()
    mcts_wins = 0
    random_wins = 0
    draws = 0

    for g in range(1, num_games + 1):
        mcts_player = 1 if g % 2 == 1 else 2
        state = ConnectFourState()
        plies = 0
        t0 = time.time()

        while not state.is_terminal:
            if state.current_player == mcts_player:
                move = mcts.get_best_move(state, num_simulations=num_simulations)
            else:
                move = random.choice(state.get_legal_moves())
            state = state.make_move(move)
            plies += 1

        dt = time.time() - t0
        if state.winner == mcts_player:
            res = "MCTS WON"
            mcts_wins += 1
        elif state.winner == 0:
            res = "DRAW"
            draws += 1
        else:
            res = "Random WON"
            random_wins += 1

        print(f"Game {g}/{num_games}: {res} in {plies} plies ({dt:.2f}s)")

    win_rate = mcts_wins / num_games * 100
    print(f"\nConnect Four Results over {num_games} games:")
    print(f"  MCTS Wins:     {mcts_wins} ({win_rate:.1f}%)")
    print(f"  Random Wins:   {random_wins}")
    print(f"  Draws:         {draws}")
    print("=" * 65)

    assert win_rate >= 80.0, f"MCTS Connect Four win rate ({win_rate}%) was below expected benchmark."
    return mcts_wins, random_wins, draws


if __name__ == "__main__":
    print("=" * 65)
    print("MONTE CARLO TREE SEARCH — VERIFICATION SUITE")
    print("=" * 65)

    # 1. Tic-Tac-Toe vs Random (fast, 20 games)
    run_tictactoe_vs_random(num_games=20, num_simulations=300)

    # 2. Tic-Tac-Toe vs Perfect Minimax (10 games)
    run_tictactoe_vs_minimax(num_games=10, num_simulations=600)

    # 3. Connect Four vs Random (5 games)
    run_connect_four_vs_random(num_games=5, num_simulations=300)

    print("\n" + "=" * 65)
    print("ALL MCTS BENCHMARK TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 65)
