#!/usr/bin/env bash
# Regression coverage for YAML frontmatter emitted by convert.sh.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/agency-convert-frontmatter.XXXXXX")"
trap 'rm -rf "$OUTPUT_DIR"' EXIT

for tool in gemini-cli opencode qwen; do
  "$SCRIPT_DIR/convert.sh" --tool "$tool" --out "$OUTPUT_DIR" >/dev/null
done

assert_quoted() {
  local file="$1" field="$2" line prefix
  line="$(awk -v key="$field" '$0 ~ "^" key ":" { print; exit }' "$file")"
  prefix="$field: '"
  [[ "$line" == "$prefix"*"'" ]] || {
    printf 'Expected %s in %s to be a single-quoted YAML scalar, got: %s\n' \
      "$field" "$file" "$line" >&2
    return 1
  }
}

assert_quoted \
  "$OUTPUT_DIR/gemini-cli/agents/developer-tooling-engineer.md" \
  description
assert_quoted \
  "$OUTPUT_DIR/opencode/agents/developer-tooling-engineer.md" \
  name
assert_quoted \
  "$OUTPUT_DIR/opencode/agents/developer-tooling-engineer.md" \
  description
assert_quoted \
  "$OUTPUT_DIR/qwen/agents/programmatic-display-buyer.md" \
  tools

# Maestro must be a primary agent in OpenCode so it shows up in the /agents
# selector like the built-in build/plan agents. Every other agent stays a
# subagent (available through @mention only).
assert_mode() {
  local file="$1" expected="$2" line
  line="$(awk '$0 ~ /^mode:/ { print; exit }' "$file")"
  [[ "$line" == "mode: $expected" ]] || {
    printf 'Expected %s in %s, got: %s\n' "$expected" "$file" "$line" >&2
    return 1
  }
}

assert_mode "$OUTPUT_DIR/opencode/agents/maestro.md" primary
assert_mode "$OUTPUT_DIR/opencode/agents/code-reviewer.md" subagent

echo "PASS: converted YAML frontmatter keeps scalar values safely quoted"
