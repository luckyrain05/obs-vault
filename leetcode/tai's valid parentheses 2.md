Almost exactly as the leetcode question [[leetcode20 valid parentheses|valid parentheses]], but the input can contain anything in addition to the bracket characters. A little warm up drill.

# Solution

```python

def isValid(self, s : str) -> bool:
	stack = []
	closing = { '}' : '{', ']' : '[', ')' : '(' }
	opening = { '{', '[', '(' }
	
	
	for char in s:
		if char in opening:
			stack.append(char)
		
		if char in closing and \
			(stack.pop() != closing[char] or not stack):
			return False
			
		else:
			continue
		
		return True
```

## TS Complexity

- `O(n)` TC, `O(n)` SC

## Explanation

1. Same logic as [[leetcode20 valid parentheses|valid parentheses]], except we need a new set `opening` to detect if the character we have landed on should be ignored, or tracked.
## Notes

