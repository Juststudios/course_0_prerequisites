"""
Checkers: Core Game Engine
===========================
An 8x8 American / English Draughts game engine implementing complete,
rigorous tournament rules:
  - 8x8 Board with 32 dark playable squares
  - Men (move diagonally forward) and Kings (move diagonally forward & backward)
  - Mandatory Forced Capture rule (if any jump exists, only jumps are legal)
  - Recursive Multi-Jump expansion (generates all complete multi-jump paths)
  - King Promotion (crowning on opponent baseline; crowning ends turn)
  - Terminal detection (loss when blocked or out of pieces; draw on 40-move rule)
"""

import numpy as np

# Piece definitions
EMPTY = 0
RED_MAN = 1      # Player 1 standard piece (starts rows 5, 6, 7; moves UP / row -1)
BLACK_MAN = 2    # Player 2 standard piece (starts rows 0, 1, 2; moves DOWN / row +1)
RED_KING = 3     # Player 1 crowned King
BLACK_KING = 4   # Player 2 crowned King

PLAYER_RED = 1
PLAYER_BLACK = 2


def is_dark_square(r, c):
    """Check if (r, c) is a playable dark square on the 8x8 checkerboard."""
    return (r + c) % 2 == 1


class CheckersState:
    """
    Immutable representation of an 8x8 Checkers game state.
    """

    def __init__(self, board=None, current_player=PLAYER_RED, halfmove_clock=0):
        if board is None:
            self.board = self._create_initial_board()
        else:
            self.board = np.copy(board)

        self.current_player = current_player
        self.halfmove_clock = halfmove_clock
        self.winner = None
        self.is_terminal = False
        self._check_terminal()

    @staticmethod
    def _create_initial_board():
        """Initialize standard 8x8 checkers board with 12 pieces per player."""
        b = np.zeros((8, 8), dtype=np.int8)
        # Black pieces on rows 0, 1, 2 (dark squares)
        for r in range(3):
            for c in range(8):
                if is_dark_square(r, c):
                    b[r, c] = BLACK_MAN

        # Red pieces on rows 5, 6, 7 (dark squares)
        for r in range(5, 8):
            for c in range(8):
                if is_dark_square(r, c):
                    b[r, c] = RED_MAN
        return b

    def _is_opponent_piece(self, piece, player):
        """Return True if piece belongs to the opponent of player."""
        if player == PLAYER_RED:
            return piece in (BLACK_MAN, BLACK_KING)
        else:
            return piece in (RED_MAN, RED_KING)

    def _is_own_piece(self, piece, player):
        """Return True if piece belongs to player."""
        if player == PLAYER_RED:
            return piece in (RED_MAN, RED_KING)
        else:
            return piece in (BLACK_MAN, BLACK_KING)

    def _get_piece_directions(self, piece):
        """Return list of (dr, dc) directions the piece can move."""
        if piece == RED_MAN:
            return [(-1, -1), (-1, 1)]  # Moves UP
        elif piece == BLACK_MAN:
            return [(1, -1), (1, 1)]   # Moves DOWN
        elif piece in (RED_KING, BLACK_KING):
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Both directions
        return []

    def _find_jumps_for_piece(self, r, c, piece, board):
        """
        Recursively find all multi-jump paths for a piece from (r, c).
        Returns a list of coordinate tuples: [((r, c), (r1, c1), (r2, c2)), ...]
        """
        directions = self._get_piece_directions(piece)
        jumps = []
        player = PLAYER_RED if piece in (RED_MAN, RED_KING) else PLAYER_BLACK
        king_row = 0 if player == PLAYER_RED else 7

        for dr, dc in directions:
            mid_r, mid_c = r + dr, c + dc
            dest_r, dest_c = r + 2 * dr, c + 2 * dc

            # Check bounds
            if 0 <= dest_r < 8 and 0 <= dest_c < 8:
                mid_piece = board[mid_r, mid_c]
                # Check if jumping over opponent into empty space
                if self._is_opponent_piece(mid_piece, player) and board[dest_r, dest_c] == EMPTY:
                    # Check crowning on jump
                    is_crowned = (piece in (RED_MAN, BLACK_MAN) and dest_r == king_row)
                    
                    if is_crowned:
                        # Standard American draughts rule: Crowning ends the turn immediately
                        jumps.append(((r, c), (dest_r, dest_c)))
                    else:
                        # Continue recursive multi-jump with temporary board
                        temp_board = np.copy(board)
                        temp_board[r, c] = EMPTY
                        temp_board[mid_r, mid_c] = EMPTY
                        temp_board[dest_r, dest_c] = piece

                        further_jumps = self._find_jumps_for_piece(dest_r, dest_c, piece, temp_board)
                        if further_jumps:
                            for fj in further_jumps:
                                # Prepend starting point (r, c) to full continuation path
                                jumps.append(((r, c),) + fj)
                        else:
                            jumps.append(((r, c), (dest_r, dest_c)))
        return jumps

    def get_legal_moves(self):
        """
        Generate all legal moves for current_player under mandatory capture rules.
        
        Returns
        -------
        list of tuples of (r, c) coordinates representing move paths.
        Example step: [((5, 2), (4, 3))]
        Example jump: [((5, 2), (3, 4), (1, 2))]
        """
        if self.is_terminal:
            return []

        jump_moves = []
        step_moves = []

        for r in range(8):
            for c in range(8):
                piece = self.board[r, c]
                if self._is_own_piece(piece, self.current_player):
                    # 1. Search for captures
                    piece_jumps = self._find_jumps_for_piece(r, c, piece, self.board)
                    jump_moves.extend(piece_jumps)

                    # 2. Search for simple steps (only used if no jumps exist)
                    if not jump_moves:
                        directions = self._get_piece_directions(piece)
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr, nc] == EMPTY:
                                step_moves.append(((r, c), (nr, nc)))

        # Mandatory capture rule: If jumps are available, only jumps are legal!
        if jump_moves:
            return jump_moves
        return step_moves

    def make_move(self, move):
        """
        Execute move and return a new CheckersState.
        
        Parameters
        ----------
        move : tuple of (r, c) coordinates
            Path taken by moving piece.
            
        Returns
        -------
        CheckersState
            Updated immutable game state.
        """
        if self.is_terminal:
            raise ValueError("Cannot move in terminal state.")

        legal_moves = self.get_legal_moves()
        if move not in legal_moves:
            raise ValueError(f"Illegal move {move}. Legal moves are: {legal_moves}")

        new_board = np.copy(self.board)
        start_r, start_c = move[0]
        piece = new_board[start_r, start_c]
        new_board[start_r, start_c] = EMPTY

        is_jump = (abs(move[1][0] - move[0][0]) == 2)
        halfmove = 0 if is_jump else (self.halfmove_clock + 1)

        # Handle hops
        curr_r, curr_c = start_r, start_c
        for next_r, next_c in move[1:]:
            if abs(next_r - curr_r) == 2:
                # Capture midpoint piece
                cap_r = (curr_r + next_r) // 2
                cap_c = (curr_c + next_c) // 2
                new_board[cap_r, cap_c] = EMPTY
            curr_r, curr_c = next_r, next_c

        # Check king promotion at final square
        final_r, final_c = move[-1]
        if piece == RED_MAN and final_r == 0:
            piece = RED_KING
            halfmove = 0
        elif piece == BLACK_MAN and final_r == 7:
            piece = BLACK_KING
            halfmove = 0

        new_board[final_r, final_c] = piece

        next_player = PLAYER_BLACK if self.current_player == PLAYER_RED else PLAYER_RED
        return CheckersState(new_board, next_player, halfmove)

    def _check_terminal(self):
        """Check whether state is terminal (no legal moves or 40-move draw rule)."""
        # 40-move rule: 80 half-moves without capture or promotion
        if self.halfmove_clock >= 80:
            self.is_terminal = True
            self.winner = 0  # Draw
            return

        # Check if current player has pieces remaining
        p1_pieces = np.sum((self.board == RED_MAN) | (self.board == RED_KING))
        p2_pieces = np.sum((self.board == BLACK_MAN) | (self.board == BLACK_KING))

        if p1_pieces == 0:
            self.is_terminal = True
            self.winner = PLAYER_BLACK
            return
        if p2_pieces == 0:
            self.is_terminal = True
            self.winner = PLAYER_RED
            return

        # Check if current player has any legal moves
        moves = self.get_legal_moves()
        if len(moves) == 0:
            self.is_terminal = True
            # The player who cannot move loses!
            self.winner = PLAYER_BLACK if self.current_player == PLAYER_RED else PLAYER_RED

    def render(self):
        """Return formatted ASCII representation of the checkers board."""
        symbols = {
            EMPTY: '.',
            RED_MAN: 'r',
            BLACK_MAN: 'b',
            RED_KING: 'R',
            BLACK_KING: 'B'
        }
        lines = ["  0 1 2 3 4 5 6 7"]
        for r in range(8):
            row_str = f"{r} "
            for c in range(8):
                if is_dark_square(r, c):
                    row_str += symbols[self.board[r, c]] + " "
                else:
                    row_str += "  "
            lines.append(row_str)
        player_name = "Red (Player 1)" if self.current_player == PLAYER_RED else "Black (Player 2)"
        lines.append(f"Turn: {player_name}")
        return "\n".join(lines)

    def count_pieces(self):
        """Return dict with count of pieces for both players."""
        return {
            'red_men': int(np.sum(self.board == RED_MAN)),
            'red_kings': int(np.sum(self.board == RED_KING)),
            'black_men': int(np.sum(self.board == BLACK_MAN)),
            'black_kings': int(np.sum(self.board == BLACK_KING)),
        }
