#!/usr/bin/env -S uvx python
"""Regression test for the Task 17 core/reference split.

Claude Code, Copilot and the Hermes router each consume ONE file/string. They
cannot follow a sibling <agent>.reference.md, so the full agent (frontmatter +
core + reference) must be inlined by install.sh and build-hermes-plugin.py.
This test walks all 167 split agents through the three paths that used to drop
the reference, and fails on the first missing marker.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.sh"
BUILDER = ROOT / "scripts" / "build-hermes-plugin.py"
DIVISIONS = json.loads((ROOT / "divisions.json").read_text(encoding="utf-8"))["divisions"]

failures: list[str] = []


def check(label: str, condition: bool) -> None:
    if not condition:
        failures.append(label)


def sources_with_reference() -> list[tuple[str, Path, Path]]:
    agents = []
    for division in DIVISIONS:
        base = ROOT / division
        if not base.is_dir():
            continue
        # Nested source dirs exist under game-development (unity, godot, ...).
        for source in sorted(base.rglob("*.md")):
            reference = source.with_suffix(".reference.md")
            if reference.is_file() and source.read_text(encoding="utf-8").startswith("---\n"):
                agents.append((division, source, reference))
    return agents


def assert_full_agent(label: str, output: str, source: Path, reference: Path,
                      *, frontmatter: bool = True) -> None:
    core = source.read_text(encoding="utf-8")
    # For the body, mirror lib.sh's get_body: every line that is exactly `---`
    # is a fence and is stripped, so compare prose paragraphs, not fences.
    if frontmatter:
        fm = core.split("---\n", 2)[1]
        check(f"{label}: frontmatter preserved", fm.strip() in output)
    strip_fences = lambda text: "\n".join(l for l in text.splitlines() if l != "---").strip()
    core_body = strip_fences(core.split("---\n", 2)[2])
    check(f"{label}: core body present", core_body in strip_fences(output))
    reference_body = strip_fences(reference.read_text(encoding="utf-8"))
    check(f"{label}: reference body present", reference_body in strip_fences(output))


def main() -> int:
    agents = sources_with_reference()
    check(f"found 167 reference-backed agents (got {len(agents)})", len(agents) >= 167)
    if not agents:
        print("no reference-backed agents found")
        return 1

    with tempfile.TemporaryDirectory(prefix="identity-reference-") as tmp:
        base = Path(tmp)
        for tool in ("claude-code", "copilot"):
            dest = base / tool
            env = {**os.environ, "HOME": str(base / "home")}
            if tool == "copilot":
                env["COPILOT_AGENT_DIR"] = str(dest)
            run = subprocess.run(
                [str(INSTALL), "--no-interactive", "--tool", tool, "--path", str(dest)],
                cwd=ROOT, env=env, capture_output=True, text=True,
            )
            if run.returncode != 0:
                failures.append(f"{tool}: install failed: {run.stderr.strip()[:200]}")
                continue
            for division, source, reference in agents:
                installed = dest / source.name
                if not installed.is_file():
                    failures.append(f"{tool}: {division}/{source.name} not installed")
                    continue
                assert_full_agent(f"{tool}:{source.name}",
                                  installed.read_text(encoding="utf-8"), source, reference)

        out = base / "hermes"
        run = subprocess.run(
            ["uvx", "python", str(BUILDER), "--repo-root", str(ROOT), "--out", str(out)],
            cwd=ROOT, capture_output=True, text=True,
        )
        if run.returncode != 0:
            failures.append(f"hermes: build failed: {run.stderr.strip()[:200]}")
        else:
            candidates = list(out.rglob("agents.json"))
            if not candidates:
                failures.append("hermes: agents.json not generated")
            else:
                entries = json.loads(candidates[0].read_text(encoding="utf-8"))
                by_path = {entry.get("source_path"): entry for entry in entries}
                for division, source, reference in agents:
                    entry = by_path.get(str(source.relative_to(ROOT)))
                    if not entry:
                        failures.append(f"hermes: {division}/{source.name} missing from agents.json")
                        continue
                    # The Hermes router stores fields separately; its `body`
                    # is the core + reference only (no frontmatter).
                    assert_full_agent(f"hermes:{source.name}",
                                      entry.get("body", ""), source, reference,
                                      frontmatter=False)

    if failures:
        for item in failures[:20]:
            print(f"  FAIL {item}")
        if len(failures) > 20:
            print(f"  ...and {len(failures) - 20} more")
        print(f"FAILED: {len(failures)} check(s)")
        return 1
    print(f"PASSED: {len(agents)} split agents x 3 identity paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
