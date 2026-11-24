# OpenMausBot — chat-first alternative

A **separate chat-first client**, not a new persona and not a replacement for the Maestro protocol. It is listed as `COMPLEMENTAR` / `INTEGRACAO` in the canonical fork inventory (P2). This document records the consumption contract for this repository's generated files; it does not install the app.

## What it consumes

OpenMausBot reads local `SKILL.md` files. This repository already generates that format for two adapters: `integrations/osaurus/{slug}/SKILL.md` and `integrations/antigravity/{slug}/SKILL.md` (both `format: skill-md` in `tools.json`). Point the chat client at those files or at the repo's `skills/*/SKILL.md` through the client's own skill library. Nothing is auto-installed by `aa`, and no adapter id is added to `tools.json`.

- **One source, one persona.** Import the generated file as-is; do not fork a "Maus" copy of an agent. `maestro`, `motion-studio` and the P2 skills keep their single definitions here.
- **Keep the ledger outside.** Bot memory belongs to the chat client. The Maestro ledger stays the single source of truth for pipeline state; do not mirror it into a second store.
- **BYOK.** Provider logins and keys stay in the client's own configuration. No token, `.env`, credential file or placeholder key in this repository or in a commit message.
- **Python, if any:** use `uvx`. No other package-manager subcommand and no bare interpreter in helper code.

## OpenCode status — read before promising coverage

Upstream documents OpenCode as an **optional ACP engine**: the app spawns the maintained OpenCode CLI through ACP stdio, so sessions, streaming, tools, permission requests, MCP and cancellation use that runtime. That is distinct from the archived Go fork catalogued as `opencode` in `forks-index`; the active TypeScript runtime is `opencode-ts`. The README still leads with `claude`/`codex`/`grok` CLIs, and ACP coverage depends on the locally installed CLI and provider login.

This adapter therefore **does not guarantee** that an OpenCode session auto-loads these generated skills. Install or import the `skill-md` files through the client's own mechanism and verify in the target session. No new OpenCode adapter is claimed here, and no OpenCode coverage is promised without that check.

## Provenance

- Fork: `rosaldo/OpenMausBot` — upstream `milind-soni/OpenMausBot`, Apache-2.0. Technique and interface contract documented here; no upstream code, binary or prompt file vendored.
- Tool selection: from the canonical inventory row `OpenMausBot`, `COMPLEMENTAR` / `INTEGRACAO`, priority P2.
