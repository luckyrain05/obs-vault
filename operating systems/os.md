- The ==operating system== is a [[compilers|compiled binary]] the [[hardware architecture|hardware]] loads on [[boot]], before any other programs.
- Once running, it mediates every other binary's access to the machine. This file frames the gap it fills and lists the mechanisms it provides; each hands off to its own note.
- Raw hardware have serious problems for humans to directly interact with.

**Memory Collision**

- Programmer $A$ and $B$ can store data to the same [[memory#Memory Addresses|memory address]] and poison each other's data. 
- It is unrealistic for any large groups of developers to coordinate the usage of memory.

**Resource Hoarding**

- Whichever program started first will run until completion or indefinitely, hoarding compute from other programs.

**Security**

- One bug or user mistake can halt or break the machine.
- Data is accessible to any user and program.

# OS Spaces

**Kernel space**

- The kernel binary, mapped supervisor-only into every process's [[virtual memory|virtual address space]].
- Resident exactly once in physical RAM; per-process page tables alias the same physical kernel pages, so a trap into the kernel does not require switching tables.

**User space**

- Every other program runs at ring 3 in its own [[virtual memory|virtual address space]].
- Cannot touch hardware, swap page tables, or read another process's memory.

- The ==kernel== is a compiled binary like any other — text, data, BSS produced by the same toolchain — distinguished only by being loaded first and granted hardware privilege.
- Stays resident in RAM for the machine's entire uptime.

**Ring 0 and ring 3**

- The [[cpu]] enforces a ==privilege-level field== with two values that matter: ==ring 0== (==kernel mode==, all instructions allowed) and ==ring 3== (==user mode==, the privileged subset faults).
- The field itself is protected. User code cannot raise it; it changes only through the traps in `# Kernel Traps`.

**Supervisor pages**

- Each page-table entry carries a supervisor bit.
- A ring 3 access to a supervisor page raises a fault.

```
+-----------------------+
|    user processes     |   ring 3, restricted
+-----------------------+
|        kernel         |   ring 0, privileged
+-----------------------+
|       hardware        |
+-----------------------+
```

# [[virtual memory]]

- The [[cpu#MMU|MMU]] translates virtual to physical on every access, but the kernel writes the page tables the MMU walks.
- Each user program gets its own table; the kernel installs the right one when scheduling that program by writing its root address into `CR3`.
- Two user programs' writes to virtual `0x1000` translate to different physical pages. Page tables themselves live in supervisor-only memory; user code cannot rewrite the mapping that contains it.

# Kernel Traps

- User code is sealed at ring 3 but still needs services owned by the kernel: open a file, allocate memory, send a packet.
- Three events take the CPU from ring 3 to ring 0. Each vectors into a handler the kernel registered at [[boot]].

**Hardware interrupt**

- An external device (timer, disk, network card) raises a signal line into the CPU.
- Asynchronous — not caused by the running program.
- Drives time-slicing (timer fires the [[schedulers|scheduler]]) and wakes blocked programs.

**[[software interrupt]]**

- The current instruction faults: divide-by-zero, page fault, illegal opcode, privileged instruction at ring 3.
- Synchronous — caused by the program itself.
- The CPU latches the cause (e.g. faulting address into `CR2` for a page fault), pushes an error code, and traps into the handler.

**[[system calls]]**

- The user program deliberately traps in by executing a designated instruction (`syscall` on x86-64) with a syscall number and arguments in registers.
- The only legitimate path from user code to kernel services.

# [[processes]]

- A loaded user binary becomes a ==process==: a private virtual address space, kernel bookkeeping (open files, register snapshot, PID, parent), and at least one execution stream.
- Created by a parent process forking a copy of itself, then the child execing — overlaying its address space from a compiled executable on disk.
- The process is the unit the kernel multiplexes across the CPU.

# [[schedulers]]

- Many ready threads, few cores. The kernel decides which thread runs where and for how long.
- A periodic ==timer interrupt== fires on every core, forcing the CPU back into ring 0.
- The scheduler saves the current thread's registers, picks the next by policy, and restores its registers.

# [[file systems]]

- Programs need data that outlives them. Disks hand the kernel raw numbered blocks; the file system turns them into a tree of named files with permissions, sizes, and owners.
- User programs read and write through system calls (`open`, `read`, `write`, `close`).
- The kernel returns ==[[file descriptors]]== — small integers naming kernel-side file objects — that subsequent calls quote.

# [[boot]]

- The kernel is itself a program on disk. Something has to load it before any of the above can run.
- The CPU starts in a minimal 16-bit mode running firmware (==BIOS==), which loads a small ==bootloader== from a known location on disk, which loads the kernel binary.
- The kernel initializes hardware (registers trap handlers, builds the initial page tables, programs the timer) and hand-builds the first process, ==init== (PID 1). Every other user-space process descends from it via fork.
