Shift every element of an array to the right by k positions, wrapping around the end, and do it in place. k is non-negative and can be larger than the array length. Aim for an O(1)-space solution.

# Solution

```python
class Solution:
	def rotate_array(array, k):
		index = 0
		prev = array[0]
		visited = set()
		
		for _ in range(len(arary)):
			index %= len(carry)
			if index in visited:
				index += 1
			
			curr = array[index + k]
			array[index + k] = prev
			prev = curr
			index += k
```