#!/usr/bin/env python3
"""Block writes that use a term before its ==definition== or **bold subheading**.

Definitions in the intro zone (before the first '#' heading) are exempt — that
zone is for setting up the file's terminology. After the first heading, every
==term== highlight and every line that is exactly **Bold Subheading** must not
have its bare term appear in any earlier post-intro line.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    allow, deny, get_post_edit_content, is_vault_note,
    load_config, read_input,
)

HIGHLIGHT_RE = re.compile(r"==([^=\n]+)==")
BOLD_LINE_RE = re.compile(r"^\*\*([^*\n]+)\*\*$")


def find_intro_end(lines):
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return i
    return len(lines)


def collect_definitions(lines, intro_end):
    """List of (term, line_number_1based, marker_string) for all post-intro defs."""
    defs = []
    seen = set()
    for i, line in enumerate(lines):
        if i < intro_end:
            continue
        for m in HIGHLIGHT_RE.finditer(line):
            term = m.group(1).strip()
            if term and (term, "==") not in seen:
                defs.append((term, i + 1, f"=={term}=="))
                seen.add((term, "=="))
        m = BOLD_LINE_RE.match(line.strip())
        if m:
            term = m.group(1).strip()
            if term and (term, "**") not in seen:
                defs.append((term, i + 1, f"**{term}**"))
                seen.add((term, "**"))
    return defs


def find_earlier_use(term, lines, intro_end, def_line):
    """Return 1-based line number of first earlier post-intro use of term, or None."""
    pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    own_marker_eq = f"=={term}=="
    own_marker_bold = f"**{term}**"
    for i, line in enumerate(lines[: def_line - 1]):
        if i < intro_end:
            continue
        if own_marker_eq in line or own_marker_bold in line:
            continue
        if pattern.search(line):
            return i + 1
    return None


def main():
    try:
        config = load_config()
        if not config:
            allow()
        payload = read_input()
        file_path, content = get_post_edit_content(payload)
        if not is_vault_note(file_path, config):
            allow()

        lines = content.split("\n")
        intro_end = find_intro_end(lines)
        defs = collect_definitions(lines, intro_end)

        violations = []
        for term, def_line, marker in defs:
            use_line = find_earlier_use(term, lines, intro_end, def_line)
            if use_line is not None:
                violations.append((term, use_line, def_line, marker))
                if len(violations) >= 3:
                    break

        if violations:
            parts = [
                f"'{t}' first used at line {u} but {m} is at line {d}"
                for t, u, d, m in violations
            ]
            reason = (
                "forward reference: " + "; ".join(parts) +
                ". Reorder so each ==term== or **Bold subheading** precedes any "
                "use of that term, or move the introduction to the opening "
                "bullets (the intro zone before the first '#' heading is exempt)."
            )
            deny(reason)
        allow()
    except Exception:
        allow()


if __name__ == "__main__":
    main()
