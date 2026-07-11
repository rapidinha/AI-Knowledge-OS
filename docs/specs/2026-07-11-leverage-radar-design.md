# Design: Leverage Radar (AI Knowledge OS)

**Status:** Accepted for implementation  
**Date:** 2026-07-11  
**Repo roles:** Public library (`rapidinha/AI-Knowledge-OS`) + private personal SoT (lab)  
**Approach:** Skill-first vault protocol (Approach 1)

---

## 1. Goal

Help engineers answer **"What deserves my attention today?"** instead of **"What happened today?"**

Leverage Radar is a **Stage 1 discovery** capability: lightweight, ephemeral signal detection that recommends where to invest cognitive effort. Durable wiki knowledge is created only later, after explicit human approval (Stage 2).

### Success criteria

- Morning ritual: one Obsidian-readable daily report with clear Top Opportunities
- Human decides before any research work
- Quality over quantity (not an RSS/news feed)
- Git-native, human-curated; aligns with public/private governance
- Extensible providers and score dimensions without hardcoded ranking formulas
- Documented well enough that others can adopt the protocol and add adapters

### Non-goals (v1)

- Standalone `radar` CLI binary
- Always-on daemon / hosted service
- Autonomous deep research or automatic `wiki/` merges
- News aggregation / clickbait ranking
- X / TikTok / YouTube providers (deferred to v2)

---

## 2. Core philosophy — two stages

| Stage | Goal | Output | Durable? |
|-------|------|--------|----------|
| **1 — Discovery** | Detect leverage opportunities | Single daily Markdown report | No (ephemeral journal) |
| **2 — Research** | Turn approved trends into knowledge | Permanent wiki (later); **v1 = stub only** | Stub yes; wiki synthesis post-v1 |

**v1 Stage 2 depth:** queue-only research stubs under `research/radar/<slug>/` for token efficiency. No collect→draft→PR pipeline in v1.

---

## 3. Architecture

### 3.1 Product shape

**Vault-native protocol** driven entirely by an **agentic AI** (Claude Code **or** Cursor). No CLI outside the agent.

| Surface | Role |
|---------|------|
| Claude Code or Cursor | Fetch, cluster, score (LLM), write daily report, apply decisions, create research stubs, optional scheduled headless runs |
| Obsidian | Primary morning reading UX for `journals/radar/YYYY-MM-DD.md`; optional in-note decision edits |

Markdown files are the **source of truth**. The agent is the **only writer** of radar artifacts.

### 3.2 Data flow

```text
Providers (adapters)
    → journals/radar/_raw/YYYY-MM-DD.jsonl   (signal cache; prefer gitignore)
    → cheap URL/title dedupe
    → LLM: cluster → Opportunities + leverage category
    → LLM: extensible score map + rationale
    → journals/radar/YYYY-MM-DD.md           (Obsidian daily)
    → Human decision (in-note or via agent chat)
    → agent updates note + decisions.yaml
    → if research: research/radar/<slug>/README.md stub
```

Nothing enters durable `wiki/principles/` or public case studies from Stage 1.

### 3.3 Scheduling

- **Interactive:** user invokes the Leverage Radar skill in Claude Code or Cursor  
- **Headless:** same skill/contract runnable on a schedule (e.g. cron invoking the agent) so a report exists for morning Obsidian review  

Same protocol either way; no separate daemon product.

---

## 4. Data model & Obsidian UX

### 4.1 Paths (private lab)

| Path | Purpose |
|------|---------|
| `journals/radar/YYYY-MM-DD.md` | Daily Leverage Radar report (Obsidian) |
| `journals/radar/decisions.yaml` | Optional append-only decision log (agent-maintained) |
| `journals/radar/_raw/YYYY-MM-DD.jsonl` | Per-day signal cache |
| `journals/radar/config.yaml` | Private: weights, subs, keys, personal relevance (**never promote**) |
| `research/radar/<slug>/README.md` | Stage 2 research stub (v1) |

### 4.2 Entities

**Signal** — one provider item: `id`, `provider`, `url`, `title`, `ts`, `author?`, `text?`, `metrics{}`, `provenance`.

**Opportunity** — clustered trend: `slug`, `category`, `scores{}`, `sources[]`, `rationale`, `status`.

**Decision** — `ignore` | `watch` | `research` | `known` | `merge`.

### 4.3 Leverage categories

| Category | Question |
|----------|----------|
| **Knowledge** | Makes the engineer better? (papers, architectures, techniques) |
| **Influence** | Early content leverage? (emerging discussions, paradigm shifts) |
| **Opportunity** | Career/business leverage? (hiring, funding, platforms) |
| **Builder** | Can become a project? (APIs, SDKs, OSS, hackathons) |

### 4.4 Daily note shape (Obsidian-first)

Frontmatter example:

```yaml
date: 2026-07-11
status: open
generated_by: claude-code | cursor
providers: [hn, github-trending, arxiv, reddit]
signal_count: 84
opportunity_count: 7
```

Body sections:

1. **Executive Summary** (2–4 sentences)  
2. **Top Opportunities** (category + scores + Decide line)  
3. **Highest ROI** — Learning / Content / Project (one each)  
4. **Worth Watching**  
5. **Ignore**  
6. **Signals** (collapsed or linked to `_raw/`)  

