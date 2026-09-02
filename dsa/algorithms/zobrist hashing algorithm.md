- Game-tree search (minimax, alpha-beta) explores positions by repeatedly making a move, recursing, then unmaking it to try the next move. A ==transposition table== — a [[hashs|hash table]] keyed by position — skips re-searching a position already reached by a different move order.
- Hashing the whole board from scratch after every make/unmake is `O(n)` in board size. Zobrist hashing updates the hash in `O(1)` per move instead, and — because of how it's built — unmaking a move turns out to be the exact same operation as making one.

# XOR Property

- Zobrist hashing is built entirely out of one bitwise operation, XOR (`^`), because of a property it has that addition and multiplication don't give for free.

**XOR**

- `a ^ b` is `1` in each bit position where `a` and `b` differ, `0` where they match.
- Commutative and associative: `a ^ b = b ^ a` and `(a ^ b) ^ c = a ^ (b ^ c)`. The order values are XOR'd in doesn't matter.

**Self-inverse**

- `b ^ b = 0` for any `b`, and `a ^ 0 = a`. So `a ^ b ^ b = a` — XOR-ing the same value in twice cancels it and restores what was there before.
- "Add" and "remove" become the same operation: XOR-ing a value in a second time is how it comes back out.

# Zobrist Table

- Precompute one independent random number for every board feature — each `(square, piece type)` pair — before any hashing happens.

```python
import random

SQUARES = 64
PIECE_TYPES = 12  # 6 piece types x 2 colors

zobrist_table = [[random.getrandbits(64) for _ in range(PIECE_TYPES)] for _ in range(SQUARES)]

def initial_hash(board):
	h = 0
	for square, piece in board.items():  # board: {square: piece_type}
		h ^= zobrist_table[square][piece]
	return h
```

- `O(n)` TC, `O(1)` SC (the table is fixed-size, independent of board state).

1. Build the table once, at the start of a search — one random 64-bit number per `(square, piece)` pair.
2. To hash a starting position, XOR together the table entries for every occupied square.
3. The result is one 64-bit number representing that exact board state.

# Incremental Update

- A move touches a handful of squares, not the whole board, so a move only needs to XOR out the entries that changed and XOR in the entries that replaced them.

```python
def make_move(h, square, piece, to_square, captured=None):
	h ^= zobrist_table[square][piece]         # remove piece from old square
	h ^= zobrist_table[to_square][piece]       # place piece on new square
	if captured is not None:
		h ^= zobrist_table[to_square][captured]  # remove captured piece
	return h
```

- `O(1)` TC, `O(1)` SC.

1. XOR out the moving piece's entry at its old square.
2. XOR in the moving piece's entry at its new square.
3. If a piece was captured, XOR out its entry too.

`Notes:`

- Unmaking a move calls this exact same function with the exact same arguments. XOR-ing the same entries again reverses steps 1-3 in any order, since `^` is self-inverse and order-independent — no separate undo logic needed.

# Collisions

- The board has vastly more reachable states than a 64-bit number has values, so two different positions can XOR to the same hash — the same [[hashs#Collision|collision]] problem general-purpose hash tables have.
- A transposition-table hit is only trusted after confirming the stored position actually matches, not just the hash. That guards against this.
