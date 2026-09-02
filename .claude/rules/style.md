# Style

Mechanics for the page. The ethos is in `ethos.md`; this file is the syntax that carries it.

# Opening

- Every note starts with bullets at the top of the file. No heading above them.
- Opening bullets state what the file is, what it's for, and wikilink any parent concept (the note this one extends or specializes).

# Headings

- `#` only. Flush-left.
- Never `##`, `###`, or below.
- All non-heading content sits under `- ` bullets.

# Definition titles

- `**Bold**` flush-left, never inside a bullet, never mid-sentence.
- Bold acts as a sub-heading within a `#` section. Use it whenever a section contains multiple parallel sub-concepts — types (e.g. `**Little-endian**` / `**Big-endian**`), aspects (e.g. `**Allocator**` / `**Lifetime**` of the heap), parts (e.g. `**Block Offset**` / `**Set Index**` / `**Tag**` of cache metadata), or any named sub-topic that has its own bullets. Bold the name, then list its properties as bullets below.
- If a section is more than ~10 bullets or covers more than one named sub-topic, look for bold-able sub-concepts. The default is to split, not to leave a long flat bullet list.
- Never bold a keyword in the middle of a sentence.
- When a bold subheading is itself the term being defined, drop the inline `==term==` highlight — the bold serves as the definition title.

Definition block (title-style):

```
**Keyword**

- Definition...
- Thing to know...
- Another thing to know...
```

# Highlights

- `==term==` only inline within sentences, only to mark a term being defined.
- Example: "this is referred to as ==coupon rate==."
- Never use highlights as titles.
- Never highlight non-definition keywords.

# Voice

- Terse, declarative, lecturer register.
- No hedging: "you can think of it as," "intuitively," "kind of like," "sort of."
- No fluff: no history, no example machines, no "intuition" paragraphs, no "common mistakes," no "when to use," no "in summary."
- No emojis.
- Profanity is acceptable when accurate ("essentially dog shit" is fine for thrashing).

# Spacing

- Blank line between every block (between bullets and a bold definition title, between a bold block and the next bullet group, between sections).
- Never blank-line bullets within the same group to fake paragraph breaks. Obsidian's reading view joins consecutive bullets into one list regardless of source spacing, so the visual separation does not render. If a group needs a break, the right tool is a bold sub-heading (see `# Definition titles`), not whitespace.

# Math

- LaTeX inline: `$x$`, `$2^{64}$`, `$\log_2(\text{block size})$`.
- For graphs of mathematical or financial functions, use the Obsidian Desmos community plugin (already installed). Never ASCII for math curves.

# Wikilinks and the dependency graph

- Wikilinks are dependency edges, not associations.
- Link only when the target concept is a major structural neighbor of the current note — something the note genuinely covers, depends on, or connects to as a primary concept. If the reader does not need to follow the link to keep reading, the link does not belong.
- Do not wikilink concepts that appear only as examples, illustrations, or passing mentions.
- The wikilink graph must remain a real DAG of dependencies. See `anti-patterns.md` → "Associative wikilink" and "Example wikilink."

**Syntax**

- `[[topic]]` — links to a note; displays the filename.
- `[[topic#Section Heading]]` — links to a specific section within a note.
- `[[topic|display text]]` — links to a note but renders custom display text.
- `[[topic#Section Heading|display text]]` — links to a specific section with custom display text.

# Section-name wikilinks for handoffs

When a section delegates its mechanism to a child note, the section heading must BE the wikilink, not a plain heading followed by a "See [[X]]" sentence in the body.

GOOD:

```
# [[virtual memory]]

- The MMU translates virtual to physical, but the kernel writes the page tables it walks.
- Each user program gets its own table; the kernel installs the right one when scheduling that program.
```

BAD:

```
# Virtual memory

- The MMU translates virtual to physical.
- See [[virtual memory]] for the page-table format and the walk algorithm.
```

The handoff lives in the heading. The body gives 2-3 framing bullets — the why, the mental model, the one-line connection to the parent file. Mechanism stays in the child note. The `PreToolUse-section-handoff` hook rejects body-text "See [[X]]" patterns at write time.

# Definition order

Every term that appears in a `==term==` highlight or as a `**Bold subheading**` (a line that is exactly `**Term**`) must not appear in the file before its definition.

The exception: the opening bullets above the first `#` heading are the introduction zone, where any term may be introduced. After the first heading, dependency order is enforced — sections may only reference concepts already named in the opening bullets, in earlier sections of the same file, or in wikilinked prerequisites.

The classic failure: discussing "the kernel" in `# OS Spaces` before the section that defines `==kernel==`. The reader has no anchor for the word. Reorder so the defining section comes first, or move the introduction to the opening bullets. The `PreToolUse-forward-ref` hook rejects forward references at write time.

# Vocabulary discipline

Tokens that require `[[x86 assembly]]` or `[[cpu]]` to recognize — instruction mnemonics (`HLT`, `JMP`), register names (`EIP`, `ESP`, `EAX`, `EBX`, `EDX`, `ECX`, `RSP`), control registers (`CR0`, `CR2`, `CR3`), syscall instructions (`syscall`, `sysenter`, `sysret`) — may appear in a note only if that note wikilinks the prereq, or is itself the prereq target.

A high-level overview that doesn't establish CPU/assembly context cannot drop `CR3` into prose. Either link the prereq, or remove the token. Foundation notes especially: prefer "the page-table root register" over `CR3`, "the privileged instructions" over the named list. Specifics belong in the child note that owns the mechanism.

The `PreToolUse-vocab-check` hook rejects writes containing these tokens unless the prereq link is present. The token list lives in `.claude/lint-config.json` and can be tuned without editing the script.

# Scope discipline

- Only modify files the user explicitly specifies.
- Never change anything the user has written unless asked.
- When working on a file, explain its concepts in a vacuum. Wikilink elsewhere only when required.
- No "while I'm here" cleanups, no opportunistic edits to neighbouring notes.
