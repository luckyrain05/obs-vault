#!/usr/bin/env python3
"""Inject calibration files (cache.md + hardware architecture.md) as context.

Non-blocking. On any vault .md write/edit, prepends the contents of the
calibration target notes into Claude's context for that tool call. Puts the
target structure literally in the prompt at write time instead of relying on
Claude's cached abstract memory of the rules.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    allow, get_post_edit_content, inject_context, is_vault_note,
    load_config, read_input,
)


def main():
    try:
        config = load_config()
        if not config:
            allow()
        payload = read_input()
        file_path, _content = get_post_edit_content(payload)
        if not is_vault_note(file_path, config):
            allow()

        vault_root = Path(config["vault_root"])
        calibration_files = config.get("calibration_files", [])

        parts = []
        for rel in calibration_files:
            path = vault_root / rel
            try:
                text = path.read_text()
            except (FileNotFoundError, OSError):
                continue
            parts.append(f"=== Calibration target: {rel} ===\n\n{text}")

        if not parts:
            allow()

        header = (
            "[vault] You are about to write/edit a vault .md note. The files "
            "below are the calibration targets for structure, density, and "
            "voice. Match them: short framing bullets at section tops, bold "
            "sub-blocks for parallel concepts, terse declarative voice, "
            "diagrams at the point of need. Hand off mechanism via wikilinks "
            "rather than duplicating it."
        )
        body = "\n\n---\n\n".join(parts)
        inject_context(f"{header}\n\n{body}")
    except Exception:
        allow()


if __name__ == "__main__":
    main()
