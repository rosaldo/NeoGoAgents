# Paperclip — interface base (self-hosted)

Paperclip is the **interface**, not the brain. It orchestrates agent work with goals, budgets, approvals and an audit trail. Maestro remains the single orchestration protocol in this repository and the ledger remains the single memory of record. This document registers the integration contract; it does not install an app or add a `tools.json` id (Paperclip is a server/UI, not a per-agent renderer).

**Decision record (owner, 24/11/2026 — Task 23):** evaluate and document Paperclip as a self-hosted interface base; **no** API/MCP adapter id in `tools.json`, because Paperclip is a server/UI rather than a per-agent renderer. Product priority P1 does not move the task's place in the plan. Source: `project-tasks/forks-index_consolidacao-agency-agents-tasklist.md` (Task 23) and `project-docs/forks-index_context-baseline.md`.

## Why it was chosen

From the canonical inventory: `paperclip` is `ADOTAR` / `INTEGRACAO`, priority P1 — orchestrates Claude, Codex, Cursor, OpenCode and Gemini with goals, budgets and governance; best interface base for the active OpenCode runtime. The upstream project is MIT-licensed (`paperclipai/paperclip`).

- **Goals and org chart:** assign goals to agents, review strategy, then run. Work is a task manager with approval gates, not a chat transcript.
- **Budgets with hard stop:** per-agent monthly spend limits; at 100% the agent is auto-paused and heartbeats stop. Cost tracking and burn rate stay visible in the dashboard.
- **Sessions that persist:** agent state, skills, tasks and history live in the Paperclip instance, so work survives restarts. This does **not** replace the Maestro ledger for pipeline state.
- **Audit trail:** every approval/review decision is recorded with actor, outcome, comment and run id. Use it to explain what happened, not to duplicate logs in agent prompts.

## OpenCode coverage

Upstream documents an `opencode_local` adapter and lists OpenCode among supported agents; the active TypeScript runtime (`opencode-ts`) is the one to test, **not** the archived Go fork catalogued as `opencode` in `forks-index`. Confirm the installed CLI, provider login and adapter availability in the target instance before promising coverage. No second "code graph" or second agent catalog is registered here.

## BYOK and boundaries

- Keys, provider logins and agent JWTs belong to the owner's Paperclip instance. No key, token, `.env`, credential file or placeholder secret in this repository or in a commit message.
- Do not let an external task protocol bypass governance (checkout, approvals, blockers, budgets, execution policy). A mutation without an approval record is a bug.
- Python helpers, if any, go through `uvx`. Other package-manager subcommands and bare interpreters are out.

## Onboard evaluation (isolated, 24/11/2026)

`npx paperclipai@latest onboard --yes` was run with a temporary `HOME` and npm cache under `/tmp/opencode`, no credentials and no global install. It downloaded the package, applied migrations, started an embedded Postgres on loopback (`127.0.0.1:3100`), enabled auth, DB backups and a 30 s heartbeat, and wrote config only under that temporary home. The command does not exit on its own — it runs the server — so the evaluation was stopped with a timeout after startup was confirmed. Nothing was installed globally and nothing was pushed.

## Provenance

- Fork: `rosaldo/paperclip` — upstream `paperclipai/paperclip`, MIT. Capabilities documented from upstream README and docs; no upstream source, model or binary vendored here.
- Selection: canonical inventory row `paperclip`, `ADOTAR` / `INTEGRACAO`, P1.
