- Assembly is an ultra low language language that talks directly with the CPU.
- All programs [[compilers|compile]] to machine code before execution, and assembly is simply a format of machine code for humans to read. Thus, all programs is technically some form of assembly.
- ==x86== is Intel and AMD's CPU architecture; this note covers x86 assembly.

# x86 CPU

- x86 is a CPU architecture used by Intel and AMD.
	- Assembly is architecture specific. x86 assembly will not run on ARM architecture. x86 assembly will be frequently shortened to just "x86".
- Assembly modifies values in the [[cpu#Programmer-visible state|CPU registers]] directly.
	- `mov eax, 5` -> The binary value 5 is stored in register eax.
	- `mov ebx, [eax]` -> The value at address eax is stored in ebx
- Languages don't get more low level than this, we are literally writing to the CPU.

# x86 CPU Operating Modes

**Protected Mode**

- Native mode, includes all features. Used by Windows and Linux.
- 4 GB address space, 32-bit addresses.

**Virtual 8086 Mode**

- Runs within protected mode. Allows for multiple 16-bit DOS programs to run simultaneously, each as its own 8086 virtual machine.
- Enables legacy compatibility.
- 1 MB address space, 20-bit addresses.

**Real Address Mode**

- 16-bit mode. Direct hardware access, no memory protection, 1 MB memory limit.
- Used when CPU boots.

**System Management Mode**

- Special mode for firmware only.

# [[c]] compilation stages:

1. **Preprocessing** - Handles directives like `#include`, `#define`, etc. Produces `.i` file.
2. **Compilation** - Translates C code into assembly language. Produces `.s` file.
3. **Assembly** - Converts assembly into machine code (object code). Produces `.o` file.
4. **Linking** - Combines object files and libraries into executable, this runs on the CPU.

# Registers

**General Registers**

- `EAX`, `EBX`, `ECX`, `EDX`, `ESI`, `EDI`

**Special Registers**

- `EBP` - Base Pointer
	- A [[memory#Pointers|pointer]] that points to the bottom of the [[x86 assembly#Memory Stack|stack]].
- `ESP` - Stack Pointer
	- A [[memory#Pointers|pointer]] that points to the top of the [[x86 assembly#Memory Stack|stack]].

**Flags Register**

- ==EFLAGS==

**Segment Registers**

- `CS`, `SS`, `DS`, `ES`, `FS`, `GS`

**Program Counter**

- `EIP`

**Control Register**

- `CR0`, `CR1`, ... , `CR4`

# Register Bit Layout

- We will study 32 bit assembly, thus x86 registers are [[memory#Memory Addresses|32 bits wide]], but can be accessed in smaller pieces for backward compatibility with 16-bit and 8-bit code.

```
                  +-------+-------+
                  |  AH   |  AL   |  # 8 bits each
                  +-------+-------+
                  |      AX       |  # 16 bit
  +-------+-------+-------+-------+
  |              EAX              |  # 32 bit
  +-------------------------------+
```

- The same layout applies to
	- `EBX`/`BX`/`BH`/`BL`
	- `ECX`/`CX`/`CH`/`CL`
	- `EDX`/`DX`/`DH`/`DL`

# EFLAGS

- Each bit is a ==flag== set by arithmetic/logic instructions.
- Conditional branches (`jCC`) and conditional moves (`cmovCC`) read these flags to decide whether to execute.

```
+-----+------+------------------------------------------+
| Bit | Flag | Meaning                                  |
+-----+------+------------------------------------------+
|  0  |  CF  | Carry Flag -- unsigned overflow           |
|  6  |  ZF  | Zero Flag -- result was zero              |
|  7  |  SF  | Sign Flag -- result was negative (MSB=1)  |
| 11  |  OF  | Overflow Flag -- signed overflow          |
+-----+------+------------------------------------------+
```

- `cmp x, y` sets flags based on `x - y`:
	- `ZF = 1` if `x == y`
	- `SF = 1` if `x - y` is negative
	- `CF = 1` if unsigned borrow occurred
	- `OF = 1` if signed overflow occurred

# [[memory#Stacks|Memory Stack]]

- The x86 stack grows downward. The bottom of the stack has the highest memory address, and the top of the stack has the lowest.
	- Pushing decreases the memory address.
	- Popping increases the memory address.

```
   High addresses
+------------------+
|       ...        |
+------------------+
| older data       |
+------------------+
| newest data      |  <- esp (top of stack)
+------------------+
    Low addresses
          |
          v  (stack grows this way)
```

**Operations**

- `push SRC`
	- Decrement `ESP` by 4. 
	- In 32 bit, every line is 4 bytes. Thus `push` decrements `ESP` by exactly 4 lines.
	- Store `SRC` at the address `ESP` now points to.
- `pop DST`
	- Load the value at `ESP` into `DST`.
	- Increment `ESP` by 4.

```nasm
push eax              ; esp -= 4, then [esp] = eax
pop ebx               ; ebx = [esp], then esp += 4
```

# Data Movement

- `mov` moves data between [[cpu#Programmer-visible state|registers]] and memory.
	- Intel syntax follows `mov DST, SRC`.
	- `mov edx, eax` -> `edx = eax`

```nasm
mov ebx, 0x123          ; ebx = 0x123
mov ebx, [0x123]        ; ebx = *(int *)0x123
mov edx, [ebx]          ; edx = *(int *)ebx
mov edx, [ebx + 4]      ; edx = *(int *)(ebx + 4)
```

- `;` declares in-line comment.

# Arithmetic

- x86 supports arithmetic operations between 2 [[x86 assembly#Registers|registers]].

**+ and -**

- `add DST, SRC` -> `DST = DST + SRC`
- `sub DST, SRC` -> `DST = DST - SRC`
- `inc DST` -> `DST = DST + 1`
- `dec DST` -> `DST = DST + 1`

**Multiply**

- `imul DST, SRC` -> Signed multiply. `DST = DST * SRC`
- `mul SRC` -> Unsigned multiply.

**Division**

- `idiv SRC` -> Signed division.
- `div SRC` -> Unsigned division.
- The numerator, or dividend, and the storage of the result depends on the bit size of `SRC`. x86 only supports 8, 16, and 32-bit division.

| Operand Size | Numerator | Quotient | Remainder |
| ------------ | --------- | -------- | --------- |
| 8-bit        | AX        | AL       | AH        |
| 16-bit       | DX:AX     | AX       | DX        |
| 32-bit       | EDX:EAX   | EAX      | EDX       |

- `neg DST`
	- Two's complement negation. `DST = -DST`

```nasm
add eax, 5           ; eax = eax + 5
sub ecx, ebx         ; ecx = ecx - ebx
imul edx, 3          ; edx = edx * 3
inc eax              ; eax++

; divide eax by 4
cdq                   ; sign-extend eax into edx:eax
mov ecx, 4
idiv ecx              ; eax = quotient, edx = remainder
```

# Bitwise Operations

- `and DST, SRC`
	- `DST = DST & SRC`
- `or DST, SRC`
	- `DST = DST | SRC`
- `xor DST, SRC`
	- `DST = DST ^ SRC`
- `not DST`
	- `DST = ~DST` (flip all bits)
- `shl DST, COUNT`
	- Shift left. `DST = DST << COUNT`
- `shr DST, COUNT`
	- Logical shift right. `DST = DST >> COUNT` (zero-fill)
- `sar DST, COUNT`
	- Arithmetic shift right. `DST = DST >> COUNT` (sign-fill)

```nasm
and eax, 0xFF        ; mask lower byte
shl ebx, 2           ; ebx = ebx * 4
xor eax, eax         ; eax = 0 (fast zero idiom)
```

# Logic Operators

- `test DST, SRC` -- computes `DST & SRC`, sets flags, **discards the result**.
	- Used to check if specific bits are set, or if a value is zero/negative.
- `cmp DST, SRC` -- computes `DST - SRC`, sets flags, **discards the result**.
	- Used before conditional jumps to compare two values.
- Both instructions exist only to set [[x86 assembly#EFLAGS|EFLAGS]] for a subsequent conditional jump or conditional move.

```nasm
test eax, eax         ; sets ZF if eax == 0, SF if eax < 0
je label              ; jump if eax == 0

cmp ebx, 10          ; sets flags based on ebx - 10
jl label              ; jump if ebx < 10
```

# Jumps

- `jCC label` -- jump to label if condition `CC` is true (reads [[x86 assembly#EFLAGS|EFLAGS]]).
- There are a LOT, the important ones are below.

```
+------+--------------------+-------------------+
| Inst | Condition          | Flags Checked     |
+------+--------------------+-------------------+
| je   | equal              | ZF = 1            |
| jne  | not equal          | ZF = 0            |
| jl   | less (signed)      | SF != OF          |
| jle  | less/equal (signed)| ZF=1 or SF != OF  |
| jg   | greater (signed)   | ZF=0 and SF = OF  |
| jge  | greater/eq (signed)| SF = OF           |
| jb   | below (unsigned)   | CF = 1            |
| ja   | above (unsigned)   | CF=0 and ZF=0     |
| js   | sign (negative)    | SF = 1            |
| jz   | zero               | ZF = 1 (same: je) |
+------+--------------------+-------------------+
```

- `jmp label` -- unconditional jump (does not check flags).

# Conditional Move

- `cmovCC DST, SRC` -- moves `SRC` into `DST` only if condition `CC` is true.

```nasm
cmp eax, ebx
cmovl eax, ebx        ; eax = min(eax, ebx)
```

# Strings

- In x86, each ASCII character is 1 byte. Technically 7 bits but stored in a byte.
- String instructions operate on implicit operands. No explicit operands in the instruction.
	- Source: `DS:ESI`
	- Destination: `ES:EDI`
- After each operation, `ESI` and/or `EDI` are incremented (or decremented if the direction flag `DF` is set).

**Operations**

- `lodsb`
	- Load byte at `[ESI]` into `AL`, increment `ESI`.
- `stosb`
	- Store `AL` into `[EDI]`, increment `EDI`.
- `movsb`
	- Copy byte from `[ESI]` to `[EDI]`, increment both.
- `scasb`
	- Compare `AL` with byte at `[EDI]`, set flags, increment `EDI`.
- `rep` prefix
	- Repeat the instruction `ECX` times, decrementing `ECX` each iteration.
- `repe`/`repne`
	- Repeat while equal/not equal (checks `ZF` after each iteration).

```nasm
; copy 100 bytes from src to dst
mov ecx, 100
rep movsb             ; memcpy(edi, esi, ecx)
```

# System

- `int 0x80` -- executes a software interrupt. Traps into the kernel to perform a system call.
- `iret` -- return from an interrupt handler back to user mode.
- `sysenter` / `sysexit` -- fast system call entry/exit. Avoids full interrupt overhead.

# Labels

**Data Label**

- Identifies a location in the data section. Must be unique.
- `myArray: db 10`

**Code Label**

- Identifies a location in the code section. Ends with a colon.
- Target of `jmp`, `jCC`, `call`, and `loop` instructions.

```nasm
section .data
myVar:   dd 42

section .text
_start:
    mov eax, [myVar]
    cmp eax, 0
    je done
    dec eax
done:
```
