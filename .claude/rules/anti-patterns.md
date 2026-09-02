# Anti-patterns

Failure modes seen in real vault notes. Each entry has a name, a definition, the failure mode, a BAD example (often quoted from the vault), and a GOOD form. The named failures should be recognized in new instances, not just memorized as a list.

The root pattern across all of these: presenting **labels of a model** rather than **the model itself**. `computer architecture/cache.md` does the opposite — give the mechanism, and the labels become consequences.

# Reduction of N categories to N−1

- Collapsing distinct categories under an umbrella because they share one property.
- The omitted categories return as bugs in the reader's mental model the first time a downstream note touches them.

BAD:

- Memory layout described as "stack and heap." Text, data, and BSS are silently absent. Later, learning thread layout, the reader sees "shared heap" and pattern-matches a Data-segment global onto heap because heap is the only named shared region.

GOOD:

- The virtual address space is divided into text, data, BSS, heap, and stack. Each is defined: what it stores, who allocates it, who frees it, whether threads share it.

# Labels without mechanism

- Naming a thing instead of explaining how it operates.
- The reader can repeat the name but cannot reconstruct the behavior.

BAD (historical, from a now-removed `os spaces.md`):

- "Runs at ring 3 in x86 — the least privileged CPU mode." Ring 3 is named, but what *makes* it privileged is never defined.

GOOD:

- A ring is a 2-bit privilege field stored in the CS segment register. The CPU checks this field before executing privileged instructions (HLT, IN/OUT, MOV to CR0, etc.) and before accessing pages whose page-table entry has the supervisor bit set. Ring 0 passes every check; ring 3 fails most. Then name the rings.

# Hand-wave disclaimer

- Any "below is basics only," "this is approximately," "trust me, here's the simple version."
- The reader interprets the disclaimer as permission to stop digging — and the model is left incomplete on purpose.

BAD (historical, from an earlier draft of `memory.md`):

- "It is a extremely complicated topic, below is basics only."

GOOD:

- Scope the file explicitly: "this file covers the storage hierarchy and the address layout in physical memory. Paging and the MMU are in `[[virtual memory]]`." Then be complete within that scope. If the topic is too large for one file, split along conceptual seams (see `ethos.md`).

# Associative wikilink

- Linking a concept that is *related* to the current one, but not a *prerequisite* for understanding it.
- The wikilink graph stops being a DAG of dependencies and becomes a thesaurus.

BAD (historical, from an earlier draft of `memory.md`):

- "Stored as `[[stacks]]`" referring to memory addresses. Stacks-the-data-structure are not how addresses are stored. The link is associative.

GOOD:

- Wikilink only when the target concept is *required* to understand the current note. If the reader does not need to follow the link to keep reading, the link does not belong.

# Conflation

- Fusing formally distinct concepts into one fuzzy term.
- The reader cannot later distinguish the components when a downstream note depends on the distinction.

BAD (historical, from an earlier draft of `memory.md`):

- "We often see 64-bit and 32-bit designations" mixing CPU word size, physical address bus width, virtual address width, and OS bitness into one term.

GOOD:

- Define each separately. Word size = the natural integer width the ALU operates on. Physical address bus width = how many distinct physical addresses the CPU can drive on the bus. Virtual address width = how many bits of virtual address the MMU translates (often less than the word size; e.g. x86-64 uses 48 of 64). OS bitness = the size of pointers and integers the kernel and userland are compiled for. Then explain how they interact.

# Topology as fait accompli

- Stating a structural division without justifying why the division exists.
- The structure looks arbitrary and the reader cannot predict what changes if the topology changes.

BAD (historical, from a now-removed `os spaces.md`):

- "Modern OSs divide the process virtual address space into two regions." No reason given.

GOOD:

- Justify first: the kernel must run at higher privilege than the process and must be reachable from any process without a context switch on every syscall. The cheapest mechanism is a single virtual address space per process where one half is mapped (with supervisor-only page-table entries) to kernel memory and the other half is mapped to user memory. *Then* name the two regions.

# Mechanism-free hierarchy

- Listing levels of a hierarchy without explaining why the hierarchy exists or how data flows between levels.
- The hierarchy is memorized as a list, not understood as a system.

BAD (historical, from an earlier draft of `memory.md`):

- Seven storage levels listed (registers, L1, L2, L3, RAM, SSD, external) with no rationale and no inter-level mechanism.

GOOD:

- Explain the latency/cost trade-off (each level is roughly an order of magnitude slower and cheaper per byte than the level above). List levels with size and access-time contrast. Describe how data is promoted up (cache fill on miss) and demoted down (eviction). State the inclusion property (most hierarchies are inclusive — L1 ⊆ L2 ⊆ L3 ⊆ RAM).

# Example wikilink

- Linking a concept that appears only as an example or illustration, not as a concept the note is teaching or structurally connected to.
- The link implies the reader needs to understand the target to follow the current note. They don't — the target was just cited in passing.

BAD:

- "In [[c]], `malloc` and `free` manage the heap." C is not being taught; it is cited as an example language. The reader does not need to read the C note to understand heap allocation.

GOOD:

- No link. Write: "The allocator (`malloc`/`free`) manages it." C and other languages can be mentioned as syntax examples without becoming wikilinks.

# Definition without grounding

- Defining a concept by analogy, category name, or by what it is "like" without first walking the reader through the concrete thing the analogy or category points at.
- Telling someone spaghetti "tastes like tomato" is useless if they have never tasted a tomato. The description compiles only against a referent the reader already holds; without the referent, the description is noise.
- The vault failure: stating that the OS solves "abstraction, sharing, and security" before showing the reader, concretely, what actually breaks on bare hardware. The three category names land on nothing — the reader cannot reconstruct the failure they supposedly summarize.

BAD (historical, from an earlier draft of `os.md`):

- "Raw hardware has three concrete problems with personal computing: abstraction, sharing, security." Three category names with one-line gestures at each. The reader is told what categories of problem the OS solves before ever being walked through the bare-hardware behavior that produces them.

GOOD:

- Put the tomato in the reader's hand first. Walk through what specifically breaks on bare hardware: two compiled binaries' stores to the same virtual address collide on the same physical word; either binary can execute a CPU-halting instruction and freeze the other; neither hands the CPU back. *Then* the categories are not labels — they are names for failures the reader has already seen.
- The rule generalizes: any analogy, category name, or comparison-based definition must come *after* the reader has been shown the concrete thing it abstracts. Lead with the tomato, then the analogy.

# Missing diagram on a textbook diagram case

- Skipping the ASCII diagram on a topic that is fundamentally visual.
- Address layouts, page tables, cache structure, ring 0/3 transitions: the mental model is geometric. Prose alone leaves a gap.

BAD:

- Describing the virtual address space layout in prose with no diagram.

GOOD:

- An ASCII diagram (`+`, `-`, `|` borders) showing the regions in their actual address order, with each labeled. See `computer architecture/cache.md` for the format.
