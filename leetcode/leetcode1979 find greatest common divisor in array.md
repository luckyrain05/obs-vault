Given an integer [[arrays|array]] `nums`, return _the **greatest common divisor** of the smallest number and largest number in_ `nums`.

The **greatest common divisor** of two numbers is the largest positive integer that evenly divides both numbers.

# Solution

```python
def findGCD(self, nums: List[int]) -> int:

	def euclidean(int: a, int: b) -> int:
		if a == 0:
			return b
		elif b == 0:
			return a
		elif a == b:
			return a
		elif a > b: 
			bigger, smaller = a, b
		else: 
			bigger, smaller = b, a
		
		while True:
			bigger, smaller = smaller, bigger % smaller
			
			if smaller == 0:
				return bigger
	
	# find biggest and smallest in one pass
	mx, mn = float('-inf'), float('inf')
	for num in nums:
		if num > mx: mx = num
		if num < mn: mn = num
	
	return euclidean(mn, mx)
```

## TS Complexity

- `O(n)` TC, `O(1)` SC 

## Explanation

1. [[array searching|Find biggest]] and smallest in the array with one pass.
2. Use [[euclidean's algorithm]] based on step 1.

## Notes

- We can also use `math.gcd()` here, but its 50% less memory efficient according to LC.