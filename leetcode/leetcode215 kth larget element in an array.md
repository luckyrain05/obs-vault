Given an integer [[arrays|array]] `nums` and an integer `k`, return _the_ `kth` _largest element in the array_.

Note that it is the `kth` largest element in the sorted order, not the `kth` distinct element.

# Brute Force Solution

```python
def findKthLargest(self, nums: List[int], k: int) -> int:
	return heapq.nlargest(k, nums)[k-1]
```

## TS Complexity

- This is extremely slow as `heapify` is `O(n)` and `heap.nlargest` is another `O(n * log k)`.

## Explanation

## Notes

# Optimal Solution

```python
def findKthLargest(self, nums: List[int], k: int) -> int:
	if k == len(nums):
		return sorted(nums)[0]
		
    heap = nums[:k]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
            
    return heap[0]
```

## TS Complexity

- `O(n)` TC, `O(k)` SC.

## Explanation

1. Keep a `k` sized min heap from the first `k` number of the array.
2. Iterate from `k`, for every number bigger than the smallest number in the heap, replace it.
3. By the end, the min-heap should contain the biggest `k` numbers in `nums`. Simply return `heap[0]` for the answer.

## Notes

- This is simplify performing a [[array searching#Top K Sort]].



