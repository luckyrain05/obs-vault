# Ethos

This vault teaches by **building**, not by **labeling**. Every note must produce a mental model the reader can reconstruct mechanically — not a list of names that sound right.

# 刨根问底

For every concept in a note, answer three questions before moving on:

1. **Why does it exist?** What problem motivated it.
2. **What is it?** The actual definition.
3. **How does it operate mechanically?** What the hardware, OS, or runtime actually does.

If any of the three is missing, either fill it in or wikilink to a note that does. Hand-waved disclaimers — "below is basics only," "trust me," "this is approximately" — are forbidden. Either give the mechanism or hand the reader a prerequisite link. There is no third option.

# Build, don't list

Every level of the vault — the vault itself, each file, each section, each sentence — is built by laying concepts on top of previously-introduced concepts. Nothing is referenced before it is introduced. This is the same DAG discipline as wikilinks, but applied recursively at every scope.

The unit of building is always the same shape: **introduce the problem → state the mental model → expand into details → briefly indicate implementation → hand off mechanism to children**. The mental model lives at the current scope; the mechanism lives in the layer below.

At the **vault** scope: `os.md` introduces the OS as the mediator between compiled binaries and hardware, and the rest of the `operating systems/` notes build on it. `os.md` is the soil; `virtual memory.md`, `processes.md`, `threads.md`, `schedulers.md`, `file systems.md`, `boot.md` are the floors.

At the **file** scope: opening bullets state the problem the file resolves. The first `#` section introduces the foundational concept. Each subsequent section uses only concepts already introduced. The classic failure: `os.md` discusses virtual memory or system calls before the kernel is defined, so the reader has nothing to attach those concepts to.

At the **section** scope: `# Kernel and User Space` introduces the kernel and the privilege boundary as a mental model first (one or two framing bullets), then expands into details (bold sub-blocks for ring 0/3, privileged instructions, supervisor pages, kernel space, user space), then names the implementation only briefly (the page-table-entry supervisor bit, the privilege-level field). Mechanism deeper than that lives in child notes.

At the **sentence** scope: a sentence that uses an undefined term is a sentence in the wrong place. Move it later, or define the term first.

The user-articulated example for `os.md`: the intro states the problem (memory collision, resource hoarding, security on bare hardware). The first section is `# Kernel and User Space` — chosen first because it introduces the kernel, which lets every later section refer to "the kernel" without ambiguity. Then `# [[virtual memory]]` can say "the kernel writes the page tables" without confusion. Then `# Kernel Traps` can say "the CPU goes from ring 3 to ring 0" without confusion. Each section earns its terms from the sections before it.

When drafting a foundation note, the planning order is: opening bullets → section list (in dependency order) → per-section build shape → vocabulary check → only then content. Drafting content before the dependency order is set is the path to forward references and reader confusion. The `vault-pre-write` skill enforces this order.

# The skyscraper

A mental model is a building. Pick the right soil, lay the right foundation, then build floors. A bad foundation collapses the entire structure once you load weight on it.

This happened concretely in this vault: an early note reduced memory layout to "stack vs heap." Later, learning thread memory layout (text, data, BSS, heap, stack — threads share everything except stack), the reader saw "shared heap" and pattern-matched a Data-segment global onto the heap, because heap was the only named shared region in the foundation. The reductive model became a false foundation, and every concept built on top inherited the confusion.

The lesson: never collapse N categories down to N−1 because they share one property. The omitted categories will return as bugs in the reader's mental model.

# The dependency graph

Notes form a DAG. Concurrent branches are normal — processes, threads, and schedulers all build on each other in parallel, not sequentially.

A complete mental model lives in **one file** when it fits at roughly the size of `computer architecture/cache.md`. Split only along *conceptual seams*. The split criterion is:

> Is this sub-concept a complete mental model that other notes would wikilink to in isolation?

Yes → split into its own file. No → keep it in place. Never split because a file is "getting long." Length is not a seam.

# The cache.md anatomy

`computer architecture/cache.md` is the calibration target. Read it before writing notes in any new domain. The patterns to extract:

1. **Self-contained head with prerequisite wikilinks.** Opening bullets at the top of the file (no heading) state what the file is, what it's for, and link any parent concept. `cache.md` does this in two lines.
2. **Dependency-ordered sections.** Each section requires only what came before. Sections cannot be reordered without breaking the chain. (Locality → cache structure → hits/misses → eviction → variants.)
3. **Why before what.** The reason a concept exists is established before its mechanics. Locality is explained before cache structure, because locality is *why* the structure exists.
4. **Mechanism, not labels.** "The CPU walks set → line → offset, MSB to LSB by convention." Not "the metadata is laid out like this."
5. **Model first, variants after.** The core model is built completely. Then parameterizations (direct-mapped, fully-associative, N-way) come at the end.
6. **Diagrams at the point of need.** ASCII tables reinforce non-trivial mechanics. They are not decoration; they appear where prose alone leaves a gap.
7. **Edge cases acknowledged in one line, not exhaustively.** "Most real caches are set-associative." No rabbit hole.
8. **Terse, declarative voice.** Lecturer register. No hedging. "Essentially dog shit" is acceptable when accurate.

When a new note feels harder to write than `cache.md` reads, the cause is almost always missing prerequisites. Find them, link them, and the current note shrinks back to its real scope.
