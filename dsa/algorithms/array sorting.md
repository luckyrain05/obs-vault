- The following are the main [[arrays]] sorting algorithms. 
- `O(n log n)` is the fastest known TC for complete sorts.

# Merge Sort

```python
def merge_sort(arr):
	if len(arr) <= 1:
		return arr

	mid = len(arr) // 2
	left = merge_sort(arr[:mid])
	right = merge_sort(arr[mid:])

	return merge(left, right)

def merge(left, right):
	result = []
	i, j = 0, 0
	
	while i < len(left) and j < len(right):
		if left[i] <= right[j]:
			result.append(left[i])
			i += 1
		else:
			result.append(right[j])
			j += 1
			
	result.extend(left[i:])
	result.extend(right[j:])
	
	return result
```

- `O(n log n)`TC in all cases, `O(n)` SC.
- Split the array in half [[recursion]], then merges the sorted halves back together.

# Quick Sort

```python
def quick_sort(arr, low, high):
	if low < high:
		pivot_index = partition(arr, low, high)
		quick_sort(arr, low, pivot_index - 1)
		quick_sort(arr, pivot_index + 1, high)

def partition(arr, low, high):
	pivot = arr[high]
	i = low - 1
	
	for j in range(low, high):
		if arr[j] <= pivot:
			i += 1
			arr[i], arr[j] = arr[j], arr[i]
	arr[i + 1], arr[high] = arr[high], arr[i + 1]
	
	return i + 1
```

- `O(n log n)` TC average case, `O(n^2)` worst case. `O(log n)` SC.
- Picks a pivot, partitions the array so elements less than pivot go left and greater go right. Recursively repeat this step with the moved indexes as new pivots.
- Despite worse TC than merge sort, it is usually faster due to superior [[cache#Cache Locality|cache locality]].

# Insertion Sort

```python
def insertion_sort(arr):
	for i in range(1, len(arr)):
		key = arr[i]
		j = i - 1
		
		while j >= 0 and arr[j] > key:
			arr[j + 1] = arr[j]
			j -= 1
		arr[j + 1] = key
		
	return arr
```

- `O(n^2)` TC worst and average case, `O(n)` only when array already sorted.
- Iterates through the array, and for each element, shifts it left until it is in the correct position relative to the already-sorted portion.
- Essentially dog shit, do not use.



