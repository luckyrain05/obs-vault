Given an `m x n` 2D binary [[graphs|grid]] `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return _the number of islands_.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

# [[dfs]] Solution

```python
def numIslands(grid):
	rows, cols = len(grid), len(grid[0])
	count = 0

	def dfs(r, c):
		if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
			return
		
		grid[r][c] = '0'
		
		dfs(r + 1, c)
		dfs(r - 1, c)
		dfs(r, c + 1)
		dfs(r, c - 1)
	
	for r in range(rows):
		for c in range(cols):
			if grid[r][c] == '1':
				count += 1
				dfs(r, c)
	
	return count
```

## TS Complexity

- `O(m*n)` TC, `O(m*n)` SC.

## Explanation

1. Iterate through every cell. When a `'1'` is found, increment the island count and launch a [[dfs]] to sink the entire island.
2. DFS marks every connected `'1'` as `'0'` so it won't be counted again.
3. Each cell is visited at most once across all DFS calls.

## Notes

- Worst case SC is `O(m*n)`, the recursion stack depth on a grid that is entirely land.
- Mutates the input grid to avoid a separate visited set. If that's not allowed, use a `visited` set for `O(m*n)` extra space.

# [[bfs]] Solution

```python
from collections import deque

def numIslands(self, grid: List[List[str]]) -> int:
	if not grid or not grid[0]:
		return 0
	
	rows, cols = len(grid), len(grid[0])
	answer = 0
	
	def bfs(row, col):
		q = deque([(row, col)])
		grid[row][col] = '0'
		
		while q:
			r, c = q.popleft()
			for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
				nr, nc = r + dr, c + dc
				
				if (
					0 <= nr < rows and \ 
					0 <= nc < cols and \
					grid[nr][nc] == '1'
					):
					grid[nr][nc] = '0'
					q.append((nr, nc))
	
	for r in range(rows):
		for c in range(cols):
			if grid[r][c] == '1':
				answer += 1
				bfs(r, c)
	
	return answer
```

## TS Complexity

## Explanation

## Notes
