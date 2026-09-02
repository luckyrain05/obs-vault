- An array is a contiguous block of memory where elements are stored at consecutive [[memory#Memory Addresses|memory addresses]]. it is a fundamental data structure.
- Unlike other data structures covered, arrays are not an conceptual data structure. The definition for arrays is rooted in hardware.

- Each element is the same fixed size, so accessing any index is a single arithmetic operation: `base_address + index * element_size`.

# Memory Layout

- Arrays map directly to memory, a block of consecutive addresses.
- Thus, at a low level, languages simply +1 to a starting memory address to access additional indexes in an array.
- This design maximally leverages [[cache#Cache Locality|cache spatial locality]]. It is why arrays are favored in modern computer and algorithm design.

```
arr = [10, 20, 30, 40, 50]

+--------+--------+--------+--------+--------+
| addr 0 | addr 1 | addr 2 | addr 3 | addr 4 |
+--------+--------+--------+--------+--------+
|   10   |   20   |   30   |   40   |   50   |
+--------+--------+--------+--------+--------+
```

- `arr[2]` goes to `base + 2 * size`, lands directly on `30`. No scanning needed.

# Row Major Order (RMO)

- Arrays can be nested inside another array, it represents dimentional matrices, thus we refer to them as multi-dimentional arrays.
- But, memory is one-dimensional. A 2D matrix must be flattened into a single contiguous block. 
- ==Row major order== stores a multidimensional array in memory row by row, one after another.

- Below is a 2D array representing a 2D matrix:

```
matrix = [[1, 2, 3],
          [4, 5, 6]]
```

- Element at `matrix[i][j]` in an `m x n` matrix maps to memory index `i * n + j`.

```
In memory (row major):
+---+---+---+---+---+---+
| 1 | 2 | 3 | 4 | 5 | 6 |
+---+---+---+---+---+---+
 row 0       row 1
```

- Used by C, C++, Python, Java.
- Iterating column by column in a RMO language will cause more cache misses.

# Column Major Order (CMO)

- ==Column major order== stores a multidimensional array in memory column by column.

```
matrix = [[1, 2, 3],
          [4, 5, 6]]

In memory (column major):
+---+---+---+---+---+---+
| 1 | 4 | 2 | 5 | 3 | 6 |
+---+---+---+---+---+---+
 col 0   col 1   col 2
```

- Element at `matrix[i][j]` in an `m x n` matrix maps to memory index `j * m + i`.
- Used by Fortran, MATLAB, R.
- Iterating row by row in a CMO language will cause more cache misses.

- Neither CMO or RMO is superior. It depends on if the language will see column by column or row by row iteration more. CMO is more closely aligned with vectors.

# Static vs Dynamic Arrays

**Static array**
- Fixed size, allocated once. Cannot grow or shrink.
- Languages like C and Java use static arrays by default.
**Dynamic array**
- Resizable. When capacity is exceeded, a new larger array is allocated and elements are copied over.
- Python's `list` is a dynamic array.
- ==Amortized== `O(1)` append — most appends are instant, but occasionally one triggers a resize (`O(n)` copy). Averaged out, still `O(1)` per operation.

# Operations

**Access** — `O(1)` TC. Direct index arithmetic.
**Search** — `O(n)` TC. Linear scan. `O(log n)` if sorted.
**Insert** — `O(n)` TC. Shift all elements after the insertion point right by one.
**Delete** — `O(n)` TC. Shift all elements after the deletion point left by one.
**Append** — `O(1)` amortized TC. Add to the end, no shifting.

# Python Arrays

- Python's `list` is a dynamic array. Resizing is handled automatically.
- Below is a list of array methods that Python supports:

```python
arr = []
arr.append(1)          # O(1) amortized — add to end
arr.pop()              # O(1) — remove from end
arr.pop(i)             # O(n) — remove at index, shifts elements
arr.insert(i, val)     # O(n) — insert at index, shifts elements
arr[i]                 # O(1) — access by index
arr[i] = val           # O(1) — update by index
len(arr)               # O(1)
val in arr             # O(n) — linear search
arr.index(val)         # O(n) — first index of val
arr.sort()             # O(n log n) — in-place, Timsort
arr.reverse()          # O(n)
arr.copy()             # O(n) — shallow copy
```

# Slicing

- Slicing creates a **new** list from a range of indices.
- `arr[start:stop:step]` — start inclusive, stop exclusive.

```python
arr = [0, 1, 2, 3, 4, 5]

arr[1:4]      # [1, 2, 3]
arr[:3]       # [0, 1, 2]
arr[3:]       # [3, 4, 5]
arr[::2]      # [0, 2, 4]         — every 2nd element
arr[::-1]     # [5, 4, 3, 2, 1, 0] — reversed copy
arr[1:5:2]    # [1, 3]
```

- `O(k)` TC and SC, where `k` is the size of the slice.