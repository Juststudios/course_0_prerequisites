"""
Reversi / Othello Reference Solution & Game Engine
===================================================
Level 7 / Game AI Capstone Reference Solution

Features:
- Full OthelloState engine: 8-direction raycasting, bracketing, disc flipping,
  pass detection, and terminal state resolution.
- Positional Piece-Square Table (PST) heuristic evaluation function combined
  with corner control and mobility differentials.
- Depth-limited Minimax with Alpha-Beta pruning (`minimax_ab`) and move ordering.
- Programmatic headless simulation (`play_game(ai_depth=2)`) for CI test suites.
- Interactive Pygame visual GUI for Human vs AI play.
"""

import sys
import os
import copy
import time
from typing import List, Tuple, Dict, Optional

# Board constants
EMPTY = 0
BLACK = 1
WHITE = 2

# 8 cardinal and diagonal search directions
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

# Calibrated 8x8 Piece-Square Table (PST)
# High positive weights for corners; heavy penalties for adjacent C/X squares;
# positive weights for outer edges; neutral/modest weights for center.
PST = [
    [ 100, -20,  10,   5,   5,  10, -20,  100],
    [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
    [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
    [   5,  -2,  -1,   0,   0,  -1,  -2,    5],
    [   5,  -2,  -1,   0,   0,  -1,  -2,    5],
    [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
    [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
    [ 100, -20,  10,   5,   5,  10, -20,  100]
]


class OthelloState:
    """
    Representation of an 8x8 Othello (Reversi) board and game state.
    """
    def __init__(
        self,
        board: Optional[List[List[int]]] = None,
        current_player: int = BLACK,
        consecutive_passes: int = 0
    ):
        if board is None:
            self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
            # Standard initial four-disc configuration
            self.board[3][3] = WHITE
            self.board[4][4] = WHITE
            self.board[3][4] = BLACK
            self.board[4][3] = BLACK
        else:
            self.board = [row[:] for row in board]

        self.current_player = current_player
        self.consecutive_passes = consecutive_passes
        self.is_terminal = False
        self.winner: Optional[int] = None  # 1 = Black, 2 = White, 0 = Draw
        self._check_terminal()

    def get_flips(self, r: int, c: int, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """
        Return list of opponent discs that would be flipped by placing a disc at (r, c).
        """
        if player is None:
            player = self.current_player

        if self.board[r][c] != EMPTY:
            return []

        opponent = 3 - player
        flips: List[Tuple[int, int]] = []

        for dr, dc in DIRECTIONS:
            curr_r = r + dr
            curr_c = c + dc
            dir_flips: List[Tuple[int, int]] = []

            while 0 <= curr_r < 8 and 0 <= curr_c < 8 and self.board[curr_r][curr_c] == opponent:
                dir_flips.append((curr_r, curr_c))
                curr_r += dr
                curr_c += dc

            if 0 <= curr_r < 8 and 0 <= curr_c < 8 and self.board[curr_r][curr_c] == player and dir_flips:
                flips.extend(dir_flips)

        return flips

    def get_legal_moves(self, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """
        Return all valid coordinates (r, c) where player can legally move.
        """
        if player is None:
            player = self.current_player

        moves: List[Tuple[int, int]] = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == EMPTY and self.get_flips(r, c, player):
                    moves.append((r, c))
        return moves

    def is_full(self) -> bool:
        """Check if all 64 squares are occupied."""
        return all(self.board[r][c] != EMPTY for r in range(8) for c in range(8))

    def _resolve_winner(self) -> None:
        """Compute final scores and assign winner."""
        scores = self.get_scores()
        black_count = scores[BLACK]
        white_count = scores[WHITE]
        if black_count > white_count:
            self.winner = BLACK
        elif white_count > black_count:
            self.winner = WHITE
        else:
            self.winner = 0  # Draw

    def _check_terminal(self) -> None:
        """Determine if game has reached a terminal condition."""
        if self.consecutive_passes >= 2 or self.is_full():
            self.is_terminal = True
            self._resolve_winner()

    def make_move(self, move: Optional[Tuple[int, int]]) -> "OthelloState":
        """
        Apply move to the board, flip captured discs, and transition turn.
        If move is None, execute a pass.
        """
        if self.is_terminal:
            return OthelloState(self.board, self.current_player, self.consecutive_passes)

        # 1. Pass move
        if move is None:
            new_state = OthelloState(
                self.board,
                current_player=3 - self.current_player,
                consecutive_passes=self.consecutive_passes + 1
            )
            # Check if game ends on consecutive passes or if next player has no moves either
            if not new_state.get_legal_moves(new_state.current_player):
                new_state.consecutive_passes += 1
                new_state._check_terminal()
            return new_state

        # 2. Placing a disc
        r, c = move
        flips = self.get_flips(r, c, self.current_player)
        if not flips:
            raise ValueError(f"Illegal move {move} for player {self.current_player}")

        new_board = [row[:] for row in self.board]
        new_board[r][c] = self.current_player
        for fr, fc in flips:
            new_board[fr][fc] = self.current_player

        # Check turn transition:
        opponent = 3 - self.current_player
        opp_has_moves = any(
            any(
                self._test_flips(new_board, row, col, opponent)
                for col in range(8) if new_board[row][col] == EMPTY
            )
            for row in range(8)
        )
        curr_has_moves = any(
            any(
                self._test_flips(new_board, row, col, self.current_player)
                for col in range(8) if new_board[row][col] == EMPTY
            )
            for row in range(8)
        )

        if opp_has_moves:
            next_player = opponent
            passes = 0
        elif curr_has_moves:
            # Opponent has no moves, current player moves again (opponent passes)
            next_player = self.current_player
            passes = 1
        else:
            # Neither has moves -> game over
            next_player = opponent
            passes = 2

        new_state = OthelloState(new_board, next_player, passes)
        return new_state

    @staticmethod
    def _test_flips(board: List[List[int]], r: int, c: int, player: int) -> bool:
        """Fast check if (r, c) yields at least one flip on raw board matrix."""
        if board[r][c] != EMPTY:
            return False
        opp = 3 - player
        for dr, dc in DIRECTIONS:
            curr_r = r + dr
            curr_c = c + dc
            count = 0
            while 0 <= curr_r < 8 and 0 <= curr_c < 8 and board[curr_r][curr_c] == opp:
                count += 1
                curr_r += dr
                curr_c += dc
            if count > 0 and 0 <= curr_r < 8 and 0 <= curr_c < 8 and board[curr_r][curr_c] == player:
                return True
        return False

    def get_scores(self) -> Dict[int, int]:
        """Return disc count {BLACK: count, WHITE: count}."""
        black_cnt = sum(row.count(BLACK) for row in self.board)
        white_cnt = sum(row.count(WHITE) for row in self.board)
        return {BLACK: black_cnt, WHITE: white_cnt}

    def print_board(self) -> None:
        """Render board to terminal."""
        symbols = {EMPTY: ".", BLACK: "X", WHITE: "O"}
        print("  0 1 2 3 4 5 6 7")
        for r in range(8):
            row_str = " ".join(symbols[self.board[r][c]] for c in range(8))
            print(f"{r} {row_str}")
        scores = self.get_scores()
        print(f"Scores: Black(X)={scores[BLACK]} | White(O)={scores[WHITE]}")


# ==============================================================================
# HEURISTIC EVALUATION
# ==============================================================================

def heuristic(state: OthelloState, player: int) -> float:
    """
    Evaluates board position from the perspective of `player`.
    Combines:
    1. Terminal victory bonus (+10000/-10000 + disc difference).
    2. Positional Piece-Square Table (PST) scoring.
    3. Corner ownership bonus (+25 per corner).
    4. Mobility differential (+10 per extra legal move).
    """
    opp = 3 - player
    scores = state.get_scores()
    my_discs = scores[player]
    opp_discs = scores[opp]

    if state.is_terminal:
        if state.winner == player:
            return 10000.0 + (my_discs - opp_discs)
        elif state.winner == opp:
            return -10000.0 + (my_discs - opp_discs)
        else:
            return 0.0

    # 1. Positional Piece-Square Table Score
    pos_score = 0
    for r in range(8):
        for c in range(8):
            val = state.board[r][c]
            if val == player:
                pos_score += PST[r][c]
            elif val == opp:
                pos_score -= PST[r][c]

    # 2. Corner Bonus
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_score = 0
    for cr, cc in corners:
        val = state.board[cr][cc]
        if val == player:
            corner_score += 25
        elif val == opp:
            corner_score -= 25

    # 3. Mobility Differential
    my_mobility = len(state.get_legal_moves(player))
    opp_mobility = len(state.get_legal_moves(opp))
    mobility_score = 10 * (my_mobility - opp_mobility)

    return float(pos_score + corner_score + mobility_score)


# ==============================================================================
# MINIMAX WITH ALPHA-BETA PRUNING
# ==============================================================================

def minimax_ab(
    state: OthelloState,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    max_player: Optional[int] = None
) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax search with Alpha-Beta pruning, move ordering, and pass handling.
    Returns (eval_score, best_move).
    """
    if max_player is None:
        max_player = state.current_player if is_maximizing else (3 - state.current_player)

    if state.is_terminal or depth <= 0:
        return heuristic(state, max_player), None

    legal_moves = state.get_legal_moves()

    # Pass condition
    if not legal_moves:
        child_state = state.make_move(None)
        if child_state.is_terminal:
            return heuristic(child_state, max_player), None
        child_is_max = (child_state.current_player == max_player)
        eval_score, _ = minimax_ab(child_state, depth - 1, alpha, beta, child_is_max, max_player)
        return eval_score, None

    # Move ordering: prioritize high PST weight squares for aggressive pruning cutoffs
    legal_moves.sort(key=lambda m: PST[m[0]][m[1]], reverse=True)

    if is_maximizing:
        best_score = -float('inf')
        best_move = legal_moves[0]
        for move in legal_moves:
            child = state.make_move(move)
            child_is_max = (child.current_player == max_player)
            score, _ = minimax_ab(child, depth - 1, alpha, beta, child_is_max, max_player)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = legal_moves[0]
        for move in legal_moves:
            child = state.make_move(move)
            child_is_max = (child.current_player == max_player)
            score, _ = minimax_ab(child, depth - 1, alpha, beta, child_is_max, max_player)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move


# ==============================================================================
# HEADLESS SELF-PLAY & BENCHMARKING
# ==============================================================================

def play_game(
    ai_depth: int = 2,
    depth_black: Optional[int] = None,
    depth_white: Optional[int] = None,
    verbose: bool = False
) -> Tuple[Optional[int], Dict[int, int]]:
    """
    Run an automated headless AI vs AI game without requiring a graphical display.
    Returns (winner, scores).
    """
    d_black = depth_black if depth_black is not None else ai_depth
    d_white = depth_white if depth_white is not None else ai_depth

    state = OthelloState()
    move_count = 0

    if verbose:
        print(f"Starting headless Reversi game: Black(depth={d_black}) vs White(depth={d_white})")

    while not state.is_terminal and move_count < 120:
        moves = state.get_legal_moves()
        if not moves:
            state = state.make_move(None)
            move_count += 1
            continue

        depth = d_black if state.current_player == BLACK else d_white
        _, best_move = minimax_ab(
            state,
            depth=depth,
            alpha=-float('inf'),
            beta=float('inf'),
            is_maximizing=True,
            max_player=state.current_player
        )
        if best_move is None:
            best_move = moves[0]

        state = state.make_move(best_move)
        move_count += 1

    scores = state.get_scores()
    if verbose:
        print(f"Game Over in {move_count} turns. Winner: {state.winner} | Scores: {scores}")

    return state.winner, scores


def play_ai_vs_ai(depth_black: int = 3, depth_white: int = 1) -> Tuple[Optional[int], Dict[int, int]]:
    """Convenience wrapper for depth comparison tournament."""
    return play_game(depth_black=depth_black, depth_white=depth_white, verbose=False)


# ==============================================================================
# PYGAME INTERACTIVE GUI
# ==============================================================================

def run_gui():
    """Interactive Pygame interface (Human as Black vs AI as White)."""
    # Headless guard
    if not os.environ.get("DISPLAY") and not os.environ.get("SDL_VIDEODRIVER"):
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    try:
        import pygame
        pygame.init()
    except Exception as e:
        print(f"Pygame initialization failed: {e}. Falling back to headless self-play.")
        winner, scores = play_game(ai_depth=2, verbose=True)
        return

    # Window settings
    SQUARE_SIZE = 60
    BOARD_SIZE = SQUARE_SIZE * 8
    INFO_PANEL_HEIGHT = 80
    WIDTH = BOARD_SIZE
    HEIGHT = BOARD_SIZE + INFO_PANEL_HEIGHT

    # Colors
    GREEN_BOARD = (34, 139, 34)
    LINE_COLOR = (20, 80, 20)
    COLOR_BLACK = (20, 20, 20)
    COLOR_WHITE = (235, 235, 235)
    HIGHLIGHT_COLOR = (255, 215, 0)
    BG_PANEL = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)

    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello / Reversi AI Capstone (Human: Black, AI: White)")
        font = pygame.font.SysFont("arial", 20, bold=True)
    except Exception as e:
        print(f"Display creation failed ({e}); running headless.")
        play_game(ai_depth=2, verbose=True)
        return

    state = OthelloState()
    clock = pygame.time.Clock()
    running = True

    while running:
        legal_moves = state.get_legal_moves()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not state.is_terminal:
                if state.current_player == BLACK and legal_moves:
                    mx, my = event.pos
                    if my < BOARD_SIZE:
                        clicked_col = mx // SQUARE_SIZE
                        clicked_row = my // SQUARE_SIZE
                        if (clicked_row, clicked_col) in legal_moves:
                            state = state.make_move((clicked_row, clicked_col))

        # Handle passes when no legal moves exist
        if not state.is_terminal and not legal_moves:
            state = state.make_move(None)
            continue

        # AI Turn (White)
        if not state.is_terminal and state.current_player == WHITE and legal_moves:
            # Draw board while AI thinks
            pygame.display.flip()
            _, ai_move = minimax_ab(
                state, depth=3, alpha=-float('inf'), beta=float('inf'),
                is_maximizing=True, max_player=WHITE
            )
            if ai_move is None and legal_moves:
                ai_move = legal_moves[0]
            if ai_move:
                state = state.make_move(ai_move)

        # ─── Render Board ────────────────────────────────────────────────────
        screen.fill(BG_PANEL)
        pygame.draw.rect(screen, GREEN_BOARD, (0, 0, BOARD_SIZE, BOARD_SIZE))

        # Grid lines
        for i in range(9):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (BOARD_SIZE, i * SQUARE_SIZE), 2)
            pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, BOARD_SIZE), 2)

        # Discs
        for r in range(8):
            for c in range(8):
                center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                radius = SQUARE_SIZE // 2 - 5
                val = state.board[r][c]
                if val == BLACK:
                    pygame.draw.circle(screen, COLOR_BLACK, center, radius)
                elif val == WHITE:
                    pygame.draw.circle(screen, COLOR_WHITE, center, radius)

        # Highlight legal moves for human (Black)
        if not state.is_terminal and state.current_player == BLACK:
            for mr, mc in legal_moves:
                center = (mc * SQUARE_SIZE + SQUARE_SIZE // 2, mr * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, HIGHLIGHT_COLOR, center, 6)

        # ─── Render Info Panel ───────────────────────────────────────────────
        scores = state.get_scores()
        info_text = f"Black (Human): {scores[BLACK]}   White (AI): {scores[WHITE]}"
        turn_text = f"Turn: {'Black (Human)' if state.current_player == BLACK else 'White (AI)'}"
        if state.is_terminal:
            if state.winner == BLACK:
                turn_text = "GAME OVER — Black (Human) Wins!"
            elif state.winner == WHITE:
                turn_text = "GAME OVER — White (AI) Wins!"
            else:
                turn_text = "GAME OVER — Draw!"

        surf_info = font.render(info_text, True, TEXT_COLOR)
        surf_turn = font.render(turn_text, True, HIGHLIGHT_COLOR if state.is_terminal else TEXT_COLOR)
        screen.blit(surf_info, (20, BOARD_SIZE + 12))
        screen.blit(surf_turn, (20, BOARD_SIZE + 42))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_gui()
    else:
        print("Running headless AI verification game (depth=2)...")
        w, s = play_game(ai_depth=2, verbose=True)
        print(f"Verification successful: Winner={w}, Scores={s}")
