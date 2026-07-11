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
cp -R templates/instance/knowledge .
cp -R templates/instance/notes .
cp -R templates/instance/research .
cp -R templates/instance/journals .
cp -R templates/instance/experiments .
cp templates/instance/LAB.md ./LAB.md
cp templates/instance/AGENTS.private.md ./AGENTS.private.md

# 4) Edit LAB.md remotes for your accounts, then commit to origin (private)

# 5) Optional — Trend Radar
cp templates/radar/config.example.yaml journals/radar/config.yaml
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
├── README.md                    ← you are here
├── LAB.md                       ← copy to private root
├── AGENTS.private.md            ← copy to private root
├── scripts/
│   └── sync-from-upstream.sh    ← sync framework without clobbering wiki
├── knowledge/
│   ├── README.md
│   ├── private/
│   ├── shared/
│   └── imported/
├── notes/
├── research/
├── journals/
└── experiments/
```

After copy, the private instance root looks like:

```text
(private instance)/
├── wiki/                        ← from upstream (scaffold) + your living KB
├── knowledge/{private,shared,imported}/
├── notes/
├── research/
├── journals/
├── experiments/
├── LAB.md
├── AGENTS.private.md
└── …
```

## Rules (unchanged)

- Never open a public PR that adds root-level `knowledge/`, `notes/`, `research/`, `journals/`, `experiments/`, `obsidian/`, or `vault/`.
- Promote only via sanitization → `feature/public/*` → PR to upstream.
- See root [GOVERNANCE.md](../../GOVERNANCE.md).
