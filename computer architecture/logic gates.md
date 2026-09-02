- A ==logic gate== is a small physical circuit that takes one or more 1-bit inputs and produces a 1-bit output computed by a fixed Boolean function.
- The layer between transistors and structured hardware. Above: every register, ALU, and ultimately the CPU is a graph of gates. Below: each gate is a handful of ==transistors==.

# Why gates exist

- A computer must compute Boolean functions of arbitrary complexity. Two reasons gates are the right primitive.

**Universality**

- Any Boolean function of $N$ inputs can be expressed as a circuit of NAND gates alone.
- A single gate type suffices to build any computation.
- Real chips mix gate types because a 2-input AND is cheaper to lay out than two cascaded NANDs. The universality argument is what makes the layer above gates possible.

**Compactness**

- A gate is two to six ==transistors== in CMOS.
- A modern chip holds tens of billions of transistors, so a chip can hold many billions of gates.
- Composition at this scale is what produces a CPU.

# Boolean signals

- Wires carry one of two voltage levels. The high level is interpreted as logical 1, the low level as logical 0.
- The mapping is a convention; the circuit cares only that the two levels are distinguishable.
- A gate's output is fully determined by its inputs at the moment of observation.
- Once inputs settle, the output settles after a small ==propagation delay== — the time the transistors take to switch.
- Every higher construction inherits this delay; long chains of gates accumulate it.

# The seven gates

- Each gate is fully described by its truth table. Inputs are 1 bit each. Output is 1 bit. Two inputs unless noted.

**NOT** (inverter)

- 1 input. Output is the opposite of the input.

```
+---+---+
| A | Y |
+---+---+
| 0 | 1 |
| 1 | 0 |
+---+---+
```

**AND**

- Output 1 iff both inputs are 1.

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |
+---+---+---+
```

**OR**

- Output 1 iff at least one input is 1.

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |
+---+---+---+
```

**NAND**

- AND followed by NOT. Output 0 iff both inputs are 1.

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |
+---+---+---+
```

**NOR**

- OR followed by NOT. Output 1 iff both inputs are 0.

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 0 |
+---+---+---+
```

**XOR**

- Output 1 iff inputs differ. The "1-bit difference detector."

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |
+---+---+---+
```

**XNOR**

- XOR followed by NOT. Output 1 iff inputs are equal.
- The "1-bit equality detector."

```
+---+---+---+
| A | B | Y |
+---+---+---+
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |
+---+---+---+
```

# Universality of NAND

- Any of the other six gates can be built from NANDs alone. Three constructions show why.
- NOT: tie both inputs of a NAND together. $\text{NAND}(A, A) = \text{NOT}(A)$.
- AND: NAND the inputs, then NOT the result. $\text{AND}(A, B) = \text{NOT}(\text{NAND}(A, B))$.
- OR: NOT each input, then NAND the negations. $\text{OR}(A, B) = \text{NAND}(\text{NOT}(A), \text{NOT}(B))$.
- Once NOT, AND, OR exist, every Boolean function is expressible.
- A truth table of $N$ inputs has $2^N$ rows; the function equals the OR of the AND-of-literals for every row whose output is 1 (==sum of products== form).
- NAND alone is enough for any digital circuit.

# Combinational vs sequential

- All circuits split into two families. Every higher construction in this note is one or the other, and they are wired differently.

**Combinational**

- Output is a pure function of the current inputs. No memory.
- Built from gates only, no feedback loops.
- Once inputs settle, output settles after the propagation delay.

**Sequential**

- Output depends on current inputs *and* stored state.
- Built from gates *with* feedback loops, plus a clock signal that gates when the state can change.
- Examples: latches, flip-flops, registers, register files.

# Multi-bit values

- A single gate operates on 1-bit signals. To operate on an $N$-bit value, replicate the gate $N$ times in parallel and bus the inputs and outputs as $N$-wire bundles.
- A 16-bit AND is sixteen 1-bit ANDs side by side: bit $i$ of the output is $A_i \text{ AND } B_i$. Same idea for any bitwise op.
- Word-level operations that mix bits across positions — addition, comparison — need richer constructions covered below.

# Multiplexer

- Combinational. Selects one of several inputs and routes it to the output. The select lines decide which input wins.
- The simplest case is a 2-to-1 mux: one select bit, two data inputs.
- $\text{mux}(s, A, B) = (\overline{s} \text{ AND } A) \text{ OR } (s \text{ AND } B)$.
- $s = 0$ → output is $A$. $s = 1$ → output is $B$.

```
       A ----+
             |
             v
            +---+
       s -->|MUX|----> Y
             +---+
             ^
             |
       B ----+
