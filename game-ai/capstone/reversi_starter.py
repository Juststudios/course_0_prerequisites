"""
Othello (Reversi) Engine, AI & Playable UI
===========================================
Completed Game AI Capstone Implementation:
1. THE ENGINE: Full OthelloState with 8-direction raycasting, bracketing,
   disc flipping, consecutive pass handling, and terminal detection.
2. THE AI: Heuristic evaluation function using Piece-Square Table (PST),
   mobility differential, and corner capture weights.
   Minimax algorithm with Alpha-Beta pruning (`minimax_ab`).
3. THE UI: Pygame interactive interface (Human as Black vs AI as White)
   with fallback to headless play (`play_game(ai_depth=2)`).
"""

import copy
import os
import sys
import time
from typing import List, Tuple, Dict, Optional

# Board constants
EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1)
]

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


# ==============================================================================
# 1. THE ENGINE
# ==============================================================================

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
            # 8x8 board. 0=Empty, 1=Black, 2=White
            self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
            # Standard initial position
            self.board[3][3] = WHITE
            self.board[4][4] = WHITE
            self.board[3][4] = BLACK
            self.board[4][3] = BLACK
        else:
            self.board = [row[:] for row in board]

        self.current_player = current_player
        self.consecutive_passes = consecutive_passes
        self.is_terminal = False
        self.winner: Optional[int] = None
        self._check_terminal()

    def get_flips(self, r: int, c: int, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """Return list of opponent discs flipped by placing piece at (r, c)."""
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
        """Return list of (row, col) coordinates of all legal moves."""
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
        """Compute final disc score and determine winner."""
        scores = self.get_scores()
        if scores[BLACK] > scores[WHITE]:
            self.winner = BLACK
        elif scores[WHITE] > scores[BLACK]:
            self.winner = WHITE
        else:
            self.winner = 0  # Draw

    def _check_terminal(self) -> None:
        """Check if game has reached a terminal condition."""
        if self.consecutive_passes >= 2 or self.is_full():
            self.is_terminal = True
            self._resolve_winner()

    def make_move(self, move: Optional[Tuple[int, int]]) -> "OthelloState":
        """
        Return new OthelloState applying move and flipping captured pieces.
        If move is None, execute a pass.
        """
        if self.is_terminal:
            return OthelloState(self.board, self.current_player, self.consecutive_passes)

        if move is None:
            new_state = OthelloState(
                self.board,
                current_player=3 - self.current_player,
                consecutive_passes=self.consecutive_passes + 1
            )
            if not new_state.get_legal_moves(new_state.current_player):
                new_state.consecutive_passes += 1
                new_state._check_terminal()
            return new_state

        r, c = move
        flips = self.get_flips(r, c, self.current_player)
        if not flips:
            raise ValueError(f"Illegal move {move} for player {self.current_player}")

        new_board = [row[:] for row in self.board]
        new_board[r][c] = self.current_player
        for fr, fc in flips:
            new_board[fr][fc] = self.current_player

        # Determine next turn
        opp = 3 - self.current_player
        opp_moves = any(
            self.get_flips(row, col, opp)
            for row in range(8) for col in range(8)
            if new_board[row][col] == EMPTY
        )
        curr_moves = any(
            self.get_flips(row, col, self.current_player)
            for row in range(8) for col in range(8)
            if new_board[row][col] == EMPTY
        )

        if opp_moves:
            next_player = opp
            passes = 0
        elif curr_moves:
            next_player = self.current_player
            passes = 1
        else:
            next_player = opp
            passes = 2

        new_state = OthelloState(new_board, next_player, passes)
        return new_state

    def get_scores(self) -> Dict[int, int]:
        """Return disc counts {BLACK: count, WHITE: count}."""
        black_cnt = sum(row.count(BLACK) for row in self.board)
        white_cnt = sum(row.count(WHITE) for row in self.board)
        return {BLACK: black_cnt, WHITE: white_cnt}


# ==============================================================================
# 2. THE AI
# ==============================================================================

def heuristic(state: OthelloState, player: int) -> float:
    """
    Evaluates board position from perspective of `player`.
    Combines terminal bonus, PST weights, corner control, and mobility.
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

    pos_score = 0
    for r in range(8):
        for c in range(8):
            val = state.board[r][c]
            if val == player:
                pos_score += PST[r][c]
            elif val == opp:
                pos_score -= PST[r][c]

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    corner_score = sum(
        25 if state.board[cr][cc] == player else (-25 if state.board[cr][cc] == opp else 0)
        for cr, cc in corners
    )

    my_mobility = len(state.get_legal_moves(player))
    opp_mobility = len(state.get_legal_moves(opp))
    mobility_score = 10 * (my_mobility - opp_mobility)

    return float(pos_score + corner_score + mobility_score)


def minimax_ab(
    state: OthelloState,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    max_player: Optional[int] = None
) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax search with Alpha-Beta pruning and PST move ordering.
    """
    if max_player is None:
        max_player = state.current_player if is_maximizing else (3 - state.current_player)

    if state.is_terminal or depth <= 0:
        return heuristic(state, max_player), None

    legal_moves = state.get_legal_moves()
    if not legal_moves:
        child = state.make_move(None)
        if child.is_terminal:
            return heuristic(child, max_player), None
        child_is_max = (child.current_player == max_player)
        eval_score, _ = minimax_ab(child, depth - 1, alpha, beta, child_is_max, max_player)
        return eval_score, None

    # Move ordering for rapid alpha-beta cutoffs
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


def play_game(
    ai_depth: int = 2,
    depth_black: Optional[int] = None,
    depth_white: Optional[int] = None,
    verbose: bool = False
) -> Tuple[Optional[int], Dict[int, int]]:
    """Automated headless self-play function for CI testing."""
    d_black = depth_black if depth_black is not None else ai_depth
    d_white = depth_white if depth_white is not None else ai_depth

    state = OthelloState()
    move_count = 0

    while not state.is_terminal and move_count < 120:
        moves = state.get_legal_moves()
        if not moves:
            state = state.make_move(None)
            move_count += 1
            continue

        depth = d_black if state.current_player == BLACK else d_white
        _, best_move = minimax_ab(
            state, depth=depth, alpha=-float('inf'), beta=float('inf'),
            is_maximizing=True, max_player=state.current_player
        )
        if best_move is None:
            best_move = moves[0]

        state = state.make_move(best_move)
        move_count += 1

    return state.winner, state.get_scores()


# ==============================================================================
# 3. THE UI
# ==============================================================================

def main():
    """Run interactive Pygame loop or fall back to headless simulation."""
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    try:
        import pygame
        pygame.init()
    except Exception as e:
        print(f"Pygame unavailable ({e}). Running headless verification...")
        winner, scores = play_game(ai_depth=2, verbose=True)
        print(f"Game finished. Winner={winner}, Scores={scores}")
        return

    SQUARE_SIZE = 60
    BOARD_SIZE = SQUARE_SIZE * 8
    INFO_PANEL_HEIGHT = 80
    WIDTH = BOARD_SIZE
    HEIGHT = BOARD_SIZE + INFO_PANEL_HEIGHT

    GREEN_BOARD = (34, 139, 34)
    LINE_COLOR = (20, 80, 20)
    COLOR_BLACK = (20, 20, 20)
    COLOR_WHITE = (235, 235, 235)
    HIGHLIGHT_COLOR = (255, 215, 0)
    BG_PANEL = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)

    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello (Reversi) Capstone")
        font = pygame.font.SysFont("arial", 20, bold=True)
    except Exception as e:
        print(f"Display mode unavailable ({e}). Running headless verification...")
        winner, scores = play_game(ai_depth=2, verbose=True)
        print(f"Game finished. Winner={winner}, Scores={scores}")
        return

    state = OthelloState()
    clock = pygame.time.Clock()
    running = True

    while running:
        legal_moves = state.get_legal_moves()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not state.is_terminal:
                if state.current_player == BLACK and legal_moves:
                    mx, my = event.pos
                    if my < BOARD_SIZE:
                        c = mx // SQUARE_SIZE
                        r = my // SQUARE_SIZE
                        if (r, c) in legal_moves:
                            state = state.make_move((r, c))

        if not state.is_terminal and not legal_moves:
            state = state.make_move(None)
            continue

        if not state.is_terminal and state.current_player == WHITE and legal_moves:
            pygame.display.flip()
            _, ai_move = minimax_ab(
                state, depth=3, alpha=-float('inf'), beta=float('inf'),
                is_maximizing=True, max_player=WHITE
            )
            if ai_move is None and legal_moves:
                ai_move = legal_moves[0]
            if ai_move:
                state = state.make_move(ai_move)

        screen.fill(BG_PANEL)
        pygame.draw.rect(screen, GREEN_BOARD, (0, 0, BOARD_SIZE, BOARD_SIZE))

        for i in range(9):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (BOARD_SIZE, i * SQUARE_SIZE), 2)
            pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, BOARD_SIZE), 2)

        for r in range(8):
            for c in range(8):
                center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
                rad = SQUARE_SIZE // 2 - 5
                val = state.board[r][c]
                if val == BLACK:
                    pygame.draw.circle(screen, COLOR_BLACK, center, rad)
                elif val == WHITE:
                    pygame.draw.circle(screen, COLOR_WHITE, center, rad)

        if not state.is_terminal and state.current_player == BLACK:
            for mr, mc in legal_moves:
                center = (mc * SQUARE_SIZE + SQUARE_SIZE // 2, mr * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, HIGHLIGHT_COLOR, center, 6)

        scores = state.get_scores()
        info_str = f"Black (Human): {scores[BLACK]}   White (AI): {scores[WHITE]}"
        turn_str = f"Turn: {'Black (Human)' if state.current_player == BLACK else 'White (AI)'}"
        if state.is_terminal:
            if state.winner == BLACK:
                turn_str = "GAME OVER — Black Wins!"
            elif state.winner == WHITE:
                turn_str = "GAME OVER — White Wins!"
            else:
                turn_str = "GAME OVER — Draw!"

        screen.blit(font.render(info_str, True, TEXT_COLOR), (20, BOARD_SIZE + 12))
        screen.blit(font.render(turn_str, True, HIGHLIGHT_COLOR if state.is_terminal else TEXT_COLOR), (20, BOARD_SIZE + 42))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
