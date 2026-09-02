- Finds the majority element (appears more than `n/2` times) in an [[arrays|array]].
- Only works when a majority element is guaranteed to exist in said array.

```python
def boyer_moore(nums):
	candidate = count = 0
	
	for num in nums:
		if count == 0:
			candidate = num
		if num == candidate:
			count += 1
		else:
			count -= 1
	
	return candidate
```

##  TS Complexity

- `O(n)` TC, `O(1)`SC

## Explanation:

1. A [[greedy]] algorithm. Iterate through the array, choose first element as a candidate. Increment a vote if we see the same element twice, decrement if different.
2. When vote is below equal to 0, then we know that there are at least equal numbers of different elements at the current iteration. Thus we switch candidates to the current element.
3. Thus, the element that is majority will have more votes than the rest combined, and survive until the end as candidate.

## Notes

-  Other methods would require at least `O(n) SC`. A catch all method would be to use a [[hashs#Dictionary|dictionary]] to track the appearance of every element, but that would require `O(n)` SC, as we need a dictionary at least equal to the size of the array.
- But this only works when a majority element is guaranteed to exist in said array.

