Given a string `s`, find the length of the **longest** without duplicate characters.

# Solution

```python
def lengthOfLongestSubstring(self, s: str) -> int:
	seen = set()
	left = answer = 0
	  
	for right in range(len(s)):
		while s[right] in seen:
			seen.remove(s[left])
			left += 1
			
		seen.add(s[right])
		answer = max(answer, right - left + 1)
	
	return answer
```

## TS Complexity

- `O(n)` TC, `O(n) SC`

## Explanation

1. Use [[sliding window]], very self explanatory.

## Notes

- Main lesson here is the RAW and WAW errors that can happen.

**WAW**

```python
left += 1
seen.remove(s[left])
```

- If we increment the left pointer without removing the element from `seen` first, the element at index `left` before `+= 1` executes remains in the set.
- In any [[two pointer]] solution, **always execute action before moving a pointer.** 

**RAW**

```python
seen.add(s[right])
while s[right] in seen:
```

- If we add to `seen` before checking for duplicates, the `while` will always return true.
- It's asking if `s[right]` is in the set. No shit, we just put it in.