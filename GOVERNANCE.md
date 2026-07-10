# Governance RFC — Public wiki vs personal laboratory

**Status:** Active  
**Date:** 2026-07-10  
**Model:** G2 (defense in depth) · A1-equivalent (private SoT + upstream) · P1+P2 · W2

## 1. Goals

- Keep **AI-Knowledge-OS** fully reusable by anyone.
- Allow the maintainer (and any user) to run a **personal laboratory** that consumes the wiki.
- Make accidental publication of personal knowledge **hard**.
- Let generic improvements flow back to the public library through **sanitization**.

## 2. Repository roles

| Role | Repository | Visibility | Responsibility |
|------|------------|------------|----------------|
| **Upstream (library)** | `rapidinha/AI-Knowledge-OS` | Public | Canonical public wiki, governance, CI boundaries |
| **Contribution fork** | Personal GitHub fork of upstream | Public | Branches for PRs only — **no personal vault** |
| **Personal SoT (lab)** | Private repo with `upstream` = library | Private | Daily work, Obsidian vault at repo root, personal trees |

### Platform constraint (A1-equivalent)

GitHub **does not allow** a fork of a public repository to be private. Therefore the personal source of truth is a **private repository** that tracks upstream via remotes — not the GitHub “Fork” button. Colloquially this is still a “private fork”; technically it is an independent private clone with `upstream`.

```text
Personal use / lab (private SoT)
        ↓
Implement + validate (often editing wiki/ in the lab — W2)
        ↓
Generalize (strip personal dependence)
        ↓
feature/public/* on a clean worktree (P1+P2)
        ↓
PR → upstream
```

**Never:** personal note → commit → public tree.

## 3. Directory architecture

### 3.1 Public repository (allowed)

```text
AI-Knowledge-OS/
├── README.md                 # Constitution
├── GOVERNANCE.md             # This file
├── CONTRIBUTING.md
├── AGENTS.md
├── LICENSE
├── .github/                  # PR template, boundary CI
├── docs/                     # Specs/plans for this project
│   ├── specs/
│   └── plans/
└── wiki/                     # Public Obsidian vault root for contributors
    ├── index.md
    ├── MOC/
    ├── principles/
    ├── case-studies/
    └── _meta/
```

### 3.2 Paths that must never exist on upstream

These names are **forbidden** on the public repository (CI must fail if they appear):

| Path | Reason |
|------|--------|
| `knowledge/` | Personal knowledge domain |
| `notes/` | Personal notes |
| `research/` | Personal research corpus |
| `journals/` | Journals / diaries |
| `experiments/` | Personal experiments |
| `obsidian/` | Private vault config dumps |
| `vault/` | Alternate personal vault roots |

### 3.3 Personal SoT (private only)

Vault **physical root** = repository root (one Obsidian graph). **Logical domains:**

```text
(private SoT)/
├── wiki/                     # Lab copy of the public tree (W2)
├── knowledge/
│   ├── private/              # Never promote
│   ├── shared/               # Published elsewhere (blog/talk) — still not auto-upstream
│   └── imported/             # Clippings / external imports
├── notes/
├── research/
├── journals/
├── experiments/
├── docs/                     # May include private lab runbooks
└── …                         # Same public files as upstream when synced
```

| Domain | May open public PR? | Notes |
|--------|---------------------|-------|
| `wiki/**` after sanitization | Yes | Only via `feature/public/*` + clean worktree |
| `knowledge/private/**` | **No** | |
| `knowledge/shared/**` | **No** (not automatic) | May *inspire* a rewritten public note |
| `knowledge/imported/**` | **No** | |
| `notes/`, `research/`, `journals/`, `experiments/` | **No** | |

Cross-domain `[[wikilinks]]` are allowed **only** in the private SoT. Upstream `wiki/` must remain self-contained.

## 4. Classification decision tree

Before adding or promoting any file:

```text
Does this content require the author’s private biography,
unpublished research, career context, or private vault paths
to make sense?
        │
        ├─ YES → PRIVATE (knowledge/private, notes, research, …)
        │         Do not open a public PR.
        │
        └─ NO
            │
            Would any stranger reuse this without your
            personal context?
                │
                ├─ NO → PRIVATE (or rewrite until YES)
                │
                └─ YES
                    │
                    Is it a reusable principle/pattern/playbook
                    (no org leakage)?
                        │
                        ├─ YES → wiki/principles/ (or docs/ if about this repo)
                        │
                        └─ NO — is it evidence-backed case study
                            of a named system, still free of secrets?
                                │
                                ├─ YES → wiki/case-studies/<org>/
                                │
                                └─ NO → keep private or discard
```

**Default under uncertainty:** private.

