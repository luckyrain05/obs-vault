---
name: vault-pre-write
description: Active scope-and-build declaration before writing or editing any vault .md note. Use whenever editing notes under operating systems/, computer architecture/, dsa/, leetcode/, cs general/, git/, calculus/, finance/, or misc/. Forces dependency-ordered planning so concepts are not referenced before they are introduced. Invoke before drafting content, not after.
---

# Vault pre-write

Before writing or editing any vault `.md` note, emit the five-block declaration below in chat. Drafting content without first emitting this declaration is the failure mode this skill exists to prevent. The mechanical hooks (`PreToolUse-forward-ref`, `PreToolUse-vocab-check`, `PreToolUse-section-handoff`) will reject downstream symptoms; this skill prevents the upstream cause.

# The five blocks

## 1. File role

State whether the file is a foundation note (`os.md`, `hardware architecture.md`, `memory.md`, `concurrency.md`, or any entry-point note for a domain) or a child note (a note one or more foundation notes hand off to). Foundation notes own no mechanism — they hand off. Child notes own depth.

## 2. Problem statement

Quote the file's opening bullets — the bullets above the first `#` heading. These set up the problem the rest of the file resolves. If they don't exist or don't set up a problem, the file has no foundation and the rest of the work is premature. Write or revise the opening bullets first.

## 3. Section dependency order

List the planned `#` headings in order. For each, name the earlier sections (or opening bullets) it depends on. A section that uses a concept not yet introduced is misplaced. Reorder before drafting.

Example for `os.md`:

- `# The gap` — depends on opening bullets (which name the OS as a compiled binary).
- `# Kernel and User Space` — depends on `# The gap` (which establishes the need for a privileged mediator). Introduces the kernel and the privilege boundary.
- `# [[virtual memory]]` — depends on `# Kernel and User Space` (which introduces the kernel writing things into hardware-enforced privileged state). Hands off mechanism.
- `# Kernel Traps` — depends on `# Kernel and User Space` (rings) and the implied need for user code to reach kernel services.
- `# [[processes]]` — depends on `# Kernel and User Space` and `# [[virtual memory]]`.

A section that says "the kernel" before `# Kernel and User Space` is a forward reference and will be rejected by the forward-ref hook.

## 4. Per-section build shape

For each section, plan three layers in this order:

- **Mental model**: the why and the what, in 1-3 framing bullets at the top of the section.
- **Details**: bold sub-blocks naming the parallel sub-concepts (e.g., `**Kernel space**` / `**User space**`), each with 1-3 short bullets.
- **Implementation handoff**: name which child note(s) own the mechanism this file delegates. The handoff itself goes in the next section's heading as a wikilink (`# [[virtual memory]]`), not in body prose. The section-handoff hook will reject `- See [[virtual memory]] for X` patterns.

Foundation notes spend most of their lines on the mental model and the bold-detail layer; mechanism handoffs are short. Child notes invert this: they own the mechanism layer in depth.

## 5. Vocabulary check

List any technical tokens that will appear in the file (instruction mnemonics like `HLT`, `JMP`; register names like `EIP`, `ESP`, `EAX`, `CR3`; syscall names like `syscall`, `sysenter`). For each token, name the wikilinked prereq that licenses it (`[[x86 assembly]]` or `[[cpu]]`), or commit to removing the token. The vocab-check hook will reject any of these tokens in a file that doesn't wikilink the prereq.

If the file is a high-level overview that doesn't depend on assembly or CPU internals, the answer is "no such tokens" — and any token that sneaks in must be removed in the draft.

# After the declaration

Only after emitting all five blocks do you begin drafting. The declaration is the contract; the draft is the execution. If during drafting you find a section needs a concept not declared in §3, stop, revise the declaration, then continue. Do not patch the structure mid-draft.
