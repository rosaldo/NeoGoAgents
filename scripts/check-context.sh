#!/usr/bin/env bash
#
# check-context.sh — guard the prompt-context budget of the canonical agents.
#
# Checks the SOURCE agent files (not integrations/ or skills/ outputs):
#   1. description > 140 chars                 -> ERROR
#   2. core (body after frontmatter) > 12.000 bytes -> WARN (ERROR with --strict-core)
#   3. sum of the 281 descriptions > 28.000 chars -> ERROR
#   4. CATALOG.md drift vs frontmatter          -> ERROR
#
# No jq, no Python, bash 3.2 + coreutils only, so it runs in CI and locally.
#
# Usage: ./scripts/check-context.sh [--strict-core]

set -euo pipefail
cd "$(dirname "$0")/.."

strict=0
[[ "${1:-}" == "--strict-core" ]] && strict=1

JSON="divisions.json"
CATALOG="CATALOG.md"
EXCLUDED=(integrations skills scripts quant-engine dist strategy examples .claude)

errors=0
warnings=0
agents=0
desc_total=0
fail() { echo "ERROR $*"; errors=$((errors + 1)); }
warn() { echo "WARN $*"; warnings=$((warnings + 1)); }

[[ -f "$JSON" ]] || { echo "ERROR $JSON not found at repo root"; exit 1; }
[[ -f "$CATALOG" ]] || { echo "ERROR $CATALOG not found at repo root"; exit 1; }

divisions="$(awk '/"divisions"[[:space:]]*:[[:space:]]*\{/{f=1; next} f' "$JSON" \
  | grep -oE '"[a-z0-9-]+"[[:space:]]*:[[:space:]]*\{' \
  | sed -E 's/"([a-z0-9-]+)".*/\1/' | sort -u)"

is_division() {
  local base="$1"
  printf '%s\n' "$divisions" | grep -Fxq "$base"
}

is_excluded() {
  local base="$1" ex
  for ex in "${EXCLUDED[@]}"; do
    [[ "$base" == "$ex" ]] && return 0
  done
  return 1
}

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
: > "$tmp/source"
: > "$tmp/catalog"

while IFS= read -r f; do
  base="${f#./}"; base="${base%%/*}"
  [[ "$f" == *.md ]] || continue
  is_division "$base" || continue
  is_excluded "$base" && continue
  agents=$((agents + 1))

  desc="$(awk '/^description:[ \t]*/{sub(/^description:[ \t]*/, ""); print; exit}' "$f")"
  [[ -n "$desc" ]] || fail "$f: missing description"
  n="$(printf '%s' "$desc" | wc -m | tr -d ' ')"
  desc_total=$((desc_total + n))
  [[ "$n" -le 140 ]] || fail "$f: description has $n chars (max 140)"
  printf '%s\n' "$desc" >> "$tmp/source"

  core="$(LC_ALL=C awk 'NR==1 && $0=="---"{fm=1; next} fm==1 && $0=="---"{fm=2; next} fm==2{n+=length($0)+1} END{print n+0}' "$f")"
  if [[ "$core" -gt 12000 ]]; then
    if [[ "$strict" -eq 1 ]]; then
      fail "$f: core has $core bytes (max 12000, --strict-core)"
    else
      warn "$f: core >12.000 bytes"
    fi
  fi
done < <(find . -path ./.git -prune -o -type f -name '*.md' -print | LC_ALL=C sort)

[[ "$desc_total" -le 28000 ]] || fail "description budget: $desc_total chars (max 28000)"

LC_ALL=C sort "$tmp/source" -o "$tmp/source"
sed -n 's/^- `[^`]*` — //p' "$CATALOG" | LC_ALL=C sort > "$tmp/catalog"
if ! diff -u "$tmp/source" "$tmp/catalog" > "$tmp/diff"; then
  fail "CATALOG.md is out of sync with agent frontmatter"
  sed -n '1,20p' "$tmp/diff"
fi

echo "checked: $agents agents, $desc_total description chars"
if [[ "$errors" -gt 0 ]]; then
  echo "FAILED: $errors error(s); $warnings warning(s)"
  exit 1
fi
if [[ "$warnings" -gt 0 ]]; then
  if [[ "$strict" -eq 1 ]]; then
    echo "FAILED: 0 error(s); $warnings warning(s) (strict-core enabled)"
    exit 1
  fi
  echo "PASSED: $agents agents; WARN: $warnings cores >12.000 bytes (strict-core not enabled)"
else
  echo "PASSED: $agents agents; WARN: 0 cores >12.000 bytes"
fi
exit 0
