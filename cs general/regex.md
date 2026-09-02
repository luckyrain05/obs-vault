- ==Regular expressions== are patterns used to match character combinations in strings.
- A regex pattern is read left to right. Each piece of the pattern must match in order.
- Python uses the `re` module. Always use ==raw strings== (`r""`) so backslashes are treated literally.

```python
import re

re.search(r"pattern", "string")   # first match anywhere in string, or None
re.match(r"pattern", "string")    # match only at the start of string
re.findall(r"pattern", "string")  # list of all matches
re.sub(r"pattern", "repl", "string")  # replace all matches
```

# Literal Characters

- Most characters match themselves. `abc` matches the string "abc".
- Special characters need to be escaped with `\` to match literally: `\.` `\*` `\+` `\?` `\(` `\)` `\[` `\{` `\\`

```python
re.search(r"abc", "xabcx")       # <Match: 'abc'>
re.search(r"3\.14", "3.14")      # <Match: '3.14'>
re.search(r"3.14", "3X14")       # <Match: '3X14'> (. matches any char)
```

# Character Classes

- `[abc]` matches any one of a, b, or c.
- `[a-z]` matches any lowercase letter. `[0-9]` matches any digit.
- `[^abc]` matches any character that is not a, b, or c. `^` inside brackets means negation.
- Ranges can be combined: `[a-zA-Z0-9]` matches any alphanumeric character.

```python
re.findall(r"[aeiou]", "hello")        # ['e', 'o']
re.findall(r"[0-9]", "a1b2c3")        # ['1', '2', '3']
re.findall(r"[^0-9]", "a1b2c3")       # ['a', 'b', 'c']
```

# Shorthand Classes

- `\d` matches any digit, same as `[0-9]`.
- `\w` matches any word character, same as `[a-zA-Z0-9_]`.
- `\s` matches any whitespace (space, tab, newline).
- Uppercase inverts them: `\D` is non-digit, `\W` is non-word, `\S` is non-whitespace.
- `.` matches any character except newline.

```python
re.findall(r"\d+", "age: 25, id: 100")    # ['25', '100']
re.findall(r"\w+", "hello world!")         # ['hello', 'world']
re.findall(r"\s", "a b\tc")               # [' ', '\t']
```

# Quantifiers

- Quantifiers go after the thing they apply to.
- `*` matches 0 or more. `a*` matches "", "a", "aa", "aaa", etc.
- `+` matches 1 or more. `a+` matches "a", "aa", but not "".
- `?` matches 0 or 1. `a?` matches "" or "a".
- `{n}` matches exactly n times. `a{3}` matches "aaa".
- `{n,m}` matches between n and m times. `a{2,4}` matches "aa", "aaa", "aaaa".
- `{n,}` matches n or more times.

```python
re.findall(r"go+d", "gd god good goood")      # ['god', 'good', 'goood']
re.findall(r"colou?r", "color colour")         # ['color', 'colour']
re.findall(r"\d{3}", "12 123 1234")            # ['123', '123']
re.findall(r"\d{2,4}", "1 12 123 12345")       # ['12', '123', '1234']
```

# Greedy vs Lazy

- Quantifiers are ==greedy== by default, they match as much as possible.
- Adding `?` after a quantifier makes it ==lazy==, matches as little as possible.

```python
re.search(r"<.*>", "<a>b</a>").group()     # '<a>b</a>' (greedy)
re.search(r"<.*?>", "<a>b</a>").group()    # '<a>' (lazy)
```

# Anchors

- Anchors match positions, not characters.
- `^` matches the start of the string. `^abc` matches "abc" only at the beginning.
- `$` matches the end of the string. `abc$` matches "abc" only at the end.
- `\b` matches a ==word boundary==, the position between a word character and a non-word character.

```python
re.search(r"^hello", "hello world")    # <Match: 'hello'>
re.search(r"^hello", "say hello")      # None
re.search(r"world$", "hello world")    # <Match: 'world'>
re.findall(r"\bcat\b", "cat catalog")  # ['cat']
```

# Groups

- `()` creates a ==capture group==. Groups the pattern and captures the match for later use.
- `(abc)+` matches "abc", "abcabc", etc. Without the group, `abc+` would only repeat the c.
- `(?:abc)` is a ==non-capturing group==. Groups without capturing.
- Captured groups are referenced by index: `\1` refers to the first group's match.

```python
m = re.search(r"(\d{3})-(\d{4})", "call 555-1234")
m.group(0)    # '555-1234' (full match)
m.group(1)    # '555'
m.group(2)    # '1234'

re.findall(r"(\w+)@(\w+)", "a@b c@d")    # [('a', 'b'), ('c', 'd')]
re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")  # 'world hello'
```

# Alternation

- `|` means OR. `cat|dog` matches "cat" or "dog".
- Often combined with groups: `(cat|dog)s` matches "cats" or "dogs".

```python
re.findall(r"cat|dog", "I have a cat and a dog")   # ['cat', 'dog']
re.findall(r"(cat|dog)s", "cats and dogs")          # ['cat', 'dog']
```

# Lookahead and Lookbehind

**Lookahead**: check what comes next without consuming it.
- `a(?=b)` matches "a" only if followed by "b".
- `a(?!b)` matches "a" only if not followed by "b" (negative lookahead).
**Lookbehind**: check what came before without consuming it.
- `(?<=a)b` matches "b" only if preceded by "a".
- `(?<!a)b` matches "b" only if not preceded by "a" (negative lookbehind).

```python
re.findall(r"\w+(?=!)", "hello! world")          # ['hello']
re.findall(r"\d+(?!px)", "12px 34em 56px")       # ['1', '34', '5']
re.findall(r"(?<=\$)\d+", "$100 and $200")       # ['100', '200']
```

# Common Patterns

```python
re.search(r"\w+@\w+\.\w+", "user@mail.com")                      # email
re.search(r"^\d+$", "12345")                                      # digits only
re.sub(r"^\s+|\s+$", "", "  hello  ")                             # trim ws
re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "192.168.1.1")  # IP addr
```
