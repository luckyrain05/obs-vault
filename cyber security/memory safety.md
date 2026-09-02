- The class of vulnerabilities that exist because [[c|C]] and C++ let a program write past the end of an object. The OS cannot prevent the bug at compile time but can make exploitation harder by adding runtime checks and randomization.
- Each defense forces the attacker to recover information they previously got for free. Each is bypassed eventually; the arms race continues.

# Why C is Vulnerable

- C has no array-bounds checks and no automatic bounds tracking. `arr[i]` compiles to `*(arr + i)` whether `i` is 0, 100, or $10^9$. The CPU does not know what `arr`'s length is.
- A function that copies user input into a fixed-size buffer will silently overrun if the input is too long. Whatever sits past the buffer in memory gets overwritten.
- Memory-safe languages (Rust, Go, Java, Python) bounds-check at the language level. C and C++ do not, by design — the original C trade was speed and direct hardware access in exchange for no safety net.

# Stack Buffer Overflow

- The classic exploit. Take advantage of how the [[x86 functions#Stack Frames|stack frame]] is laid out:

```
              Higher addresses
              +----------------+
              | argument 2     |
              +----------------+
              | argument 1     |
              +----------------+
              | return address |   <-- saved by call instruction
              +----------------+
              | saved RBP      |
              +----------------+
              | local vars     |
              | char buf[64]   |   <-- buf grows toward higher addr
              +----------------+
              Lower addresses (stack top)
```

- Local variables sit *below* the saved return address. A `strcpy(buf, attacker_input)` with input longer than 64 bytes writes past `buf`, through the saved RBP, and into the saved return address.
- When the function executes `ret`, the CPU pops the return address from the stack and jumps to it. If the attacker overwrote that slot with the address of attacker-supplied code (also placed on the stack as part of the input), the CPU jumps there. The attacker now controls execution.

# Stack Canaries

- Insert a random ==canary== value between the local variables and the saved return address at function entry. Check the canary's value against a saved copy before `ret`.

```
              +----------------+
              | return address |
              +----------------+
              | saved RBP      |
              +----------------+
              | CANARY (random)|   <-- inserted by compiler
              +----------------+
              | local vars     |
              | char buf[64]   |
              +----------------+
```

- A buffer overflow that overwrites the return address must also overwrite the canary on the way past. The check at `ret` time sees a corrupted canary and aborts the process before jumping.
- Bypass: leak the canary somehow (info-disclosure bug) and write its known value back into place. Defeats most non-targeted exploits, not all.

# ASLR

- ==Address Space Layout Randomization==. At process start, the kernel loads the program, libraries, stack, and heap at randomly chosen base addresses. The attacker cannot pre-compute where to jump to.
- Implementation: the kernel adds random offsets when laying out [[virtual memory|virtual address space]] regions. The randomness lives in the unused upper bits of the [[virtual memory#Virtual and Physical Addresses|virtual address]].
- Effective entropy depends on address-space size. On 32-bit systems, only ~16 bits of randomization fit, which a brute-force attacker (~65000 guesses) defeats in seconds. On 64-bit systems, 30+ bits of entropy makes brute force impractical.
- Bypass: leak any single address (info-disclosure bug) and the offset of every other region is now known.

# DEP / NX / W⊕X

- ==Data Execution Prevention==. Mark data pages as non-executable and code pages as non-writable. The hardware refuses to execute instructions fetched from a non-executable page.
- Mechanism: an extra bit in the [[virtual memory#Memory Protection|page table entry]] (the ==NX bit== on x86, ==XN== on ARM). Any instruction fetch from a page with NX set raises a fault.
- Defeats the original buffer-overflow exploit: even if the attacker overwrites the return address to point at their input, that input sits on a stack page marked non-executable. The CPU faults on the first instruction.
- Standard everywhere now. Pure data-injection attacks no longer work.

# Return-Oriented Programming (ROP)

- The attacker's response to DEP. Instead of injecting new code, reuse fragments of existing code already mapped executable.
- A ==gadget== is a short instruction sequence ending in `ret`, found inside the program's own code or its libraries. Examples:
	- `pop rdi; ret` — load whatever is on top of the stack into RDI, return.
	- `pop rsi; ret` — same for RSI.
	- `syscall; ret` — invoke a system call.

- The attacker overflows the stack to place a chain of gadget addresses interleaved with data. Each `ret` jumps to the next gadget; the gadgets together perform arbitrary computation.

```
  Stack after exploit (top of stack on top):
  +-------------------------+
  | addr of "pop rdi; ret"  |  <-- ret jumps here
  +-------------------------+
  | value to pop into RDI   |
  +-------------------------+
  | addr of "pop rsi; ret"  |
  +-------------------------+
  | value to pop into RSI   |
  +-------------------------+
  | addr of "syscall; ret"  |
  +-------------------------+
```

- Every byte fetched is from existing executable code; DEP does not fire.
- Combined with ASLR, ROP requires the attacker to first leak a code address. Modern exploits chain an info-disclosure bug with ROP to get past both defenses.

# Use-After-Free

- A second class of memory-safety bug. The program calls `free(p)` and then later dereferences `p`.

```c
int *A = malloc(128);
...
free(A);
...
A[0] = year_of_birth;   // A's storage may now belong to a different object
```

- Between the `free` and the dereference, another allocation may have reused the same memory. The dereference now reads or writes a *different* object's storage. If the attacker can force the reused allocation to be one whose contents matter to control flow (a vtable pointer, a function pointer), they can hijack execution.
- Defenses: address sanitizers in development; quarantine pools in production allocators; switching to memory-safe languages.

# TOCTOU

- ==Time-of-check-to-time-of-use==. A check on an object and the action that depends on the check are not atomic. An attacker swaps the object between them.

```c
if (access("./my_document", W_OK) != 0) exit(1);
fd = open("./my_document", O_WRONLY);
write(fd, user_input, sizeof(user_input));
```

- Between the `access` check and the `open`, an attacker replaces `./my_document` with a [[file systems#Hard and Symbolic Links|symbolic link]] pointing at a sensitive file the attacker cannot directly write. The `access` check passed for the user's own file; the `open` follows the symlink to the sensitive one.
- Concurrency-flavored — a race condition where the attacker is the other thread.
- Fix: open the file first, then perform permission checks on the file descriptor. The FD points to a specific [[file systems#Inode Block Pointers|inode]] that cannot be swapped out from under the program.

# Side Channels

- A class of attack that does not exploit a memory-safety bug at all. Information leaks through measurable side effects of the system: timing, [[cache|cache]] state, power consumption, branch prediction.
- ==Spectre== and ==Meltdown== (2018) exploit speculative execution: the CPU executes instructions that should not have run, leaves traces in the cache, and the attacker measures the cache to recover those instructions' results.
- The bug is in the CPU, not the OS. Mitigations are in the OS and compiler — selectively flushing caches, inserting speculation barriers, isolating kernel pages from user pages so a misspeculated kernel access cannot leak.
