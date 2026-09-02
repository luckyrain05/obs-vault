Given a `m x n` `grid` filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

**Note:** You can only move either down or right at any point in time.

```python
def minPathSum(self, grid: List[List[int]]) -> int:
	m = len(grid)
	n = len(grid[0])
	
	tab = []
	total = 0
	for i in range(n):
		total += grid[0][i]
		tab.append(total)
	
	for r in range(1, m):
		for c in range(n):
			if c == 0:
				tab[c] += grid[r][c]
			else:
				tab[c] = grid[r][c] + min(tab[c], tab[c - 1])
	
	return tab[-1]
```

- 