Given a `triangle` [[arrays|array]], return _the minimum path sum from top to bottom_.

For each step, you may move to an adjacent number of the row below. More formally, if you are on index `i` on the current row, you may move to either index `i` or index `i + 1` on the next row.

# Solution

```python
def minimumTotal(triangle):
	dp = triangle[-1]
	
	for row in range(len(triangle) - 2, -1, -1):
		for col in range(len(triangle[row])):
			dp[col] = triangle[row][col] + min(dp[col], dp[col + 1])

	return dp[0]
```

## TS Complexity

- `O(n^2)` TC, `O(n)` SC, where `n` is the number of rows.

## Explanation

1. Start from the bottom most row.
2. Iterate through the row above, save the smaller sum path from the above row to the bottom row.
3. Repeat until we reach the top, this way, `dp[0]` at the end will naturally have the smallest possible sum for a full traversal. 

## Notes

- The brute force approach would essentially be [[beam search]], the amount of unique paths we can keep grows exponential.
- With [[dp#Tabulation|tabulation]], we are encoding the best possible path we could've taken at every iteration into `dp`. One sweep, all it takes.

