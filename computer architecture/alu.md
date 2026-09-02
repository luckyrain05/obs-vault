- The ==ALU== (Arithmetic Logic Unit) is the combinational block on the [[cpu]] that performs every arithmetic, bitwise, and comparison operation an ISA exposes.
- One unit, many operations, selected by a few control bits each cycle.
- Built strictly out of primitives from [[logic gates]]: gates, multiplexers, ripple-carry adders, sign-fill shifters.

# ALU structure

- A program needs maybe a dozen arithmetic and bitwise operations: add, subtract, AND, OR, XOR, NOT, shift left, shift right, compare.

**The naive design**

- Build a dedicated circuit for each operation.
- Wastes silicon. At any moment the CPU executes one instruction, so only one of those circuits is active — the rest sit idle.
- Every cycle, area-efficient design demands a way to share.

**The sharing discipline**

- Build one wide combinational block whose sub-units (adder, bitwise gates, shifter) compute *all* possible answers in parallel.
- Use a final [[logic gates#Multiplexer|mux]] to expose only the one the current instruction wants. Unused sub-units' outputs are ignored.

**Combinational**

- The ALU has no memory of its own — outputs are a pure function of the current inputs.
- State lives in the [[logic gates#Sequential storage|registers]] feeding it, not inside it.
- This is what makes the ALU compose with sequential logic: registers hold the values, the ALU transforms them, registers hold the new values on the next clock edge.

# Interface

- The ALU is a black box with three input ports and two output ports.

```
                         +-----------+
   A     [N bits] -----> |           |
                         |           |
   B     [N bits] -----> |    ALU    | -----> result   [N bits]
                         |           |
   op    [k bits] -----> |           | -----> flags    [4 bits]
                         +-----------+
```

**Operands**

- $A$ and $B$ are the two $N$-bit operands.
- Both come from the [[logic gates#Sequential storage|register file]] or, in some cycles, from a sign-extended immediate field.

**Op-select**

- $k$ control bits naming which operation to expose on the result port.
- $k = 4$ bits names 16 distinct operations — enough to cover add, sub, AND, OR, XOR, NOT, shifts, and a few comparisons.
- The op-select is produced by a small combinational table mapping the instruction's opcode bits to ALU op-select bits. Where that table lives in the broader CPU is outside the ALU's scope.

**Result**

- The single $N$-bit output.
- Wired to the data-path mux that decides whether the result goes back to the register file (most ops), forms a memory address (for `mov reg, [base+disp]`), or is discarded (for `cmp`, `test`).

**Flags**

- Each flag is a one-bit summary of the operation's outcome that subsequent conditional instructions can branch on without re-deriving the comparison.
- $Z$: zero. The result was zero.
- $N$: negative. The result's sign bit (high bit) is 1.
- $C$: carry. The N-bit add produced a carry-out — unsigned overflow.
- $V$: overflow. Signed overflow occurred (the result's sign disagrees with what two's-complement arithmetic should produce).
- Mechanically each flag is one wire driven by a small combinational circuit on the adder's outputs. Detail in `# Comparator` below.

# Bitwise unit

- For every bitwise op the ALU needs, drop $N$ copies of the corresponding 1-bit gate side by side.
- Bit $i$ of the input feeds bit $i$ of the gate; the $N$ outputs form an $N$-bit result.
- This is the construction in [[logic gates#Multi-bit values]].

**AND**

- $\text{result}_i = A_i \text{ AND } B_i$ for all $i$.
- Used by `and reg, reg`, masks like `and eax, 0xFF`.

**OR**

- $\text{result}_i = A_i \text{ OR } B_i$ for all $i$.

**XOR**

- $\text{result}_i = A_i \text{ XOR } B_i$ for all $i$.
- The fast-zero idiom `xor eax, eax` exploits this — $A_i \text{ XOR } A_i$ = 0 for every bit.

**NOT**

- $\text{result}_i = \text{NOT } A_i$ for all $i$.
- The $B$ operand is unused for this op; the bitwise unit just routes $A$ through a row of inverters.

```
   A_31 A_30  ...  A_1  A_0          B_31 B_30  ...  B_1  B_0
     |    |        |    |              |    |        |    |
     +-+--+--------+----+              +--+--+--------+---+
       |                                  |
       v                                  v
     +-------------------------+      +-------------------------+
     |   32 parallel ANDs      | OR  |   32 parallel ORs       |  ... etc
     +-------------------------+      +-------------------------+
       |    |        |    |              |    |        |    |
     R_31 R_30  ...  R_1  R_0          (similar for OR / XOR)
```

- The four bitwise sub-units run in parallel every cycle.
- The op-select mux at the end picks which row's output reaches the result port; the others are discarded.

# Shifter

- A shift moves every bit of $A$ left or right by $k$ positions, filling the vacated end with zeros (or with the sign bit, for arithmetic right shift).
- $k$ comes from $B$'s low bits.
- Naive: build a shift-by-1 circuit, cascade $k$ of them. Cost: depth proportional to $k$, slow for large shifts.
- Modern ALUs use a ==barrel shifter== — a tree of [[logic gates#Multiplexer|muxes]] whose total depth is $\log_2 N$ regardless of shift amount.

**Barrel shifter (left)**

- Stage $i$ shifts by $2^i$ bits or doesn't shift, controlled by bit $i$ of $k$.
- For a 32-bit shifter, five stages: shift-by-1, shift-by-2, shift-by-4, shift-by-8, shift-by-16.
- Any shift from 0 to 31 is the OR of these powers of two.

```
   stage 0:  k_0 selects   no-op  vs  shift left by 1
   stage 1:  k_1 selects   no-op  vs  shift left by 2
   stage 2:  k_2 selects   no-op  vs  shift left by 4
   stage 3:  k_3 selects   no-op  vs  shift left by 8
   stage 4:  k_4 selects   no-op  vs  shift left by 16
```

- Each stage is $N$ 2-to-1 muxes side by side.
- The "shift" input of each mux is wired to a position $2^i$ bits away in the previous stage's output; the "no-op" input is the same bit.
- The wiring of the muxes encodes the shift; only the mux selects vary.
- Vacated bits at the bottom are wired to constant 0.

**Right shifts**

- Same construction with the wiring mirrored. Two variants:
- ==Logical right shift== (`shr`): vacated bits at the top are wired to constant 0.
- ==Arithmetic right shift== (`sar`): vacated bits at the top are wired to the sign bit $A_{N-1}$ of the input. Preserves sign for two's-complement signed division by powers of 2.

# Adder/subtractor

- The arithmetic core of the ALU.
- Built from the [[logic gates#Adders|ripple-carry adder]]: $N$ full adders chained, $C_{out}$ of bit $i$ feeds $C_{in}$ of bit $i+1$.
- One construction handles both addition and subtraction. The trick is two's complement: $A - B = A + (\overline{B}) + 1$, where $\overline{B}$ is the bitwise NOT of $B$.

**The shared adder**

- Place a row of $N$ XOR gates in front of the $B$ input. One XOR per bit, with the second input tied to a single control wire `sub`.
- `sub` = 0: the XORs pass $B$ through unchanged.
- `sub` = 1: the XORs invert every bit of $B$, producing $\overline{B}$.
- Tie the lowest full adder's $C_{in}$ to the same `sub` wire.
- `sub` = 0: $C_{in}$ = 0, the adder computes $A + B$.
- `sub` = 1: $C_{in}$ = 1, the adder computes $A + \overline{B} + 1 = A - B$.

```
       A_i                              B_i
        |                                |
        |                                v
        |                              +---+
        |                  sub ------->|XOR|
        |                              +---+
        |                                |
        v                                v
   +---------------------------------------------+
   |              full adder bit i               |   <-- chained from bit i-1
   +---------------------------------------------+
                          |
                          v
                        sum_i
```

- For bit 0, $C_{in}$ = `sub`. For bit $i > 0$, $C_{in}$ comes from the carry-out of bit $i-1$ as in the plain ripple-carry adder.

**Cost**

- The carry chain still propagates linearly through $N$ stages, so the adder is the slowest sub-unit and bounds the ALU's clock period.
- Real CPUs use carry-lookahead or carry-select adders that compute carries in $O(\log N)$ depth. The function computed is identical, only the timing differs.

# Comparator

- A comparison instruction (`cmp eax, ebx`) needs to know whether $A < B$, $A = B$, or $A > B$, but does *not* need the difference itself.
- The comparator reuses the adder/subtractor: compute $A - B$, throw away the result, keep the flags.

**Z (zero)**

- $Z = 1$ iff every bit of the sum is 0.
- Wire all $N$ sum bits into a single $N$-input NOR. Equivalently, OR all bits and invert.
- For `cmp`, $Z$ = 1 iff $A = B$. This is what `je` (jump if equal) reads.

**N (negative)**

- $N$ = the high (sign) bit of the sum. One wire, no logic.
- For `cmp`, $N$ = 1 iff $A - B$'s two's-complement representation is negative.

**C (carry)**

- $C$ = the carry-out of the highest full adder. One wire from the existing carry chain.
- For unsigned `add`, $C$ = 1 means the result didn't fit in $N$ bits — unsigned overflow.
- For `sub` (encoded as add with $\overline{B} + 1$), the convention inverts: $C$ = 0 means a borrow occurred, $C$ = 1 means it didn't.
- The hardware just exposes the carry-out wire; the meaning depends on whether the operation was add or subtract.

**V (overflow)**

- $V = C_{N-1} \text{ XOR } C_N$, where $C_{N-1}$ is the carry into the sign bit and $C_N$ is the carry out of it. One XOR gate.
- Why this works. Signed overflow occurs exactly when the sign of the result disagrees with what two's-complement arithmetic should produce.
- That happens iff the carry into the sign bit and the carry out of the sign bit disagree.
- Adding two positives that overflow into a negative produces $C_{N-1} = 1, C_N = 0$; adding two negatives that overflow into a positive produces the opposite. The XOR catches both.

```
                                    +-----------+
   A,B  --->  adder/subtractor ---->|           |---- result_bus
                |    |              |  result   |
                |    +-- sign bit ->|  (used by |
                |                   |   data    |
                |                   |   path)   |
                |                   +-----------+
                |
                +---->  sum bits  --->  NOR    --->  Z
                |                                       
                +---->  sign bit  -----------------> N
                |                                       
                +---->  C_N (high carry-out) -----> C
                |                                       
                +---->  C_{N-1} XOR C_N -----------> V
```

- All four flags are one or two gates each; they are essentially free to compute.
- `cmp` is an `add` instruction with `sub` = 1, the result-port write disabled, and the flag register's write enabled.

# Op-select mux

- Every sub-unit — bitwise AND, bitwise OR, bitwise XOR, NOT, shifter, adder/subtractor — runs every cycle, on the same $A$ and $B$.
- Each produces an $N$-bit candidate result. None of them know which one will actually win.
- The decision lives in the final stage: an $N$-bit-wide [[logic gates#Multiplexer|mux]] whose data inputs are the candidate results and whose select lines are the op-select bits.
- Exactly one candidate routes to the result port; the rest are dropped on the floor.

```
                  bitwise AND result   ---+
                  bitwise OR result    ---+
                  bitwise XOR result   ---+
                  NOT result           ---+
                  shift left result    ---+--->  N-bit mux  --->  result
                  shift right result   ---+        ^
                  adder/subtractor sum ---+        |
                  ...                    |       op-select (k bits)
                                         |
   sub control wire                       --- (also feeds adder/subtractor)
```

- The flags-generation circuit always reads the adder/subtractor's outputs, regardless of which op the mux selects.
- The data path can choose, per-instruction, whether to actually clock the flag register that cycle.

# The whole ALU

```
   A [N]                       B [N]
     |                           |
     +---+---+----------+        +---+---+----------+
     |   |   |          |            |   |          |
     v   v   v          v            v   v          v
   +-----+ +----+ +-----+--+       +----------------+
   | AND | | OR | | XOR/NOT|       |   shifter      |
   +-----+ +----+ +--------+       +----------------+
     |       |       |                     |
     |       |       |     +----------------+
     |       |       |     |
     |       |       |     |     +-------------------+
     |       |       |     |     | adder/subtractor  | <-- sub
     |       |       |     |     +-------------------+
     |       |       |     |          |       |
     |       |       |     |          |       +---> flags (Z N C V)
     v       v       v     v          v
   +---------------------------------------+
   |                MUX                    | <-- op-select [k]
   +---------------------------------------+
                    |
                    v
                  result [N]
```

- Every cycle: $A$ and $B$ fan out to all sub-units, all sub-units compute, the op-select mux exposes one.
- Flags are written from the adder regardless.
- This is the entire ALU.

# Width

- The construction is identical at every word width — only $N$ changes.
- $N = 64$ produces a 64-bit ALU for x86-64: 64 of each, 6-stage shifter, 64-stage carry chain.
- The op-select bits, the flag derivation, and the topology are unchanged.
