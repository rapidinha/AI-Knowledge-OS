# Personal lab template (structure only)

Generic scaffold for a **private** source-of-truth repository that consumes [AI-Knowledge-OS](https://github.com/rapidinha/AI-Knowledge-OS).

This directory is safe on the **public** tree. The same folder names at the **repository root** (`knowledge/`, `notes/`, …) are forbidden on upstream — they belong only in each member’s private SoT.

## Who this is for

Any org member (or external user) who wants:

1. The public wiki as a library
2. A private Obsidian vault that also holds personal knowledge
3. A clear path to promote sanitized notes back upstream

## Bootstrap

```bash
# 1) Create a PRIVATE repo (not a GitHub fork of the public repo — forks cannot be private)
gh repo create <you>/AI-Knowledge-OS-private --private --clone
cd AI-Knowledge-OS-private

# 2) Pull the public library as upstream history (or clone upstream then add private remote)
git remote add upstream https://github.com/rapidinha/AI-Knowledge-OS.git
git fetch upstream
git checkout -B main upstream/main

# 3) Copy this template to the repo root (structure only — no personal content)
cp -R templates/personal-lab/knowledge .
cp -R templates/personal-lab/notes .
cp -R templates/personal-lab/research .
cp -R templates/personal-lab/journals .
cp -R templates/personal-lab/experiments .
cp templates/personal-lab/LAB.md ./LAB.md
cp templates/personal-lab/AGENTS.private.md ./AGENTS.private.md

# 4) Edit LAB.md remotes for your accounts, then commit to origin (private)

# 5) Optional — Leverage Radar
cp templates/radar/config.example.yaml journals/radar/config.yaml
# enable providers; then run the leverage-radar skill in Cursor or Claude Code
```

Open the **private repo root** in Obsidian (not only `wiki/`).

## Layout

```text
templates/personal-lab/          ← lives on public upstream (this folder)
├── README.md                    ← you are here
├── LAB.md                       ← copy to private root
├── AGENTS.private.md            ← copy to private root
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

After copy, the private SoT root looks like:

```text
(private SoT)/
├── wiki/                        ← from upstream
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