```

- An $N$-to-1 mux needs $\log_2(N)$ select bits.
- A 4-to-1 mux: select bits $s_1 s_0$ pick one of inputs $D_0, D_1, D_2, D_3$.

**Why it matters**

- Anywhere two or more wires want to feed the same destination, you cannot tie them together — voltages would conflict.
- A mux is the discipline: choose one source per cycle.
- Every junction in a CPU's data path where the current instruction decides which source to use (register vs. immediate, ALU result vs. memory load, sequential PC vs. branch target) is a mux.

# Decoder

- Combinational. Inverse of a mux.
- Takes an $N$-bit binary input and produces $2^N$ output lines, exactly one of which goes high.
- The high line corresponds to the binary value of the input.

```
3-to-8 decoder

input
A2 A1 A0    Y0 Y1 Y2 Y3 Y4 Y5 Y6 Y7
 0  0  0     1  0  0  0  0  0  0  0
 0  0  1     0  1  0  0  0  0  0  0
 0  1  0     0  0  1  0  0  0  0  0
 ...
 1  1  1     0  0  0  0  0  0  0  1
```

**Why it matters**

- The register file uses a decoder to translate a register number into a one-hot signal that activates exactly the chosen register's write-enable line.
- Same role inside RAM addressing — an address selects exactly one row.

# Adders

- Three constructions in increasing scale. Half adder is the 1-bit base case; full adder accepts an incoming carry so it can chain; ripple-carry chains $N$ full adders into an $N$-bit adder.

**Half adder**

- Combinational. Adds two 1-bit numbers.
- Output is a 2-bit number: a sum bit and a carry bit.
- $\text{sum} = A \text{ XOR } B$. The XOR is exactly the low bit of $A + B$ when both are 1 bit.
- $\text{carry} = A \text{ AND } B$. Carry happens only when both inputs are 1.

```
+---+---+-----+-------+
| A | B | sum | carry |
+---+---+-----+-------+
| 0 | 0 |  0  |   0   |
| 0 | 1 |  1  |   0   |
| 1 | 0 |  1  |   0   |
| 1 | 1 |  0  |   1   |
+---+---+-----+-------+
```

- A half adder cannot chain. It accepts only $A$ and $B$, with no input for an incoming carry from the bit below.
- It can serve as the lowest bit of a multi-bit adder, but no other position.

**Full adder**

- Adds three 1-bit numbers: $A$, $B$, and an incoming carry $C_{in}$.
- $\text{sum} = A \text{ XOR } B \text{ XOR } C_{in}$. The sum bit is 1 iff an odd number of the three inputs is 1.
- $\text{carry}_{out} = (A \text{ AND } B) \text{ OR } (C_{in} \text{ AND } (A \text{ XOR } B))$. The carry-out is 1 iff at least two of the three inputs are 1.

```
                    A     B
                    |     |
                    v     v
                   +---+
                   |XOR|
                   +---+
                     |
            Cin --+--+---+
                  |      |
                  v      v
                 +---+  +---+
                 |XOR|  |AND|--+
                 +---+  +---+  |
                   |           |    A,B both 1
                   v           v
                  sum    +-----+----+
                         |          |
                         v          |
                        +---+       |
                        |OR |<------+
                        +---+
                          |
                          v
                       carry_out
```

- A full adder chains: its $C_{out}$ feeds the $C_{in}$ of the next bit up.
- One cell serves every bit of an $N$-bit adder.

**Ripple-carry adder**

- $N$ full adders chained: $C_{out}$ of bit $i$ wires into $C_{in}$ of bit $i + 1$.
- The lowest bit's $C_{in}$ is hardwired to 0 (or to 1 to implement two's-complement subtraction by adding $\overline{B} + 1$).

```
          A0 B0           A1 B1           A2 B2           A3 B3
           | |             | |             | |             | |
           v v             v v             v v             v v
   0 --> +-----+ C1 ---> +-----+ C2 ---> +-----+ C3 ---> +-----+ ----> C4
         | FA0 |         | FA1 |         | FA2 |         | FA3 |
         +-----+         +-----+         +-----+         +-----+
            |               |               |               |
            v               v               v               v
            S0              S1              S2              S3
