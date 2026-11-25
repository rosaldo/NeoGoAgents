#!/usr/bin/env -S uvx python
"""Versioned regression test for check-python-tooling.py.

Each case below was measured against v2.7.5/v2.7.9: the violations were false
negatives there, and the allowed lines became false positives in earlier
attempts to close them. The fixtures run through the detector's real main() on
a throwaway repo root, so area coverage (PR template, JSON, Dockerfile,
extensionless shebangs) is tested as well as pattern matching. Nothing in the
working tree is modified.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check-python-tooling.py"
spec = importlib.util.spec_from_file_location("check_python_tooling", CHECK)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

# name, relative path in the throwaway repo, contents, must be a violation
CASES = [
    ("instead-of-comma", "agents/a.md",
     "Instead of uv, use pip install requests\n", True),
    ("dont-then-comma", "agents/a.md",
     "Don't use uv run, use pip install requests\n", True),
    ("do-not-then-comma", "agents/a.md",
     "Do not use uv sync, run pip install -r requirements.txt\n", True),
    ("versioned-interpreter", "agents/a.md",
     "python3.11 -m venv .venv\n", True),
    ("python2-install", "agents/a.md",
     "python2 setup.py install\n", True),
    ("setup-colon", "agents/a.md",
     "Setup: python -m venv .venv\n", True),
    ("mid-sentence-execute", "agents/a.md",
     "To train, execute python train.py\n", True),
    ("json-command", "integrations/x/tool.json",
     '{"command": "python", "args": ["-m", "venv"]}\n', True),
    ("dockerfile-cmd", "quant-engine/Dockerfile",
     'CMD ["python", "app.py"]\n', True),
    ("pr-template-area", ".github/PULL_REQUEST_TEMPLATE.md",
     "python -m venv .venv\n", True),
    ("usr-bin-shebang", "skills/tool",
     "#!/usr/bin/python3\n", True),
    ("canonical-prohibition-list", "agents/a.md",
     "- Never `pip`, `pip3`, `pipx` or `python -m pip` — and never `uv pip` either.\n",
     False),
    ("uvx-is-allowed", "agents/a.md",
     "uvx python -m unittest discover\n", False),
    ("package-name-is-not-a-call", "agents/a.md",
     "- **Python**: `python-pptx`\n", False),
    ("pip-audit-is-a-tool", "agents/a.md", "uvx pip-audit\n", False),
    ("historical-changelog-prose", "CHANGELOG.md",
     "- use uv instead of pip in the Sigma CI example\n", False),
]


def run_case(name: str, rel: str, text: str, expected: bool) -> str | None:
    with tempfile.TemporaryDirectory(prefix="tooling-fixture-") as tmp:
        root = Path(tmp)
        (root / "divisions.json").write_text(
            json.dumps({"divisions": ["agents"]}), encoding="utf-8")
        (root / "agents").mkdir(exist_ok=True)
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        checker.ROOT = root
        checker.DIVISIONS = ["agents"]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = checker.main()
        detected = code != 0
        if detected == expected:
            return None
        verb = "missed" if expected else "false positive"
        return f"{name}: {verb} (rc={code})\n{output.getvalue().strip()}"


def main() -> int:
    failures = []
    for name, rel, text, expected in CASES:
        problem = run_case(name, rel, text, expected)
        if problem:
            failures.append(problem)
    if failures:
        for item in failures[:10]:
            print(f"  FAIL {item}")
        if len(failures) > 10:
            print(f"  ...and {len(failures) - 10} more")
        print(f"FAILED: {len(failures)} of {len(CASES)} fixture(s)")
        return 1
    print(f"PASSED: {len(CASES)} fixtures ({len(CASES) - 5} violations / 5 allowed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
