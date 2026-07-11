#!/usr/bin/env bash
# Sync Protocol Kernel framework into an instance without overwriting living wiki files.
set -euo pipefail

UPSTREAM=""
INSTANCE=""
FRAMEWORK_DIRS=(contracts engine agents providers integrations prompts docs examples assets templates)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --upstream) UPSTREAM="$2"; shift 2 ;;
    --instance) INSTANCE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$UPSTREAM" && -n "$INSTANCE" ]] || { echo "Usage: $0 --upstream DIR --instance DIR" >&2; exit 2; }
[[ -d "$UPSTREAM" && -d "$INSTANCE" ]] || { echo "Dirs must exist" >&2; exit 2; }

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync is required but not found in PATH" >&2
  exit 1
fi

# Copy framework dirs (overwrite framework files OK)
for d in "${FRAMEWORK_DIRS[@]}"; do
  if [[ -d "$UPSTREAM/$d" ]]; then
    mkdir -p "$INSTANCE/$d"
    rsync -a --delete "$UPSTREAM/$d/" "$INSTANCE/$d/"
  fi
done

# Institutional root docs (overwrite OK)
for f in README.md VISION.md MISSION.md ARCHITECTURE.md GOVERNANCE.md CONTRIBUTING.md \
         AGENTS.md ROADMAP.md FAQ.md GLOSSARY.md LICENSE; do
  if [[ -f "$UPSTREAM/$f" ]]; then
    cp "$UPSTREAM/$f" "$INSTANCE/$f"
  fi
done

# Wiki: never delete instance files; only copy missing paths (scaffold fill-in)
if [[ -d "$UPSTREAM/wiki" ]]; then
  mkdir -p "$INSTANCE/wiki"
  # copy files that do not exist in instance; do not overwrite
  rsync -a --ignore-existing "$UPSTREAM/wiki/" "$INSTANCE/wiki/"
fi

# research scaffold at root: ignore-existing only
if [[ -d "$UPSTREAM/research" ]]; then
  mkdir -p "$INSTANCE/research"
  rsync -a --ignore-existing "$UPSTREAM/research/" "$INSTANCE/research/"
fi

echo "Sync complete. Instance wiki preserved (ignore-existing)."
