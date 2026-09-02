- [[ram|RAM]] is expensive. If [[processes]] used physical memory directly, the amount of memory that typical personal computing habits requires would not be possible at a reasonable price. 
- ==Virtual memory== is an abstraction layer between physical memory and processes. It gives each process the illusion that it has infinite memory space.

# Page

- Both virtual and physical memory are divided into fixed-size chunks called ==pages==.
- A page is typically 4KB. The OS and hardware agree on this size at [[boot]].
- Virtual pages live in a process's address space. Physical pages (also called ==frames==) live in RAM.
- A virtual page can map to a physical frame, a location on disk, or nothing (unmapped).

```
    Process 1               Physical Memory            Process 2
  (what it sees)            (what exists)            (what it sees)

+----------------+                                +----------------+
| 0x000000000000 |       +----------------+       | 0x000000000000 |
|                |  +--->| Page: Proc 1   |<--+   |                |
|   my memory!   |  |    +----------------+   |   |   my memory!   |
|                |--+    | Page: Proc 2   |   +---|                |
|                |       +----------------+       |                |
|                |       | Page: Proc 1   |       |                |
| 0xFFFFFFFFFFF  |       +----------------+       | 0xFFFFFFFFFFF  |
+----------------+       | Page: Proc 2   |       +----------------+
                         +----------------+
                         |    (empty)     |
                         +----------------+
```

