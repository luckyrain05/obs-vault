- ==Pipelining== is a rearrangement of the [[cpu#The data path|single-cycle data path]] so that multiple instructions are in flight at the same time, each at a different stage of execution.
- Throughput rises without changing the ISA the CPU executes.
- Built from the same primitives as the rest of the data path: combinational [[logic gates|gate]] networks for the work, [[logic gates#Sequential storage|D flip-flops]] arranged into pipeline registers for the seams between stages.

# Why pipelining exists

- A [[cpu#The data path|single-cycle data path]] does one full instruction per clock edge.
- The clock period must be long enough that the *longest* instruction's combinational path settles before the edge arrives:
- $T_{clk} = \max_{\text{instr}} \text{ (combinational delay of that instruction)}$

**Slack**

- A `nop` and a `mov reg, [base+disp]` share the same clock period even though the `nop` could be done in a fraction of it.
- Every short instruction gives the cycle back unused.

**Headroom for one**

- The longest instruction (typically a memory-touching one) sets the floor.
- Even if 99% of executed instructions are short ALU ops, the clock cannot speed up because the rare long one must still fit.

**The fix**

- Slice the long path into shorter ones.
- Each slice runs on its own short clock period.
- As long as you can hand the partial result of slice $k$ to slice $k+1$ on the next edge, the overall throughput is one full instruction per *short* cycle — even though each instruction now spans several short cycles end to end.

# Pipeline registers

- The seams between stages must remember stage $k$'s outputs from one clock edge to the next so stage $k+1$ has a stable snapshot to read.
- The mechanism is a row of [[logic gates#Sequential storage|D flip-flops]] called a ==pipeline register==.
- On every rising clock edge, the pipeline register captures whatever stage $k$ produced during the just-elapsed cycle.
- From that moment, stage $k+1$'s combinational logic sees a frozen input while stage $k$ starts working on the *next* instruction's data.
- Same D-flip-flop construction as a programmer-visible [[logic gates#Sequential storage|register]], differing only in role: programmer-visible registers are the ISA's named storage; pipeline registers are anonymous storage between hardware stages, invisible to the program.

```
       stage k                pipeline register             stage k+1
  +---------------+               +-----+               +---------------+
  |  combinational| ---data--->   |  D  |   ---data---> |  combinational|
  |    logic      |               |     |               |    logic      |
  +---------------+               +-----+               +---------------+
                                     ^
                                     |
                                    clk
```

- The pipeline register adds a small fixed delay (its own setup/hold/clock-to-Q time) to every stage.
- A pipelined data path's per-stage cycle is not exactly $T_{long} / S$ for $S$ stages — it's that plus the pipeline-register delay.
- The throughput win still dominates for any reasonable $S$.

# The five canonical stages

- A standard pipeline cuts the data path into five stages.

**IF — Instruction Fetch**

- Read the instruction word at the address `EIP` names.
- PC update logic computes the next-sequential `EIP` and writes it back.
- The instruction word goes into the IF/ID pipeline register.

**ID — Instruction Decode**

- The decoder splits the instruction word into opcode and operand fields.
- The opcode goes to the control unit, which produces every mux select and ALU op-select for the rest of the stages.
- Register-number fields drive the [[logic gates#Sequential storage|register file]]'s read ports; the two operand values pop out the same cycle.
- The ID/EX pipeline register stores: the operand values, the immediate (sign-extended), the destination register number, and every control signal the later stages will need.

**EX — Execute**

- The [[alu|ALU]] runs. Inputs come from the ID/EX pipeline register.
- Output is the ALU result and the flag bundle.
- For a branch, this stage also computes the branch target (`EIP` + sign-extended displacement) and the taken/not-taken decision.
- The EX/MEM pipeline register stores the ALU result, the value to store (for `mov [addr], reg`), the destination register number, and the branch decision.

**MEM — Memory access**

- Only used by load and store instructions.
- For `mov reg, [addr]`, the ALU result from EX is the address; this stage drives it onto the address bus and reads the data back.
- For `mov [addr], reg`, this stage drives both address and the value to store.
- ALU-only instructions pass through this stage doing nothing — their data sits in the MEM/WB pipeline register unchanged.
- The MEM/WB pipeline register stores: the value to write back (either ALU result or memory load data) and the destination register number.

**WB — Write back**

- Drives the register file's write port.
- The value from MEM/WB lands in the destination register on this cycle's clock edge.
- After this stage, the instruction is fully retired.

```
     IF        ID        EX        MEM        WB
   +----+    +----+    +----+    +----+    +----+
   |    |--> |    |--> |    |--> |    |--> |    |
   +----+ R  +----+ R  +----+ R  +----+ R  +----+
          1         2         3         4
                                 (R_i = pipeline registers)
```

- A new instruction enters IF every cycle. Five instructions are in flight at any moment, each in a different stage.

# Throughput and latency

**Latency**

- Time from an instruction entering IF to leaving WB.
- Single-cycle: 1 cycle. Pipelined: 5 cycles (plus the pipeline-register delays).
- A single instruction takes *longer* to finish under pipelining.

**Throughput**

- Instructions completed per unit time.
- Single-cycle: 1 per (long) cycle. Pipelined: 1 per (short) cycle, in steady state.
- The short cycle is roughly 5x faster than the long one, so throughput is roughly 5x higher.

**Trade**

- Unambiguously worth it. Most workloads care about throughput — total work per second — not the latency of any single instruction.
- The exceptions (latency-critical branches in the hot path) get their own mitigations (branch prediction, below).

# Hazards

- The clean five-stage picture assumes every instruction can advance every cycle.
- ==Hazards== are the cases where it can't — the next instruction's stage cannot run because something it depends on isn't ready.

**Structural**

- Two instructions in different stages want the same hardware in the same cycle.
- Example: a single-port memory unit, where IF wants to fetch the next instruction the same cycle MEM wants to do a load.
- Mechanism A (duplicate). Split L1 cache into separate I-cache and D-cache, so IF and MEM can't collide.
- Mechanism B (stall). Hold the contending stage's pipeline register so its data does not advance, leaving a ==bubble== (a no-op) in the next stage.

**Data**

- Instruction $i+1$ reads a register that instruction $i$ writes, and $i$ hasn't written yet.
- The register file's read in ID happens *before* $i$'s WB stage. The naive read returns the stale value.

```
   cycle:    1    2    3    4    5    6
   instr i:  IF   ID   EX   MEM  WB
   instr i+1:     IF   ID   EX   MEM  WB     <-- ID happens in cycle 3
                            ^                    but i's WB isn't until 5
                            |
                       reads register here, before i has written it
```

- Mechanism A (stall). Hold $i+1$ in ID for two cycles until $i$'s WB completes. Insert two bubbles into EX. Slow.
- Mechanism B (forwarding). $i$'s ALU result exists at the end of cycle 3 — it just hasn't reached the register file yet.
- Wire the EX-stage output (and the MEM-stage output, for loads) back to the EX-stage input through a small mux.
- The control logic in EX detects when its source register matches a destination register of an in-flight earlier instruction and selects the forwarded value over the (stale) register-file read. Zero bubbles for ALU-to-ALU dependencies.
- Forwarding doesn't fix every data hazard. A load followed immediately by a use of the loaded value still stalls one cycle, because the loaded value isn't available until end of MEM (cycle 4 in the example above), and EX of the dependent instruction runs in the same cycle.
- Compilers reorder code to fill that load-use slot with an unrelated instruction.

**Control**

- A branch's outcome is decided in EX (or later — Intel's Pentium 4 had branch resolution at stage 17).
- IF must decide which instruction to fetch *next cycle*, well before the branch resolves. So the pipeline must guess.
- Mechanism A (stall until resolved). Freeze IF until the branch resolves. For a 5-stage pipeline with branch resolution in EX, stall 2 cycles per branch. Branches are common (often 1 in every 5 instructions); a 2-cycle stall on every branch is catastrophic.
- Mechanism B (predict not-taken). Always fetch the sequential next instruction. If the branch turns out to be taken, ==flush== the wrongly-fetched instructions (squash them in the pipeline registers, replacing them with bubbles) and re-fetch from the branch target. Good when most branches aren't taken; bad for loops where the back-edge is taken almost every iteration.
- Mechanism C (branch prediction). Maintain a small table that *guesses* per-branch whether it will be taken. Detail in `# Branch prediction` below.

# Forwarding

- The hardware extension that makes most data hazards cost zero cycles.
- Two muxes in front of the ALU let EX use a value from a not-yet-retired earlier instruction.

```
                          forward from EX/MEM register
                                   |
                                   v
                              +----+----+
   ID/EX register reg A ----> |   mux   | -----> ALU input A
                              +----+----+
                                   ^
                                   |
                          forward from MEM/WB register


                          forward from EX/MEM register
                                   |
                                   v
                              +----+----+
   ID/EX register reg B ----> |   mux   | -----> ALU input B
                              +----+----+
                                   ^
                                   |
                          forward from MEM/WB register
```

- The mux selects come from a small combinational ==forwarding unit== that compares the destination register numbers held in EX/MEM and MEM/WB against the source register numbers in ID/EX.
- On a match, route the forwarded value; otherwise route the register-file read.
- Just an application of [[logic gates#Multiplexer]] — three-way mux, three select cases, gates the size of a small comparator.

# Branch prediction

**Saturating counter**

- A small table indexed by the low bits of the branch's `EIP`.
- Each entry holds a 2-bit ==saturating counter==. The counter encodes the recent history of this branch:
- $00$: strongly not-taken
- $01$: weakly not-taken
- $10$: weakly taken
- $11$: strongly taken
- Predict taken if the counter's high bit is 1, not taken otherwise.
- On every branch resolution, increment the counter if the branch was taken, decrement if not taken; saturate at $00$ and $11$.

```
   counter
   state    on taken   on not-taken
   00 -->     01           00       (saturate at 00)
   01 -->     10           00
   10 -->     11           01
   11 -->     11           10       (saturate at 11)
```

- Saturating, not wrapping. A branch that has been taken many times in a row sits at $11$; a single not-taken outcome moves it to $10$ but still predicts taken.
- This is what makes the predictor robust to one-off mispredictions in tight loops.

**Misprediction handling**

- Flush the wrongly-speculated instructions (clear their pipeline registers to bubbles).
- Update the counter, and re-fetch from the correct target.

**More sophisticated predictors**

- Two-level, GShare, TAGE use the global history of recent branches as additional index bits.
- Underlying mechanism — a table of small saturating counters indexed by some function of branch history — is the same.

# Beyond five stages

- The five-stage pipeline is the floor, not the ceiling. Two extensions matter.

**Superscalar**

- Issue multiple instructions per cycle by widening every stage.
- A 4-wide pipeline has four ALUs in EX, four read ports on the register file, four IF lanes.
- Throughput rises proportionally for instruction streams with enough independence to fill the lanes.

**Out-of-order execution**

- The in-order pipeline stalls when an instruction's operand isn't ready, even if a later, independent instruction could have run.
- Out-of-order issue maintains a window of decoded instructions and dispatches whichever ones have ready operands, in any order.
- ==Reorders== the results before retirement so the architectural state still appears to update sequentially.

- Both extensions complicate the pipeline-register layout and the hazard-detection logic, but they are extensions of this same single-instruction-stream pipelined model — not new computational ideas. Their depth deserves separate notes.