Templates ship under `templates/radar/` for consistent Obsidian rendering.

---

## 5. Providers, clustering & scoring

### 5.1 Provider contract

Source-agnostic adapters:

```text
fetch(window) → Signal[]
```

New sources register by implementing the contract and listing themselves in skill/config docs—no core formula changes.

### 5.2 v1 reference adapters (public)

- Hacker News  
- GitHub Trending  
- arXiv  
- Reddit (selected subs; OAuth/secrets private)

### 5.3 v2 providers

- X  
- TikTok  
- YouTube  

### 5.4 Scoring

**LLM-assisted** (via Claude Code or Cursor — either agent using an LLM).

- Dimensions are an **extensible map**, not a hardcoded formula in core  
- Suggested defaults: `knowledge_gain`, `influence`, `market_opportunity`, `buildability`, `source_authority`, `signal_consensus`, `growth_velocity`, `novelty`, optional `personal_relevance`  
- Weights and personal relevance live only in private `config.yaml`  
- Cheap heuristics may pre-filter/dedupe; ranking and narrative remain LLM-produced  

---

## 6. Human-in-the-loop

Every opportunity requires an explicit decision before Stage 2 work.

| Action | Effect (v1) |
|--------|-------------|
| **Ignore** | Close; optionally suppress similar signals briefly |
| **Watch** | Keep on radar for N days |
| **Research** | Create `research/radar/<slug>/` stub with provenance + checklist |
| **Already known** | Link existing note if present |
| **Merge topic** | Attach to existing research/wiki topic (link only; no auto-edit of principles) |

Decisions may be written in the daily Markdown or requested in agent chat; the **agent applies** file updates.

**No autonomous research** without approval.

---

## 7. Documentation (required deliverable)

Documentation is part of the product, not an afterthought.

### Public docs to ship

| Doc | Content |
|-----|---------|
| This design spec | Architecture, data model, non-goals, roadmap |
| `docs/radar/protocol.md` | File layout, frontmatter, decision semantics |
| `docs/radar/obsidian.md` | How to read/edit the daily note in Obsidian |
| `docs/radar/providers.md` | Adapter contract + how to add a provider |
| `docs/radar/scoring.md` | Dimension map, extensibility, private weights |
| Skill README | How to run interactively and headless (Claude Code or Cursor) |

### Not published as product docs

- Personal weights, API keys, private schedules, org-specific subs  

---

## 8. OSS packaging

### Public upstream

```text
docs/specs/2026-07-11-leverage-radar-design.md
docs/radar/                      # protocol, Obsidian, providers, scoring guides
templates/radar/                 # daily note + research stub templates
skills/leverage-radar/           # agent skill (Claude Code or Cursor)
radar/providers/{hn,github,arxiv,reddit}/
templates/personal-lab/…         # pointers for journals/radar scaffold
```

### Private SoT only

- `journals/radar/config.yaml`  
- API keys, personal weights, live schedule, org-specific configuration  
- Live daily reports and research stubs (user content)

Governance: radar **protocol** may be promoted via sanitized `feature/public/*`; personal radar **content** never auto-upstreams.

---

## 9. Roadmap

| Version | Scope |
|---------|--------|
| **v1** | Vault protocol · agent skill · 4 adapters · Obsidian daily · HITL · research stubs · full docs |
| **v2** | X / TikTok / YouTube · richer watchlists · optional assisted research draft |
| **Later** | Knowledge-graph integration · org private radars · deeper Stage 2 (collect → draft → PR) |

---

## 10. Challenges to assumptions (accepted)

| Assumption challenged | Decision |
|----------------------|----------|
| Need a CLI for Git-native tools | Rejected for v1 — agent-only writers keep one SoT and Obsidian UX |
| Need a daemon for “continuous” radar | Rejected — scheduled headless agent runs are enough |
| Hardcoded score formula for consistency | Rejected — extensible dimension map + private weights |
| Full research pipeline in v1 | Rejected — stubs only (token efficiency) |
| Social video in v1 | Deferred to v2 |

---

## 11. Open implementation details (for the plan, not blockers)

These do not change the design; resolve during implementation planning:

- Exact skill packaging paths for Claude Code vs Cursor (may mirror or symlink)  
- Whether `_raw/` is gitignored by default in personal-lab template  
- Default Watch window (N days) and Ignore suppression window  
- Minimal fixture set for adapter tests without live network  

---

## 12. Approval record (brainstorm)

| Topic | Choice |
|-------|--------|
| Product shape | Vault-native |
| Ephemeral home | `journals/radar/` |
| Decisions UX | Markdown SoT; agent applies (no CLI) |
| Obsidian | Primary reading surface |
| Sources v1 | HN, GitHub Trending, arXiv, Reddit |
| Sources v2 | X, TikTok, YouTube |
| Scoring | LLM-assisted via Claude Code or Cursor |
| Runner | Interactive agent + schedulable headless |
| Public OSS | Templates + skill + reference adapters + docs |
| Stage 2 v1 | Research stub queue only |
| Architecture approach | Skill-first vault protocol |
