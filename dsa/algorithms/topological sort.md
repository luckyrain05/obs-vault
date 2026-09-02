![[resources/03Graphs.pdf]]

-  Finds if a graph is acyclic or not. 
- For dependency resolution. Represent dependencies in [[graphs]], if resulting in DAG, there is no conflicting dependency and the end goal can be achieved.
- Opposite is true. If a cycle exists, it is impossible to resolve dependency.

```python
graph = {} # assume populated dictionary
visited = set()
visiting = set()

def topological_sort(node):
	if node in visited:
		return True
	if node in visiting or not node in graph:
		return False
	
	visiting.add(node)
	for neighbor in graph[node]:
		if topological_sort(neighbor) == False:
			return False
	
	visiting.remove(node)
	visited.add(node)
	
	return True
```

- Can be implemented in both [[dfs]] and [[bfs]], using dfs in this case.
- `O(v+e)` TC, `O(v+e)` SC.