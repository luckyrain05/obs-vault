- x86 translates code and data addresses using segment registers — Intel's solution to the 8086's mismatch between 16-bit registers and a 20-bit address bus.
- Each segment register carries a hidden ==descriptor cache==: the base address, limit, and access rights the CPU precomputes and uses for every memory access.
- Prereqs: [[x86 assembly]] (segment registers, instruction mnemonics). The protected-mode form is exercised in [[boot]]; segmentation is replaced by [[virtual memory]] in modern kernels.

# The 8086 Problem

- The 8086 had 20 address lines: $2^{20}$ = 1 MB addressable physical memory.
- Its registers were 16-bit: a single register could only express $2^{16}$ = 64 KB of addresses.
- One register cannot reach 1 MB. Intel's solution: combine two 16-bit values to produce a 20-bit physical address.

# Real-Mode Segmentation

- The CPU left-shifts the segment register by 4 bits and adds the 16-bit offset: `physical = (segment << 4) + offset`.
- The shift promotes the segment to bits [19:4] of the result; the offset contributes bits [15:0]. Bits [15:4] overlap, so the two values are added, not concatenated.

```
segment:   SSSS SSSS SSSS SSSS 0000   (shifted left 4)
offset:    0000 OOOO OOOO OOOO OOOO   (16-bit offset)
           ----------------------------
physical:  PPPP PPPP PPPP PPPP PPPP   (20-bit result)
```

- The overlap means multiple segment:offset pairs can address the same physical byte (aliasing). This is a property of the model, not a bug.

**Segment registers and their implicit roles**

- `CS` — Code Segment. Every instruction fetch uses `CS` as the segment. The instruction pointer is always `CS:IP`.
- `DS` — Data Segment. Default segment for data reads and writes (`mov`, arithmetic memory operands).
- `SS` — Stack Segment. Used implicitly by `ESP` and `EBP`; all stack operations (`push`, `pop`, stack-relative loads) address `SS:ESP`.
- `ES` — Extra Segment. Used by string instructions (`movsb`, `stosb`, `scasb`) as the destination segment.
- `FS`, `GS` — No fixed hardware role in real mode. Kernel-assigned in protected mode.

# The Descriptor Cache

- Every segment register has two parts: a visible 16-bit selector and the hidden descriptor cache.
- The CPU loads the descriptor cache when a value is written into a segment register (including via a far `JMP`). All subsequent memory accesses consume the cache; the visible selector is not re-read on each access.

```
+--------------------+--------------------------------------------------+
| Visible selector   | Hidden descriptor cache                          |
| (16 bits)          | base (32-bit) | limit (20-bit) | access rights   |
+--------------------+--------------------------------------------------+
```

- In real mode the CPU computes the cache base as `selector × 16` at load time. Memory accesses then use `cache_base + offset` — same arithmetic, but precomputed once.

**Reset vector consequence**

- At power-on, Intel hardcodes the CS descriptor cache base to `0xFFFF0000` while the visible CS selector is `0xF000`. The `× 16` formula would give `0xF0000`, but the hidden cache overrides it.
- IP is forced to `0xFFF0`. First fetch = `0xFFFF0000 + 0xFFF0 = 0xFFFFFFF0` — the reset vector, located in ROM.
- When ROM executes a far `JMP` to `0xF000:0xE05B`, the CPU writes `0xF000` into CS. This reloads the cache base as `0xF000 × 16 = 0xF0000`. The CPU is now in true real mode.

# Protected-Mode Segmentation

- In protected mode the visible selector is no longer a base address. It is a 16-bit index structure pointing into the Global Descriptor Table (GDT) in RAM. Writing a selector causes the CPU to fetch the GDT entry and load its fields into the descriptor cache. Memory accesses still use only the cache.

**Selector layout**

```
+-----------------------------------------------+----+-----+
| Index (13 bits) — GDT entry number            | TI | RPL |
+-----------------------------------------------+----+-----+
  bits [15:3]                                   bit2  [1:0]
```

- TI (Table Indicator): 0 = GDT, 1 = LDT (local descriptor table, rarely used).
- RPL (Requested Privilege Level): privilege of the requestor — 0 = kernel, 3 = user.

**GDT structure**

- The GDT is an array of 8-byte ==segment descriptors== in RAM. The bootloader allocates it and loads its address and size into the GDTR register via `LGDT`.
- Index 0 is the mandatory ==null descriptor== — a zeroed entry. Loading it into a segment register and then accessing memory faults immediately.

**Descriptor fields**

- Base address (32 bits, split across the 8-byte entry for historical layout reasons): where the segment starts in physical memory.
- Limit (20 bits + granularity bit): size of the segment. If the granularity bit is set, limit is in 4 KB pages; otherwise in bytes.
- Access byte: encodes descriptor type (code/data), privilege ring (DPL), and present bit. The CPU checks DPL against CPL (current privilege level in CS) on every access.

# Flat Model

- Modern OSes set every GDT descriptor to base = 0, limit = 4 GB. The address formula becomes `physical = 0 + offset = offset`. Segmentation is arithmetically neutralized.
- Paging replaces segmentation for isolation: it operates at 4 KB granularity per page rather than per segment, and maps virtual to physical addresses independently of the segment base.
- `FS` and `GS` remain active in the flat model. The kernel writes non-zero bases into them for thread-local storage (user space) and per-CPU kernel data structures.
- In 64-bit mode the CPU ignores the base and limit of `CS`, `DS`, `SS`, and `ES` entirely. Only `FS` and `GS` bases are honored, set via model-specific registers rather than the GDT.
