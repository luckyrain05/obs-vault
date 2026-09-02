- A deeper dive into the [[hardware architecture#CPU|CPU]].
- Programs are sequences of binary instruction words stored in memory; the CPU fetches each word, interprets it, and applies it to data — cycling until the program ends.
- The ==ISA== (instruction set architecture) is the contract that defines what words mean; everything below the ISA is the CPU's private implementation, invisible to software.

# ISA

- The ==instruction set architecture== defines the instructions that the CPU is capable of and the registers that the programmer can read/write with.
- Two CPUs with the same ISA can run the same binary even if their internal designs are completely different.

**Opcode**

- The bits that name the operation (add, load, store, branch, ...).
- The ISA encoding specifies which bit positions hold the opcode for each instruction type.

**Operands**

- The bits that name what to operate on: a register number, an immediate constant embedded in the instruction, a memory displacement, or some combination.
- Which operand fields exist and how wide they are is fixed per instruction type by the ISA encoding.

# Programmer-visible state

- The state the ISA exposes. Every instruction reads from this state and writes back to it.
- The ISA specifies exactly which parts of this state exist; the hardware implements them however it likes as long as the observable results match the specification.

**Registers**

- Named, fixed-width storage slots inside the CPU. Reading is single-cycle; writing completes at the clock edge.
- The ISA names how many registers exist and how wide each is.

**Program counter**

- A special register holding the address of the next instruction to fetch.
- Updated every cycle: either PC + instruction length (sequential) or a branch target.

**Main memory**

- The flat byte-addressed array described in [[memory]].
- Both instructions and data live here. Instructions sit at the addresses the compiler placed them; data lives in segments the OS maps per-process.

# What a program is

- A program is a sequence of instruction words stored at consecutive addresses in memory.
- The compiler turns source code into those words and places them at known addresses. The CPU never sees source; it only sees binary words.
- Executing the program is the CPU consuming those words one at a time, each instruction transforming programmer-visible state.
- Control flow (branches) changes which address the PC takes next, so execution need not be strictly sequential — but it is still one instruction at a time, one address at a time.

# The data path

- The wires and units that carry data through one fetch-decode-execute iteration.
- Purely combinational — every component here is gates and muxes, no memory inside. Programmer-visible state lives in the clocked registers named above.
- Every component is built from primitives in [[logic gates]].

**Instruction memory port**

- The CPU drives the PC value onto the bus; memory returns the instruction word.
- In real chips, fronted by an L1 instruction [[cache]] so access is single-cycle on a hit.

**Register file**

- Two read ports return operand values combinationally the same cycle the addresses arrive.
- One write port: on the clock edge, if the control unit asserts write-enable, the addressed register captures the result.
- Construction from [[logic gates#Sequential storage|sequential logic]].

**Decoder**

- Splits the fetched instruction word into named fields by hardwired bit position.
- The opcode field goes to the control unit; register-number fields go to the register file's read addresses; the immediate field is sign-extended to the full word width.

**[[ALU]]**

- Computes the result: an arithmetic or logic operation on two inputs. The [[alu]] note owns the mechanism.
- Produces a result value and a flag bundle (zero, negative, carry, overflow) always available on the output wires.

**A mux and B mux**

- Select what feeds the ALU's two inputs.
- B mux's common job: pick between a register value (register-register op) or the sign-extended immediate (register-immediate op, or a memory displacement).

**Data memory port**

- Read port for loads: address = ALU result; memory read data is made available as output.
- Write port for stores: address = ALU result; data = source register value.
- Fronted by an L1 data [[cache]] in real chips.

**Writeback mux**

- Selects what lands at the register file's write port: ALU result (for arithmetic) or memory read data (for loads).

**PC mux**

- Selects the next PC: PC + instruction length (sequential), a branch target (PC-relative), an absolute immediate, or a register value (indirect branch).
- The branch case is gated by the flag bundle: only takes the branch target if the relevant flag matches the condition.

```
   +------+
   |  PC  | <-----------------------------------------------------+
   +------+                                                       |
       |                                                          |
       v                                                          |
  +----------+                                                    |
  |  instr   |                                                    |
  |  memory  |                                                    |
  +----------+                                                    |
       |                                                          |
       v                                                          |
  +----------+                                                    |
  |  decoder |                                                    |
  +----------+                                                    |
  |  |   |  |                                                     |
  |  |   |  +-- opcode --> control unit --> all mux selects       |
  |  |   +---- imm ---------------------------+                   |
  |  +-- regA#                                |                   |
  +---- regB#                                 |                   |
       regD#                                  |                   |
          |                                   |                   |
          v                                   |                   |
  +---------------+                           |                   |
  | register file |                           |                   |
  +---------------+                           |                   |
     rdA |  rdB |                             |                   |
         v      v                             v                   |
      +------+ +------+                                           |
      | A mux| | B mux| <-- imm                                   |
      +------+ +------+                                           |
          |       |                                               |
          v       v                                               |
        +---------+                                               |
        |   ALU   | ---- flags ---> [flags reg]                   |
        +---------+                                               |
              |                                                   |
              v                                                   |
        +----------+                                              |
        |   data   |                                              |
        |  memory  | <-- addr=ALU result, data=rdB (for stores)   |
        +----------+                                              |
              |                                                   |
              v                                                   |
        +----------+                                              |
        |  WB mux  | --> register file write port                 |
        +----------+                                              |
                                                                  |
   +---------+                                                    |
   |  PC mux | <-- branch target (ALU result, gated by flags)     |
   +----+----+ <-- absolute immediate                             |
        |       <-- register value (indirect branch)              |
        |       <-- PC + instr_len (sequential default)           |
        +----------------------------------------------------------+
```

- Every cycle: all wires settle combinationally, then the clock edge captures stable values into PC, the flags register, and the register file write port (and data memory, for stores). The next cycle begins with PC pointing at the next instruction.

# The control unit

- A combinational block with no state.
- Input: opcode bits from the decoder.
- Output: every mux select in the data path, the ALU's operation select, and enable signals (register write, memory read, memory write, flag write).
- Mechanically a truth table compiled into gates: each output is a Boolean function of the opcode bits; synthesis turns the table into an AND-OR-NOT network.

# Instruction cycle

- The CPU repeats this loop for every instruction. In a single-cycle data path, all four phases happen within one clock period.
- Fetch: PC drives instruction memory; the instruction word comes back.
- Decode: the decoder splits fields; the control unit emits signals; the register file reads operands.
- Execute: the ALU computes; data memory reads or writes if needed; the PC mux selects the next PC.
- Writeback: on the rising clock edge, PC, the flags register, the register file, and (for stores) data memory latch their new values.

```
+-------+    +--------+    +---------+    +-----------+
| Fetch | -> | Decode | -> | Execute | -> | Writeback |
+-------+    +--------+    +---------+    +-----------+
    ^                                           |
    +-------------------------------------------+
```

- The four labels are combinational regions within one clock period, not separate periods. The edge at the end of Writeback is what makes them discrete.

# The clock

**Definition**

- A square wave wired to every sequential element: PC, the flags register, the register file write port, and the data memory write port.
- On every rising edge, the [[logic gates#Sequential storage|D flip-flops]] inside those elements capture their current inputs.
- The interval between two rising edges is one ==clock cycle==.

**Cycle time bound**

- Combinational logic must finish settling before the edge. The longest path from any flip-flop output to any flip-flop input bounds the minimum cycle time:
- $T_{clk} \geq T_{prop\_max} + T_{setup} + T_{skew}$
- $T_{prop\_max}$: worst-case propagation delay through the combinational logic. $T_{setup}$: flip-flop setup time. $T_{skew}$: clock distribution skew across the chip.
- Clock speed is $1 / T_{clk}$. Going faster requires shortening the longest combinational path — better gates, fewer logic levels, or [[pipelining]].

# [[pipelining]]

- The single-cycle data path's clock period is bounded by the slowest instruction's path through the diagram.
- Pipelining cuts the path into stages, each with its own short clock period, so a new instruction enters every cycle while earlier instructions are still completing.

# Cores

- A modern CPU packages several independent execution units on one die.
- Each core has its own register file, ALU, control unit, PC, flags register, and private L1/L2 [[cache]].
- Cores share L3 cache and RAM.

```
+----------------------------------------------+
|                     CPU                      |
|  +--------+  +--------+  +--------+          |
|  | Core 0 |  | Core 1 |  | Core 2 |   ...    |
|  | L1, L2 |  | L1, L2 |  | L1, L2 |          |
|  +--------+  +--------+  +--------+          |
|  +----------------------------------------+  |
|  |                L3 cache                |  |
|  +----------------------------------------+  |
+----------------------------------------------+
                       |
                       v
                  +---------+
                  |   RAM   |
                  +---------+
```

- Each core executes one [[threads|thread]] at a time. The OS [[schedulers|scheduler]] assigns runnable threads to free cores. With $N$ cores and $T$ threads, up to $N$ execute truly simultaneously; the rest wait.

# [[virtual memory]]

- Programs are compiled against virtual addresses — each program's address space starts at 0 and appears private. RAM has one physical address space shared by all programs.
- The MMU (memory management unit) sits between the data path's memory ports and the bus, translating every virtual address the data path emits to a physical address before it leaves the chip.
- Full mechanism — TLB, page table walk, permission checks, context switch: [[virtual memory]].

# Bus

- The shared wires between the CPU and RAM. Three lanes operate together on each access.

**Address bus**

- CPU-driven. Carries the physical address of the word to read or write.
- Width bounds the physical address space: $N$ wires give $2^N$ addressable bytes.

**Control bus**

- CPU-driven. Carries the operation type (read or write) and timing signals.

**Data bus**

- Bidirectional. CPU drives on writes; RAM drives on reads.

**Read/write protocol**

- Read: CPU places the address on the address bus and signals read on the control bus; RAM drives the word onto the data bus.
- Write: CPU drives both address and data; RAM stores.
