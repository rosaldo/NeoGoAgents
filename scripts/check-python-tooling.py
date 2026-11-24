#!/usr/bin/env -S uvx python
"""Versioned guard for the uvx-only Python convention (Task 29 follow-up).

The Task 29 grep only looked at *.sh, *.py and *.md in the agent divisions, so
seven extensionless scripts under skills/motion-studio/scripts/ kept `uv run`
and the check still printed zero. This check walks every source area, including
extensionless scripts, .reference.md files, skills/, integrations/ and CI, and
fails on any legacy invocation. It lives in the repo and runs in the commit
gate — the earlier /tmp detector was never part of either.

Allowed: uvx <tool>, uvx python -m ..., uvx --with <pkg> python -c "..."
Blocked: pip*, uv add/run/sync/tool install/uv pip, bare python/python3 calls.
"Never ..." lines are prohibition text, not executable guidance.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIVISIONS = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8"))["divisions"]

OLD_CONVENTION = "All Python you write, run or recommend goes through `uv`"
BAD_UV = re.compile(r"\buv\s+(?:add|run|sync|tool\s+install|pip)\b")
BAD_PIP = re.compile(r"\bpip3?(?![-\w])\b(?!\s+audit\b)|\bpipx\b|\bpython3?\s+-m\s+pip\b")
# A bare interpreter sits in command position: line start, $(), a shell
# separator or an env/exec wrapper. Prose, package names and argv literals are
# not calls.
CALL = re.compile(r"(?:^\s*|\$\(|[|&;]\s*|\b(?:env|exec|command|sudo)\s+)python3?\b")
ALLOWED_UVX = re.compile(r"\buvx(?:\s+\S+)*?\s+python3?\b")
FENCE = re.compile(r"^\s*```")
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "dist"}
TEXT_SUFFIXES = {".md", ".sh", ".py", ".yaml", ".yml", ".toml", ".json", ".mdc", ".txt"}
PROHIBITION = re.compile(r"\b(?:never|avoid|forbidden|prohibited|reject|do\s+not|don't)\b", re.I)
# Detectors need to spell the forbidden tokens to recognize them. Skip their
# own source; lint-agents.sh is the older agent-body detector.
DETECTORS = {Path(__file__).resolve(), (ROOT / "scripts" / "lint-agents.sh").resolve()}


def logical_lines(text: str):
    """Yield (line_no, line) with backslash continuations joined.

    A command split across `uvx --with ... \\` + `python script.py` is one
    invocation; scanning the second line alone would call it a bare python.
    """
    number = 1
    buffer = ""
    start = 1
    for line in text.splitlines():
        if not buffer:
            start = number
        if line.rstrip().endswith("\\"):
            buffer += line.rstrip()[:-1] + " "
        else:
            yield start, buffer + line
            buffer = ""
        number += 1
    if buffer:
        yield start, buffer


def text_files(base: Path, *, all_files: bool = False):
    if not base.exists():
        return
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(base).parts):
            continue
        if not all_files and path.suffix not in TEXT_SUFFIXES:
            continue
        yield path


def scan_area(label: str, paths) -> list[str]:
    found: list[str] = []
    for path in paths:
        if path.resolve() in DETECTORS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if OLD_CONVENTION in text:
            found.append(f"{path.relative_to(ROOT)}: old convention")
        for number, line in logical_lines(text):
            if FENCE.match(line):
                continue
            # Prohibition text is documentation of what NOT to do. Real
            # commands in the same line would still be caught by the other
            # areas, and a line that only warns about pip is not a violation.
            if PROHIBITION.search(line):
                continue
            where = f"{path.relative_to(ROOT)}:{number}"
            if BAD_UV.search(line):
                found.append(f"{where}: uv subcommand: {line.strip()[:110]}")
            if BAD_PIP.search(line):
                found.append(f"{where}: pip: {line.strip()[:110]}")
            leftover = ALLOWED_UVX.sub(" ", line)
            if CALL.search(leftover):
                found.append(f"{where}: bare python call: {line.strip()[:110]}")
    print(f"{label}: {len(found)} violation(s)")
    for item in found[:50]:
        print(f"  {item}")
    if len(found) > 50:
        print(f"  ...and {len(found) - 50} more")
    return found


def main() -> int:
    sources = [path for div in DIVISIONS for path in text_files(ROOT / div)]
    # Divisions contain nested subdirectories (game-development/unity, ...).
    # rglob above covers them and .reference.md, whose suffix is .md.
    total = scan_area("sources", sources)
    total += scan_area("skills (incl. extensionless scripts)",
                       text_files(ROOT / "skills", all_files=True))
    total += scan_area("scripts", text_files(ROOT / "scripts", all_files=True))
    total += scan_area("integrations", text_files(ROOT / "integrations", all_files=True))
    total += scan_area("ci", text_files(ROOT / ".github" / "workflows"))

    shebangs = [p for p in (ROOT / "scripts").glob("*.py")
                if p.read_text(encoding="utf-8", errors="replace").startswith(
                    "#!/usr/bin/env python3")]
    print(f"bare-python shebangs: {len(shebangs)}")
    for path in shebangs:
        print(f"  {path.relative_to(ROOT)}")
    total += [(str(p), "shebang") for p in shebangs]

    print("FAILED" if total else "PASSED")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
