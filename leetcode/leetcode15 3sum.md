Given an integer [[arrays|array]] nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

# [[leetcode1 2sum]] solution

```python
def threeSum(self, nums: list[int]) -> list[list[int]]:
	answer = []
	dupe = set()
	
	for i in range(len(nums)-2):	
		seen = set()
		
		for j in range(i + 1, len(nums)):
			target = -nums[i] - nums[j]
			
			if target in seen:
				candidate = tuple(sorted((nums[i], target, nums[j])))
				
			if candidate not in dupe:
				dupe.add(candidate)
				answer.append(list(candidate))
				seen.add(nums[j])
			
		return answer
```

## TS Complexity

- `O(n^2)` TC, `O(n^2)` SC
- `dupe` will have worst case $n^2$ distinct triplets

## Explanation

1. Lock one element of the array, what we have left is the classic [[leetcode1 2sum]].
2. Hard part is the deduplication logic. Since the array is not sorted, we are expected to find 2 triplets that are identical in value but not order. Thus, we need to sort all of our answers so that identical triplets will match in a [[hashs#Set|set]].

## Notes

- **Lists are NOT hashable.** Must use tuples then `list()` after.

# [[two pointer]] Solution

```python
def threeSum(self, nums: list[int]) -> list[list[int]]:
	nums.sort
	n = len(nums)
	answer = []
	
	for i in range(n - 2):
		if nums[i] > 0:
			return answer
		
		if i > 0 and nums[i] == nums[i - 1]:
			continue
		
		left, right = i + 1, n - 1
		
		while left < right:
			total = nums[i] + nums[left] + nums[right]
			
			if total < 0:
				left += 1
				
			elif total > 0:
				right -= 1
				
			else:
				answer.append([nums[i], nums[left], nums[right]])
				left += 1
				right -= 1
				
				while left < right and nums[left] == nums[left - 1]:
					left += 1
				while left < right and nums[right] == nums[right + 1]:
					right -= 1
	
	return answer
```

## TS Complexity

- `O(n^2)` TC, `O(n^2)` SC
- Some conventions define SC as **auxiliary** space: everything we allocate _beyond_ the required output. In that case, SC is `O(n)`
- Point is, this solution is much more space conserving.

## Explanation

1. Instead of 2sum, we employ something similar to [[array searching#Binary Search|binary search]].
2. [[array sorting|Sort]] the array, `nlogn` is worth it here.
3. Lock one index, like the previous approach.
4. Employ 2 converging pointers and not a hash. Since array is sorted, we know which pointer to move up or down depending on our current sum. No need for hash.
5. Sorting guarantees uniqueness if we skip all neighboring duplicates.

## Notes:

- While loops can be tricky, remember that the check happens after the while loop finishes its iteration.
- Uglier code doesn't mean worse code. Much better than 2sum solution.