### Promotion checklist (sanitization)

A change may enter a public PR only if **all** answers are **No**:

1. Does this change depend on a private document?
2. Was any passage copied or closely paraphrased from personal notes?
3. Do examples contain personal or employer-specific context that is not an intentional public case study?
4. Was any private path used as an authoritative reference without rewriting?
5. Is there information only the author possesses that a reader cannot verify or generalize?

If any answer is **Yes**, rewrite until all are **No**, or keep the change private.

## 5. Git conventions

### 5.1 Remotes (personal SoT)

| Remote | Points to | Push? |
|--------|-----------|-------|
| `origin` | Private SoT | Yes (daily) |
| `upstream` | `rapidinha/AI-Knowledge-OS` | **No** (fetch only) |

Contribution fork (public): used only from a **clean worktree** for `feature/public/*` PRs.

### 5.2 Branches (semantic)

| Pattern | Intent | May contain private paths? |
|---------|--------|----------------------------|
| `main` (private) | Lab default | Yes |
| `private/*`, `notes/*`, `research/*` | Personal evolution | Yes |
| `feature/private/*` | Personal features | Yes |
| `feature/public/*` | Upstream candidates | **No** |
| `sync/upstream-*` | Merge/rebase from upstream | Prefer no new private files in the sync commit itself |

### 5.3 Sync private ← upstream

1. `git fetch upstream`
2. Rebase or merge `upstream/main` into lab `main` (merge is fine when private history diverges heavily; rebase for linear public-candidate branches).
3. Resolve conflicts in `wiki/` carefully; never “resolve” by copying private notes into `wiki/`.

### 5.4 Contributing public changes (P1+P2)

1. Create a **clean worktree** from `upstream/main` (or contribution fork `main` tracking upstream) — no checkout of private-only paths.
2. Branch `feature/public/<topic>`.
3. Apply **only** sanitized commits (cherry-pick or manual re-apply).
4. Open PR to upstream.
5. Never `git push` directly to upstream `main`.

### 5.5 Commits

Before every commit destined for upstream:

- Does every file belong under allowed public paths?
- Would this make sense to a stranger?
- Any private path, Obsidian private metadata, or internal links?

## 6. Protection (G2)

| Layer | Mechanism |
|-------|-----------|
| Structure | Forbidden path names never created on upstream |
| CI | Fail if forbidden paths appear in the tree |
| PR template | Sanitization declaration required |
| Branch protection (upstream) | No direct push to `main`; PR required |
| Agents | [AGENTS.md](AGENTS.md) — doubt ⇒ private |
| Clean worktree | PRs never built from a dirty lab tree |

Note: forbidden paths are **not** listed in upstream `.gitignore`, so a private SoT that shares history can still version the personal vault. CI + clean worktrees enforce the boundary on public remotes.

Recommended upstream branch protection: require PR, require status checks (`boundary-check`), restrict who can push.

## 7. AI agent policy

See [AGENTS.md](AGENTS.md). Summary:

- **Public domain:** may edit `wiki/`, `docs/`, governance files; propose sanitized PRs.
- **Private domain:** may organize notes/research only inside the private SoT; **must not** suggest promoting those files upstream.
- Any answer that used private paths is **private output** — not a PR source.
- When classification is unclear → **assume private**.

## 8. Maintainer checklist

### Daily (lab)

- [ ] Work on private SoT `origin`
- [ ] Keep personal content under forbidden-on-public paths
- [ ] Sync from `upstream` periodically

### Before public PR

- [ ] Clean worktree from upstream
- [ ] Branch `feature/public/*`
- [ ] Sanitization checklist all **No**
- [ ] Diff contains only allowed paths
- [ ] `wiki/` links resolve without private targets
- [ ] PR template completed

### After merge

- [ ] Fetch upstream into private SoT
- [ ] Do not “fast-forward” private notes into public history

## 9. Alternatives considered

| Option | Why not chosen |
|--------|----------------|
| G1 convention-only | Too easy to leak with agents + multi-device |
| G3 max isolation | Extra ceremony; little gain over P1+P2 + CI |
| GitHub private fork of public repo | **Impossible** on GitHub |
| Submodule envelope (A2) | Stronger isolation; slower sync; rejected in favor of A1-equivalent |
| Private paths gitignored (P3) | Breaks GitHub-as-SoT / multi-device requirement |

## 10. Recommendations

1. Treat **private SoT + upstream fetch + clean worktree PRs** as the long-term operating model.
2. Keep `knowledge/{private,shared,imported}/` even if `shared/` is empty — explicit promotion later.
3. Invest in CI path denylist more than in clever Git topology.
4. Revisit G3 only if multiple humans write to the private SoT.
