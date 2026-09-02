- ==Queue== is a FIFO (first in, first out) data structure.
- It is purely conceptual, any implementation that stores data in FIFO is a queue.
- Two operations: `enqueue` adds to the back, `dequeue` removes from the front.
- Think of a line at a store. First person in line is the first person served.

# Array Implementation

```python
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, val):
        self.items.append(val)

    def dequeue(self):
        if not self.items:
            return None
        return self.items.pop(0)

    def peek(self):
        if not self.items:
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0
```

`O(1)` TC for enqueue and peek. `O(n)` TC for dequeue (shifts all elements). `O(n)` SC.

- Dequeue is `O(n)` because `pop(0)` shifts every element left. Use `deque` to avoid this.

# Deque Implementation

```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, val):
        self.items.append(val)

    def dequeue(self):
        if not self.items:
            return None
        return self.items.popleft()

    def peek(self):
        if not self.items:
            return None
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0
```

`O(1)` TC for enqueue, dequeue, peek. `O(n)` SC.

- ==deque== (double-ended queue) is a doubly linked list under the hood, so `popleft()` is `O(1)`, always use this.

# [[linked lists]] Implementation

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, val):
        node = Node(val)
        if self.tail:
            self.tail.next = node
        self.tail = node
        if not self.head:
            self.head = node

    def dequeue(self):
        if not self.head:
            return None
        val = self.head.val
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return val

    def peek(self):
        if not self.head:
            return None
        return self.head.val

    def is_empty(self):
        return self.head is None
```

`O(1)` TC for enqueue, dequeue, peek. `O(n)` SC.

- Maintain both `head` and `tail` pointers so enqueue and dequeue are both `O(1)`.

# collections.deque

- ==collections.deque== is Python's built-in double-ended queue. Import with `from collections import deque`.
- Supports `O(1)` append and pop from both ends.

```python
from collections import deque

q = deque()

q.append(val)       # add to right end — O(1)
q.appendleft(val)   # add to left end — O(1)
q.pop()             # remove from right end — O(1)
q.popleft()         # remove from left end — O(1)
q[0]                # peek left — O(1)
q[-1]               # peek right — O(1)
len(q)              # number of elements — O(1)
```

- For a standard queue: `append` to enqueue, `popleft` to dequeue.
