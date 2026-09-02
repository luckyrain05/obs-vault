- ==R (referenced)==: hardware sets to 1 on any read or write to the page. The OS clears it periodically (e.g. on a clock tick) to detect "used since last tick."
- ==M (modified, dirty)==: hardware sets to 1 only on a write. The OS reads it to decide whether eviction needs a disk write-back; never clears it during eviction decisions.

# Average Memory Access Time

- ==AMAT== quantifies why miss rate matters: $\text{AMAT} = T_m + (P_{\text{miss}} \times T_d)$ where $T_m$ is RAM latency, $T_d$ is disk latency, $P_{\text{miss}}$ is the fault rate.
- With $T_m = 100\text{ns}$ and $T_d = 10\text{ms}$:
	- $P_{\text{miss}} = 0.1$ → AMAT ≈ 1ms (10,000× slower than RAM).
	- $P_{\text{miss}} = 0.001$ → AMAT ≈ 10μs (100× slower than RAM).
- A factor-of-100 difference in miss rate is a factor-of-100 difference in effective speed. Replacement algorithms exist to drive $P_{\text{miss}}$ down.

# Optimal

- Evict the page that will not be referenced for the longest time in the future.
- Provably optimal — no algorithm with the same information could do better.
- Unimplementable: requires knowing the future memory access trace. Used only as the theoretical lower bound on miss rate to benchmark real algorithms.

# FIFO

- Maintain a [[linked lists|linked list]] of pages in the order they were loaded into RAM. Tail is most recent; head is oldest. On a fault, evict the head.
- Simple, fast, no hardware help needed.
- Bad: oldest does not mean least useful. A page loaded at startup that the program references on every iteration gets evicted just because it has been around the longest.

**Belady's anomaly**

- For some access patterns, FIFO produces *more* page faults when given *more* frames. Adding [[ram|RAM]] can make it worse.
- This is unique to FIFO and a few related algorithms; LRU and stack algorithms are immune (more frames is always at least as good as fewer).

# Second Chance

- FIFO with a free pass for recently-used pages. Inspect the head's R bit:
	- `R = 0`: page has not been referenced since the last clock-tick clear. Evict it.
	- `R = 1`: page is hot. Clear R, move it to the tail of the list (treat it as just-loaded), and look at the new head.

```
Before fault (load times above):
  3   7   8  12  14  15  18  20      head -> [B][C][D][E][F][G][H][A]   tail

If A's R bit was set: A gets a second chance, moves to tail, R cleared:
  7   8  12  14  15  18  20  20      head -> [B][C][D][E][F][G][H][A]   tail
```

- Approximates "evict the oldest page that has not been used recently." Cheap to implement on top of FIFO.

# Clock

- Second Chance has list-shuffling cost. Same logic with a fixed circular array and one moving pointer eliminates the shuffles.

```
            +---+
            | A |
       +---+ \ /+---+
       | L |  *  | B |
   +---+   \---/   +---+
   | K |   <hand>   | C |       fault: inspect page at hand
   +---+   /---\   +---+
       | J |  *  | D |          R = 0 -> evict, advance hand
       +---+ / \+---+           R = 1 -> clear R, advance hand, repeat
            | I |
            +---+
```

- The hand sweeps until it finds an `R = 0` page. Time-since-last-reference is encoded by the hand's position; no list updates.

# Not Recently Used (NRU)

- Use both R (referenced) and M (modified) bits to put pages in 4 classes and prefer to evict the lowest-numbered nonempty class:

| Class | R | M | Meaning                          |
|-------|---|---|----------------------------------|
| 0     | 0 | 0 | not referenced, not modified     |
| 1     | 0 | 1 | not referenced, modified         |
| 2     | 1 | 0 | referenced, not modified         |
| 3     | 1 | 1 | referenced, modified             |

- A clock interrupt periodically clears R but never M (M tracks dirty status for write-back).
- Class 1 sounds impossible (modified but not referenced) but happens after a clock-tick clears R on a page that was modified earlier and not referenced since.
- Picks at random within the lowest nonempty class. Cheap; coarse.

# Least Recently Used (LRU)

- Evict the page whose most-recent reference is furthest in the past. The locality argument: a page used recently is likely to be used again soon, so it is the worst candidate to evict.
- Empirically near-optimal on real workloads — for the LRU policy column in the slide trace, hit rate matches Optimal.
- Expensive to implement exactly:
	- Software approach: walk the page list and update on every memory reference. Too slow.
	- Hardware approach: every memory reference writes a timestamp into the PTE; eviction picks the smallest. Requires a counter that increments per reference and a wide PTE field.
- Real systems use approximations.

# Reference Bit Counters

**NFU**

- Per-page counter, all initialized to 0. At each clock tick, for every page, add the R bit to its counter. Evict the lowest counter on a fault.
- Bug: a page heavily used at program startup accumulates a high count that decays slowly; long after it has gone cold it still beats currently-active pages on the counter.

**Aging**

- Decay the counter so old references weigh less than recent ones.
- At each clock tick, *shift the counter right by one bit*, then OR the R bit into the high bit. The R bit becomes the most significant bit of the counter; references from $k$ ticks ago end up in bit $k$ from the top.

