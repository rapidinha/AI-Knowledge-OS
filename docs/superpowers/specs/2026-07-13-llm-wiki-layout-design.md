# Design: LLM Wiki layout (raw → wiki) + pilot consolidate

**Status:** Accepted for planning  
**Date:** 2026-07-13  
**Repo roles:** Private personal SoT (lab) primary; public library remains dual-tree constrained  
**Approach:** Karpathy-style `raw/` + `wiki/` with explicit Ingest → Research → Consolidate (Approach 1)  
**Pilot:** `ai-advantage-expired`  
**Related:** [LAB.md](../../../LAB.md) · [AGENTS.md](../../../AGENTS.md) · [AGENTS.private.md](../../../AGENTS.private.md) · career-beginning-tech pipeline · Leverage Radar path under ops

---

## 1. Problem

The private laboratory mixes several knowledge trees at the repository root (`knowledge/`, `research/`, `journals/`, `notes/`, `experiments/`) plus the engineering `wiki/`. Agents and humans struggle to answer: *where does a source live, where does synthesis live, and what is safe to promote?*

The lab already has one good exemplar (`career-beginning-tech`: ingest → research → consolidate) and a fresh topic (`ai-advantage-expired`) that still lives under `research/radar/` without wiki consolidation.

We need a single, navigable LLM-wiki layout so:

1. Sources are immutable and easy to find.
2. The wiki is the compiled, compounding knowledge graph.
3. Ops (daily, radar, posts) do not compete with domain knowledge paths.
4. Dual-tree promotion rules stay enforceable.

---

## 2. Goals and non-goals

### Goals

- Adopt Karpathy LLM Wiki layers: **raw sources** (human-curated) + **wiki** (LLM-maintained) + **schema** (agent rules).
- Name the compile pipeline explicitly: **Ingest → Research → Consolidate**, plus **Query** and **Lint**.
- Migrate existing personal trees into `raw/`; keep compile in `wiki/`.
- Pilot by consolidating `ai-advantage-expired` into wiki concepts + one sanitized principle.
- Update schema docs and radar path references to the new ops location.

### Non-goals

- Rewriting existing named case-study principles or evidence.
- Opening an upstream public PR in this change set (structure + local pilot only).
- Building a new Python ingest pipeline beyond path fixes for Leverage Radar.
- HTML/visual companions or Obsidian plugin work.

---

## 3. Decisions (locked in brainstorming)

| Decision | Choice |
|----------|--------|
| Scope | Full lab reorg + `ai-advantage-expired` as proving pilot |
| Compiled layer location | Existing `wiki/` tree (concepts + principles + MOCs) |
| Folder migration | Move all personal knowledge/ops roots; deprecate with stubs |
| Root shape | Karpathy: `raw/` + `wiki/` + schema |
| Approach | Approach 1 — `raw/sources`, `raw/research`, `raw/ops` |

---

## 4. Architecture

### 4.1 Root layout (after migration)

```text
raw/
  sources/<slug>/          # Ingest — immutable primary sources
  research/<slug>/         # Research — secondary surveys (not yet wiki truth)
  ops/
    daily/                 # was journals/daily
    posts/                 # was journals/post-ideas
    radar/                 # was journals/radar (_raw, topics, config, decisions)
    experiments/           # was experiments/
wiki/
  index.md                 # LLM catalog (Karpathy index)
  log.md                   # ingest / consolidate / query / lint timeline
  concepts/                # concept pages (LLM-owned synthesis)
  entities/                # optional entity pages
  principles/              # generic, promotable patterns (existing)
  MOC/                     # maps of content (existing)
  case-studies/            # named evidence (existing; promote only sanitized)
  _meta/                   # templates, coverage, extraction ledger
docs/                      # repo design specs/plans (not domain knowledge)
radar/                     # Leverage Radar Python engine (code, not knowledge)
```

### 4.2 Layer rules

| Layer | Who writes | Mutability | Promote to upstream? |
|-------|------------|------------|----------------------|
| `raw/sources/` | Human (+ agent structured extraction) | Append-only preferred; never “improve” history in place | No |
| `raw/research/` | Agent + human | Editable drafts | No |
| `raw/ops/` | Agent + human | Operational | No |
| `wiki/` | Agent maintains; human steers | Compiled, may rewrite | Only `principles/` + intentional case studies after sanitization |
| `docs/`, `radar/` | Engineers | Repo product | Yes (public library code/docs) |

