---
name: reverse-engineering
description: Reverse engineer shipped binaries and packages from runtime evidence, not source assumptions.
metadata: { agent: security-architect }
---

# Reverse engineering

Use when a claim depends on a shipped binary, package, firmware image or browser target — decompilation, version comparison or runtime evidence. Skip ordinary source-repository analysis; use repository tools there.

## Route by target

Choose the first tool from the artifact supplied, not from habit:

- Native executable / archive / installer: open the binary and inspect at summary detail before going deeper.
- Electron or JavaScript tree / ASAR: analyze the JavaScript application; extract only selected files from a packaged archive when needed.
- APK / IPA / MSIX / DMG / PyInstaller: inventory members first; the bootloader is not the application layer.
- Managed PE/CLI assembly, Apple bundle resources, UEFI firmware volume: use the matching target-specific route.

## Tools and recovery

Use the tools actually registered in this session and their real schemas; a skill file may describe capabilities an installed version does not have. If a tool is absent or blocked, diagnose the observed blocker (client approval, PATH, registration, engine availability) and continue supported work. Do not repeat unchanged calls, do not run setup before every investigation, and never install unrelated runtimes or reverse-engineering engines to repair registration. An existing CLI with absolute target paths is a valid fallback when acquisition is in scope.

## Evidence discipline

Retain the artifact hash, tool versions, and the exact finding that supports each claim. Separate **observed** facts from **inferred** explanations, list limitations and unknowns, and say "not established" when evidence runs out. Do not claim behavior from source code in a different version. Keep inline evidence when the server does not advertise retained references.

## Boundaries

Authorized targets only. No credentials, no telemetry of the user's environment, no executing untrusted artifacts outside the analysis tooling.

## Provenance

- `rea` — `morluto/rea` · Licence: MIT — Copyright (c) 2026 morluto · ADOTAR — target routing and evidence discipline distilled; no MCP server or engine installed.
  - Third-party gate: CAUTION — global npm installer and setup script excluded; untrusted-target approval and evidence rules distilled.

Technique distilled from documentation and skill instructions; no upstream scripts, binaries, model files or verbatim SKILL.md bodies are vendored here. Attribution above is the record of origin.
