#!/usr/bin/env python3
import json
import re
import sys
from typing import Any


def _emit_allow() -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": "No markdown path policy violation detected",
                }
            }
        )
    )


def _emit_deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                },
                "stopReason": reason,
                "systemMessage": reason,
            }
        )
    )


def _get_nested(data: dict[str, Any], *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _looks_like_forbidden_markdown_path(path: str) -> bool:
    normalized = path.replace("\\", "/").strip()
    if not normalized.lower().endswith(".md"):
        return False

    # Allowed markdown destinations.
    if normalized.startswith("Docs/") or normalized.startswith("./Docs/"):
        return False

    # Block root-level markdown and markdown under any non-Docs directory.
    return True


def _check_create_file(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    file_path = tool_input.get("filePath")
    if isinstance(file_path, str) and _looks_like_forbidden_markdown_path(file_path):
        return (
            f"Markdown files must be created in Docs/. Blocked path: {file_path}. "
            "Use Docs/<name>.md instead."
        )
    return None


def _check_apply_patch(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    patch = tool_input.get("input")
    if not isinstance(patch, str):
        return None

    for line in patch.splitlines():
        if not line.startswith("*** Add File: "):
            continue
        path = line[len("*** Add File: ") :].strip()
        if _looks_like_forbidden_markdown_path(path):
            return (
                f"Markdown files must be created in Docs/. Blocked path: {path}. "
                "Use Docs/<name>.md instead."
            )
    return None


def _check_run_in_terminal(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    command = tool_input.get("command")
    if not isinstance(command, str):
        return None

    # Catch common patterns that write markdown outside Docs/.
    forbidden_patterns = [
        r">\s*([\w./\\-]+\.md)\b",
        r"tee\s+([\w./\\-]+\.md)\b",
        r"cat\s+<<['\"]?\w+['\"]?\s*>\s*([\w./\\-]+\.md)\b",
    ]

    for pattern in forbidden_patterns:
        for match in re.finditer(pattern, command):
            candidate = match.group(1)
            if _looks_like_forbidden_markdown_path(candidate):
                return (
                    f"Markdown files must be created in Docs/. Blocked command target: {candidate}. "
                    "Use Docs/<name>.md instead."
                )
    return None


def main() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        _emit_allow()
        return 0

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # Fail open to avoid blocking if hook payload format is unexpected.
        _emit_allow()
        return 0

    tool_name = (
        _get_nested(payload, "tool_name")
        or _get_nested(payload, "toolName")
        or _get_nested(payload, "hookSpecificInput", "tool_name")
        or _get_nested(payload, "hookSpecificInput", "toolName")
    )
    tool_input = (
        _get_nested(payload, "tool_input")
        or _get_nested(payload, "toolInput")
        or _get_nested(payload, "hookSpecificInput", "tool_input")
        or _get_nested(payload, "hookSpecificInput", "toolInput")
    )

    checker_by_tool = {
        "create_file": _check_create_file,
        "apply_patch": _check_apply_patch,
        "run_in_terminal": _check_run_in_terminal,
    }

    if isinstance(tool_name, str) and tool_name in checker_by_tool:
        reason = checker_by_tool[tool_name](tool_input)
        if reason:
            _emit_deny(reason)
            return 2

    _emit_allow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
