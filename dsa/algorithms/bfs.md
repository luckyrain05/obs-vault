- A [[greedy]] algo to traverse a [[graphs]], visits all neighboring nodes first using a [[queues|queue]].
- Finds shortest path between two nodes, only on unweighted graphs.

**Visit every node of a graph using bfs:**

```python
from collections import deque

graph = {}

def bfs(start):
	visited = set()
	queue = deque([start])
	visited.add(start)
	
	while queue:
		node = queue.popleft()
		
		for neighbor in graph[node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)
```

- `O(n+e)` TC, `O(n)` SC.

**Find shortest distance between two nodes using bfs**

```python
from collections import deque
import math

graph = {}

def bfs(start, end):
    visited = {start}
    queue = deque([(start, 0)])
	
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
	
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
	 
    return -1
```

- For every node, we also track the distance it is away from the starting node.
- Increment `dist` by 1 from a node's parent.
- When we arrive at the target node, the target's `dist` value is automatically the geographically nearest path.