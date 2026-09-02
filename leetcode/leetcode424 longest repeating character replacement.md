You are given a [[arrays|string]] `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.

Return _the length of the longest substring containing the same letter you can get after performing the above operations_.

# Solution

```python
def characterReplacement(self, s: str, k: int) -> int:

	freq = {}	
	left = answer = max_freq = 0
		
	for right in range(len(s)):
		if s[right] in freq:
			freq[s[right]] += 1
		else:
			freq[s[right]] = 1
		
		max_freq = max(freq[s[right]], max_freq)
		
		if (right - left + 1) - max_freq > k:
			freq[s[left]] -= 1
			left += 1
		
		answer = max(answer, right - left + 1)
	
	return answer
```

## TS Complexity

- `O(n)` TC, `O(n)` SC
- [[sliding window]] is `O(n)`, and our dictionary, in the worst case, will be the size of the array.

## Explanation

- A typical [[sliding window]] problem, but the validity condition is not immediately obvious, one if statement will not do it.
- We have to use a [[hashs#Dictionary|dictionary]] to track the frequency of all elements in the current window, because the largest subarray will always be the most frequent character + `k`.

## Notes

- We cannot carelessly slide the left pointer with a while loop until the sub array is valid again. This is not like [[leetcode209 minimum size subarray sum]] or [[leetcode3 longest substring without repeating characters]]. 
- Issue is `k`, the most frequently appearing character can change as the left pointer moves. We must reevaluate it at every iteration, which a nested while loop cannot do.