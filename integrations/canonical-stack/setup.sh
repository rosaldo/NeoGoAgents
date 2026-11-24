#!/usr/bin/env bash
#
# setup.sh — read-only preflight for the canonical integration stack.
#
# Writes nothing, installs nothing, asks for no credentials. Prints which
# components are reachable and the MCP config shape the owner can apply in
# their own client. See README.md for the install contract of each entry.

set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

printf 'Canonical integration stack — preflight (read-only)\n\n'

check_bin() {
  local label="$1" bin="$2"
  if command -v "$bin" >/dev/null 2>&1; then
    printf '  reachable  %-20s %s\n' "$label" "$bin"
  else
    printf '  missing    %-20s %s\n' "$label" "$bin"
  fi
}

check_bin LocalAI local-ai
check_bin koon-mcp koon-mcp
check_bin GhidraMCP ghidra-mcp
check_bin litellm litellm

if uvx --with litellm python -c 'import litellm' >/dev/null 2>&1; then
  printf '  reachable  %-20s %s\n' litellm 'via uvx'
else
  printf '  missing    %-20s %s\n' litellm 'via uvx (needs owner install)'
fi

printf '\nMCP config shape (placeholders only, no keys):\n'
cat <<'JSON'
{
  "mcpServers": {
    "codebase-memory": { "command": "codebase-memory-mcp", "args": ["--no-hooks", "--max-output-tokens", "4000"] },
    "memanto":         { "command": "memanto", "args": [] },
    "zvec":            { "command": "zvec", "args": [] },
    "koon":            { "command": "koon-mcp", "args": [] },
    "ghidra":          { "command": "GhidraMCP", "args": [] }
  }
}
JSON

printf '\nNo keys belong in this repository. Supply provider credentials through your own environment.\n'
