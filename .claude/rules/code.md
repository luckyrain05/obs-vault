# Code, DSA, tech skills, graphics

# Code blocks

- Always fenced with the language specified.
- Python is the default unless the user specifies otherwise.

# DSA notes

- Order: code block → inline TC/SC → numbered step list → optional `Notes:` section.
- TC/SC line: `` `O(x)` TC, `O(x)` SC. ``
- Numbered list explains the steps of the solution or algorithm.
- For trivial known-algorithm solutions (e.g. just topological sort, just the merge step of merge sort), omit the numbered list and wikilink the algorithm directly.

Example structure:

```python
# code goes here
```

- `` `O(n)` TC, `O(1)` SC. ``

1. First step.
2. Second step.

`Notes:`

- additional observations.

# DSA implementation

- Manual implementations preferred over library imports.
- Only use libraries when strictly necessary (e.g. `heapq` for a real priority queue).
- No `bisect`, no `Counter`, no `defaultdict` for trivial cases — write the dict logic explicitly.

# LeetCode

- LeetCode notes bridge DSA concepts via wikilinks naturally in the explanation.
- Example: "Build a directed `[[graphs|graph]]` to represent dependencies, then check for valid `[[topological sort algorithm|topological sort]]`."
- Wikilinks in a LeetCode note point at the DSA concepts the solution uses.

# Tech skills (CLI, APIs, Git, ORMs, SDKs)

- Always include a fenced code block with a working example showing exact syntax.
- Default to Python.
- Conceptual explanation is secondary. Primary value is the concrete implementation: function names, parameter order, return types, exact syntax.
- Never explain a tool or API without showing how to call it.

# ASCII graphics

- Fenced blocks with `+`, `-`, `|` borders. Never `[ ]` brackets.
- Use for visually-conceptual topics: caches, page tables, memory layouts, address spaces, ring transitions.
- Skip for algorithms and syntax — they don't need diagrams.
- Minimal words inside the diagram. Words clutter.

# Math/finance graphs

- Use the Obsidian Desmos community plugin (already installed).
- Never ASCII for mathematical curves.

**Color order**

- Apply by line index in the block:
	- 1st line: `#5da5da`
	- 2nd line: `#60bd68`
	- 3rd line: `#faa43a`
	- 4th line: `#b276b2`
	- 5th line: `#f15854`
- Beyond five lines, free choice. Most plots stay below five.
- Reuse the same color for the same role across related plots (e.g. always blue for the main curve, always green for its derivative) so meaning carries.

**Viewport**

- Pick a viewport whose x-span and y-span are equal so each grid unit has the same visual size. Default `left=0; right=10; bottom=0; top=10; grid=true`.
- Shift the y range negative when a curve dips below zero. Keep the total span equal to the x-span, e.g. `bottom=-3; top=7` for x in 0–10.

**Function scaling**

- Pick coefficients so the function stays in frame across the whole x-range. For x in 0–10 with y top=7, scale so the curve's max in-range value lands near the top, not above it.
- Reference forms used in `finance/risk analysis.md` for utility curves on the default viewport:
	- Concave: $U = 2\sqrt{W}$ (≈ 6.3 at W=10).
	- Linear: $U = 0.5 W$ (5 at W=10).
	- Convex: $U = 0.05 W^2$ (5 at W=10).
- Pick scaled forms (not raw $\sqrt{W}$, $W$, $W^2$) so all three are comparable on one viewport.

**Label placement**

- Label syntax: `(x,y)|color|label:Text`. The point itself is invisible; only the text shows.
- Place each label at a point that actually lies on the curve it labels. Plug an x into the function and use the resulting y. Don't pick coordinates by eye — they drift.
- Prefer integer y when an integer x produces one (e.g. $y = 2\sqrt{x}$ at x=9 gives y=6). Otherwise accept the function's value at a clean x.
- Color the label the same color as the curve it labels.
