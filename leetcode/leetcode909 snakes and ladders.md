You are given an `n x n` [[graphs|board]] `board` where the cells are labeled from `1` to `n2` in a [**Boustrophedon style**](https://en.wikipedia.org/wiki/Boustrophedon) starting from the bottom left of the board (i.e. `board[n - 1][0]`) and alternating direction each row.

You start on square `1` of the board. In each move, starting from square `curr`, do the following:

- Choose a destination square `next` with a label in the range `[curr + 1, min(curr + 6, n2)]`.
    - This choice simulates the result of a standard **6-sided die roll**: i.e., there are always at most 6 destinations, regardless of the size of the board.
- If `next` has a snake or ladder, you **must** move to the destination of that snake or ladder. Otherwise, you move to `next`.
- The game ends when you reach the square `n2`.

A board square on row `r` and column `c` has a snake or ladder if `board[r][c] != -1`. The destination of that snake or ladder is `board[r][c]`. Squares `1` and `n2` are not the starting points of any snake or ladder.

Note that you only take a snake or ladder at most once per dice roll. If the destination to a snake or ladder is the start of another snake or ladder, you do **not** follow the subsequent snake or ladder.

- For example, suppose the board is `[[-1,4],[-1,3]]`, and on the first move, your destination square is `2`. You follow the ladder to square `3`, but do **not** follow the subsequent ladder to `4`.

Return _the least number of dice rolls required to reach the square_ `n2`_. If it is not possible to reach the square, return_ `-1`.

# Solution

```python
from collections import deque

def snakesAndLadders(board):
	n = len(board)

	def get_pos(sq):
		r = (sq - 1) // n
		c = (sq - 1) % n
		if r % 2 == 1:
			c = n - 1 - c
		return n - 1 - r, c

	visited = set()
	queue = deque([(1, 0)])
	visited.add(1)

	while queue:
		sq, moves = queue.popleft()
		for i in range(1, 7):
			nxt = sq + i
			if nxt > n * n:
				continue
			r, c = get_pos(nxt)
			if board[r][c] != -1:
				nxt = board[r][c]
			if nxt == n * n:
				return moves + 1
			if nxt not in visited:
				visited.add(nxt)
				queue.append((nxt, moves + 1))

	return -1
```

## TS Complexity

- `O(n^2)` TC, `O(n^2)` SC.

## Explanation

1. Flatten the 2D board into 1D. `get_pos` converts a square number to its `(row, col)` on the boustrophedon board.
2. [[bfs]] from square `1`. Each state explores dice rolls `1-6`.
3. If landing on a snake or ladder (value != `-1`), teleport to that destination.
4. BFS guarantees the first time we reach `n^2` is the minimum number of moves.

## Notes

- The boustrophedon conversion is the trickiest part. Odd rows (from bottom) go right-to-left, so the column is flipped.