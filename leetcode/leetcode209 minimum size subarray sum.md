Given an array of positive integers `nums` and a positive integer `target`, return _the **minimal length** of a subarray whose sum is greater than or equal to_ `target`. If there is no such subarray, return `0` instead.

# Solution

```python
def minSubArrayLen(self, target: int, nums: List[int]) -> int:
	left = current_sum = 0
	answer = float('inf') 
	
	# increment right sentinel
	for right in range(len(nums)):
		current_sum += nums[right]

	# shrink left sentinel when we can	
	while current_sum >= target:
		# track valid candidates
		answer = min(min_length, right - left + 1)			
		current_sum -= nums[left]	
		left += 1	
		
	return answer if answer!= float('inf') else 0
```

# TS Complexity

- `O(n)` TC, `O(1)` SC

## Explanation

1. Establish two sentinels, left and right of the [[arrays|array]]. Progress right and check if we can shrink left at every iteration.
2. Use `float('inf')` and `min()` to compare every valid candidate, remaining one is naturally the smallest we've ever made.