- Each process thinks it has the entire address space to itself. The [[os#OS Spaces|kernel]] switches between the two programs at a rapid pace to mimic concurrency. 

# Virtual and Physical Addresses

**Virtual address**
- What the process sees. Consists of a virtual page number + offset.
- Independent of physical memory size and other processes.

**Physical address**
- Actual location in RAM. Consists of a physical page number + offset.
- Known only to OS and hardware.

- The offset is the same in both the virtual and physical address, but the PPN obviously would have less bits since there is physically less of it.
- This preserves [[cache#Cache Localities|spatial locality]].

```
  Virtual address:
  +---------------------------------------------+--------------+
  |   Virtual Page Number, longer in bits (VPN) |    Offset    |
  +---------------------------------------------+--------------+

  Physical address:
  +-----------------------------+--------------+
  |  Physical Page Number (PPN) |    Offset    |
  +-----------------------------+--------------+

  Translation:
  VPN --[page table]--> PPN,  offset stays the same
```

# Page Tables

- Each process has its own page table, which maps virtual page numbers to physical page numbers (or disk locations).
- A page table entry maps a virtual page to either:
	- A physical page in RAM, or
	- A location on disk.
- Unmapped entries mean the virtual page is not allocated.

```
            Page Table (Process 1234)
  +-----+-------+-----------+-----------+
  | VPN | Valid | PPN/Disk  | Perm Bits |
  +-----+-------+-----------+-----------+
  |  0  |   1   | PP 5      | RW-       |
  +-----+-------+-----------+-----------+
  |  1  |   0   |    --     |  --       |  <-- unmapped
  +-----+-------+-----------+-----------+
  |  2  |   1   | Disk @ X  | RW-       |  <-- on disk
  +-----+-------+-----------+-----------+
  |  3  |   1   | PP 8      | R--       |
  +-----+-------+-----------+-----------+
  | ... |  ...  |   ...     | ...       |
  +-----+-------+-----------+-----------+
```

# Page Hits and Page Faults

**Page hit**
- Virtual page maps to a physical page in RAM.
- Hardware translates the address and accesses it directly.

**Page fault**
- Virtual page maps to disk. Hardware generates a page fault.
- OS takes control, evicts a page from RAM to disk, loads the needed page from disk to RAM.
- OS updates the page table, returns control to the process.
- Process re-executes the same instruction.

**Segmentation fault**
- Virtual page is unmapped (not allocated). OS kills the process.

```
  Process accesses VPN 3:

  1. CPU splits virtual address into VPN + offset
  2. CPU looks up VPN 3 in page table

  +-----+-------+-----------+
  | VPN | Valid | PPN/Disk  |
  +-----+-------+-----------+
  |  3  |   1   | PP 8      |  --> Page hit! Access PP 8 + offset
  +-----+-------+-----------+

  Process accesses VPN 2:

  +-----+-------+-----------+
  | VPN | Valid | PPN/Disk  |
  +-----+-------+-----------+
  |  2  |   1   | Disk @ X  |  --> Page fault!
  +-----+-------+-----------+

       OS steps in:
       a. Pick a victim page in RAM to evict (e.g. PP 5)
       b. Write victim to disk if dirty
       c. Load VPN 2 from disk @ X into PP 5
       d. Update page table: VPN 2 --> PP 5
       e. Return to process, re-execute instruction

  Process accesses VPN 1:

  +-----+-------+-----------+
  | VPN | Valid | PPN/Disk  |
  +-----+-------+-----------+
  |  1  |   0   |    --     |  --> Segmentation fault! Process killed.
  +-----+-------+-----------+
```

# Storing Page Tables

- Page tables are stored in main memory (RAM).
- OS ==pins== page tables to physical memory so they are never swapped to disk.
- Each memory access conceptually requires two physical accesses: one for the page table, one for the data.

```
  CPU wants to read virtual address 0xABCD:

       Access 1                    Access 2
  +----------------+           +----------------+
  | Read page      |           | Read actual    |
  | table in RAM   |--found--> | data in RAM    |
  | to get PPN     |           | at PPN+offset  |
  +----------------+           +----------------+

  2 RAM accesses per 1 logical access. Slow without a TLB.
```

# Translation Lookaside Buffer

- TLB is a small cache on the CPU that stores recent page table entries.
- Hardware checks TLB first on every memory access.
	- TLB hit: no need to access the page table in memory.
	- TLB miss: load the entry from the page table into the TLB, then retry.

```
               TLB (on CPU)
  +-----+-----+-------+-----------+
  |     | VPN | PPN   | Perm Bits |
  +-----+-----+-------+-----------+
  |     |  0  | PP 5  | RW-       |
  +-----+-----+-------+-----------+
  |     |  3  | PP 8  | R--       |
  +-----+-----+-------+-----------+
  |     |  6  | PP 2  | RW-       |
  +-----+-----+-------+-----------+
  |     | ... | ...   | ...       |
  +-----+-----+-------+-----------+

  CPU accesses VPN 3:
    1. Check TLB --> VPN 3 found, PPN = 8. TLB hit!
    2. Access RAM at PP 8 + offset. Only 1 RAM access.

  CPU accesses VPN 4:
    1. Check TLB --> VPN 4 not found. TLB miss.
    2. Read page table in RAM to get PPN for VPN 4.
    3. Load VPN 4 --> PPN into TLB (evict old entry if full).
    4. Retry. Now it's a TLB hit.
```

# Memory Protection

- A process's page table only references physical pages that it owns. One process cannot access another's memory.
- ==Permission bits== in page table entries mark pages as read-only, executable, etc.
	- Prevents writing to RODATA and TEXT sections.
	- Prevents user processes from accessing OS-owned memory.

```
            Page Table (Process 1234)
  +-----+-------+-----+-------+------+-----------+
  | VPN | Valid | R   | W     | X    | PPN       |
  +-----+-------+-----+-------+------+-----------+
  |  0  |   1   |  1  |   0   |  1   | PP 5      |  TEXT (code)
  +-----+-------+-----+-------+------+-----------+
  |  1  |   1   |  1  |   0   |  0   | PP 9      |  RODATA
  +-----+-------+-----+-------+------+-----------+
  |  2  |   1   |  1  |   1   |  0   | PP 3      |  DATA/HEAP
  +-----+-------+-----+-------+------+-----------+
  |  3  |   1   |  1  |   1   |  0   | PP 7      |  STACK
  +-----+-------+-----+-------+------+-----------+

  Process tries to write to VPN 0 (TEXT):
    W = 0 --> hardware raises protection fault. Blocked.
```

# Full Memory Access Path

- After the TLB translates a virtual address to a physical address, that physical address is looked up in the [[cache]] hierarchy.
- The [[cache]] does not store pages. It stores ==cache lines== (~128 bytes), small blocks pulled from physical memory. A single page spans many cache lines.

```
Virtual Address
      |
      v
    [TLB] -- hit --> Physical Address
      |                    |
     miss                  v
      |               [L1 Cache] -- hit --> data
      v                    |
  [Page Table              miss
   in RAM]                 |
      |                    v
      v               [L2 Cache] -- hit --> data
 Physical Address          |
                          miss
                           |
                           v
                      [L3 Cache] -- hit --> data
                           |
                          miss
                           |
                           v
                        [RAM] --> data
```

# Multi-Level Page Tables

- A flat single-level page table for a 32-bit address space at 4KB pages needs $2^{20} = 1{,}048{,}576$ entries. At 4 bytes per entry, that is 4MB per process. 100 processes need 400MB just for translation tables, and the OS pins them in RAM (it cannot swap a page table to disk because you need the page table to translate addresses to disk).
- Most virtual address spaces are sparse — a process maps a few megabytes of code, data, and stack out of a 4GB range. Allocating space for translations of unused regions is waste.
- The fix is one level of indirection.

```
  Virtual address (32-bit, 4KB pages):
  +-------------+-------------+-------------+
  | Directory   | Table       | Offset      |
  | (10 bits)   | (10 bits)   | (12 bits)   |
  +-------------+-------------+-------------+

  +-----------------+         +---------------+
  | Page Directory  |         | Page Table    |
  | (4KB, 1024 PDEs)|---PDE-->| (4KB, 1024    |
  +-----------------+         |  PTEs)        |---PTE--> physical page
                              +---------------+
```

- The top 10 bits of the virtual address index into the page directory. Each directory entry (PDE) points to a 4KB second-level page table. The next 10 bits index into that page table; the entry (PTE) holds the physical page number. The last 12 bits are the offset within the 4KB page.
- $2^{10} \times 2^{10} \times 2^{12} = 2^{32}$ — the same address space, now built from 1024 small tables instead of one big one.
- Allocation savings: the OS only allocates a second-level table for a directory entry that has at least one mapped page. A process using 8MB of memory needs the page directory (4KB) plus two page tables (8KB total), 12KB instead of 4MB.
- Eviction: second-level page tables themselves can be paged to disk. The page directory must stay pinned — if it were swapped out, no page in this address space could be translated.
- x86 uses this scheme. A dedicated register holds the physical address of the current process's page directory; context-switching updates it to point at the incoming process's directory.

# Super Pages

- A second-level page table maps $1024 \times 4KB = 4MB$ of virtual memory. A super page lets a single page directory entry map that 4MB region directly to one large physical page, skipping the second-level table entirely.

```
  Virtual address (32-bit, 4MB super page):
  +-------------+-------------------------+
  | Directory   | Offset                  |
  | (10 bits)   | (22 bits)               |
  +-------------+-------------------------+

  +-----------------+
  | Page Directory  |
  | PDE.PS = 1      |---> 4MB physical page
  +-----------------+
```

- The PSE (Page Size Extension) bit in a control register enables super pages globally; the `PS` bit in each PDE selects whether that entry points to a 4KB-page table or a 4MB super page.
- Wins: one fewer memory access on translation, one TLB entry covers 4MB instead of 4KB (==TLB reach== improves 1024×).
- Cost: internal fragmentation. Allocating 4MB for a region using 100KB wastes the rest. Used selectively for the kernel and for large hot regions (e.g. JVM heaps, hugepages).

# TLB Misses: Soft vs Hard

- A TLB miss is not the same as a page fault. The miss says "I don't know the translation"; the fault says "the page isn't in RAM."

**Soft miss**

- Translation is not in the TLB, but the page is in RAM. The hardware (or software) walks the page table, finds the PTE, loads it into the TLB, retries.
- Cost: roughly 10-20 machine instructions, ~2ns. Negligible compared to a memory access.

**Hard miss**

- Translation is not in the TLB *and* the PTE marks the page as on disk. Hardware raises a page fault; the OS reads the page from disk, updates the PTE, loads the TLB.
- Cost: a few milliseconds. Roughly $10^6\times$ slower than a soft miss because of the disk I/O.

# Tagged TLBs

- A TLB entry maps a virtual page to a physical page *for the current process*. When a [[schedulers#Context Switch|context switch]] makes a different process current, the old TLB entries are wrong — VPN 5 in process A maps to a different physical page than VPN 5 in process B.
- Naive solution: flush the entire TLB on every context switch. Correct, but the new process pays soft-miss cost on every memory access for the first few thousand instructions until the TLB warms up.
- ==Tagged TLB==: each entry stores an ==ASID== (address space identifier) — the kernel-assigned ID of the process that owns the entry. The CPU's translation lookup matches both the VPN and the current ASID. Entries from other processes are present in the TLB but invisible.
- No flush needed on context switch; entries from a previously-scheduled process are still valid when its turn comes around again.
