- Use the same principles as [[dfs]] to find the shortest path from a source node to all other nodes in weighted [[graphs]].
- Does not work with negative edge weights.
- [[greedy]] algorithm, always processes the closest unvisited node next.

```python
import heapq

def dijkstra(
	graph: dict[str, list[tuple[str, float]]], 
	start: str,
) -> dict[str, float]:
	
	dist = {node: float('inf') for node in graph}
	dist[start] = 0
	heap = [(0, start)]
	
	while heap:
		curr_node, curr_dist = heapq.heappop(heap)
		if curr_dist > dist[curr_node]:
			continue  # skip stale entry
			
		for neighbour, dist_to_n in graph[curr_node]:
			dist_from_s = dist[curr_node] + dist_to_n
			if dist_from_s < dist[neighbour]:
				dist[neighbour] = dist_from_s		
				heapq.heappush(heap, (dist[neighbour], neighbour))
	
	return dist
```

## TS Complexity

- `O((n+e) log n)` TC, `O(n+e)` SC.

## Explanation

1. Regular [[bfs]] uses a [[queues|queue]] to always grab the closest nodes. However, in a weighted graph, we cannot guarantee that the physically nearest node is actually the closest.
2. Thus, we use a [[heaps#Min-Heap|min-heap]], instead, which will always give us the smallest weight for every pop. The rest follows bfs logic.
3. One issue: it is expected that we can visit the same node multiple times, and find shorter paths from `start` to said node.
	1. In this case, `dist` is updated, but `heap` might contain multiple entries of said node, with differing distances.
	2. The `if d > dist[u]: continue` line skips these stale entries in the heap.
	3. This one if statement and occasional skipped iteration is much cheaper than removing from the heap, which is `O(logn)`.
