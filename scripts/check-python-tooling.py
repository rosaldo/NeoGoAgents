#!/usr/bin/env -S uvx python
"""Versioned guard for the uvx-only Python convention (Task 29 follow-up).

The Task 29 grep only looked at *.sh, *.py and *.md in the agent divisions, so
seven extensionless scripts under skills/motion-studio/scripts/ kept `uv run`
and the check still printed zero. This check walks every source area, including
extensionless scripts, .reference.md files, skills/, integrations/, CI, the
repository root, examples/, quant-engine/ and the PR template, and fails on any
legacy invocation. It lives in the repo, runs in the commit gate, and has a
versioned regression test (scripts/test-python-tooling.py).

Allowed: uvx <tool>, uvx python -m ..., uvx --with <pkg> python -c "..."
Blocked: pip*, uv add/run/sync/tool install/uv pip, bare python/python3 calls,
including versioned interpreters (python3.11) and legacy shebangs.

Prohibition prose ("Never pip", "avoid `python`") is not a violation, but the
exemption is per match and per clause: a comma followed by "use"/"run" starts a
real recommendation, so "Don't use uv run, use pip install" is still caught.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIVISIONS = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8"))["divisions"]

PY = r"python3?(?:\.\d+)*(?![-\w])"
OLD_CONVENTION = "All Python you write, run or recommend goes through `uv`"
BAD_UV = re.compile(r"\buv\s+(?:add|run|sync|tool\s+install|pip)\b")
BAD_PIP = re.compile(
    r"\bpip3?(?![-\w])\b(?!\s+audit\b)|\bpipx\b|\b" + PY + r"\s+-m\s+pip\b"
)
# A bare interpreter sits in command position: line start, $(), a YAML `run:`
# or `Setup:` value, a Dockerfile RUN/CMD, a JSON command key, an env/exec
# wrapper, a shell pipeline, or immediately inside backticks. Prose ("Python
# examples"), package names (`python-pptx`) and table cells are not calls.
# uvx invocations are removed before this test runs.
CALL = re.compile(
    r"(?:^\s*|\$\(|\brun\s*:\s*|\b(?:setup|step|script)\s*:\s*|\bRUN\s+|"
    r"\b(?:env|exec|execute|command|sudo)\s+)" + PY
    + r"(?=\s+(?:-|\S+\.py\b|['\"])|$)",
    re.I,
)
CALL_BACKTICK = re.compile(r"(?<!``)`" + PY, re.I)
CALL_PIPE = re.compile(r"[|&;]\s*" + PY + r"\s+(?:-[\w]|['\"]|\S+\.py\b)", re.I)
CALL_JSON = re.compile(r"['\"](?:command|cmd|run|exec|script)['\"]\s*:\s*['\"]" + PY, re.I)
CALL_CMD = re.compile(r"\bCMD\s*\[\s*['\"]?" + PY, re.I)
SHEBANG = re.compile(r"^#!\s*(?:/usr/bin/env\s+)?(?:\S*/)?" + PY, re.I)
ALLOWED_UVX = re.compile(r"\buvx(?:\s+\S+)*?\s+python3?(?:\.\d+)*\b")
FENCE = re.compile(r"^\s*```")
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "dist"}
TEXT_SUFFIXES = {".md", ".sh", ".py", ".yaml", ".yml", ".toml", ".json", ".mdc", ".txt"}
PROHIBITION = re.compile(
    r"\b(?:never|no|nor|avoid|forbidden|prohibited|reject|do\s+not|don't|"
    r"falls\s+back\s+to|instead\s+of)\b",
    re.I,
)
# List items that keep a prohibition alive after a comma: "Never `pip`, `pip3`
# or `python -m pip`". Anything else after a comma ("use pip", "run pip")
# starts a new instruction and is a real violation.
LIST_CONTINUES = re.compile(
    r"['\"` ]*(?:pip3?\b|pipx\b|uv\b|" + PY + r"|or\b|nor\b|and\b|bare\b)", re.I
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
# own source and the versioned fixture test.
DETECTORS = {
    (ROOT / "scripts" / name).resolve()
    for name in ("check-python-tooling.py", "test-python-tooling.py", "lint-agents.sh")
}


def clause_before(line: str, start: int) -> str:
    """Text before `start`, with non-list commas turned into hard boundaries."""
    before = line[:start]

    def comma(match: re.Match[str]) -> str:
        # Look at the rest of the ORIGINAL line, not just the text before this
        # match: at pip3 in "Never `pip`, `pip3`, ..." only " `" is before it.
        return "," if LIST_CONTINUES.match(line[match.end():]) else ";"

    return re.sub(r",", comma, before)


def prohibited_match(line: str, start: int) -> bool:
    """True only when a nearby prohibition directly qualifies this match.

    The nearest prohibition wins. A sentence boundary, em dash, semicolon or a
    comma that starts a new instruction ("..., use pip install") closes the
    exemption, so a real command after it is never covered by an earlier
    "Never"/"avoid".
    """
    clause = re.split(r"[.!?;—\n]", clause_before(line, start))[-1]
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
        if path.is_file() and path.name != "VERSION":
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
            if SHEBANG.match(line):
                found.add(f"{where}: bare-python shebang: {line.strip()[:110]}")
            leftover = ALLOWED_UVX.sub(" ", line)
            # A `"command": "python"` key is a real command only in a JSON
            # config. The same snippet in Markdown/MDC is documentation.
            patterns = (CALL, CALL_BACKTICK, CALL_PIPE, CALL_CMD)
            if path.suffix == ".json":
                patterns += (CALL_JSON,)
            for pattern in patterns:
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
    total += scan_area(".github (incl. PR template)",
                       text_files(ROOT / ".github", all_files=True))
    total += scan_area(".claude", text_files(ROOT / ".claude", all_files=True))

    shebangs = [item for item in total if "shebang" in item]
    print(f"bare-python shebangs: {len(shebangs)}")
    for item in shebangs:
        print(f"  {item}")

    print("FAILED" if total else "PASSED")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
