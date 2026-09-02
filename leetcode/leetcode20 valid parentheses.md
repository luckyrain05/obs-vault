Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

# Solution

```python
def isValid(self, s: str) -> bool:
    stack = []
    match = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in match and \
	        (not stack or stack.pop() != match[char]):
            return False
            
        else:
            stack.append(char)
    
    return not stack
```

## TS Complexity

- `O(n) TC, O(n) SC`.

## Explanation

1. Use an [[arrays|array]] to implement a [[stacks#Stack|stack]], and a [[hashs#Dictionary|dictionary]] to track the opposite parentheses.
	- Use the closing as the key, and opening as the value.
	- The stack tracks our past iterations.
2. For every char in the input string, check if it is a closing parentheses. If it is, the one right before it should be the corresponding opening parentheses. 
3. If it is not the case outlined above, our string is invalid. Return false.
4. If it is the case, do not add the closing parentheses to the stack, use `.pop()` to remove the opening one, thus neither appears in the stack.
5. As a result, if anything is left on the stack, the string is also invalid. 

## Notes

- Python's `.pop()` allows arrays to exhibit LIFO order as well, remember this.