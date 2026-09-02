"""Shared helpers for vault PreToolUse hook scripts.

All hook scripts:
- Read JSON payload from stdin (Claude Code hook protocol).
- Resolve the post-edit content of the target file.
- Either allow (exit 0, no output) or deny (JSON with permissionDecision).
- Silently allow on any internal error so a broken hook never blocks work.
"""
import json
import os
import sys
from pathlib import Path


def load_config():
    """Load .claude/lint-config.json. Returns None if absent or unparseable."""
    this_dir = Path(__file__).resolve().parent
    config_path = this_dir.parent / "lint-config.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def read_input():
    """Read JSON payload from stdin. Returns {} on failure."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def get_post_edit_content(payload):
    """Resolve (file_path, post_edit_content) for Write/Edit/MultiEdit.

    Returns (None, None) if the payload doesn't name a file we can resolve.
    For Edit/MultiEdit, simulates the edit by reading the current file and
    applying the substitution(s), so downstream checks see the full
    post-edit document, not just the diff.
    """
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path")
    if not file_path:
        return None, None

    if tool_name == "Write":
        return file_path, tool_input.get("file_content", "") or tool_input.get("content", "")

    if tool_name == "Edit":
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")
        replace_all = tool_input.get("replace_all", False)
        try:
            current = Path(file_path).read_text()
        except (FileNotFoundError, OSError):
            return file_path, new
        if replace_all:
            return file_path, current.replace(old, new)
        return file_path, current.replace(old, new, 1)

    if tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        try:
            content = Path(file_path).read_text()
        except (FileNotFoundError, OSError):
            content = ""
        for edit in edits:
            old = edit.get("old_string", "")
            new = edit.get("new_string", "")
            if edit.get("replace_all", False):
                content = content.replace(old, new)
            else:
                content = content.replace(old, new, 1)
        return file_path, content

    return None, None


def is_vault_note(file_path, config):
    """True iff file_path is a .md note inside the vault and not excluded."""
    if not file_path or not file_path.endswith(".md"):
        return False
    if not config:
        return False
    vault_root = Path(config["vault_root"]).resolve()
    try:
        rel = Path(file_path).resolve().relative_to(vault_root)
    except ValueError:
        return False
    rel_str = str(rel)
    for excl_dir in config.get("exclude_dirs", []):
        if rel_str == excl_dir or rel_str.startswith(excl_dir + os.sep):
            return False
    for excl_file in config.get("exclude_files", []):
        if rel_str == excl_file or rel_str.endswith(os.sep + excl_file):
            return False
    return True


def relpath(file_path, config):
    """Return path relative to vault root, or None if outside."""
    if not config:
        return None
    vault_root = Path(config["vault_root"]).resolve()
    try:
        return str(Path(file_path).resolve().relative_to(vault_root))
    except ValueError:
        return None


def allow():
    """Exit 0 with no output. Tool call proceeds."""
    sys.exit(0)


def deny(reason):
    """Print JSON denying the tool call. Reason is surfaced to Claude as feedback."""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(payload))
    sys.exit(0)


def inject_context(text):
    """Print JSON injecting additional context into the next model turn."""
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": text,
        }
    }
    print(json.dumps(payload))
    sys.exit(0)
