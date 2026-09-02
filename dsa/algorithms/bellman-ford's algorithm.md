- Finds the shortest path from a source node to all other nodes in weighted [[graphs]] using a [[hashs#Dictionary|dictionary]].
	- Works with negative weights, but much slower than dijkstra.
- Can detect ==negative cycles==, if after n-1 relaxations a distance can still be reduced, a negative cycle exists.

```python
def bellman_ford(nodes, edges, start):
	dist = {node: float('inf') for node in nodes}
	dist[start] = 0

	for _ in range(len(nodes) - 1):
		for u, v, weight in edges:
			if dist[u] + weight < dist[v]:
				dist[v] = dist[u] + weight

	for u, v, weight in edges:
		if dist[u] + weight < dist[v]:
			return None

	return dist
```

## TS Complexity

 - `O(n*e)` TC, `O(n)` SC.

## Explanation
 
- Relaxes every edge n-1 times. A ==relaxation== checks if going through node u to reach v is shorter than the current known distance to v.
- The final loop checks for negative cycles. If any distance can still be reduced after n-1 passes, a cycle exists.