### 4.3 Operations

| Operation | Input | Output |
|-----------|-------|--------|
| **Ingest** | New file(s) under `raw/sources/<slug>/` | Concept/entity updates; `wiki/index.md`; append `wiki/log.md` |
| **Research** | Question / Decide=research / deep dive | Artifacts under `raw/research/<slug>/` |
| **Consolidate** | Mature ingest + research | Stable `wiki/concepts/*`; optional `wiki/principles/<slug>.md`; MOC links; log entry |
| **Query** | Chat question | Answer from wiki; optional file-back as new concept page |
| **Lint** | Periodic | Fix orphans/contradictions/gaps; suggest sources |

**Boundary:** Research is not wiki truth. Consolidate is the gate that promotes synthesis into `wiki/`.

---

## 5. Schema (agent discipline)

Update private lab schema surfaces:

- `LAB.md` — domains table points at `raw/` + `wiki/`; remove obsolete root domains.
- `AGENTS.private.md` — workflows ingest/research/consolidate/query/lint; private path list becomes `raw/**`.
- `templates/personal-lab/` — mirror the new layout for future clones.
- `wiki/_meta/templates.md` — add **concept** and **entity** templates; keep principle/case-study templates.
- `wiki/_meta/llm-wiki-schema.md` — short ops contract (ingest/research/consolidate/query/lint + index/log rules).

### 5.1 Frontmatter (wiki pages created by this system)

```yaml
type: concept | entity | principle | moc | case-study
status: draft | active | deprecated
sources: []          # paths or URLs under raw/ or external
private: false       # true = lab-only concept; never promote
```

Principles keep existing dual-tree hard rules (no company/product leakage).

### 5.2 `wiki/index.md` and `wiki/log.md`

- `index.md` — catalog of concepts, principles, entities, MOCs (machine + human navigable).
- `log.md` — append-only timeline: date, op, slug, pages touched, one-line note.

---

## 6. Migration map

| Current path | Target path |
|--------------|-------------|
| `knowledge/private/<topic>/ingest/` | `raw/sources/<topic>/` |
| `knowledge/private/<topic>/consolidate/` | Refile into `wiki/concepts/` or archive under `raw/research/<topic>/_archive/` |
| `knowledge/private/<topic>/patterns/` | `raw/research/<topic>/patterns/` |
| `knowledge/private/sources/` | `raw/sources/_archives/` |
| `knowledge/shared/` | `raw/sources/shared/` |
| `knowledge/imported/` | `raw/sources/imported/` |
| `research/<topic>/` | `raw/research/<topic>/` |
| `journals/daily/` | `raw/ops/daily/` |
| `journals/post-ideas/` | `raw/ops/posts/` |
| `journals/radar/` | `raw/ops/radar/` |
| `journals/*.md` (week notes) | `raw/ops/daily/` or `raw/ops/posts/` as appropriate |
| `experiments/` | `raw/ops/experiments/` |
| `notes/` | `raw/sources/notes/` if non-empty; else remove |

### 6.1 Deprecation

For each old root, leave a short `README.md` stub: “Moved to `<new path>`.” Keep stubs until internal wikilinks and skills are updated; then delete empty roots.

### 6.2 Path updates required

- Leverage Radar skill + `docs/radar/*` references: `journals/radar` → `raw/ops/radar`
- Any config defaults that hardcode `journals/radar`
- `research/README.md`, `knowledge/README.md` → stubs or redirects
- Cross-links inside career-beginning-tech and radar topic notes

---

## 7. Pilot: `ai-advantage-expired`

### 7.1 Move

| From | To |
|------|----|
| `research/radar/ai-advantage-expired/ingest/` | `raw/sources/ai-advantage-expired/` |
| `research/radar/ai-advantage-expired/` (research + guides) | `raw/research/ai-advantage-expired/` |
| Radar topic note | `raw/ops/radar/topics/ai-advantage-expired.md` (path after ops move) |

