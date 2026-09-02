```python
from collections import deque

def orangesRotting(self, grid: List[List[int]]) -> int:
	m = len(grid)
	n = len(grid[0])
	fresh = set()
	q = deque()
	minutes = -1
	
	#find our initial rotten and fresh positions
	for r in range(m):
		for c in range(n):
			if grid[r][c] == 2:
				q.append((r, c))
			if grid[r][c] == 1:
				fresh.add((r, c))
	
	if not q and not fresh:
		return 0
	
	#bfs starting from rotten positions, layer by layer
	#remove fresh oranges from tracker as they rot
	#keep visited set to avoid same node picked up by multiple sources
	visited = set()
	while q:
		for _ in range(len(q)):
			row, col = q.popleft()
			
			if grid[row][col] == 1:
				grid[row][col] = 2
				fresh.remove((row, col))
			
			for r, c in [(1, 0), (-1, 0), (0, 1), (0,-1)]:
				dr, dc = row + r, col + c
				if \
					0 <= dr < m and \
					0 <= dc < n and \
					grid[dr][dc] == 1 and \
					(dr, dc) not in visited:
					visited.add((dr, dc))
					q.append((dr, dc))
		minute += 1
	
	if fresh:
		return -1
	
	return minutes
```