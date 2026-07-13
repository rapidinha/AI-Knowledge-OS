# Instance template (Context Engine)

Generic scaffold for a **private instance** — a source-of-truth repository that consumes [AI-Knowledge-OS](https://github.com/rapidinha/AI-Knowledge-OS) as its Protocol Kernel.

This directory is safe on the **public** tree. The same folder names at the **repository root** (`knowledge/`, `notes/`, …) are forbidden on upstream — they belong only in each member's private instance.

## Who this is for

Any org member (or external user) who wants:

1. The public framework as a library
2. A private Obsidian vault that holds their living Knowledge Base
3. A clear path to promote sanitized notes back upstream

## Bootstrap

```bash
# 1) Create a PRIVATE repo (not a GitHub fork of the public repo — forks cannot be private)
gh repo create <you>/AI-Knowledge-OS-instance --private --clone
cd AI-Knowledge-OS-instance

# 2) Pull the public library as upstream history (or clone upstream then add private remote)
git remote add upstream https://github.com/rapidinha/AI-Knowledge-OS.git
git fetch upstream
git checkout -B main upstream/main

# 3) Copy this template to the repo root (structure only — no personal content)
cp -R templates/instance/raw .
cp templates/instance/LAB.md ./LAB.md
cp templates/instance/AGENTS.private.md ./AGENTS.private.md

# 4) Edit LAB.md remotes for your accounts, then commit to origin (private)

# 5) Optional — Trend Radar
cp templates/radar/config.example.yaml raw/ops/radar/config.yaml
# enable providers; then run the trend-radar skill in Cursor or Claude Code
```

Open the **private repo root** in Obsidian (not only `wiki/`).

## Sync from upstream

After bootstrap, pull framework updates without overwriting your instance wiki. **Default:** use the sync script (ships with this template):

```bash
templates/instance/scripts/sync-from-upstream.sh --upstream /path/to/AI-Knowledge-OS --instance .
```

The script rsyncs framework paths (`contracts/`, `engine/`, `agents/`, `providers/`, `docs/`, institutional root docs) and uses `--ignore-existing` semantics for `wiki/`. **Rule:** instance `wiki/` wins.

**Fallback only:** if the script is unavailable, manually merge the same framework paths and preserve existing `wiki/` files.

## Layout

```text
templates/instance/              ← lives on public upstream (this folder)
├── README.md
├── LAB.md
├── AGENTS.private.md
├── scripts/sync-from-upstream.sh
├── raw/
│   ├── sources/                 ← ingest
│   ├── research/                ← secondary research
│   └── ops/{daily,posts,radar,experiments}
└── knowledge|notes|journals|research|experiments/  ← stubs → see raw/
```

After copy, the private instance root looks like:

```text
(private instance)/
├── wiki/                        ← compiled LLM wiki (instance-owned)
├── raw/sources|research|ops/
├── LAB.md
├── AGENTS.private.md
└── (framework paths synced from upstream)
```

**Forbidden on upstream root:** `raw/`, `knowledge/`, `notes/`, `journals/`, `experiments/`, … — see `AGENTS.md`.

Schema for ingest → research → consolidate → query → lint: `wiki/_meta/llm-wiki-schema.md`.
