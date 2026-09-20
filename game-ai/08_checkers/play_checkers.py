"""
Checkers: Interactive Play & Automated AI Benchmark
===================================================
Supports:
  1. Headless AI Benchmarking: Automated tournaments validating engine mechanics,
     forced capture enforcement, and AI strategic dominance.
  2. Interactive CLI Play: Human vs Alpha-Beta AI with formatted board rendering.
"""

import sys
import argparse
import random
import time
from checkers import (
    CheckersState, EMPTY, RED_MAN, BLACK_MAN, RED_KING, BLACK_KING,
    PLAYER_RED, PLAYER_BLACK
)
from checkers_ai import get_best_move, evaluate_checkers


def format_move(move):
    """Format a move tuple into readable notation like (5,2)->(4,3)."""
    return "->".join(f"({r},{c})" for r, c in move)


def parse_human_move(input_str, legal_moves):
    """
    Parse human input into a legal move.
    Supports either index (e.g. '1') or coordinate notation (e.g. '5,2 to 4,3' or '5,2-4,3').
    """
    input_str = input_str.strip()
    # Try 1-based index
    if input_str.isdigit():
        idx = int(input_str) - 1
        if 0 <= idx < len(legal_moves):
            return legal_moves[idx]
        return None

    # Try coordinate matching
    cleaned = input_str.replace("to", "-").replace("->", "-").replace(" ", "")
    parts = cleaned.split("-")
    try:
        coords = []
        for p in parts:
            p = p.strip("()")
            r, c = p.split(",")
            coords.append((int(r), int(c)))
        candidate = tuple(coords)
        if candidate in legal_moves:
            return candidate
    except Exception:
        pass
    return None


def run_benchmark(num_games=3, ai_depth=3, max_turns=80, verbose=False):
    """
    Run an automated headless tournament between Alpha-Beta AI (Red)
    and Random Player (Black).
    """
    print("=" * 65)
    print("CHECKERS HEADLESS AI BENCHMARK: Alpha-Beta AI vs Random")
    print("=" * 65)
    print(f"Games: {num_games} | AI Search Depth: {ai_depth} | Max Plies: {max_turns}")

    ai_wins = 0
    random_wins = 0
    draws = 0
    total_moves_played = 0

    for game_idx in range(1, num_games + 1):
        state = CheckersState()
        ply = 0
        captures_count = 0
        multi_jump_count = 0

        start_time = time.time()
        while not state.is_terminal and ply < max_turns:
            legal = state.get_legal_moves()
            if not legal:
                break

            # Verify forced capture integrity:
            # If any move has length > 2 (jump), all legal moves MUST be jumps
            has_jumps = any(abs(m[1][0] - m[0][0]) == 2 for m in legal)
            if has_jumps:
                for m in legal:
                    assert abs(m[1][0] - m[0][0]) == 2, f"Forced capture violated! Found non-jump: {m}"

            if state.current_player == PLAYER_RED:
                move = get_best_move(state, depth=ai_depth)
            else:
                move = random.choice(legal)

            is_jump = (abs(move[1][0] - move[0][0]) == 2)
            if is_jump:
                captures_count += 1
                if len(move) > 2:
                    multi_jump_count += 1

            state = state.make_move(move)
            ply += 1

        elapsed = time.time() - start_time
        total_moves_played += ply
        pieces = state.count_pieces()

        if state.winner == PLAYER_RED:
            result = "AI (Red) WON"
            ai_wins += 1
        elif state.winner == PLAYER_BLACK:
            result = "Random (Black) WON"
            random_wins += 1
        else:
            result = "DRAW"
            draws += 1

        print(f"\nGame {game_idx}/{num_games}: {result} in {ply} plies ({elapsed:.2f}s)")
        print(f"  Captures: {captures_count} (Multi-jumps: {multi_jump_count})")
        print(f"  Final Pieces: Red Men={pieces['red_men']}, Kings={pieces['red_kings']} | "
              f"Black Men={pieces['black_men']}, Kings={pieces['black_kings']}")

        if verbose or game_idx == 1:
            print("  Final Board State:")
            for line in state.render().splitlines():
                print(f"    {line}")

    print("\n" + "=" * 65)
    print("BENCHMARK SUMMARY:")
    print(f"  AI (Red) Wins:     {ai_wins} / {num_games} ({ai_wins / num_games * 100:.1f}%)")
    print(f"  Random Wins:       {random_wins} / {num_games}")
    print(f"  Draws:             {draws} / {num_games}")
    print(f"  Avg Plies / Game:  {total_moves_played / num_games:.1f}")
    print("=" * 65)

    assert ai_wins + draws == num_games, "AI unexpectedly lost to Random agent!"
    return ai_wins, random_wins, draws


def play_interactive(human_color=PLAYER_RED, ai_depth=4):
    """Play an interactive game against Checkers AI."""
    print("=" * 65)
    print("WELCOME TO CHECKERS CLI")
    print("=" * 65)
    print("Rules: Forced captures are mandatory. Multi-jumps are executed in a single turn.")
    print("Move format: Enter the number from the legal moves list (e.g. '1')")
    print("             or coordinates like '5,2 to 4,3' or '5,0-3,2-1,4'.")
    print("=" * 65)

    state = CheckersState()

    while not state.is_terminal:
        print("\n" + state.render())

        legal_moves = state.get_legal_moves()
        if not legal_moves:
            break

        if state.current_player == human_color:
            print(f"\nYour turn! Legal moves ({len(legal_moves)}):")
            for idx, m in enumerate(legal_moves, 1):
                jump_tag = " [CAPTURE!]" if abs(m[1][0] - m[0][0]) == 2 else ""
                print(f"  {idx}. {format_move(m)}{jump_tag}")

            chosen_move = None
            while chosen_move is None:
                try:
                    user_inp = input("Enter your move (or 'q' to quit): ").strip()
                    if user_inp.lower() in ('q', 'quit'):
                        print("Game aborted.")
                        return
                    chosen_move = parse_human_move(user_inp, legal_moves)
                    if chosen_move is None:
                        print("Invalid move. Enter a valid number from the list above.")
                except (EOFError, KeyboardInterrupt):
                    print("\nGame exited.")
                    return
            state = state.make_move(chosen_move)
        else:
            print("\nAI is thinking...")
            t0 = time.time()
            ai_move = get_best_move(state, depth=ai_depth)
            dt = time.time() - t0
            print(f"AI chose: {format_move(ai_move)} in {dt:.2f}s")
            state = state.make_move(ai_move)

    print("\n" + "=" * 65)
    print("GAME OVER")
    print(state.render())
    if state.winner == human_color:
        print("Congratulations! You WON!")
    elif state.winner == 0:
        print("Game ended in a DRAW!")
    else:
        print("AI WON! Better luck next time!")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Checkers Game Engine & AI")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive human vs AI game")
    parser.add_argument("--games", type=int, default=3, help="Number of benchmark games to run")
    parser.add_argument("--depth", type=int, default=3, help="Search depth for Alpha-Beta AI")
    parser.add_argument("--verbose", action="store_true", help="Print verbose game logs")
    args = parser.parse_args()

    if args.interactive:
        play_interactive(human_color=PLAYER_RED, ai_depth=args.depth)
    else:
        run_benchmark(num_games=args.games, ai_depth=args.depth, verbose=args.verbose)
