- A heap is a [[trees]] stored as a flat [[arrays]], there are property constrains between parent and children that makes this data structure extremely useful. 
- ==Complete binary tree==. All levels filled except possibly the last, filled strictly left to right.
- `O(n)` to heapify an array, `O(logn)` to insert and extract from heap.

# Min-Heap

- Every parent ≤ its children, thus root is always smallest.
- `heapq.heapify(arr)` automatically assumes min heap.

```
          1          ← minimum
        /   \
       3     2
      / \   / \
     7   5 4   6

array: [1, 3, 2, 7, 5, 4, 6]
```

# Max-Heap

- Every parent ≥ its children, thus root is always largest.
- To implement max-heap behavior, multiply all values in an array by `-1`. This way, the largest number becomes the smallest.
	- `heapq.heapify([-x for x in arr]`
	- Remember to multiply by `-1` again to read the intended value.

```
          9          ← maximum
        /   \
       7     8
      / \   / \
     3   5 4   6

array: [9, 7, 8, 3, 5, 4, 6]
```

# Heapify

- Reorder an arbitrary, unsorted array into a heap. 

```python
def sift_down(heap, i, size):
    while 2 * i + 1 < size:
        left, right = 2 * i + 1, 2 * i + 2
        smallest = i
        
        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right
            
        if smallest == i:
            break
            
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest

def heapify(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, i, n)
```

- `O(n)` TC, `O(1)` SC
- Build a valid heap in-place from an unsorted array. Start at the last internal node (`n // 2 - 1`) and sift down to the root.
- Faster than inserting `n` elements one by one (`O(n log n)`).

**Real Example**

```
Input: [9, 4, 7, 2, 8, 1, 5]

As a tree:
           9         ← index 0
          / \
         4   7       ← index 1, 2
        / \ / \
       2  8 1  5     ← index 3, 4, 5, 6
```

- Leaf nodes will always satisfy heap constraints, so we skip those. 
- Last non-leaf is always at `n // 2 - 1`, since the number of nodes in the last row will always be 1 greater than the rest of the tree combined.

**Iteration 1:** 

```
Children: left = 5 (value 1), right = 6 (value 5)
Smallest child is 1 at index 5. 7 > 1, so swap.

           9
          / \
         4   1       ← 7 and 1 swapped
        / \ / \
       2  8 7  5
```

**Iteration 2:**

```
Children: left = 3 (value 2), right = 4 (value 8)
Smallest child is 2 at index 3. 4 > 2, so swap.

           9
          / \
         2   1       ← 4 and 2 swapped
        / \ / \
       4  8 7  5
```

**Iteration 3:**

```
Children: left = 1 (value 2), right = 2 (value 1)
Smallest child is 1 at index 2. 9 > 1, so swap.

           1
          / \
         2   9       ← 9 and 1 swapped
        / \ / \
       4  8 7  5

9 is not done — it must keep sifting down.
Children of index 2: left = 5 (value 7), right = 6 (value 5)
Smallest is 5 at index 6. 9 > 5, so swap.

           1
          / \
         2   5       ← 9 and 5 swapped
        / \ / \
       4  8 7  9

9 has no children. Stop.
```

# Insert

```python
def insert(heap, val):
    heap.append(val)
    i = len(heap) - 1
    
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] > heap[i]:   # flip > to < for max-heap
            heap[parent], heap[i] = heap[i], heap[parent]
            i = parent
        else:
            break
```

- `O(log n)` TC, `O(1)` SC
- Append to end, then sift up: swap with parent until heap property holds.

# Extract

```python
def extract_min(heap):
    if len(heap) == 1:
        return heap.pop()
    root = heap[0]
    heap[0] = heap.pop()
    i = 0
    
    while True:
        left, right = 2 * i + 1, 2 * i + 2
        smallest = i
        if left < len(heap) and heap[left] < heap[smallest]:
            smallest = left
        if right < len(heap) and heap[right] < heap[smallest]:
            smallest = right
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
        
    return root
```

- `O(log n)` TC, `O(1)` SC
- Swap root with last element, pop last, then sift down: swap with the smaller child until heap property holds.

# heapq

- ==heapq== is python's heap external heap library, import with `import heapq`.
- `heapq` APIs are capable of heap function covered above, and more.

```python
import heapq

'''
Heapify — O(n)
'''
arr = []
heapq.heapify(arr)

'''
Insert — O(log n)
'''
heapq.heappush(heap, val)

'''
Remove and return min — O(log n)
'''
popped = heapq.heappop(heap)

'''
Peek min without removing — O(1)
'''
heap[0]

'''
Push then pop. Returns smaller of val or current min — O(log n)
Faster than heappush + heappop separately.
'''
result = heapq.heappushpop(heap, val)

'''
Pop then push. Raises IndexError if empty — O(log n)
Faster than heappop + heappush separately.
'''
result = heapq.heapreplace(heap, val)

'''
k smallest / k largest — O(n log k)
Obviously if k = n, TC would equal to sort()
'''
heapq.nsmallest(k, iterable)
heapq.nlargest(k, iterable)

'''
In case of tuples, heap sorted by first element, ties broken by second.
'''
heapq.heappush(heap, (priority, item))
```
