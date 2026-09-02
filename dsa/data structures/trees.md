- A tree is simply a [[graphs|graph]] that fits a certain criteria. 
	1. Must be an acyclic graph where one node is the ==root==.
	2. Each node has at most one parent and zero or more children.
- ==Leaf node== is a node with no children.
- Height of a tree is the longest path from root to a leaf.

```
        1
       / \
      2   3
     / \   \
    4   5   6
```

# Traversal Methods

- Like a graph, a tree can and should be traversed. But there are specific orders of doing so.
- For all algorithms below, we will assume the tree is represented by its root, a singular `TreeNode` class object.

```python
class TreeNode:
	def __init__(self, val : int):
		self.val = val
		self.left = None
		self.right = None	
```

- All traversal methods are `O(n)`.

## [[dfs|Depth First]] Traversals

- Uses the [[dfs]] algorithm to traverse, always start at the bottom most subtree.

### Inorder

```python
def inorder(node):
    result = []
    
    if node:
        result.extend(inorder(node.left))
        result.append(node.val)
        result.extend(inorder(node.right))
        
    return result
```

- Left, root, right.
- For ==binary search trees==, this gives nodes in sorted order.

### Preorder

```python
def preorder(node):
    result = []
    
    if node:
        result.append(node.val)
        result.extend(preorder(node.left))
        result.extend(preorder(node.right))
        
    return result
```

- Root, left, right.

### Postorder

```python
def postorder(node):
    result = []
    
    if node:
        result.extend(postorder(node.left))
        result.extend(postorder(node.right))
        result.append(node.val)
        
    return result
```

- Left, right, root.

## [[bfs|Breadth First]]  Traversals

- Uses [[bfs]], level order is the only one. 

### Level Order

```python
from collections import deque

def level_order(node):
	if not node:
		return []
	
	queue = deque([node])
	result = []
	
	while queue:
		curr = queue.popleft()
		result.append(curr)
		
		if curr.left:
			queue.append(curr.left)
		
		if curr.right:
			result.append(curr.right)
			queue.append(curr.right)
	
	return result
```

- Visits each layer at a time.

# Binary Search Tree

- A ==binary tree== (tree with at most 2 children per node) where every node's left subtree contains only smaller values and right subtree contains only larger values.
- ==In-place invariant==, no duplicate values allowed.
- Designed around inorder traversal, where inorder BST gives a sorted list.

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

## TS Complexity

- Since we only need to visit one layer at a time, and not every node, the **TC of all operations (not traversals or validate) on a BST is `O(h)`**, `h` being the height, not number of nodes.
- `O(n)` SC.

## Balanced BST

- A ==balanced binary search tree== has its left and right subtree's height differ by at most a small constant, usually 1.

```
        8
       / \
      3   10
     / \  / \
    1  6 9  14
```

- A perfectly balanced BST has a height of `O(logn / log2)`, `n` being the number of nodes. Since the nodes are neatly stacked together (see above).

### TS Complexity 

- By extension, **all operations on a balanced BST have a TC of`O(logn / log2)`.
- SC will always be `O(n)`, since we need a node for every element.

## Degenerate BST

- A degenerate BST is one that does not enforce any height requirements. And thus, the shape below is still a valid BST, but offers no searching advantages.

```
	1
     \
      2
       \
        3
         \
          4
```

### TS Complexity 

- `O(n)` TC
- `O(n)` SC

## Searching

```python
def search(node, target):
	if not node:
		return None
		
	if target == node.val:
		return node
		
	if target < node.val:
		return search(node.left, target)
		
	return search(node.right, target)
```

- [[recursion|Recursively]] compare target to current node, go left if smaller, right if larger, if equal we have found the target (since no duplicates are allowed).

## Inserting

```python
def insert(node, val):
	if not node:
		return TreeNode(val)
		
	if val < node.val:
		node.left = insert(node.left, val)
		
	elif val > node.val:
		node.right = insert(node.right, val)
		
	return node
```

- Search as if the value is there, and create a new node where it should be.
- Base case returns the new node, and the call stack above it will set it in place, then return itself as to not mutate the tree.

## Deletion

```python
def delete(node, val):
	if not node:
		return None
		
	if val < node.val:
		node.left = delete(node.left, val)
		
	elif val > node.val:
		node.right = delete(node.right, val)
		
	else:
		if not node.left:
			return node.right
			
		if not node.right:
			return node.left
			
		successor = node.right
		
		while successor.left:
			successor = successor.left
			
		node.val = successor.val
		node.right = delete(node.right, successor.val)
		
	return node
```

- Delete is trickier, 3 cases:
	1. Node is a leaf, simply remove it.
	2. Node has one child (not counting grandchildren), replace node with its child.
	3. Node has two children, replace node's value with its ==inorder successor==, then delete that successor.

## Validate

```python
def is_valid_bst(node, lo=float('-inf'), hi=float('inf')):
	if not node:
		return True
	if not (lo < node.val < hi):
		return False
	return (is_valid_bst(node.left, lo, node.val) and
	        is_valid_bst(node.right, node.val, hi))
```

- Validate a BST by checking that every node falls within a valid `(min, max)` range.
- Not `O(h)` TC but `O(n)`, since we need to check every node.
