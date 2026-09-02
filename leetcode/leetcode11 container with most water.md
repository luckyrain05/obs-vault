You are given an integer [[arrays|array]] `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `ith` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return _the maximum amount of water a container can store_.

**Notice** that you may not slant the container.

# Solution

```python
def maxArea(self, height: List[int]) -> int:
	left, right = 0, len(height) - 1
	answer = 0
	maxh = max(height)
	
	while left < right:
		hl, hr = height[left], height[right]
		answer = max(
			answer, 
			(right - left) * min(height[left], height[right])
		)
		
		if answer >= maxh * (right - left):
			break
	
		if hl < hr:
			left += 1		
		elif hl >= hr:
			right -= 1
		
	return answer
```



