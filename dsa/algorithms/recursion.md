- A function that calls itself to solve smaller subproblems until it reaches a ==base case==.
- Every recursive function has three structural parts: the base case, the middle (before the recursive call), and the bottom (after the recursive call returns).

# Basic Structure

```python
def factorial(n):
    if n <= 1:                   # 1. BASE CASE — when to stop
        return 1

    # 2. MIDDLE — work before the recursive call (runs on the way DOWN)
    # here, n is captured and waits to be multiplied

    result = factorial(n - 1)    #    the recursive call

    # 3. BOTTOM — work after the recursive call returns (runs on the way UP)
    return n * result
```

**Base case**: the exit condition. Without it, infinite recursion and a stack overflow. Ask: what is the smallest version of this problem I can solve trivially?

**Middle**: everything before you recurse. Runs on the way down the stack, from the original call toward the base case.

**Bottom**: everything after the recursive call. Runs on the way back up, from the base case toward the original call. Each frame is still sitting on the stack, waiting. When the call below returns, the frame wakes up and executes.

# Call Stack

- Every recursive call pushes a new [[memory#Stack|stack frame]] onto the call stack.
- Each frame holds its own copy of local variables and parameters.
- Frames resolve in ==LIFO== order, deepest call finishes first, then bubbles back up.

```
+----------------------------------+
| factorial(4)                     |
| n=4, needs 4 * factorial(3)      |
| +------------------------------+ |
| | factorial(3)                 | |
| | n=3, needs 3 * factorial(2)  | |
| | +--------------------------+ | |
| | | factorial(2)             | | |
| | | n=2, needs 2 * fact(1)   | | |
| | | +----------------------+ | | |
| | | | factorial(1)         | | | |
| | | | BASE CASE -> return 1| | | |
| | | +----------------------+ | | |
| | | return 2 * 1 = 2         | | |
| | +--------------------------+ | |
| | return 3 * 2 = 6             | |
| +------------------------------+ |
| return 4 * 6 = 24                |
+----------------------------------+
```

- The stack grows n frames deep, so recursion always costs at least `O(n)` SC.