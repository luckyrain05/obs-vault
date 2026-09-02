A farmland is represented in a `n x m` [[graphs|grid]]. The matrix is filled with `0`s and `1`s, with `1`s being land that can be farmed on, and `0`s are not. The farmer that owns this land can only farm on squares, find the largest viable farmland for this farmer.

- A singular `1` is considered a square.

Return an `int` representing the area of the largest square.

# Solution

```python
def largest_farmland(farm: List[List[int]]) -> int:
	m = len(farm)
	n = len(farm[0])
	prev = curr = n * [0]	
	ans = 0
	
	for r in range(m):
		prev, curr = curr, n * [0]
		
		for c in range(n):
			if grid[r][c] == 1:
				if c == 0:
					curr[c] = 1
				else:
					curr[c] = min(
						curr[c - 1],
						prev[c],
						prev[c - 1]
					) + 1
				
			ans = max(ans, curr[c])
```

## TS Complexity

- `O(m*n)` TC, `O(m)` SC.

## Explanation

1. Use [[dp#Tabulation|tabulation]] with 2 external, empty arrays to scan through the farm grid.
2. Starting from the top row, left to right, we try to build the largest square assuming the current node is the bottom right of the square.
	1. At column 0, obviously we cannot build a bigger square than 1, so we set `left = up = diag = 0`, and the `min()` below gracefully sets current node as `1`.
	2. At row 0, same case.
	3. In other cases, the largest square we can possibly build is the smallest square surrounding it + 1. 

## Notes

- This is a top-down [[dp]] solution, and the most optimal solution for this problem.
- [[dfs]] or [[bfs]] with memoization will also be an optimal solution.
	- But for every recursion + memo solution, there usually exists a tabulation solution, and it is usually much more elegant and/or optimal.