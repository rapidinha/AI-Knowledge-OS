# Governance — Context Engine framework vs private instance

**Status:** Active  
**Date:** 2026-07-11  
**Model:** G2 (defense in depth) · A1-equivalent (private SoT + upstream) · P1+P2

## 1. Goals

- Keep **AI Knowledge OS** a reusable **Protocol Kernel** anyone can instantiate.
- Allow each user to run a **private instance** with a living Knowledge Base.
- Make accidental publication of personal knowledge **hard**.
- Let generic framework improvements flow upstream through **sanitization**.

## 2. Repository roles

| Role | Repository | Visibility | Responsibility |
|------|------------|------------|----------------|
| **Upstream (framework)** | `rapidinha/AI-Knowledge-OS` | Public | Contracts, engine, agents, providers, wiki scaffold, governance, CI |
| **Contribution fork** | Personal GitHub fork of upstream | Public | Branches for PRs only — **no personal vault** |
| **Private instance (SoT)** | Private repo with `upstream` = framework | Private | Daily work, living `wiki/`, personal trees |

### Platform constraint (A1-equivalent)

GitHub **does not allow** a fork of a public repository to be private. The personal source of truth is a **private repository** that tracks upstream via remotes — not the GitHub "Fork" button.

```text
Private instance (SoT)
        ↓
Run cycle + evolve wiki/ and personal trees
        ↓
Generalize (strip personal dependence)
        ↓
feature/public/* on a clean worktree (P1+P2)
        ↓
PR → upstream (framework only, by default)
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
├── VISION.md
├── MISSION.md
├── ARCHITECTURE.md
├── LICENSE
├── .github/                  # PR template, boundary CI
├── contracts/                # Artifact schemas
├── engine/                   # Cycle protocol + invariants
├── agents/                   # Skill packs
├── providers/                # Reference providers
├── docs/                     # Institutional + feature docs
├── templates/
│   └── instance/             # Private instance scaffold (copy into private repo)
└── wiki/                     # Knowledge Base scaffold only (not living notes)
    ├── index.md
    └── _meta/
```

### 3.2 Paths that must never exist at upstream **root**

These names are **forbidden at the repository root** on the public repository (CI must fail if they appear there):

| Path | Reason |
|------|--------|
| `knowledge/` | Personal knowledge domain |
| `notes/` | Personal notes |
| `journals/` | Journals / diaries |
| `experiments/` | Personal experiments |
| `obsidian/` | Private vault config dumps |
| `vault/` | Alternate personal vault roots |

**Exception — `research/`:** allowed **only** as scaffold (`README.md`, `.gitkeep`). No personal research corpus at upstream root.

**Allowed on upstream:** the same structure as a **template** under [`templates/instance/`](templates/instance/) (structure and empty READMEs only — no personal content). Copy that template into a private repo root.

> **Note:** Until the directory rename lands, the template may still appear as `templates/personal-lab/` locally; treat it as `templates/instance/`.

### 3.3 Private instance (SoT)

Vault **physical root** = repository root. **Logical domains:**

```text
(private instance)/
├── wiki/                     # Living Knowledge Base (canonical long-term memory)
├── knowledge/
│   ├── private/              # Never promote
│   ├── shared/               # Published elsewhere — still not auto-upstream
│   └── imported/             # Clippings / external imports
├── notes/
├── research/
├── journals/
├── experiments/
├── docs/                     # May include private runbooks
└── …                         # Same framework files as upstream when synced
```

| Domain | May open public PR? | Notes |
|--------|---------------------|-------|
| Framework paths after sanitization | Yes | `contracts/`, `engine/`, `agents/`, `providers/`, `docs/`, wiki scaffold |
| `wiki/**` (living notes) | **No** (by default) | Instance wiki is sovereign; see §4 |
| `knowledge/private/**` | **No** | |
| `knowledge/shared/**` | **No** (not automatic) | May *inspire* a rewritten public doc |
| `knowledge/imported/**` | **No** | |
| `notes/`, `research/`, `journals/`, `experiments/` | **No** | |

Cross-domain links are allowed **only** in the private instance. Upstream `wiki/` scaffold must remain self-contained.

## 4. Instance wiki preservation

The instance `wiki/` is the canonical long-term Knowledge Base.  
Upstream sync must never replace living instance notes with empty scaffold files.  
Use `templates/instance/scripts/sync-from-upstream.sh`.

**Wiki merge policy:** **instance wiki wins.** Upstream may add new scaffold files; it must not overwrite instance content with empty templates.

