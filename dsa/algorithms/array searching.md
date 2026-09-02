- Algorithms below finds element(s) in an [[arrays|array]].

# Linear Search

```python
def linear_search(arr, target):
	for i in range(len(arr)):
		if arr[i] == target:
			return i
	return -1
```

- `O(n)` TC, `O(1)` SC.
- Checks every element in the array one by one until the target is found or the end is reached.

# Binary Search

```python
def binary_search(arr, target):
	low, high = 0, len(arr) - 1
	while low <= high:
		mid = (low + high) // 2
		if arr[mid] == target:
			return mid
		elif arr[mid] < target:
			low = mid + 1
		else:
			high = mid - 1
	return -1
```

- `O(log N)` TC, `O(1)` SC.
- Only works for sorted arrays.
- Repeatedly splits a sorted array in half, comparing the middle element to the target.
- If the target is smaller, search the left half. If larger, search the right half.

# Top K Search

```python
import heapq

def top_k_sort(arr, k):
	if k >= len(arr):
		return sorted(arr)

	heap = arr[:k]
	heapq.heapify(heap)

	for num in arr[k:]:
		if num > heap[0]:
			heapq.heapreplace(heap, num)

	return heap
```

- `O(n log k)` TC, `O(k)` SC.
- Returns the largest or smallest k elements of an array.
- Maintains a [[heaps#heapq|heapq]] of size k. Iterate through the array, if the current element is larger than the heap's minimum, replace it. At the end, the heap contains the k largest elements.