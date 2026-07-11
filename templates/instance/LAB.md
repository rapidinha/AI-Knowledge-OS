# Personal laboratory (private SoT)

**Visibility:** private GitHub repository  
**Vault:** open **this repository root** in Obsidian (`wiki/` + personal trees)  
**Upstream library:** `rapidinha/AI-Knowledge-OS` (fetch only)

## Why this is not a GitHub “fork”

GitHub cannot make a fork of a public repository private. Use a **private repo** plus remotes (A1-equivalent):

| Remote | Points to | Push |
|--------|-----------|------|
| `origin` | your private SoT | yes (daily) |
| `upstream` | `https://github.com/rapidinha/AI-Knowledge-OS.git` | **never** (fetch only) |
| `fork` | your **public** contribution fork of upstream | only sanitized `feature/public/*` from a clean worktree |

Do not store personal trees on the public contribution fork.

## Domains

| Path | Domain |
|------|--------|
| `wiki/` | Lab copy of the public wiki — promote only after sanitization |
| `knowledge/private/` | Never promote |
| `knowledge/shared/` | Published elsewhere; still not auto-upstream |
| `knowledge/imported/` | Imports; never auto-upstream |
| `notes/`, `research/`, `journals/`, `experiments/` | Never promote |

## Sync from upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main   # or rebase if you prefer linear wiki history
```

Do not resolve conflicts by copying personal notes into `wiki/`.

## Public PR (P1+P2)

```bash
git fetch upstream
git worktree add ../AI-Knowledge-OS-public upstream/main
cd ../AI-Knowledge-OS-public
git checkout -b feature/public/<topic>
# re-apply only sanitized changes
# push to your PUBLIC contribution fork → PR against rapidinha/AI-Knowledge-OS
```

Sanitization: [GOVERNANCE.md](GOVERNANCE.md) §4.

## Agent rules (lab)

- Personal trees are write-private; never suggest PRs that include them.
- If you used any file under `knowledge/`, `notes/`, `research/`, `journals/`, or `experiments/`, the output is **private**.
- Doubt ⇒ private.

## Leverage Radar

Optional discovery journal under `journals/radar/`. Copy `templates/radar/config.example.yaml` to `journals/radar/config.yaml`, enable providers, then run the **leverage-radar** skill in Cursor or Claude Code. See `docs/radar/using-agents.md`.

