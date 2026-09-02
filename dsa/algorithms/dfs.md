- A [[greedy]] [[graphs]] traversal method. Continues down one branch until a leaf node, then backtracks and repeats.
- Best implemented with [[recursion]].

```python
graph = {} # assume populated adjacency list
visited = set()

def dfs(node):

	if node in visited:
		return
		
	visited.add(node)
	
	for neighbor in graph[node]:
		dfs(neighbor)
```

- `O(n+e)` TC, `O(n)` SC.

Give sorted order of a Binary Search Tree using dfs.

```python
def dfs(root, arr): # assumes root object
	
	# base case
	if not root.left and not root.right:	
		return root.val
	
	# recrusive case
	if root.left
		left = dfs(root.left)
		arr.append(left, arr)
	
	if root.right
		right = dfs(root.right)
		arr.append(right, arr)
	
	# end case	
	arr.append(root.val)
	return root.val	
```

- Example of how dfs is useful. Function above traverses the tree in inorder traversal. In a BST, 

