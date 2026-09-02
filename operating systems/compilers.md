- The ==compiler== is the program that translates human-readable source into a binary executable a CPU can fetch and execute directly.
- Prerequisite: [[hardware architecture]] — the CPU executes binary opcodes; the compiler targets a specific instruction set architecture.
- The compiler commits fixed values to the executable at ==compile time== — before the program runs; anything depending on execution is ==runtime==.
- The executable file is divided into ==sections==: ==text== (compiled instructions), ==data== (initialized globals), ==BSS== (zero-initialized globals).

# Compile Time vs Runtime

- The compiler translates source without running it. Not all values are knowable at translation; some depend on input the compiler never has.
- Fixed values — sizes of globals, binary opcodes per function, initial values of constants — are committed directly to the executable file on disk.
- Runtime-dependent values — user input, file contents, network data — are emitted as instructions that compute them during execution.
- `int x = 5;` ships the value `5` in the executable. `int x = atoi(argv[1]);` ships only the call instruction.

# The Compilation Pipeline

- A C source file passes through four stages on its way to an executable. Each stage is a separate program; gcc invokes them in sequence.

**Preprocessor**

- Expands `#include` directives by pasting in header file contents, expands `#define` macros, and strips comments.
- Output: a single source file with all imports inlined.

**Compiler proper**

- Parses the preprocessed source, type-checks it, and emits assembly targeting the CPU's instruction set architecture.
- Output: a `.s` assembly file.

**Assembler**

- Translates assembly mnemonics into binary opcodes. Each instruction maps to its fixed bit pattern; symbol names (function names, global variable references) become placeholder addresses to be resolved later.
- Output: a `.o` object file containing binary machine code with unresolved symbols.

**Linker**

- Combines one or more object files with library code. Resolves every symbol placeholder to a real address, lays out the sections, and writes the final executable file on disk.

# Executable Sections

- The linker structures the executable so the hardware can enforce different permissions per region.
- Instructions must be readable and executable but not writable — a program that could modify its own opcodes could redirect control flow arbitrarily. Mutable globals must be read-write. Constants must be read-only. Separate sections enforce these distinctions.
- The three core sections are text, data, and BSS.

```
+-----------+   executable file on disk
|   data    |
+-----------+
|    BSS    |   (size record only — no stored bytes)
+-----------+
|   text    |
+-----------+
```

# Text

- Holds the binary opcodes of every compiled function — the machine instructions the CPU fetches and executes.
- Read-only and executable. Non-writable: if the program could rewrite its own text it could replace opcodes with arbitrary ones and redirect control flow.
- The CPU fetches each instruction sequentially via the program counter, advancing it after each instruction and branching when control-flow instructions say so.
- Fixed in size for the program's entire lifetime.

# Data

- Holds the initial values of every global or static variable initialized at compile time.
- `int counter = 5;` reserves a 4-byte slot and ships the value `5` inside the executable. Those bytes appear verbatim in the data section.
- Read and write permitted; not executable. Fixed in size — the linker counted every initialized global.

```c
int counter = 5;       // data
static char tag = 'x'; // data
```

**RODATA**

- A read-only sub-region of data. Holds compile-time constants: string literals, `const` globals.
- Non-writable; a write attempt faults. The split from writable data lets the hardware enforce immutability for values the programmer declared constant.

# BSS

- Zero-initialized globals could go in data, but storing their zero bytes verbatim would inflate the executable by the full size of every such global.
- Instead the executable records only the size of the zero-initialized region. BSS contains no data bytes in the file; it is a size declaration.
- Before the program's entry point runs, a zero-filled region of that size is established in memory. Uninitialized globals and statics read as `0` for this reason. Local variables carry no such guarantee — they are stack-allocated and uninitialized by default.

```c
int buffer[1024]; // BSS — size stored only, no zero bytes in executable
static int count; // BSS
int total = 0;    // BSS — zero initial value goes here, not data
```


[[c]]

[[x86 assembly]]