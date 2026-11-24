# Canonical integration stack

The **only** set registered as an installed integration stack for this fork. Everything else in `integrations/` is a harness adapter or a documented technique, not an extra runtime. Bring your own keys: no key, token, `.env` or credential file is versioned here.

| Component | Role | Install contract | Verify |
| --- | --- | --- | --- |
| `codebase-memory-mcp` | Code knowledge graph: `search_graph` → `trace_path` → `get_code_snippet` → `query_graph` → `get_architecture` | MCP server registered in the client config with **`--no-hooks`** and an output cap (≤4k tokens per call by default). Prefer graph tools over grep/glob for code discovery. No repository hooks. | `search_graph(name_pattern=".*Agent.*")` returns nodes; a single call stays under the cap. |
| `litellm` | BYOK model gateway: one interface, provider keys supplied by the owner at runtime | Local client config only; keys injected from the environment of the calling process, never written into this repo. | `uvx --with litellm python -c "import litellm; print(litellm.__version__)"` |
| `memanto` | Session/decision memory across agent handoffs | MCP entry with a local data directory outside the repo; tag by agent and project. The Maestro ledger remains the source of truth for pipeline state. | Recall a decision written in the previous session. |
| `zvec` | Local vector index for retrieval experiments | Local index directory, rebuildable from source documents; no hosted endpoint by default. | Index a small fixture and retrieve it by semantic query. |
| `LocalAI` | Local OpenAI-compatible inference endpoint | Self-hosted process on the owner's machine; base URL supplied by configuration, no baked URL in prompts or agents. | `curl --fail http://<local-host>:<port>/v1/models` with the owner's address. |
| `koon-mcp` | MCP bridge for codebase context | Registered only when the host exposes the required tools; no second "code graph" entry competing with `codebase-memory-mcp`. | Tool list contains the bridge tools and no duplicate graph tool set. |
| `GhidraMCP` | Binary/decompilation support for authorized targets | Local Ghidra installation plus MCP bridge; explicit approval before touching a target artifact. Never part of an auto-loaded skill. | Decompile a known sample and compare a symbol with the shipped artifact. |

## Rules

1. **One graph server.** `codebase-memory-mcp` is the canonical code-graph provider. `koon-mcp` is a bridge, and any other graph-shaped tool stays in [the technique/fallback doc](../technique-fallbacks/README.md) — never a second installed graph server.
2. **`--no-hooks` always.** The graph server must not inject instructions into every turn. Cap its output so a broad query cannot flood the context budget.
3. **BYOK.** Keys live in the owner's environment or client config outside the repository. A config example may contain placeholder names only. Never paste a token into a prompt, an agent, a skill or a commit message.
4. **Python goes through `uvx`.** Use `uvx <tool>`, `uvx python -m ...` or `uvx --with <pkg> python -c "..."`. Other package-manager subcommands, installers and bare interpreters are out.
5. **No redundant installs.** Installing a component here does not mean duplicating a harness adapter from `tools.json`: adapters render agents, this stack provides runtime services.

## Setup

See [`setup.sh`](setup.sh) for a read-only preflight that reports which components are reachable and prints the MCP config shape. It writes nothing and asks for no credentials. The owner applies the config in their own client.

## Provenance

Registry entries follow the canonical fork inventory (`20261123-231543`): these seven are the P3 stack marked for real installation. No upstream source, model or binary is vendored in `agency-agents`.
