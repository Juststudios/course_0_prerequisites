# Module 8: Checkers (Draughts) Engine & AI

## What You Will Learn
- How to represent an 8x8 checkers board state with pure NumPy arrays and immutable state transitions.
- How to implement tournament-grade rules:
  1. Diagonal movement for standard pieces (Men).
  2. Mandatory forced captures (jumps take priority over non-capture steps).
  3. Recursive multi-jump branching to find all complete jump sequences.
  4. King promotion upon reaching the opponent's back rank.
- How to design a multi-component heuristic combining material, center control, advancement, home defense, and mobility.
- How to build a depth-limited Alpha-Beta search AI that consistently outperforms baseline agents.

---

## 1. The Complexity of Checkers Rules

Unlike Tic-Tac-Toe or Connect Four where move generation involves simply scanning for open squares, American / English Draughts requires strict rule validation:

1. **Board Representation:** Played exclusively on the 32 dark squares of an 8x8 grid where `(row + col) % 2 == 1`.
2. **Standard Movement:** Men only move diagonally forward 1 step into an unoccupied dark square.
3. **King Movement:** When a Man reaches the furthest opposite rank (row 0 for Red, row 7 for Black), it is crowned King (`RED_KING` or `BLACK_KING`) and can move both forward and backward.
4. **Mandatory Forced Captures:** If any jump move is available on the board for the active player, that player **must** make a capture. Non-capture steps are strictly illegal.
5. **Multi-Jumps (Successive Captures):** If a jumping piece lands on a square from which another capture is immediately possible, the piece must continue jumping in the same turn. If multiple multi-jump paths exist, the player may choose which sequence to execute.
6. **Crowning Termination:** When an uncrowned Man reaches the king row via a jump, it is crowned immediately and its turn ends (it cannot continue jumping on that turn as a King).

---

## 2. Engine Architecture (`checkers.py`)

The engine is encapsulated in the immutable class `CheckersState`:

```text
CheckersState
  ├── board: np.ndarray (8x8 int8)
  │     0 = EMPTY
  │     1 = RED_MAN (moves row - 1)
  │     2 = BLACK_MAN (moves row + 1)
  │     3 = RED_KING (moves row ± 1)
  │     4 = BLACK_KING (moves row ± 1)
  ├── current_player: PLAYER_RED (1) or PLAYER_BLACK (2)
  ├── is_terminal: bool (True when a player has no legal moves or 40-move draw)
  └── winner: 1 (Red), 2 (Black), 0 (Draw), or None
```

### Key Engine Methods

- `get_legal_moves()`: Returns a list of coordinate path tuples.
  - Simple Step: `[((5, 0), (4, 1))]`
  - Multi-Jump: `[((5, 0), (3, 2), (1, 4))]`
  - Enforces mandatory captures: if any jump paths exist, step moves are pruned.
- `make_move(move)`: Returns a new `CheckersState` with:
  - Moving piece relocated.
  - Midpoint captured pieces removed from the board.
  - King promotions applied.
  - Active player toggled.
  - Terminal status updated.

---

## 3. Checkers AI Heuristic (`checkers_ai.py`)

Checkers has a game-tree complexity of approximately $5 \times 10^{20}$. To make decisions in real time, the AI utilizes **Depth-Limited Minimax with Alpha-Beta Pruning** paired with a domain-specific evaluation function:

$$V(s) = w_{\text{mat}} \cdot \Delta\text{Material} + w_{\text{pos}} \cdot \Delta\text{Positional} + w_{\text{mob}} \cdot \Delta\text{Mobility}$$

### Heuristic Components

1. **Material Advantage:**
   - Standard Man = 100 points
   - King = 180 points (valuable because Kings can move in all 4 diagonal directions)
2. **Positional Advantage:**
   - **Center Board Control:** +15 points for occupying central dark squares `(3,2), (3,4), (4,1), (4,3), (4,5), (3,6)`, enabling rapid diagonal transitions.
   - **Advancement:** +8 points per rank advanced towards the crowning row for Men.
   - **Home Rank Defense:** +20 points for keeping pieces on the back row (row 7 for Red, row 0 for Black) to deny easy opponent crowning.
3. **Mobility:**
   - +5 points per legal move available, preventing the AI from getting cornered or blocked into zugzwang.

---

## 4. Running the Code & Benchmarks

### Automated Headless Benchmark (Default)
Runs automated games between the Alpha-Beta AI (Red, depth 3) and a Random baseline (Black):

```bash
python3 game-ai/08_checkers/play_checkers.py
```

Expected output:
- Verifies forced capture integrity on every turn.
- Tracks captures, multi-jumps, and remaining piece counts.
- AI achieves a 100% win rate against random play.

### Interactive CLI Play
Challenge the Alpha-Beta AI in your terminal:

```bash
python3 game-ai/08_checkers/play_checkers.py --interactive --depth 4
```

You can select moves by typing the index from the legal move list or using coordinate syntax (e.g., `5,0 to 4,1` or `5,0-3,2-1,4`).
