# Stack

- ==Stack== is a LIFO data structure.
- It is purely conceptual, ANY implementation that stores data in LIFO is a stack.

- A stack should at least support two operations. `push` adds to the top, `pop` removes from the top.

# [[arrays|Array]] Implementation

- Arrays are naturally LIFO. 
- Array version is simpler and has better cache locality.

```python
arr = []     # assume it is populated.
arr.append() # adds to top
arr.pop()    # removes from top 
```

- `O(1)` TC for push, pop, peek. `O(n)` SC.

# [[linked lists]] Implementation

- Like pretty much all conceptual data structures, we can also use objects to represent them.
- In practice this approach is easier, but there is pointer overhead. 

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, val):
        node = Node(val)
        node.next = self.top
        self.top = node

    def pop(self):
        if not self.top:
            return None
        val = self.top.val
        self.top = self.top.next
        return val

    def peek(self):
        if not self.top:
            return None
        return self.top.val

    def is_empty(self):
        return self.top is None
```

- `O(1)` TC for push, pop, peek. `O(n)` SC.

