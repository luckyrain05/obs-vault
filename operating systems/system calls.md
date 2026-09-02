- The user-mode program's only way to invoke kernel services. A deliberate [[software interrupt#Three Flavors|trap]] that crosses the [[os#OS Spaces|privilege boundary]] under the kernel's control.
- The instruction-level mechanism lives in [[x86 assembly]]; this file covers the kernel-level dispatch on top.
- The kernel cannot trust user code to be correct, so the syscall path is hardened: a fixed entry instruction, kernel-controlled dispatch, validated arguments, and a documented return convention.

# Why a Trap

- Functions that allocate memory, open files, or send packets all need to touch hardware or kernel-owned data. User code at ring 3 cannot do that directly — the relevant instructions and pages are privileged.
- A direct call (`call kernel_open`) is impossible: ring-3 code cannot jump to a ring-0 address; the page is supervisor-only, and the call would fault as a [[software interrupt#Three Flavors|protection exception]].
- A controlled trap solves both problems. The user runs one designated instruction; the hardware atomically raises the privilege level *and* jumps to a kernel-chosen address, in one step. The kernel chose the entry point at [[boot]]; user code cannot redirect it.

# Calling Convention

- The kernel exposes each system call as a numeric ID. The convention specifies which registers carry the syscall number, the arguments, and the return value.
- On x86-64 Linux:

```
rax  syscall number
rdi  arg 1
rsi  arg 2
rdx  arg 3
r10  arg 4
r8   arg 5
r9   arg 6
syscall    ; the instruction
rax  return value (negative on error: -errno)
```

- On 32-bit x86 the historical entry was `int 0x80` with arguments in `ebx, ecx, edx, esi, edi, ebp`. Modern x86-64 uses the dedicated `syscall` instruction — same effect, faster path (no IDT lookup; the entry address is in a Model-Specific Register).

# The Trap Path

```
1. User code loads syscall number into rax, args into rdi/rsi/...
2. User code executes `syscall`.
3. Hardware raises privilege to ring 0, loads RIP from the syscall MSR
   (LSTAR), saves the user RIP and RFLAGS into other MSRs.
4. Kernel entry stub switches to the kernel stack for this thread,
   saves the rest of the user registers.
5. Kernel reads rax, indexes into the syscall table, calls the handler.
6. Handler validates arguments, performs the work, sets rax to the
   return value.
7. Kernel entry stub restores user registers from the saved frame.
8. `sysret` returns to ring 3 with the saved RIP and RFLAGS.
```

- The syscall table is a kernel-internal array of function pointers indexed by syscall number. An invalid number returns `-ENOSYS`.

# Argument Validation

- A user-supplied pointer cannot be trusted. The kernel must check that:
	- The pointer lies in the user portion of the address space (not the kernel half).
	- The pointed-to range is mapped in the calling process's [[virtual memory|page table]] with the required permission (read for input buffers, write for output buffers).
- A malicious or buggy program could otherwise pass a pointer into kernel memory, tricking the kernel into reading or writing privileged data on its behalf. The check happens at the syscall boundary; once validated, the kernel uses dedicated copy routines (`copy_from_user`, `copy_to_user`) that handle a fault gracefully if the page is later unmapped.
- Sizes (lengths, counts) are also clamped to prevent integer overflow or read-past-end.

# Library Wrappers

- User code rarely emits the `syscall` instruction directly. The C library provides one wrapper per syscall — `read()`, `write()`, `open()`, `fork()` — that loads the registers, traps, and converts the return value to the C convention (errors return -1 and set `errno`).
- The wrapper is the [[api]]; the trap is the mechanism. The kernel only sees the trap.
