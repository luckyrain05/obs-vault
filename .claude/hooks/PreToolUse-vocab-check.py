#!/usr/bin/env python3
"""Block writes containing assembly vocabulary unless required prereqs are wikilinked.

Tokens like HLT, EIP, CR3 require either [[x86 assembly]] or [[cpu]] to be
wikilinked from the file (or the file itself is one of those prereqs). Catches
the failure pattern of dropping low-level instruction/register names into
high-level overview notes that don't link the prereq context.
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

        required_prereqs = config.get("vocab_required_prereqs", [])
        # Exception: the file IS one of the prereq targets (e.g. cpu.md, x86 assembly.md).
        prereq_stems = [p.strip("[]") for p in required_prereqs]
        file_stem = Path(file_path).stem
        if file_stem in prereq_stems:
            allow()

        if any(prereq in content for prereq in required_prereqs):
            allow()

        blocklist = config.get("vocab_blocklist", [])
        found = []
        for token in blocklist:
            pattern = re.compile(r"\b" + re.escape(token) + r"\b")
            m = pattern.search(content)
            if m:
                line_num = content[: m.start()].count("\n") + 1
                found.append((token, line_num))
                if len(found) >= 3:
                    break

        if found:
            violations = ", ".join(f"'{tok}' at line {ln}" for tok, ln in found)
            prereqs = " or ".join(required_prereqs)
            reason = (
                f"vocabulary creep: {violations}. These tokens require {prereqs} "
                f"to be wikilinked from this file, or remove the tokens. Don't "
                f"drop low-level mnemonics into a high-level note that doesn't "
                f"establish the prereq context."
            )
            deny(reason)
        allow()
    except Exception:
        allow()


if __name__ == "__main__":
    main()
