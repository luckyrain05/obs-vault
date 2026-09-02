Write a function that returns the `n` index of the fib sequence.

# [[recursion|Recursive]] Solution

```python
def fib(n):
	if n == 0:
		return 0
	if n == 1:
		return 1
	
	return fib(n-1) + fib(n-2)
```

## TS Complexity

- `O(2^n)` TC, `O(n)` SC.

## Explanation

## Notes

# [[dp|Memoization]] Solution

```python
# Memoization
def fibonacci(n, memo={}):
    if n <= 1: return n
    if n in memo: return memo[n]
    
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]
```

## TS Complexity

- `O(n)` TC, `O(n)` SC.

## Explanation

## Notes

# [[dp|Tabulation]] Solution

```python
# Tabulation
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

## TS Complexity

- `O(n)` TC, `O(1)` SC.

## Explanation

## Notes

- Tabulation [[dp]] is technically the most efficient solution. 
- But all solutions here are good simple examples to recursion and dp.
