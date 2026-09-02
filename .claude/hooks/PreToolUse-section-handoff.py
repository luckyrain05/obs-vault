#!/usr/bin/env python3
"""Block 'See [[X]]' / 'Mechanism in [[X]]' prose handoffs in section bodies.

When a section delegates its mechanism to a child note, the section heading
must BE the wikilink (e.g., '# [[virtual memory]]'), not a plain heading
followed by 'See [[virtual memory]] for details.' in body prose.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    allow, deny, get_post_edit_content, is_vault_note,
    load_config, read_input,
)


def main():
    try:
        config = load_config()
        if not config:
            allow()
        payload = read_input()
        file_path, content = get_post_edit_content(payload)
        if not is_vault_note(file_path, config):
            allow()

        patterns = config.get("handoff_prose_patterns", [])
        compiled = [re.compile(p) for p in patterns]

        found = []
        for i, line in enumerate(content.split("\n"), start=1):
            for pat in compiled:
                if pat.search(line):
                    snippet = line.strip()
                    if len(snippet) > 80:
                        snippet = snippet[:77] + "..."
                    found.append((i, snippet))
                    break
            if len(found) >= 3:
                break

        if found:
            violations = "; ".join(f"line {ln}: {text!r}" for ln, text in found)
            reason = (
                f"prose handoff: {violations}. Convert to a section-name "
                f"wikilink — make the heading itself the link (e.g., "
                f"'# [[virtual memory]]') so the handoff lives in the heading "
                f"rather than body prose."
            )
            deny(reason)
        allow()
    except Exception:
        allow()


if __name__ == "__main__":
    main()
