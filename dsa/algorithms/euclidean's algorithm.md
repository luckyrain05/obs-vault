- An recursive algorithm that give us the greatest common denominator for a pair of positive integers $(a, b)$.

1. Identify which number is bigger.
2. Now let  `big = big % small`.
3. Now it is guaranteed that the smaller number is now bigger.
4. Repeat step two and three until one number = 0, in which case the other number is the greatest common denominator.

- If either $a$ or $b$ is 0, we consider the other non-zero integer to be the GCD. 
- If both $a$ and $b$ are 0, we consider the GCD to be 0.

# [[recursion|Recursive]] Implementation

- The natural implementation, since the algorithm is mathematically considered recursive.

```python
def euclidean(int: a, int: b) -> int:
	# base case
	if a == 0:
		return b 
	if b == 0:
		return a
	if a == b: 
		return a
		
	# define bigger and smaller
	if a > b: 
		bigger, smaller = a, b
	else: 
		bigger, smaller = b, a
	
	# recursive case and return	
	ans = euclidean(bigger % smaller, smaller)
	return ans	 
```

- `O(1)` TC, `O(1)` SC.

# [[dp#Tabulation|Tabulation]] Implementation

- Only the latest $(a, b)$ pair is relevant for an answer.
- Much more memory efficient since we are not keeping call stacks.

```python
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
```

- `O(1)` TC, `O(1)` SC.

# gcd library

- Python has a native gcd library.

```python
from math import gcd

gcd  = gcd(a, b)
gcd1 = math.gcd(a, b) # also works
```

