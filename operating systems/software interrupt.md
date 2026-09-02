- An interrupt forces the CPU to stop its current instruction stream, jump to a kernel-supplied handler, and resume the original stream when the handler returns. The hardware mechanism that crosses the [[os#OS Spaces|kernel/user boundary]] in either direction.
- All three asynchronous-or-forced control transfers use the same machinery: hardware interrupts from devices, exceptions from the CPU itself, and software interrupts (==traps==) raised by user code. Differ only in who triggered them.

# Three Flavors

**Hardware interrupt**

- Raised by an external device asserting a signal line on the bus. Asynchronous — fires at any instruction boundary regardless of what the CPU is doing.
- Examples: timer tick, keyboard keypress, disk transfer complete, network packet arrival.

**Exception** (fault)

- Raised by the CPU itself when an instruction cannot be completed. Synchronous — always fires on a specific instruction.
- Examples: page fault (PTE marks the page absent — see [[virtual memory#Page Hits and Page Faults|page faults]]), divide-by-zero, invalid opcode, general protection fault.

**Software interrupt** (trap)

- Raised by user code executing a special instruction (`int n` on x86, `syscall` on x86-64, `svc` on ARM). Synchronous and deliberate.
- The user-side mechanism for [[system calls]] — a controlled way to enter ring 0.

# Interrupt Vector Table

- Each interrupt source has a numeric ==vector==. The CPU stores the base address of the ==interrupt vector table== (IVT, on x86 the IDT, ==Interrupt Descriptor Table==) in a privileged register. Each entry holds the address of the corresponding handler.
- On interrupt, the CPU reads the vector, indexes into the IVT, jumps to the handler address. The whole dispatch is hardware.

```
         Vector              IDT                  Handler code
                 +-----------------------------+
   N  ---index-->| handler address, ring level |---jump--> isr_N:
                 +-----------------------------+              push ...
                 | handler address, ring level |              ...
                 +-----------------------------+              iret
                 |          ...                |
                 +-----------------------------+
```

- The IVT is set up by the kernel at [[boot]]. User code cannot modify it — it sits in kernel memory.

# Handler Entry and Exit

- Before running the handler, the CPU must preserve enough state that the interrupted instruction stream can resume exactly where it left off.
	1. Hardware pushes the current `RIP` (instruction pointer), `CS` (code segment, includes ring level), and `RFLAGS` onto the kernel stack. For some interrupts it also pushes an error code.
	2. Hardware switches `CS` to the kernel's code segment (ring 0) and loads the handler address from the IVT.
	3. Handler runs. It saves any general-purpose registers it intends to clobber (push them, pop on exit).
	4. Handler executes `iret` (interrupt return). Hardware pops `RFLAGS`, `CS`, `RIP` and restores them in one atomic instruction. Execution resumes.

- For a hardware interrupt, the interrupted instruction had already completed. For an exception, the saved `RIP` points at the instruction that *caused* the fault — re-executing it after the handler resolves the fault (e.g. page fault loaded the missing page) lets the original instruction succeed.

# Interrupt Controller

- A chip (==PIC==, modern systems use ==APIC==) that sits between hardware devices and the CPU. Devices assert their request lines into the controller; the controller multiplexes them onto the CPU's single interrupt signal.
- Without it, the CPU would need one input pin per device. The controller turns N device lines into one CPU signal plus a vector number.
- Steps for a hardware interrupt:
	1. Device asserts its request line.
	2. Controller buffers it; if higher-priority requests are not pending, asserts the CPU's `INTR` line and supplies the vector.
	3. CPU completes its current instruction, saves state, runs the handler.
	4. Handler reads device status, services it, sends an ==EOI== (end-of-interrupt) to the controller.
	5. Controller is free to deliver the next pending request.

# Priority and Masking

- Interrupts have priority levels. The controller delivers higher priority before lower; a handler running at level $k$ blocks interrupts at level $\le k$ but can be interrupted by levels $> k$.
- ==Masking==: software can selectively disable specific interrupts. On x86, `cli` clears the interrupt-enable flag (mask all maskable interrupts); `sti` sets it. The non-maskable interrupt (NMI) bypasses this — used for hardware errors that must always be serviced.
- Masking is the primitive that builds [[locks#Interrupt Locks|disable-interrupts locks]] in the uniprocessor kernel. Used sparingly: while interrupts are masked, no device can be serviced — long masked regions cause dropped data and missed timer ticks.
