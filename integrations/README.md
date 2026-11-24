# 🔌 Integrations

This directory contains The Agency integrations and converted formats for
supported agentic coding tools.

## Supported Tools

- **[Claude Code](#claude-code)** — `.md` agents, use the repo directly
- **[GitHub Copilot](#github-copilot)** — `.md` agents, use the repo directly
- **[Antigravity](#antigravity)** — `SKILL.md` per agent in `antigravity/`
- **[Gemini CLI](#gemini-cli)** — `.md` agent files in `gemini-cli/agents/`
- **[OpenCode](#opencode)** — `.md` agent files in `opencode/`
- **[OpenClaw](#openclaw)** — `SOUL.md` + `AGENTS.md` + `IDENTITY.md` workspaces
- **[Cursor](#cursor)** — `.mdc` rule files in `cursor/`
- **[Aider](#aider)** — `CONVENTIONS.md` in `aider/`
- **[Windsurf](#windsurf)** — `.windsurfrules` in `windsurf/`
- **[Kimi Code](#kimi-code)** — YAML agent specs in `kimi/`
- **[Qwen Code](#qwen-code)** — project-scoped `.md` SubAgents in `.qwen/agents/`
- **[Codex](#codex)** — `.toml` custom agents in `codex/`
- **[Mistral Vibe](vibe/README.md)** — `.toml` agents + prompt files generated in `vibe/`
- **Osaurus** -- `SKILL.md` skills generated in `osaurus/`
- **[Hermes](hermes/README.md)** -- lazy-router plugin generated in `hermes/`
- **Zcode** — `.md` agent files in `zcode/`

## Default Locations per Harness

Paths are relative to the user's home (user scope) or the project root (project
scope). `install.sh --tool <id>` writes to these locations; none of them is
mandatory, and each harness reads its own standard location. `tools.json` is the
source of truth for the ids and formats below.

| tools.json id | Format | User scope | Project scope |
|---|---|---|---|
| `claude-code` | `identity` | `.claude/agents/{slug}.md` | `.claude/agents/{slug}.md` |
| `codex` | `codex-toml` | `.codex/agents/{slug}.toml` | `.codex/agents/{slug}.toml` |
| `gemini-cli` | `gemini-md` | `.gemini/agents/{slug}.md` | `.gemini/agents/{slug}.md` |
| `copilot` | `identity` | `.copilot/agents/{slug}.md`, `.github/agents/{slug}.md` | `.github/agents/{slug}.md` |
| `qwen` | `qwen-md` | `.qwen/agents/{slug}.md` | `.qwen/agents/{slug}.md` |
| `cursor` | `cursor-mdc` | — | `.cursor/rules/{slug}.mdc` |
| `opencode` | `opencode-md` | `.config/opencode/agents/{slug}.md` | `.opencode/agents/{slug}.md` |
| `osaurus` | `skill-md` | `.osaurus/skills/{slug}/SKILL.md` | — |
| `aider` | `aider-conventions` | — | `CONVENTIONS.md` |
| `antigravity` | `skill-md` | `.gemini/config/skills/{slug}/SKILL.md` | `.agents/skills/{slug}/SKILL.md` |
| `kimi` | `kimi-agent` | `.config/kimi/agents/{slug}/agent.yaml`, `.config/kimi/agents/{slug}/system.md` | — |
| `openclaw` | `openclaw-workspace` | `.openclaw/agency-agents/{slug}/SOUL.md`, `.openclaw/agency-agents/{slug}/AGENTS.md`, `.openclaw/agency-agents/{slug}/IDENTITY.md` | — |
| `windsurf` | `windsurf-rules` | — | `.windsurfrules` |
| `hermes` | `hermes-router-plugin` | `.hermes/plugins/agency-agents-router` | — |
| `vibe` | `vibe-toml` | `.vibe/agents/{slug}.toml`, `.vibe/prompts/{slug}.md` | `.vibe/agents/{slug}.toml`, `.vibe/prompts/{slug}.md` |
| `zcode` | `zcode-md` | `.zcode/agents/{slug}.md` | `.zcode/agents/{slug}.md` |

### OpenCode: three different roles

- **Catalog `opencode`** — the archived Go fork catalogued in `forks-index`; it is not the runtime this adapter targets.
- **`opencode-ts`** — the active TypeScript OpenCode runtime (`anomalyco/opencode`, opencode.ai).
- **`opencode` id in `tools.json`** — this repository's adapter (`format: opencode-md`), writing to `.config/opencode/agents/{slug}.md` (user scope) and `.opencode/agents/{slug}.md` (project scope).

Those two directories are the adapter's paths for the active TypeScript runtime,
not paths of the archived Go fork.

## Runtime services and technique docs

These are **not** harness adapters and have no `tools.json` id: `aa` must not render
them as per-agent files. They are registered separately so the stack has one owner.

- **[Canonical stack](canonical-stack/README.md)** — the installed runtime services:
  `codebase-memory-mcp` (`--no-hooks`, output cap), `litellm`, `memanto`, `zvec`,
  `LocalAI`, `koon-mcp` and `GhidraMCP`. BYOK only; `setup.sh` is a read-only preflight.
- **[Techniques and fallbacks](technique-fallbacks/README.md)** — documented, not installed:
  `Graft`, `graphify`, `Understand-Anything`, `milvus`, `OmniRoute` (memory OFF),
  `freellmapi`, and protocol references for the Maestro ledger.

## Quick Install

```bash
# Install for all detected tools automatically
./scripts/install.sh

# Install a specific home-scoped tool
./scripts/install.sh --tool antigravity
./scripts/install.sh --tool copilot
./scripts/install.sh --tool openclaw
./scripts/install.sh --tool claude-code
./scripts/install.sh --tool codex
./scripts/install.sh --tool osaurus
./scripts/install.sh --tool hermes

# Gemini CLI needs generated integration files on a fresh clone
./scripts/convert.sh --tool gemini-cli
./scripts/install.sh --tool gemini-cli

# Qwen Code also needs generated SubAgent files on a fresh clone
./scripts/convert.sh --tool qwen
./scripts/install.sh --tool qwen
```

If you install OpenClaw and the gateway is already running, restart it after installation:

```bash
openclaw gateway restart
```

For project-scoped tools such as OpenCode, Cursor, Aider, Windsurf, and Qwen
Code, run
the installer from your target project root as shown in the tool-specific
sections below.

## Regenerating Integration Files

If you add or modify agents, regenerate all integration files:

```bash
./scripts/convert.sh
```

---

## Claude Code

The Agency was originally designed for Claude Code. Agents work natively
without conversion.

```bash
./scripts/install.sh --tool claude-code
```

Optional manual copy (not required): `cp -r <category>/*.md ~/.claude/agents/`.

See [claude-code/README.md](claude-code/README.md) for details.

---

## GitHub Copilot

The Agency also works natively with GitHub Copilot. Agents can be copied
directly into `~/.github/agents/` and `~/.copilot/agents/` without conversion.

```bash
./scripts/install.sh --tool copilot
```

See [github-copilot/README.md](github-copilot/README.md) for details.

---

## Antigravity

Skills are installed to `~/.gemini/config/skills/`. Each agent becomes
a separate skill prefixed with `agency-` to avoid naming conflicts.

```bash
./scripts/install.sh --tool antigravity
```

See [antigravity/README.md](antigravity/README.md) for details.

---

## Gemini CLI

Agents are packaged as Gemini CLI subagents.
Subagents are installed to `~/.gemini/agents/`.
Because the agent files are generated artifacts, run
`./scripts/convert.sh --tool gemini-cli` before installing from a fresh clone.

```bash
./scripts/convert.sh --tool gemini-cli
./scripts/install.sh --tool gemini-cli
```

See [gemini-cli/README.md](gemini-cli/README.md) for details.

---

## OpenCode

Each agent becomes a project-scoped `.md` file in `.opencode/agents/`.

```bash
cd /your/project && /path/to/agency-agents/scripts/install.sh --tool opencode
```

See [opencode/README.md](opencode/README.md) for details.

---

## OpenClaw

Each agent becomes an OpenClaw workspace containing `SOUL.md`, `AGENTS.md`,
and `IDENTITY.md`.

Before installing, generate the OpenClaw workspaces:

```bash
./scripts/convert.sh --tool openclaw
```

Then install them:

```bash
./scripts/install.sh --tool openclaw
```

See [openclaw/README.md](openclaw/README.md) for details.

---

## Cursor

Each agent becomes a `.mdc` rule file. Rules are project-scoped — run the
installer from your project root.

```bash
cd /your/project && /path/to/agency-agents/scripts/install.sh --tool cursor
```

See [cursor/README.md](cursor/README.md) for details.

---

## Aider

All agents are consolidated into a single `CONVENTIONS.md` file that Aider
reads automatically when present in your project root.

```bash
cd /your/project && /path/to/agency-agents/scripts/install.sh --tool aider
```

See [aider/README.md](aider/README.md) for details.

---

## Windsurf

All agents are consolidated into a single `.windsurfrules` file for your
project root.

```bash
cd /your/project && /path/to/agency-agents/scripts/install.sh --tool windsurf
```

See [windsurf/README.md](windsurf/README.md) for details.

---

## Kimi Code

Each agent is converted to a Kimi Code CLI agent specification (YAML format with
separate system prompt files). Agents are installed to `~/.config/kimi/agents/`.

Because the Kimi agent files are generated from the source Markdown, run
`./scripts/convert.sh --tool kimi` before installing from a fresh clone.

```bash
./scripts/convert.sh --tool kimi
./scripts/install.sh --tool kimi
```

### Usage

After installation, use an agent with the `--agent-file` flag:

```bash
kimi --agent-file ~/.config/kimi/agents/frontend-developer/agent.yaml
```

Or in a specific project:

```bash
cd /your/project
kimi --agent-file ~/.config/kimi/agents/frontend-developer/agent.yaml \
     --work-dir /your/project
```

See [kimi/README.md](kimi/README.md) for details.

---

## Qwen Code

Each agent becomes a project-scoped `.md` SubAgent file in `.qwen/agents/`.

From a fresh clone, generate the Qwen files first:

```bash
./scripts/convert.sh --tool qwen
```

Then install them from your project root:

```bash
cd /your/project && /path/to/agency-agents/scripts/install.sh --tool qwen
```

See [qwen/README.md](qwen/README.md) for details.

---

## Codex

Each agent is converted into a standalone Codex custom agent TOML file and
installed to `~/.codex/agents/`.

Because Codex uses generated TOML files rather than the source Markdown
directly, run the converter before installing from a fresh clone:

```bash
./scripts/convert.sh --tool codex
./scripts/install.sh --tool codex
```

See [codex/README.md](codex/README.md) for details.
