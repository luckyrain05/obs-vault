- A linked list is a sequence of node [[oop|objects]] where each node stores a value and a pointer to the next node. 
- Alternative implementation of a list to [[arrays]], situationally better.

**Pros**

- Insertion and deletion are `O(1)` given a reference to the node, since traversal and reodering is not required.

 **Cons**
 
- Elements are not stored contiguously in [[memory#Memory Addresses|memory]], therefore does not benefit from [[cache#Cache Locality|cache locality]].
- Access is `O(n)`. No index arithmetic, must traverse from the head.
- MUCH more memory intensive, each element is a [[memory#Pointers|pointer]] holding an object.

# Memory Layout

- Nodes are scattered across memory. Each node holds a value and a reference to the next node.

```
head → [10 | *] → [20 | *] → [30 | *] → None

+----------+        +----------+        +----------+
| val:  10 |        | val:  20 |        | val:  30 |
| next: ------→    | next: ------→    | next: None |
+----------+        +----------+        +----------+
  addr 47             addr 102            addr 5
```

- Addresses are arbitrary — nodes can live anywhere in memory.

# Singly Linked List

- Each node has a `val` and a `next` pointer.

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
```

- Build a list by chaining nodes:

```python
class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, val):
        node = Node(val)
        node.next = self.head
        self.head = node

    def append(self, val):
        node = Node(val)
        if not self.head:
            self.head = node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = node

    def delete(self, val):
        if not self.head:
            return
        if self.head.val == val:
            self.head = self.head.next
            return
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                return
            curr = curr.next

    def search(self, val):
        curr = self.head
        while curr:
            if curr.val == val:
                return curr
            curr = curr.next
        return None
```

# Operations

**Prepend** — `O(1)` TC. Set new node's next to head, update head.
**Append** — `O(n)` TC. Traverse to tail. `O(1)` with a tail pointer.
**Delete** — `O(n)` TC. Traverse to find the node before the target.
**Search** — `O(n)` TC. Linear traversal.
**Access by index** — `O(n)` TC. No direct indexing.
- All operations `O(1)` SC.

# Doubly Linked List

- Each node has `val`, `next`, and `prev` pointers.
- Traversal works in both directions. Deletion of a known node is `O(1)` without needing to find the previous node.

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None
```

- Python's `collections.deque` is a doubly linked list under the hood.

# Dummy Head

- A ==dummy head== (also called sentinel node) is a placeholder node at the start of the list.
- Eliminates edge cases for operations on the first node — no special `if not head` checks.
- The real list starts at `dummy.next`.

```python
dummy = Node(0)
dummy.next = head

# after operations:
return dummy.next  # new head
```

# Reverse

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

- `O(n)` TC, `O(1)` SC.

1. Save `curr.next` before overwriting it.
2. Point `curr.next` back to `prev`.
3. Advance `prev` and `curr` forward.
4. When `curr` is `None`, `prev` is the new head.

# Cycle Detection

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

- `O(n)` TC, `O(1)` SC.
- Slow moves 1 step, fast moves 2 steps. If they meet, there is a cycle.

# Find Middle

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

- `O(n)` TC, `O(1)` SC.
- When fast reaches the end, slow is at the middle node.
