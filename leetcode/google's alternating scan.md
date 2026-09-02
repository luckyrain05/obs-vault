
Given an integer [[arrays|array]] `nums`, a starting index `s`, and an integer `offset`, simulate an alternating traversal process and return the number of valid operations performed.

Start at the index `s`, with **operation 1**.

**Operation 1:** From the current position, scan **left**. Find the first element `e` where `e == nums[current] + 1`. Replace it with `nums[current] + offset`. Move to `e`'s index. Proceed to Operation 2.

**Operation 2:** From the current position, scan **right**. Find the first element `e` where `e == nums[current] + 1`. Replace it with `nums[current] + offset`. Move to `e`'s index. Proceed back to Operation 1.

Repeat until no valid element is found. Return the number of operations successfully completed.

# Solution

```python
def scan(nums: List[int], s: int, offset: int) -> int:
	# offset canot be -1
	if offset == -1: return 0 	
	
	# create dict from the array
	pos_of = {}
	for i in range(len(nums)):
		if nums[i] not in pos_of: pos_of[nums[i]] = []
		pos_of[nums[i]].append(i)
	
	ops = 0
	curr_val = nums[s]
	
	while True:
		target = curr_val + 1
		# if value does not exist, nuke the function
		if target not in pos_of or len(pos_of[target]) == 0: break
		
		positions = pos_of[target]
		
		# see if we are scanning left or right
		if ops % 2 == 0: 
			r = range(len(positions) - 1, -1, -1)
			cmp = lambda a, b : a < b
		else: 
			r = range(len(positions))
			cmp = lambda a, b : a > b
		
		for i in r:
			if cmp(positions[i], s)
				# add new_val to the hash
				new_val = curr_val + offset
				if new_val not in pos_of: pos_of[new_val] = []
				
				# "move" to new pos by setting s to it
				s = positions[i]
				pos_of[new_val].append(s)
				curr_val = new_val
				break
		
		else: break
		
		op += 1
	
	return ops
```

## TS Complexity

 - `O(n)` TC, `O(n)` SC.
 
## Explanation

1. Represent the array using a [[hashs#Dictionary|dictionary]], with the data in `nums` being the key and their indexes the value as an array. 
2. Calculate target before our search. If target exists in the array, check if its in a valid position relative to the current index (left or right). 
	1. To do so, use a 2 pointer approach, `i` and `s`. `s` is provided as the starting index, use`i` to traverse the list of indexes of our target.
	2. Since `positions` is in an increasing order, to find the nearest valid value that is left of `s`, we must increment in reverse.
	3. If `positions[i]` is a value that is on the left/right, we have found the nearest valid position of our target value. 
3. Modify our dictionary to simulate that it has been replaced by `curr_val + offset`. 
	1. Create a new dict entry for `new_val`, and its position.
	2. Update `s` to be the position of our target `position[i]`.
	3. `.pop()` is not needed, since mathematically the same node cannot be visited twice unless `offset` is `-1`, in which case an infinite loop will occur as well.

## Notes

-  The obvious brute force approach uses essentially [[array searching#Linear Search|linear search]] resulting in `O(n^2)` runtime. 
- If offset is `-1`, an infinite loop could occur, where a value `n` searches for value `n+1` and replaces it with `n-1`. In which case it is guaranteed that the following scan in the opposite direction will reach `n` again, replacing it with `n-2`, looping infinitely.
	- This constraint should be clearly communicated with to the interviewer.
	- In every other case, the same value cannot be revisited.