```

- This is the construction the [[alu|ALU]] uses for its $N$-bit add. A 32-bit adder for [[x86 assembly|x86]] is thirty-two full adders chained.
- ==Cost==. The carry has to propagate through all $N$ stages before the high bit's sum is valid. Worst-case delay grows linearly with $N$.
- Real CPUs use carry-lookahead or carry-select adders to break the dependency chain. The function computed is the same.

# Sequential storage

- Four constructions at increasing scale, each built from the last. Latch holds one bit; D flip-flop is a clock-controlled latch; register is $N$ flip-flops; register file is $K$ registers.

**Latch**

- Sequential. The smallest circuit that remembers a single bit.
- Built from a feedback loop. Two cross-coupled NOR gates form an ==SR latch==.
- $S = 1$ sets the stored bit to 1. $R = 1$ resets it to 0. When both are 0, the latch holds.

```
        S ----+    +-----.
              |    |     |
              v    |     v
             +----------+
             |   NOR    |---+--- Q
             +----------+   |
                            |
                       +----+
                       |
             +----------+
             |   NOR    |---+--- Q'  (= NOT Q)
             +----------+   |
              ^             |
              |             |
        R ----+    +--------+
                   |
                   '
```

- $Q$ is the stored value. $Q'$ is its complement; the cross-coupling holds them consistent.
- The feedback is the memory: each NOR's output drives the other NOR's input.
- A stable pair of values $(Q, Q') = (1, 0)$ or $(0, 1)$ persists when $S = R = 0$.

**D flip-flop**

- The latch above accepts $S$ and $R$ continuously, so input glitches can corrupt the stored bit.
- Real registers need to update at controlled, predictable moments.
- A ==D flip-flop== takes one data input $D$ and one clock input.
- On the rising edge of the clock, the flip-flop captures $D$ and holds it on $Q$ until the next rising edge.
- Between edges, $D$ can change freely; the stored value does not.

```
   D --->+-----------+
         |           |
   clk ->| D flip-   |--- Q
         |   flop    |
         +-----------+
```

- The clock edge synchronizes a synchronous digital system.
- Every flip-flop sampled on the same edge sees a consistent snapshot of its inputs.
- The interval between edges is one ==clock cycle==. Combinational logic must finish settling within that interval.

**Register**

- $N$ D flip-flops in parallel, sharing a clock and a write-enable line. Stores an $N$-bit word.
- Write enable gates the clock: the flip-flops capture $D$ only when the clock edges *and* write-enable is 1.
- A register holds its value for as many cycles as needed and updates only on cycles the control unit asserts write-enable.

```
   D[15:0] ---+--+--+   ...   +--+
              |  |  |         |
              v  v  v         v
            +-----------------------+
            |   16 D flip-flops     |
   clk ---> |                       |---> Q[15:0]
   we  ---> |                       |
            +-----------------------+
```

- Every named architectural register — general-purpose registers, the program counter, the stack pointer — is a register in this sense.

**Register file**

- An array of $K$ registers with two read ports and one write port.
- Reads supply two operands simultaneously; writes accept one result on the next clock edge.
- Reads are combinational: a read-port address (a register number) is fed through a mux that selects the addressed register's $Q$ and routes it to the read-port data output.
- Both reads complete within the same cycle, in parallel.
- Writes are sequential: the write-port address is decoded into a one-hot signal, ANDed with the global write-enable to produce a per-register write-enable.
- On the rising clock edge, only the addressed register captures the write-port data; the rest hold.

```
                          +---------------------+
                          |                     |
   read_addr_a (3) -----> |                     |---- read_data_a (32)
                          |                     |
   read_addr_b (3) -----> |    register file    |---- read_data_b (32)
                          |    8 x 32 bits      |
   write_addr  (3) -----> |                     |
   write_data (32) -----> |                     |
   write_en    (1) -----> |                     |
   clk         (1) -----> |                     |
                          +---------------------+
```

- The architecturally-visible register file is 8 entries wide and 32 bits deep.
- Two reads per cycle let it supply both operands of an `add` simultaneously; one write per cycle lets it accept the result on the next clock edge.
- Real x86 hardware stores far more registers than the architecture exposes — register renaming maps the 8 architectural names onto a much wider physical file to dissolve false dependencies.