### 7.2 Consolidate into wiki

| Page | Role |
|------|------|
| `wiki/concepts/post-ai-competitive-advantage.md` | Consensus map + thesis + bias warnings |
| `wiki/concepts/career-advantage-ladder.md` | Previous / current / emerging advantage narrative |
| `wiki/principles/judgment-over-generation.md` | Sanitized reusable principle (no X handles, no private biography) |
| MOC link | `wiki/MOC/engineering-practice.md` and/or new `wiki/MOC/career-leverage.md` if a dedicated map is cleaner |

### 7.3 Explicitly not principles

- Nominal X quotes / author tables → stay in `raw/sources/`
- Junior-anxiety speaking guides with personal tone → `raw/research/.../guides/` until generalized
- Content pipeline drafts → `raw/ops/posts/` when turned into post ideas

### 7.4 Log + index

Append consolidate entry to `wiki/log.md`; register new pages in `wiki/index.md`.

---

## 8. Dual-tree and sanitization

Unchanged golden rule: when unsure, treat as private; do not open a public PR.

Promotion gate (existing AGENTS checklist) still applies. This design **does not** auto-promote. After the pilot principle exists locally, a separate human Decide may open `feature/public/*` with sanitization rewrite.

`raw/**` must remain blocked from upstream contribution trees (same intent as today’s `knowledge/`, `journals/`, etc.). Update CI/agent deny-lists from old root names to `raw/` when those checks exist.

---

## 9. Testing / verification

| Check | How |
|-------|-----|
| Layout smoke | Root shows `raw/`, `wiki/`, `docs/`, `radar/`; old roots are stubs or gone |
| Link smoke | Grep for `journals/radar`, `knowledge/private`, `research/radar` — zero live references (except historical stubs/docs that point to migration) |
| Pilot smoke | Three wiki pages exist; log + index mention slug; raw sources/research present |
| Radar smoke | Skill docs path updated; config still loads from `raw/ops/radar/config.yaml` |
| Dual-tree smoke | Principle `judgment-over-generation` has zero company/personal leakage |

No new automated test suite required for markdown moves beyond existing radar unit tests if import paths change (they should not — Python package stays `radar/`).

---

## 10. Implementation sequence (for writing-plans)

1. Scaffold `raw/{sources,research,ops}` and `wiki/{concepts,entities,log.md}`; enrich `wiki/index.md`.
2. Migrate ops (`journals` → `raw/ops`) and update radar skill/docs paths.
3. Migrate knowledge + research trees into `raw/sources` and `raw/research`.
4. Stub/deprecate old roots; update LAB + AGENTS.private + personal-lab templates.
5. Add concept/entity templates under `wiki/_meta/`.
6. Pilot consolidate `ai-advantage-expired` (move + wiki pages + log/index).
7. Lint pass: fix broken wikilinks; grep for stale paths.
8. Stop — no upstream PR unless separately requested.

---

## 11. Risks

| Risk | Mitigation |
|------|------------|
| Broken Obsidian links after moves | Systematic grep + stub READMEs; update high-traffic notes first |
| Radar skill still points at old paths | Treat path update as blocking for step 2 |
| Mixing private concepts into principles | Frontmatter `private: true` + consolidate checklist |
| Scope creep into named case-study rewrite | Explicit non-goal |
| Public CI still only blocks old folder names | Update deny-list to include `raw/` for contribution forks |

---

## 12. Done criteria

1. Root is navigable as `raw/` + `wiki/` + `docs/` + `radar/` (code).
2. `ai-advantage-expired` exists in raw sources/research and as wiki concepts + sanitized principle.
3. `wiki/index.md` and `wiki/log.md` are live and updated by the pilot.
4. Schema docs describe the five operations.
5. Old roots are stubs or removed; stale path grep is clean for active docs/skills.

---

## 13. Open items (resolved or deferred)

| Item | Resolution |
|------|------------|
| Visual companion | Declined (text-only) |
| Upstream PR for principle | Deferred — separate Decide |
| Whether `career-leverage` MOC is required | Prefer link from `engineering-practice` first; add MOC only if index clutter demands it |
