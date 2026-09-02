# Use Case

- If a problem has **overlapping subproblems** (same computation done multiple times) and **optimal substructure** (optimal solution is built from optimal solutions to subproblems), DP applies.
- Two approaches: **top-down** ==(memoization)== and **bottom-up** ==(tabulation)==.

# Memoization

- Consider the following [[recursion||recursive]] function to return the value of index `n` of the fib sequence.

```python
def fib(n):
	if n <= 1:
		return n
	return fib(n - 1) + fib(n - 2)
```

- This is has `O(2^n)` TC because the call stack is essentially a binary tree. `O(n)` SC because only one branch ( `fib(n-1)` first,  then `fib(n-2)`) is on the stack at a time. 

```
                fib(5)
              /        \
          fib(4)        fib(3)     ← fib(3) computed TWICE
         /    \        /    \
      fib(3) fib(2) fib(2) fib(1) ← fib(2) computed THREE times
      /   \
   fib(2) fib(1)
```

- We can avoid building a full binary tree by adding memoization to our solution.

```python
def fib(n, memo={}):
	if n <= 1:
		return n
	if n in memo:
		return memo[n]
	memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
	return memo[n]
```

- Now `O(n)` TC and `O(n)` SC. Each subproblem computed exactly once.

# Tabulation

- Use an table to store where each index represents a subproblem.
- No recursion, no call stack,  purely iterative.

```python
def fib(n):
	if n <= 1:
		return n
		
	dp = [0] * (n + 1)
	dp[1] = 1
	
	for i in range(2, n + 1):
		dp[i] = dp[i - 1] + dp[i - 2]
		
	return dp[n]
```

- Also `O(n)` time and `O(n)` space.

# Space Optimization

- If a subproblem only depends on a fixed number of previous subproblems, you don't need the whole table.
- For Fibonacci, you only need the last two values:

```python
def fib(n):
	if n <= 1:
		return n
		
	prev2, prev1 = 0, 1
	
	for i in range(2, n + 1):
		curr = prev1 + prev2
		prev2 = prev1
		prev1 = curr
		
	return prev1
```

- `O(n)` TC, `O(1)` SC. 
- [[google's largest square farmland]] is a good example, its solution only uses two rows at a time.