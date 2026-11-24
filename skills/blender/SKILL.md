---
name: blender
description: Route Blender asset work — modeling, lookdev, rigging, rendering and QA — through one entry point with screenshot-backed verification. Use when a task needs a Blender asset or scene and no single specialized skill is already loaded.
metadata: { agent: technical-artist }
---

# Blender

One router for Blender work. It chooses the working mode, then gets out of the way. It does not teach Blender from memory, install a server, or impersonate a 15-year veteran technical director.

## Route first

1. Read the request and the files in the project. Pick **one** entry mode: asset build, lookdev/materials, rigging/animation, scene assembly/render, or QA before handoff.
2. Name the mode and the reason in one line. Read only the instructions needed for that mode; open long references on demand. Re-route only when the task **pivots** to another mode.
3. If a reference image exists, analyze proportions, palette and silhouette before touching geometry. Use it as a target to compare against, never as a licence to copy a protected design.

## Execution contract

- Inspect the tools actually registered in this session and their schemas before calling them. A skill description is not proof that a tool, server or version is present.
- If a Blender bridge is unavailable, say so and work with what exists or ask the owner for the asset. **Never** install a bridge, edit agent configuration, or run a remote bootstrap to repair the session.
- Prefer non-destructive operations: duplicate or version an asset before remeshing, baking or overwriting. Ask before replacing a file the owner did not name.
- After each meaningful phase, capture a viewport screenshot at the working angle (three-quarter hero, plus profile when proportions matter) and compare it with the brief.
- Keep a budget of passes. If work exceeds the agreed budget, stop and ask before continuing; do not silently absorb rework.

## Handoff gate

End with an explicit **ship / no-ship** verdict: what was checked, the screenshot evidence, the defects by severity, and the single next fix if it is a no-ship. No verdict without evidence, and no "looks good" after an uninspected render.

## Provenance

- `blender-skills` — `arjun988/blender-skills` · Licence: MIT — Copyright (c) 2026 blender-skills contributors · Third-party gate: **APPROVE** — SkillSpector 2.12.0 (`--no-llm`) scored 100/CRITICAL, but the five HIGH hits are artifacts: `.gitignore` lines that *ignore* `.env`, docs describing an MCP tool catalogue, README badges and scaffolding text. Semantic review of the 94 skill bodies found no exfiltration, persistence or credential access.
- Excluded: `.mcp.json`, MCP setup docs with remote install commands, marketplace/plugin manifests, the `site/` web app, "Run `bpy` in Blender context" tool-catalogue text, and the upstream veteran-persona framing.
- Technique distilled from skill instructions; no upstream script, config, binary or verbatim `SKILL.md` body is vendored here.