## 5. Promotion policy

**Default:** upstream PRs carry **framework** changes only:

- `contracts/`, `engine/`, `agents/`, `providers/`
- `docs/`, governance files
- `wiki/` **scaffold** updates (templates, structure — not personal notes)

Living instance principles, case studies, journals, and personal research do **not** belong upstream unless fully sanitized into generic framework documentation — and even then, prefer keeping knowledge in the instance.

## 6. Classification decision tree

Before adding or promoting any file:

```text
Does this content require the author's private biography,
unpublished research, career context, or private vault paths
to make sense?
        │
        ├─ YES → PRIVATE (knowledge/private, notes, research, …)
        │         Do not open a public PR.
        │
        └─ NO
            │
            Is this a framework artifact (contract, engine rule,
            agent pack, provider, doc, wiki scaffold)?
                │
                ├─ YES → allowed public path (after sanitization)
                │
                └─ NO → keep in private instance
```

**Default under uncertainty:** private.

### Sanitization checklist

A change may enter a public PR only if **all** answers are **No**:

1. Does this change depend on a private document?
2. Was any passage copied or closely paraphrased from personal notes?
3. Do examples contain personal or employer-specific context?
4. Was any private path used as an authoritative reference without rewriting?
5. Is there information only the author possesses that a reader cannot verify or generalize?

If any answer is **Yes**, rewrite until all are **No**, or keep the change private.

## 7. Git conventions

### 7.1 Remotes (private instance)

| Remote | Points to | Push? |
|--------|-----------|-------|
| `origin` | Private instance | Yes (daily) |
| `upstream` | `rapidinha/AI-Knowledge-OS` | **No** (fetch only) |

Contribution fork (public): used only from a **clean worktree** for `feature/public/*` PRs.

### 7.2 Branches

| Pattern | Intent | May contain private paths? |
|---------|--------|----------------------------|
| `main` (private) | Instance default | Yes |
| `private/*`, `notes/*`, `research/*` | Personal evolution | Yes |
| `feature/private/*` | Personal features | Yes |
| `feature/public/*` | Upstream candidates | **No** |
| `sync/upstream-*` | Merge/rebase from upstream | Prefer no new private files in the sync commit itself |

### 7.3 Sync instance ← upstream

1. `git fetch upstream`
2. Rebase or merge `upstream/main` into instance `main`.
3. Run `templates/instance/scripts/sync-from-upstream.sh` for wiki scaffold merges.
4. Resolve conflicts with **instance wiki wins** — never copy private notes into upstream-bound commits.

### 7.4 Contributing framework changes (P1+P2)

1. Create a **clean worktree** from `upstream/main` — no checkout of private-only paths.
2. Branch `feature/public/<topic>`.
3. Apply **only** sanitized commits (cherry-pick or manual re-apply).
4. Open PR to upstream.
5. Never `git push` directly to upstream `main`.

## 8. Protection (G2)

| Layer | Mechanism |
|-------|-----------|
| Structure | Forbidden path names never created on upstream |
| CI | Fail if forbidden paths appear in the tree |
| PR template | Sanitization declaration required |
| Branch protection (upstream) | No direct push to `main`; PR required |
| Agents | [AGENTS.md](AGENTS.md) — doubt ⇒ private |
| Clean worktree | PRs never built from a dirty instance tree |

Forbidden paths are **not** listed in upstream `.gitignore`, so a private instance that shares history can still version personal trees. CI + clean worktrees enforce the boundary on public remotes.

## 9. AI agent policy

See [AGENTS.md](AGENTS.md). Summary:

- **Public domain:** may edit framework paths, wiki scaffold, docs; propose sanitized PRs.
- **Private domain:** may organize notes/research only inside the private instance; **must not** suggest promoting those files upstream.
- Any output that used private paths is **private output** — not a PR source.
- When classification is unclear → **assume private**.

## 10. Maintainer checklist

### Daily (instance)

- [ ] Work on private instance `origin`
- [ ] Keep personal content under forbidden-on-public paths
- [ ] Sync from `upstream` periodically (instance wiki wins)

### Before public PR

- [ ] Clean worktree from upstream
- [ ] Branch `feature/public/*`
- [ ] Sanitization checklist all **No**
- [ ] Diff contains only allowed framework paths
- [ ] PR template completed

### After merge

- [ ] Fetch upstream into private instance
- [ ] Do not fast-forward private notes into public history
