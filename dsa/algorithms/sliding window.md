- Many [[arrays|array]] problems ask for a subarray that satisfy a specific condition.
- Recomputing each subarray from scratch re-scans elements shared with its neighbor and frequently results in `O(n^2)` TC, often worse.
- A ==sliding window== is a [[greedy]] technique that keeps a running window and adjusts only its two edges as it moves, reusing everything in between instead of rescanning it.

# Fixed Window

- Suppose we must find the subarray with the biggest sum.

```python
def max_sum_fixed(arr, k):
	window_sum = sum(arr[:k])
	best = window_sum
	
	for i in range(k, len(arr)):
		window_sum += arr[i] - arr[i - k]
		best = max(best, window_sum)
	
	return best
```

## TS Complexity

- `O(n)` TC, `O(1)` SC.

## Explanation

1. Sum the first `k` elements to seed the window.
2. Slide one step: add the element entering the window, subtract the element leaving it.
3. Track the best window sum seen.

## Notes

- Brute force resums all `k` elements for every window: `O(n*k)`. Sliding reuses the overlap between adjacent windows instead, dropping that to `O(n)` — the whole reason the technique exists.

# Variable Window

- Expands to explore and contracts once some condition is met.

```python
def smallest_subarray(arr, target):
	left = 0
	window_sum = 0
	best = float('inf')

	for right in range(len(arr)):
		window_sum += arr[right]

		while window_sum >= target:
			best = min(best, right - left + 1)
			window_sum -= arr[left]
			left += 1

	return best if best != float('inf') else 0
```

## TS Complexity

- `O(n)` TC, `O(1)` SC.

## Explanation

1. Expand the window by moving `right` forward, adding each new element to `window_sum`.
2. Once the window satisfies the condition (`window_sum >= target`), shrink from `left` while it still holds, recording the smallest length along the way.
3. Each shrink removes the leftmost element from `window_sum` and advances `left`.

## Notes`

- `left` and `right` each only move forward, never backward — every element enters and leaves the window at most once. That's why this is still `O(n)` despite the nested loop.

# Longest Substring Without Repeating Characters

```python
def longest_unique_substring(s):
	seen = set()
	left = 0
	best = 0

	for right in range(len(s)):
		while s[right] in seen:
			seen.remove(s[left])
			left += 1
		seen.add(s[right])
		best = max(best, right - left + 1)

	return best
```

## TS Complexity

- `O(n)` TC, `O(min(n, alphabet size))` SC.

## Explanation

1. Expand the window by moving `right` forward.
2. If the incoming character is already in `seen`, shrink from `left`, removing characters from `seen` until the duplicate is gone.
3. Add the incoming character to `seen` and record the window length.

## Notes:`

- Same expand/contract skeleton as Variable Window, but the condition being tracked is membership, not a sum. So the window needs a [[hashs#Set|set]] for `O(1)` lookups.
