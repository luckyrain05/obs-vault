- A deeper dive into the [[hardware architecture]] memory unit.
- ==Random access memory== is the memory unit of the Von Neumann model — the working storage the CPU reads and writes while a program runs.
- ==Random access==: any address is reachable without a physical seek (access time varies with memory state; covered in # Timing).
- Volatile: all state is lost the moment power is removed.

# Why RAM

- A CPU stalled on storage is idle. Hard drives and SSDs are $10^4$–$10^6$× slower than the CPU; reading program data from disk on every instruction would reduce the CPU to a fraction of its rated speed.
- RAM is the intermediary: fast enough to keep the CPU fed (tens of nanoseconds vs milliseconds for disk), large enough to hold the working set of running processes.
- Even RAM cannot fully close the gap to the CPU — the remaining speed difference is what motivates [[cache]].

# DRAM cell

- DRAM achieves density by storing each bit as charge in a capacitor. The transistor's gate is driven by the ==word line==; when it goes high, the transistor opens and connects the capacitor to the ==bit line==. Capacitor charged = 1; discharged = 0.

**1T1C cell**

- One transistor + one capacitor per bit. The word line is the select wire; the bit line is the shared data wire connecting the cell to the rest of the array.
- Charged capacitor drives the bit line high when the word line opens the transistor; uncharged drives it low.

```
  word line
      |
  +---+---+
  | NMOS  |  (transistor)
  +---+---+
      |
  +---+---+
  |  cap  |  (capacitor)
  +-------+
      |
    GND        bit line runs through transistor drain
```

**Refresh**

- Capacitors leak charge on a millisecond timescale. Without intervention, a stored 1 degrades to an indeterminate voltage and the bit is lost.
- Every cell must be re-read and restored within 64 ms. The read is destructive — it pulls charge from the capacitor — so the restoration step writes the amplified value back.
- During refresh, cells are unavailable for access requests; this pause is a real, observable stall.

**Volatility**

- Charge requires continuous power to maintain. No power → capacitors discharge → all bits lost immediately.
- DRAM is volatile by construction. Persistent storage requires a different medium.

# Memory array

- Cells are arranged in a 2D grid. Word lines run horizontally — one word line per ==row==. Bit lines run vertically — one per column. Raising a word line connects every cell in that row to its bit line simultaneously.
- A row is the minimum activation unit — typically 8 KB. The array cannot activate a single cell; the entire row activates together.

**Bank**

- One 2D array of rows and columns. All cells in a bank share detection circuitry along one edge.
- A bank can have only one row active at a time. Accessing a second row requires closing the current one first.

**Rank**

- Multiple DRAM chips are wired in parallel so their combined data output is 64 bits wide — one full cache line per transfer. All chips respond to a single command simultaneously; this group is a rank.
- A physical module typically holds one or two ranks.

**DIMM**

- ==Dual Inline Memory Module==: the physical card inserted into the motherboard slot. Carries the chips, power rails, and signal routing.

**Channel**

- An independent 64-bit bus connecting the controller to a set of DIMMs. Two channels double available bandwidth because both operate simultaneously and independently.

```
+-------+   +-------+   +-------+
| cell  |   | cell  |   | cell  |  ...  (rows x columns = bank)
+-------+   +-------+   +-------+
      \           |           /
       +----------+-----------+
              bank
         (multiple banks)
              |
           +------+
           | rank |  (all chips together, 64-bit wide)
           +------+
              |
           +------+
           | DIMM |  (one or two ranks per module)
           +------+
              |
          +---------+
          | channel |  (independent 64-bit bus)
          +---------+
              |
          +------------+
          | controller |
          +------------+
```

# Access protocol

- Reading from DRAM requires three sequential hardware phases, each with a mandatory minimum wait before the next can begin.

**Precharge**

- Bit lines must be driven to $V_{DD}/2$ — the midpoint between 0 and $V_{DD}$ — before a row can be activated.
- Signal detection works by measuring a tiny voltage delta above or below this midpoint. Starting at the midpoint maximizes sensitivity to both 0 and 1 cells.

**Row activate (RAS)**

- The word line for the target row goes high; every transistor in the row opens and connects its capacitor to its bit line.
- Each bit line receives a tiny voltage delta above or below $V_{DD}/2$. ==Sense amplifiers== along the edge of the array detect these deltas and amplify them to full 0/1 levels.
- The entire row is latched into the ==row buffer== — a fast register holding the amplified live row state.
- The read is destructive: amplification draws charge from the capacitor. Sense amplifiers write the amplified value back immediately, restoring the charge.

**Column select (CAS)**

- The controller sends a column address. The row buffer drives the bytes at the requested column address onto the data bus.
- Subsequent column accesses within the same open row hit the row buffer directly — no precharge or RAS needed.

- After the access, the controller issues a precharge command: bit lines reset to $V_{DD}/2$, the word line de-asserts, the row closes.

```
  bit lines at V_DD/2
        |
  [Precharge]
        |
  word line raised
        |
  [Row Activate / RAS]   --> sense amps fire --> [Row Buffer latched]
        |                                                 |
  column address                                          |
        |                                                 v
  [Column Select / CAS] <--------------------------[Row Buffer]
        |
  data on bus
        |
  [Precharge] (close row)
```

# Timing

- Each phase of the access protocol carries a minimum wait measured in clock cycles. Their sum is the cold-access latency.

**tRCD**

- RAS-to-CAS delay: minimum wait between row activate and column select.
- Physically: time for sense amplifiers to settle after the word line rises. The row buffer does not hold valid data until tRCD expires.

**CL**

- CAS latency (also tCAS): minimum wait between column address and data appearing on the bus.
- Physically: time for the row buffer to read out the selected columns and drive them onto the data bus.

**tRP**

- Precharge time: minimum wait between a precharge command and the bit lines stabilizing at $V_{DD}/2$, ready for the next row activate.

**Cold access total**

- Cold access (no row currently open in the target bank): tRP + tRCD + CL.
- At DDR4-3200 with CL16: tRP ≈ 15 ns, tRCD ≈ 15 ns, CL ≈ 10 ns → ~40 ns best case. Including bus travel and controller overhead, software-visible latency is typically quoted at ~70–100 ns.

**Row buffer hit**

- If the needed address is in a row already open in the row buffer, skip precharge and RAS; pay only CL.
- Sequential access within a row is substantially faster than random access across rows.
- "Random access" means any address is reachable without a physical seek. It does not mean uniform latency — row buffer hits and misses produce measurably different access times.

# Memory controller

- The memory controller sits between the CPU and the DIMMs; in modern systems it is integrated onto the CPU die, eliminating a chipset hop on the critical read path.

**Address translation**

- The CPU issues physical addresses. The controller maps each to a (channel, DIMM, rank, bank, row, column) tuple that locates the specific cells.
- Bank interleaving: consecutive cache-line addresses are typically spread across different banks so successive accesses can be pipelined across independently operable arrays rather than serialized within one bank.

**Refresh scheduling**

- The controller issues `AUTO REFRESH` commands cycling through all cells, completing a full pass within 64 ms.
- During each refresh command, the bank being refreshed cannot serve access requests; the controller queues pending accesses and drains them once refresh completes.

**Open-page policy**

- After an access, leave the row open in the row buffer. If the next access targets the same row, it pays only CL.
- Optimal for sequential workloads where consecutive accesses fall in the same row.

**Closed-page policy**

- Precharge immediately after every access. The next access always pays tRP + tRCD + CL.
- Avoids the ==conflict== case: a new access targeting a different row in the same bank while the old row is open must first close the old row (tRP) before opening the new one — paying the full cold-access penalty regardless of policy. Closed-page makes the cost uniform and predictable for random-access workloads.

# Bandwidth

- Transfer rate and access latency are orthogonal metrics. A random access still pays the full tRP + tRCD + CL latency regardless of clock speed.

**DDR**

- DDR = Double Data Rate: the data bus transfers on both the rising and falling clock edge, doubling throughput relative to a single-edge clock at the same frequency.
- DDR4-3200: 3200 million transfers per second. With a 64-bit (8-byte) bus: $3200 \times 10^6 \times 8 = 25.6$ GB/s peak per channel.

**Bandwidth vs latency**

- High transfer rate increases throughput for sequential bulk reads — streaming a large buffer efficiently uses the pipeline.
- It does not reduce tRP + tRCD + CL. Bandwidth and latency are independent; improving one does not move the other.

**DRAM vs SRAM**

- SRAM (Static RAM) uses 6 transistors per cell — a cross-coupled latch with no capacitor and no refresh requirement.
- Access time: ~1 ns. Density: 50–100× lower than DRAM. Cost per bit: 50–100× higher.
- DRAM wins on cost and density; SRAM wins on speed. This is why [[cache]] is SRAM and main memory is DRAM — they are complementary, not interchangeable.
