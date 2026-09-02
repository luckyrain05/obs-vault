Given the `root` of a [[trees#Binary Search Tree|binary tree]], return _the level order traversal of its nodes' values_. (i.e., from left to right, level by level).

# Solution

```python
def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
    if not root:
        return []
	
    queue = deque([root])
    result = []
	
    while queue:
        layer_vals = []
		
        for _ in range(len(queue)):
            node = queue.popleft()
            layer_vals.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
		
        result.append(layer_vals)
	
    return result
```

## TS Complexity:

- `O(n)` TC, `O(n)` SC
- Required to traverse through all nodes, and store all nodes as the answer.

## Explanation

1. Outside of the standard [[trees#Inorder|inorder traversal]], the answer format must contain every level in its own [[arrays|array]]. This makes things trickier.
2. Key observation is that at every iteration of the while loop, `queue` holds one layer.
3. Thus, we use a for loop to iterate through queue to append the entire layer at once, standard [[bfs]] grabs only one element at a time, breaking the required answer format.

## Notes

- This one stumbled me when it shouldn't have.
- Below is the incorrect solution I've drafted.

```python

def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
    #edge case
    if not root:
        return []

    #queue
    queue = deque([[root]])
    result = []

    while queue:
        layer = queue.popleft()
        next_layer = [] # objects
        layer_vals = [] # ints

        for node in layer:
            layer_vals.append(node.val)
            
            if node.left:
                next_layer.append(node.left)
            
            if node.right:
                next_layer.append(node.right)
        
        queue.append(next_layer) 
        result.append(layer_vals)
            
    return result
```

-  `next_layer` is constructed and appended to `queue` at every iteration of the while loop. **Python will return truthy for objects holding any elements, even if the elements themselves are empty,** creating an infinite loop.
- `queue` holding a list as the next layer also was not necessary, although it wouldn't effect performance too much.
- Also remember that in [[bfs]], the queue always holds only the next layer.