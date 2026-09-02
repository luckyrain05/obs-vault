- A deeper dive into the [[hardware architecture#Cache|cache]].
- A ==cache== is a fast, small storage device that holds a subset of data from a slower, larger device. It is physically embedded in the [[hardware architecture#CPU|CPU]] and holds data from [[ram|RAM]].
- Each level in the hierarchy (L1, L2, L3) acts as a cache for the level below it.
	- Higher the number, larger the storage, but slower the access.

# Cache Localities

- CPUs process data in ==words== (typically 8 bytes). But repeatedly fetching words between the CPU and RAM will significantly stall the CPU.
- Rather than fetching one word at a time, we fetch a ==block== (typically 64 bytes) and store it into a cache that is much faster to access compared to RAM.
- This bets on ==cache locality==. If the CPU accessed word X, we bet that it will access words near X soon. By caching the entire block, only fetch from RAM once. 

**Temporal locality**

- The phenomenon that when a program access an address, there's is a higher probability that it access the same address in the near future.

**Spatial locality**

- The phenomenon that when a program access an address, there's is a higher probability that it access addresses near it.

# Cache Structure

- A cache is organized as a table of [[memory#Memory Addresses|memory addresses]].
	- Each row is referred to as a ==set==, and a set can have multiple ==lines==.
	- Each line contains a block.
	- Thus, we need ==metadata== to identify the exact bytes that the CPU needs.

**Block Offset**

- Selects the exact byte within the block.
- Number of bits = $log_2(block\_size)$
- 64 bit blocks need 64 unique representations, or 6 binary digits.

**Set Index**

- Selects which set in the cache to look in.
- Number of bits = $log_2(num\_of\_sets)$

**Tag**

- The remaining bits. Used to distinguish between the different lines in the set.

```
| Tag | Set Index | Block Offset |
```

- Metadata can be derived directly from the addresses, in binary.
- The CPU actually looks in the order of set -> line -> block offset. This particular ordering from most to least significant bits is strictly conventional.

```
         +-------+-------+--------------------------+
         | Valid | Tag   | Block                    |
+--------+-------+-------+--------------------------+
| Set 0  |       |   0   |                          |
+--------+-------+-------+--------------------------+
         |       |   1   |                          |
         ......................
         
+--------+-------+-------+--------------------------+
| Set 1  |       |   0   |                          |
+--------+-------+-------+--------------------------+
         |       |   1   |                          |
         ......................
```

**Valid bit**

- 1 means the line holds real data, 0 means it is empty. 
- This is stored on the cache only, not the memory address.
- On access, CPU uses the set index to pick a row, then compares the tag against every line in that set.

# Hits and Misses

- Goal of all caches: maximize hits, minimize misses.

**Cache hit**

- Requested data is found in the cache, fast.

**Cache miss**

- Data is not in cache. We must fetch from the RAM, which is slower.
- If the newly fetched data points to a populated row, we also need to ==evict== the stale block with out new one.

# Eviction Policies

**LRU** (Least Recently Used)

- Evict the block that hasn't been used the longest.
- Assumes it won't be needed again soon.
- Good for straight-line code, can be bad for large loops.

**Thrashing**

- Essentially dog shit.
- When the eviction policy constantly evicts blocks that are about to be needed.
- Every access becomes a miss.

# Direct-Mapped Cache

- Each row has exactly 1 line. A block can only go in one specific row.
- Set index determines exactly where the block goes, no choice involved.
- Fast lookup, but if two frequently used blocks map to the same set, they constantly evict each other.

```
         +-------+-------+--------------------------+
         | Valid | Tag   | Block                    |
+--------+-------+-------+--------------------------+
| Set 0  |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 1  |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 2  |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 3  |       |       |                          |
+--------+-------+-------+--------------------------+ 
```

- 1 line per set, 1 possible set location per block

# Fully Associative Cache

- The entire cache is 1 set with many lines. A block can go in any line.
- Set index is 0 bits. The entire address (minus offset) is the tag.
- No conflict misses, but hardware must compare the tag against every line in parallel. Expensive, only practical for small caches.

```
         +-------+-------+--------------------------+
         | Valid | Tag   | Block                    |
+--------+-------+-------+--------------------------+
|        |       |       |                          |
|        |       |       |                          |
| Set 0  |       |       |                          |
|        |       |       |                          |
|        |       |       |                          |
+--------+-------+-------+--------------------------+
```

- All lines in 1 set.

# N-Way Set-Associative Cache

- Each set has N lines. 
- A block maps to a specific set but can go in any line within that set.
- Compromise between direct-mapped and fully associative.
	- 2-way: each set holds 2 blocks.
	- 4-way: each set holds 4 blocks.
- Reduces conflict misses compared to direct-mapped, cheaper than fully associative.

```
         +-------+-------+--------------------------+
         | Valid | Tag   | Block                    |
+--------+-------+-------+--------------------------+
| Set 0  |       |       |                          |
|        |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 1  |       |       |                          |
|        |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 2  |       |       |                          |
|        |       |       |                          |
+--------+-------+-------+--------------------------+
| Set 3  |       |       |                          |
|        |       |       |                          |
+--------+-------+-------+--------------------------+
```

- On a miss, eviction within the set uses a policy like LRU.
- Most real caches (L1, L2, L3) are set-associative.