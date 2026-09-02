Given one json object as a string, write a function to parse the json object's fields into a dict. 

- The Json object will have correct syntax, but may not be correctly formatted. There could be whitespaces anywhere that is allowed.

# Brute Force Solution

```python
def parseJson(json_str) -> dict:
    ans = {}
    s = json_str.strip()
    i, n = 1, len(s) - 1

    def skipWhite(i):
        while i < n and s[i] == ' ':
            i += 1
        return i

    while i < n:
        i = skipWhite(i)
        
        if s[i] == '"':
            i += 1
            k = i
            while s[i] != '"':
                i += 1
            key = s[k:i]
            i += 1  # skip closing "
            
        i = skipWhite(i)
        
        if s[i] == ':':
            i += 1
        i = skipWhite(i)
        
        if s[i] == '"':
            i += 1
            v = i
            while s[i] != '"':
                i += 1
            ans[key] = s[v:i]
            i += 1  # skip closing "
            
        i = skipWhite(i)
        
        if i < n and s[i] == ',':
            i += 1
            
    return ans
```

## TS Complexity

- `O(n)` TC and `O(k)` SC, `n` being the length of the string, and `k` the number of param pairs

## Explanation

1. Set two pointers: `i` and another to be defined.
2. When we encounter a `"` character, it is guaranteed that the following text after is a field. If first opening `"`, then it is a key. If its the second, it is a value.
3. Set a new pointer at `i`, increment `i` until we reach another `"`. Read everything in between as a `key` variable. 
4. Ignore white spaces, `,`, `:` as they appear.
5. Loop until i reaches n, the index before the closing.

# [[regex]] Solution

```python
import re

def parseJson(json_str):
    return dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]*)"', json_str))
```

## TS Complexity

- Still `O(n)` TC and `O(k)` SC.

## Explanation

## Notes

- Actually slower than brute force implementation due to the regex engine overhead, but much more elegant.