```
Page    tick 0     tick 1     tick 2     tick 3     tick 4
0       10000000   11000000   11100000   11110000   01111000
1       00000000   10000000   11000000   01100000   10110000
2       10000000   01000000   00100000   00010000   10001000
```

- Recent references have higher weight (more significant bits). Evict the lowest counter value.
- An $N$-bit counter remembers $N$ ticks of history. Beyond that, the page's history is forgotten — the bit shifts off.
- A computationally cheap LRU approximation. Used in many real OSes.

# Locality Model

- Programs do not access pages randomly. They show ==locality of reference==: in any short interval, the active set of pages is small relative to the total.

**Working set**

- The working set $w(k, t)$ is the set of pages a process referenced during the last $k$ memory accesses ending at time $t$.
- Bounded above by $k$, but in practice $w(k, t)$ saturates quickly as $k$ grows — adding a few hundred more accesses adds only a handful of new pages.

**Thrashing**

- If the process's working set does not fit in its allocated frames, every page reference is likely to fault.
- The CPU spends nearly all its time on page-fault disk I/O instead of useful work. AMAT explodes by orders of magnitude.
- Diagnosis: high fault rate, low CPU utilization, high disk activity. The system is technically running but accomplishing nothing.
- Resolution (==load control==): suspend entire processes to shrink the active working set sum until the rest fits. Better one process running fast than ten thrashing.

**Prepaging**

- When swapping a process back in, the naive approach is to start it with no pages mapped and let demand-paging fault each one in.
- Prepaging predicts the working set and loads it as a batch before the process resumes. Replaces many small disk reads with one bulk read; avoids the initial fault storm.

**Working-set algorithm and WSClock**

- Replacement algorithm that prefers to evict pages outside the working set. For each page, track time of last reference. On a fault, scan the page table:
	- If R = 1, set time-of-last-use to current virtual time; clear R.
	- If R = 0 and (current virtual time − time-of-last-use) > $\tau$ (the working-set window), the page is outside the working set — evict.
	- If R = 0 and within the window, the page is in the working set — keep, remember its last-use time.

- Scanning the entire page table on every fault is expensive. WSClock combines the working-set criterion with Clock's circular sweep: the hand advances until it finds a page outside the working set, evicts that one, and stops. Used in real systems.


[[virtual memory]]


- Optimizations that exploit [[virtual memory|page faults]] as a notification mechanism. The OS marks pages absent or read-only and lets the hardware fault deliver work-on-demand.
- Each trick below converts an eager operation (allocate everything, copy everything) into a lazy one driven by the first access that needs it.

# Demand Paging

- Naive approach to `malloc(N)`: allocate $N$ bytes of physical memory and map them into the process's page table immediately. Wasted on the common case where the process allocates a 1MB buffer and only writes the first 100 bytes.
- Demand paging: the allocator does almost nothing. It records that the virtual range is reserved for the process, but the page table marks every page in the range as not-present.
	1. Process touches a virtual address in the range.
	2. Hardware page fault.
	3. OS notices the address is in a reserved range, allocates a physical frame, zeroes it, installs the PTE.
	4. Process re-executes the instruction. Memory access succeeds.
- Pages never touched are never backed by RAM. A 1GB allocation that touches 4KB consumes 4KB of physical memory.

**Overcommitting**

- The OS can hand out more virtual memory than it has physical RAM + swap, betting that allocators reserve more than they use.
- Linux does this by default — `malloc()` almost never fails. The bet usually wins.
- When it loses, the system runs out of physical memory mid-execution. The OOM killer terminates a process to recover. Errors that would have failed at allocation time fail at use time, far from their cause.

# Copy-on-Write

- `fork()` semantically gives the child a complete copy of the parent's address space. Naively, the OS would walk the parent's page table and `memcpy` every page into newly allocated frames. Slow, and wasteful when the child immediately calls `exec` and discards the inherited memory.
- Copy-on-write defers the copy until something would observe it.
	1. On `fork()`: build the child's page table to point at the *same* physical frames as the parent's. No copying.
	2. Mark every PTE in both page tables read-only. Set a kernel-internal bit recording that the page is CoW-shared.
	3. As long as both processes only read, they share frames safely.
	4. The first write triggers a protection fault (write to a read-only page).
	5. The OS sees the CoW bit, allocates a new frame, copies the contents, installs the new frame in the writing process's page table with write permission, restores write permission for the other process if it was the last sharer.
	6. Process re-executes the instruction. Write succeeds.
- A `fork()` immediately followed by `exec()` (the common shell-spawn pattern) never copies the parent's memory at all — `exec()` replaces the address space before any write happens.
- Reference counts on each shared physical frame track how many processes share it; the last writer's CoW fault decrements to 1, at which point the frame is no longer shared and stops being CoW.

# Memory-Mapped Files

- Default file I/O: `read()` copies disk bytes into a user buffer; the program works on the buffer; `write()` copies modified bytes back. Two copies and explicit calls.
- ==mmap()== maps a file's contents directly into the process's virtual address space. Address $X + N$ refers to byte $N$ of the file. Reads and writes look like ordinary memory accesses.
- Implementation: the mapped pages are marked not-present. First access faults; the OS reads the corresponding disk block into a frame, installs the PTE, retries.
- Modifications: pages marked dirty (M bit) get written back to disk on flush, on unmap, or on process exit, depending on flags.
- Composes with demand paging: only the touched portions of the file are ever in RAM.
