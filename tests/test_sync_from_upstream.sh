#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Fake upstream framework tree
mkdir -p "$TMP/upstream/wiki/principles" "$TMP/upstream/contracts"
echo "SCAFFOLD" > "$TMP/upstream/wiki/principles/.gitkeep"
echo "# contract" > "$TMP/upstream/contracts/signal.md"
echo "UPSTREAM_INDEX" > "$TMP/upstream/wiki/index.md"

# Fake instance with living wiki
mkdir -p "$TMP/instance/wiki/principles" "$TMP/instance/contracts"
echo "LIVING_PRINCIPLE" > "$TMP/instance/wiki/principles/my-principle.md"
echo "INSTANCE_INDEX" > "$TMP/instance/wiki/index.md"

"$ROOT/templates/instance/scripts/sync-from-upstream.sh" \
  --upstream "$TMP/upstream" \
  --instance "$TMP/instance"

# Living files must remain
grep -q LIVING_PRINCIPLE "$TMP/instance/wiki/principles/my-principle.md"
grep -q INSTANCE_INDEX "$TMP/instance/wiki/index.md"
# Framework file should arrive
test -f "$TMP/instance/contracts/signal.md"
# Scaffold .gitkeep may be created if missing, but must not delete living principle
test -f "$TMP/instance/wiki/principles/my-principle.md"
echo "PASS"
