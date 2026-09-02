- How a pc boots, from beginning to end.

# Reset Vector

- At power-on, the [[cpu]]'s transistors force an initial register state. 
	- No software is needed, the silicone design forces the register values.
- [[x86 assembly#Registers|x86 segment registers]] have 2 segments:
	1. The visible 16-bit selector
	2. A hidden ==descriptor cache== that holds the actual base address the CPU uses for memory accesses.
- At reset, Intel hardcodes the CS descriptor cache base to `0xFFFF0000` and IP to `0xFFF0`. First fetch = `0xFFFF0000 + 0xFFF0 = 0xFFFFFFF0`. This location is the reset vector.
- The motherboard chipset has hardwired decode logic: any access to `0xFFFFFFF0` routes to the BIOS flash ROM chip, not to RAM. RAM has no stable contents at power-on.

**The far JMP**

- The ROM places a far `JMP` at `0xFFFFFFF0` targeting a real-mode address (typically `0xF000:0xE05B`).
- A far `JMP` reloads CS from its operand. When CS = `0xF000` loads, the descriptor cache base recomputes as `0xF000 × 16 = 0xF0000`. The CPU is now in true 16-bit real mode and will not revisit `0xFFFFFFF0` unless reset.

# Real Mode

- Real mode exists because Intel's compatibility contract required every x86 successor to the 8086 to reset into 8086-compatible behavior. The 8086 only had real mode. The 286 added protected mode but still reset into real mode. Every chip since has followed this.
- Physical address = segment × 16 + offset. Both values are 16-bit: the address space tops out at 1 MB.

**Memory map**

```
+------------------+ 0xFFFFF (1 MB)
| BIOS ROM shadow  |
+------------------+ 0xE0000
| Option ROMs      |  (VGA BIOS, NIC firmware)
+------------------+ 0xC0000
| Video RAM        |
+------------------+ 0xA0000
| Conventional RAM |  ~640 KB usable
+------------------+ 0x00500
| BIOS Data Area   |
+------------------+ 0x00400
| Interrupt table  |  256 entries
+------------------+ 0x00000
```

- The region `0xA0000`–`0xFFFFF` is hardware-reserved. The usable RAM below it is called ==conventional memory==.

# BIOS and POST

- BIOS (Basic Input/Output System) is firmware stored in flash ROM on the motherboard. It is the first software to run, entirely in real mode.
- After the far JMP from the reset vector, the BIOS executes POST (Power-On Self Test) before searching for a boot device.

**POST sequence**

- Disables caches, flushes the TLB, sets MSRs to safe defaults.
- Tests RAM: writes patterns, reads them back, marks bad ranges in the BIOS Data Area (`0x00400`–`0x004FF`).
- Programs the chipset: memory controller, PCIe lanes, USB controllers.
- Walks the PCI bus and runs each device's option ROM (e.g. the GPU's VGA BIOS).

**Interrupt Vector Table**

- The ==IVT== occupies `0x00000`–`0x003FF`: 256 entries × 4 bytes, each a `segment:offset` pair pointing to the interrupt handler for that interrupt number.
- The BIOS populates it with handlers for hardware events and BIOS service calls (INT 10h for video, INT 13h for disk).
- The kernel replaces the IVT with its own IDT (Interrupt Descriptor Table) during initialization.

# Boot Device and MBR

- After POST, the BIOS iterates the boot-order list stored in CMOS/NVRAM. For each candidate device it calls INT 13h to read physical sector 0 (512 bytes) into RAM at `0x7C00`.
- It checks bytes 510–511 for `0x55 0xAA`. Absent: skip to the next device. Present: jump to `0x7C00`. Control leaves the BIOS permanently.

**MBR layout**

```
+------------------+  byte 0
| Stage 1 code     |  446 bytes
+------------------+  byte 446
| Partition table  |  64 bytes (4 × 16-byte entries)
+------------------+  byte 510
| Boot signature   |  0x55 0xAA
+------------------+  byte 512
```

- 446 bytes cannot hold filesystem drivers. Stage 1's only job is to chain-load a larger stage.

# A20 Line

- The 8086 had 20 address lines (A0–A19). A segment:offset pair can produce a 21-bit result: `0xFFFF:0xFFFF = 0x10FFEF`. On the 8086 this wrapped to `0x0FFEF` because A20 did not exist.
- Programs depended on this wrap. When the 286 added a real A20 line and broke the wrap, IBM gated A20 through the 8042 keyboard controller to preserve it. A20 disabled: addresses above 1 MB wrap. A20 enabled: bit 20 passes through.
- The gate must be opened before any mode transition that accesses memory above 1 MB.

**Enabling A20**

- Legacy: command sequence through keyboard controller ports `0x64` and `0x60`.
- Fast path (modern chipsets): set bit 1 of port `0x92`. One write, no handshake.

# Bootloader

- The MBR's 446 bytes cannot read a filesystem or hold mode-switching logic. Real bootloaders use multiple stages; xv6 collapses to two files.

**Stage 1 (MBR code)**

- Reads the next stage from a fixed sector range (sectors 1–62, the gap before the first partition) and jumps there.

**Stage 1.5**

- ~32 KB. Has filesystem drivers (ext4, FAT, etc.) built in. Reads the full bootloader from the filesystem by path.

**Stage 2**

- Full bootloader in RAM. Presents a boot menu, reads the kernel from the filesystem, enables A20, executes the mode transitions below, then jumps to the first kernel instruction.

**xv6 — bootasm.s**

- xv6's stage 1 is `bootasm.s`: [[x86 assembly]] that enables A20, transitions the CPU to 32-bit protected mode, then calls `bootmain`.

**xv6 — bootmain.c**

- Runs in 32-bit protected mode. Sets the stack pointer (`ESP`) to `0x7C00` (the now-vacated MBR area). Reads the kernel from disk, parses its ELF headers, copies each segment to the linker-specified address, then jumps to the first kernel instruction.

**xv6 — kernel.ld**

- A ==linker script==: tells the linker how to combine `.o` files into the kernel binary and where to position each section. Defines two values `bootmain.c` reads from the ELF headers: ==physical load address== (where the kernel is copied in RAM) and ==entry point== (the address of the first instruction).

# Protected Mode Transition

- Real mode has no memory protection and a 1 MB ceiling. Protected mode enables 4 GB addressing and hardware-enforced privilege rings. The CPU does not switch automatically; the bootloader triggers it with three steps.

**Step 1 — build the GDT**

- Protected mode resolves segment addresses through descriptors, not the `segment × 16` formula. The GDT (Global Descriptor Table) is a table in RAM of 8-byte ==segment descriptors==, each encoding a segment's base address, limit, and access rights.
- Minimum flat model: a mandatory null entry (index 0), a flat code descriptor (base 0, limit 4 GB, executable), and a flat data descriptor (base 0, limit 4 GB, writable).
- `LGDT` loads the GDT's physical address and size into the GDTR register.

**Step 2 — set CR0.PE**

- `CR0` is the mode-control register. Setting bit 0 (PE, Protection Enable) arms protected mode. The CPU is now in protected mode but CS still holds the old real-mode descriptor cache values.

**Step 3 — far jump**

- A far jump forces CS to reload by fetching a new descriptor from the GDT. This flushes the instruction pipeline and commits the CPU to 32-bit instruction decoding with GDT-described segments.
- After the jump: 32-bit protected mode, 4 GB flat address space, paging still off.

# Long Mode Transition

- 32-bit protected mode tops out at 4 GB. 64-bit long mode requires paging and PAE-widened page-table entries. The kernel's early setup code executes five steps.

**Step 1 — enable PAE**

- Set bit 5 of `CR4`. This widens page-table entries from 32 bits to 64 bits, which long mode requires. PAE alone does not change the address space.

**Step 2 — load CR3**

- Write the physical address of the top-level page table (PML4) into `CR3`. A minimal identity-mapped [[virtual memory|page table]] must be present before paging is enabled or the next fetch faults.

**Step 3 — set EFER.LME**

- `EFER` is a model-specific register. Bit 8 (LME, Long Mode Enable) arms long mode but does not activate it yet.

**Step 4 — enable paging**

- Set bit 31 of `CR0` (==PG==). With PE, PG, and LME all set, long mode activates — but the CPU enters ==compatibility mode== first (32-bit code executing under long-mode page tables).

**Step 5 — far jump to 64-bit code segment**

- The GDT must contain a 64-bit code descriptor with the L bit set. A far jump to that selector reloads CS and switches the CPU to 64-bit instruction decoding.

# Kernel Entry

- With long mode active (or 32-bit protected mode in xv6), the kernel binary's entry point runs for the first time.
- In xv6, `kernel.ld` points the entry to `entry.S`. At this moment paging is off; only physical addresses are valid.
- `entry.S` builds an initial page table mapping `0x80000000` → `0x00000000`, sets the paging bit, then jumps to `main()`.
- `main()` initializes devices, registers interrupt handlers, and builds the full [[virtual memory|virtual address layout]] before launching the scheduler.

# init

- `main()` hand-builds the first process. There is no parent to fork from — nothing else is running yet.
- PID 1 is always init. The kernel constructs its process struct and address space directly in memory.
- After starting, init:
  1. Opens the console device for standard I/O.
  2. `fork()`s a child and `exec()`s the shell (`sh`).
  3. Loops on `wait()`, reaping orphaned [[processes]] whose parent has exited.
- Every user-space process is a descendant of init. It is the root of the process tree.
