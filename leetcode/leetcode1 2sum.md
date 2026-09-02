Given an [[arrays|array]] of integers `nums` and an integer `target`, return _indices of the two numbers such that they add up to `target`_.

You may assume that each input would have **_exactly_ one solution**, and you may not use the _same_ element twice.

You can return the answer in any order.

# Solution

```python
def twoSum(self, nums: List[int], target: int) -> List[int]:
	seen = {}
	
	for i in range(nums):
		if (target - num) in seen:
			return [i, seen[target-num]]
		
		seen[target-num] = i
	
	return []
```

## TS Complexity

- `O(n)` TC, `O(n)` SC.

## Explanation

1. Iterate through `nums`, track every value we've seen and their indices with a [[hashs#Dictionary|dictionary]]. 
2. Then, check if the complement exists. If so, return the two indices. 
3. If we do not find anything answer does not exist.

## Notes

- [[greedy]]

