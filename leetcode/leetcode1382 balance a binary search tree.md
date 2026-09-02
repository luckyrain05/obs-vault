Given the `root` [[oop|object]] of a [[trees#Binary Search Tree|Binary Search Tree]], return _a **balanced** binary search tree with the same node values_. If there is more than one answer, return **any of them**.

A binary search tree is **balanced** if the depth of the two subtrees of every node never differs by more than `1`.

# Solution

```python
def balanceBST(root):
	nodes = []

	def inorder(node):
		if not node:
			return
		inorder(node.left)
		nodes.append(node.val)
		inorder(node.right)

	def build(lo, hi):
		if lo > hi:
			return None
		mid = (lo + hi) // 2
		node = TreeNode(nodes[mid])
		node.left = build(lo, mid - 1)
		node.right = build(mid + 1, hi)
		return node

	inorder(root)
	return build(0, len(nodes) - 1)
```

## TS Complexity

- `O(n)` TC, `O(n)` SC.

## Explanation

1. [[trees#Traversal Orders|Inorder]] traverse the BST to get a sorted list of values.
2. Recursively build a new BST by always picking the middle element as root. This guarantees balance.
3. Left half becomes the left subtree, right half becomes the right subtree.

## Notes

- Inorder on a BST always yields sorted order, this is the key insight.
- The rebuild step is identical to converting a sorted array into a BST.
- Uses [[recursion]] for both the traversal and the rebuild.