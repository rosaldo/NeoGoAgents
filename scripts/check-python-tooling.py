#!/usr/bin/env -S uvx python
"""Versioned guard for the uvx-only Python convention (Task 29 follow-up).

The Task 29 grep only looked at *.sh, *.py and *.md in the agent divisions, so
seven extensionless scripts under skills/motion-studio/scripts/ kept `uv run`
and the check still printed zero. This check walks every source area, including
extensionless scripts, .reference.md files, skills/, integrations/, CI, the
repository root, examples/ and quant-engine/, and fails on any legacy
invocation. It lives in the repo and runs in the commit gate.

Allowed: uvx <tool>, uvx python -m ..., uvx --with <pkg> python -c "..."
Blocked: pip*, uv add/run/sync/tool install/uv pip, bare python/python3 calls.

Prohibition prose ("Never pip", "avoid `python`", "don't use uv run") is not a
violation, but the exemption is per match, never per line: a real command later
on the same line is still caught.
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
# A bare interpreter sits in command position: line start, $(), a YAML `run:`
# value, a Dockerfile RUN, an env/exec wrapper, a shell pipeline, or immediately
# inside backticks. Prose ("Python examples"), package names (`python-pptx`) and
# table cells are not calls. uvx invocations are removed before this test runs.
CALL = re.compile(
    r"(?:^\s*|\$\(|\brun\s*:\s*|\bRUN\s+|\b(?:env|exec|command|sudo)\s+)"
    r"python3?(?![-\w])(?=\s+(?:-|\S+\.py\b|['\"])|$)",
    re.I,
)
CALL_BACKTICK = re.compile(r"(?<!``)`python3?(?![-\w])", re.I)
CALL_PIPE = re.compile(
    r"[|&;]\s*python3?(?![-\w])\s+(?:-[\w]|['\"]|\S+\.py\b)", re.I
)
ALLOWED_UVX = re.compile(r"\buvx(?:\s+\S+)*?\s+python3?\b")
FENCE = re.compile(r"^\s*```")
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "dist"}
TEXT_SUFFIXES = {".md", ".sh", ".py", ".yaml", ".yml", ".toml", ".json", ".mdc", ".txt"}
PROHIBITION = re.compile(
    r"\b(?:never|no|nor|avoid|forbidden|prohibited|reject|do\s+not|don't|"
    r"falls\s+back\s+to|instead\s+of)\b",
    re.I,
)
# Words that may sit between a prohibition and the forbidden token. Nothing
# else is allowed, so "never do X and then pip install" is still a violation.
FILLER = {
    "a", "add", "advice", "agents", "all", "an", "and", "any", "are", "bare",
    "c", "call", "calling", "ci", "code", "direct", "directly", "do", "either",
    "example", "examples", "in", "install", "interpreter", "invoke", "invoking",
    "its", "m", "makefile", "nor", "not", "of", "or", "pip", "pip3", "pipx",
    "python", "python3", "raw", "run", "running", "sigma", "sync", "the",
    "tool", "use", "used", "uses", "using", "uv",
}
# Detectors need to spell the forbidden tokens to recognize them. Skip their
# own source; lint-agents.sh is the older agent-body detector.
DETECTORS = {Path(__file__).resolve(), (ROOT / "scripts" / "lint-agents.sh").resolve()}


def prohibited_match(line: str, start: int) -> bool:
    """True only when a nearby prohibition directly qualifies this match.

    The nearest prohibition wins. An em dash, semicolon or sentence boundary
    starts a new thought, so a real command after it is never covered by an
    earlier "Never"/"avoid".
    """
    clause = re.split(r"[.!?;—\n]", line[:start])[-1]
    matches = list(PROHIBITION.finditer(clause))
    if not matches:
        return False
    tail = clause[matches[-1].end():]
    words = [w.lower() for w in re.findall(r"[A-Za-z']+", tail)]
    return len(words) <= 16 and (not words or all(w in FILLER for w in words))


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


def root_files():
    """Top-level files, including extensionless ones such as a root Dockerfile."""
    for path in ROOT.iterdir():
        if path.is_file() and path.name not in {"VERSION"}:
            yield path


def scan_area(label: str, paths) -> list[str]:
    found: set[str] = set()
    for path in paths:
        if path.resolve() in DETECTORS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if OLD_CONVENTION in text:
            found.add(f"{path.relative_to(ROOT)}: old convention")
        for number, line in logical_lines(text):
            if FENCE.match(line):
                continue
            where = f"{path.relative_to(ROOT)}:{number}"
            for pattern, kind in ((BAD_UV, "uv subcommand"), (BAD_PIP, "pip")):
                for m in pattern.finditer(line):
                    if not prohibited_match(line, m.start()):
                        found.add(f"{where}: {kind}: {line.strip()[:110]}")
            leftover = ALLOWED_UVX.sub(" ", line)
            for pattern in (CALL, CALL_BACKTICK, CALL_PIPE):
                for m in pattern.finditer(leftover):
                    if not prohibited_match(leftover, m.start()):
                        found.add(f"{where}: bare python call: {line.strip()[:110]}")
    result = sorted(found)
    print(f"{label}: {len(result)} violation(s)")
    for item in result[:50]:
        print(f"  {item}")
    if len(result) > 50:
        print(f"  ...and {len(result) - 50} more")
    return result


def main() -> int:
    sources = [path for div in DIVISIONS for path in text_files(ROOT / div)]
    total = scan_area("sources", sources)
    total += scan_area("root", root_files())
    total += scan_area("examples", text_files(ROOT / "examples", all_files=True))
    total += scan_area("quant-engine", text_files(ROOT / "quant-engine", all_files=True))
    total += scan_area("skills (incl. extensionless scripts)",
                       text_files(ROOT / "skills", all_files=True))
    total += scan_area("scripts", text_files(ROOT / "scripts", all_files=True))
    total += scan_area("integrations", text_files(ROOT / "integrations", all_files=True))
    total += scan_area("ci", text_files(ROOT / ".github" / "workflows"))
    total += scan_area(".claude", text_files(ROOT / ".claude", all_files=True))

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
