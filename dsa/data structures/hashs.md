- A hash table maps keys to values using a hash function to compute an [[arrays]] index.
- Backed by a fixed-size array of ==buckets==.
- Average `O(1)` insert, search, and delete.

# Hash Function

- ==Hash function== maps a key to a bucket index. Taught with`hash(key) % capacity` but is much more complicated in practice.
- A good hash function distributes keys uniformly across buckets.
- A poor one clusters keys, degrading all operations toward `O(n)`.

# Collision

- ==Collision== happens when two different keys produce the same index.
- Unavoidable, and desired in certain use cases. 
- Two strategies to handle it: **chaining** and **open addressing**.

# Chaining

- Each bucket holds a linked list of `(key, value)` pairs.
- On collision, append to that bucket's list. On lookup, scan the list for the key.
- This is a ==dictionary==.

```
Insert "listen" → hash("listen") % 4 = 0
Insert "silent" → hash("silent") % 4 = 0   ← collision, appended to bucket 0's list
Insert "dog"    → hash("dog")    % 4 = 1
Insert "cat"    → hash("cat")    % 4 = 3

+-----+--------------------------------------+
| idx | chain                                |
+-----+--------------------------------------+
|  0  | ("listen", 1) -> ("silent", 2)       |
+-----+--------------------------------------+
|  1  | ("dog", 5)                           |
+-----+--------------------------------------+
|  2  | empty                                |
+-----+--------------------------------------+
|  3  | ("cat", 3)                           |
+-----+--------------------------------------+
```

Raw Python implementation:

```python
class HashTable:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def insert(self, key, val):
        bucket = self.buckets[self._index(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, val)
                return
        bucket.append((key, val))

    def search(self, key):
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return None

    def delete(self, key):
        bucket = self.buckets[self._index(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

- `O(1)` average TC for all operations, `O(n)` worst case (all keys in one bucket). `O(n)` SC.

# Open Addressing (Linear Probing)

- All entries stored directly in the array, no lists, no pointers.
- On collision, scan forward for the next empty slot: `(hash(key) + i) % capacity`.
- This is a ==set.==

```
Insert "listen" → hash("listen") % 4 = 0   ← slot 0 empty, place here
Insert "silent" → hash("silent") % 4 = 0   ← slot 0 taken, probe to slot 1
Insert "dog"    → hash("dog")    % 4 = 3

+-----+----------+-----+
| idx |   key    | val |
+-----+----------+-----+
|  0  | "listen" |  1  |
+-----+----------+-----+
|  1  | "silent" |  2  |  ← probed here from idx 0
+-----+----------+-----+
|  2  |   None   |     |
+-----+----------+-----+
|  3  |  "dog"   |  5  |
+-----+----------+-----+
```

**Tombstone**

- A marker placed in a deleted slot so probing chains aren't broken.
- Without it, a search could hit the empty slot left by a deletion and stop early, missing keys that were probed past that slot.

Raw Python implementation:

```python
_DELETED = object()

class HashTable:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.table = [None] * capacity

    def _probe(self, key):
        i = hash(key) % self.capacity
        while self.table[i] is not None and self.table[i] is not _DELETED and self.table[i][0] != key:
            i = (i + 1) % self.capacity
        return i

    def insert(self, key, val):
        self.table[self._probe(key)] = (key, val)

    def search(self, key):
        entry = self.table[self._probe(key)]
        return entry[1] if entry and entry is not _DELETED else None

    def delete(self, key):
        i = self._probe(key)
        if self.table[i] and self.table[i] is not _DELETED:
            self.table[i] = _DELETED
```

- `O(1)` average TC for all operations, `O(n)` worst case. `O(n)` SC.
- Better cache performance than chaining — all data is contiguous in memory.

# Load Factor

- ==Load factor== — `n / capacity`, where `n` is the number of stored entries.
- As load factor grows, collision rate rises and performance degrades.
- Standard threshold: rehash and double capacity when load factor exceeds `~0.7`.
- ==Rehashing== — allocate a new larger array and reinsert all entries. `O(n)` TC.

# Dictionary

- Python's `dict` is a hash table using open addressing.
- Stores key value pairs, keys are `O(1)` average TC for lookups and insertions. 
- Keys must be hashable (immutable types: `str`, `int`, `tuple`).

```python
d = {}
d["key"] = "val"        # insert / update
val = d.get("key")      # search, returns None if missing
del d["key"]            # delete
"key" in d              # O(1) membership test

# defaultdict for grouped inserts
from collections import defaultdict
d = defaultdict(list)
d["a"].append(1)
```

# Set

- `set()` is a hash table that stores only keys, no values. Duplicates are ignored.
- Same underlying mechanism as `dict`: hashes keys into buckets, uses open addressing for collisions.
- `O(1)` average for add, remove, and membership test.
- Elements must be hashable (immutable types: `str`, `int`, `tuple`).
- `frozenset` is the immutable variant.

```python
s = set()
s = {1, 2, 3}           # literal syntax
s.add(4)                 # insert
s.remove(3)              # delete, raises KeyError if missing
s.discard(3)             # delete, no error if missing
3 in s                   # O(1) membership test

# set from iterable (deduplicates)
s = set([1, 2, 2, 3])   # {1, 2, 3}
```

- Set operations:

```python
a = {1, 2, 3}
b = {2, 3, 4}

a | b                    # union        → {1, 2, 3, 4}
a & b                    # intersection → {2, 3}
a - b                    # difference   → {1}
a ^ b                    # symmetric difference → {1, 4}
a <= b                   # subset check → False
```