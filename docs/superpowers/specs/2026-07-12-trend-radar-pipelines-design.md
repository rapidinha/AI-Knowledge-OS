# Design: Trend Radar Pipelines (patch over Leverage Radar v2)

**Status:** Accepted for planning  
**Date:** 2026-07-12  
**Repo roles:** Public library (`providers/signals/`, `docs/`, skills, templates) + private lab SoT (`journals/radar/`)  
**Approach:** Pipeline contract + adapters + light Supervisor/Sub-Agents (Python-first hybrid)  
**Depends on:** [Leverage Radar v2](2026-07-11-leverage-radar-v2-design.md)  
**Naming:** Product/docs may say **Trend Radar**; existing paths and skill id `leverage-radar` remain compatible unless a follow-up rename is planned separately.

---

## 1. Goal

Evolve Leverage Radar from “fetch → agent cluster in one shot” into an **explicit, auditable pipeline** that:

1. Collects ecosystem signals from more sources.
2. Enriches and correlates them with cheap Python + specialized agent stages.
3. Produces a Daily Leverage / Trend Radar that answers leverage questions — not a news list.
4. Keeps the vault-native Obsidian Second Brain integration (Markdown, frontmatter, wikilinks).

Target questions for the daily output:

- What changed today?
- What have few people noticed yet?
- What deserves attention?
- What looks like hype?
- What will likely keep growing?
- What may impact software engineers in the coming months?

### Success criteria

1. A daily run writes `_pipeline/YYYY-MM-DD/{signals.jsonl,enriched.jsonl,clusters.json,run_meta.json}` plus the daily note and topic dual-write.
2. Stages are invocable in isolation (ingest / enrich / correlate+score / synthesize / export) or as a full run via the supervisor skill.
3. New providers (Product Hunt, RSS, YouTube Data API, GA4, Search Console) plug in via the adapter contract; GA4/GSC only boost `personal_relevance` and never leak raw personal metrics into OSS or public text.
4. The agent can guide incomplete provider setup end-to-end (credentials, config, dry-run validate).
5. Per-provider degrade does not abort the daily run.
6. No Dagster, no vendor LLM SDKs in-repo, no UI/email productization in this patch.

### Non-goals

- Dagster / Prefect / Temporal orchestration
- LangGraph (or equivalent) stateful supervisor
- Programmatic multi-model routing
- GraphRAG / Neo4j / LlamaIndex retrieval layer
- Newsletter/email notify (Akita-style delivery)
- UI / product chrome
- Autonomous Stage 2 research or `wiki/` edits
- Committing private trees (`journals/`, `knowledge/`, secrets) to public upstream

---

> **Implementation paths (Context Engine layout):** `providers/signals/pipeline/`, `providers/signals/sources/`, `tests/providers/signals/`. Skill: `agents/trend-radar/SKILL.md`.



## 2. Design principles

| Principle | Implication |
|-----------|-------------|
| Light & extensible | Small adapters + stage functions; no heavy orchestrator dependency |
| Python-first | Deterministic work in Python; LLM only for semantic merge, judgement, synthesis |
| Low cost / token-aware | Intermediate artifacts as external memory; each sub-agent sees only its stage input |
| High explainability | Scores, degrade reasons, and cluster membership are inspectable on disk |
| Auditable artifacts | Versioned schemas; JSON/JSONL machine path; optional Markdown for human audit |
| Obsidian Second Brain | Dual-write topic graph under `journals/radar/topics/`; daily note wikilinks |
| Private-safe OSS | Generic adapters may live in public `providers/signals/`; live config, tokens, and personal outputs stay in the lab |

Inspiration from editorial pipelines (e.g. curated multi-section digests): **structured stages and specialized commentary**, not list-of-links dumping — without adopting their delivery stack.

---

## 3. Architecture

### 3.1 Layers

```text
User / Skill (Supervisor)
        │
        ▼
┌───────────────────────────────┐
│ Supervisor (session LLM)      │  route stages, aggregate, HITL, setup assist
└───────────────┬───────────────┘
                │ tools + on-disk artifacts
     ┌──────────┼──────────┬───────────┬────────────┐
     ▼          ▼          ▼           ▼            ▼
  Ingest     Enrich    Correlate    Score      Synthesize
  (Python)   (Py+LLM)  (Py+LLM)     (Py+LLM)   (LLM)
     │          │          │           │            │
     ▼          ▼          ▼           ▼            ▼
 signals → enriched → clusters (+scores) → daily md + Obsidian export
```

**Dagster is out of scope entirely** (not optional).

### 3.2 Supervisor + sub-agents (light, optional specialization)

| Role | What it is in this patch | What it is not |
|------|--------------------------|----------------|
| **Supervisor** | Primary session agent running the Trend/Leverage Radar skill | Not a separate daemon or LangGraph app |
| **Sub-agent** | Stage-specific prompt + Python tools + minimal artifact input | Not a required multi-process fleet |
| **Execution layer** | Pure Python functions / CLI entrypoints under `providers/signals/` | Not vendor LLM HTTP from the repo |

Default UX: user asks to run today’s radar → supervisor runs full pipeline. Power users / agent may invoke a single stage.

Token optimizations required in this patch:

- Stage inputs capped (`max_signals_per_enrich_batch`, `max_clusters`, `max_opportunities`)
- Enrich cache keyed by `signal.id` / canonical URL
- History via existing `topics.yaml` + topic rolling summaries (no RAG stack)
- Host chooses models; docs may *suggest* smaller models for enrich/score, but the repo does not route models

Deferred: LangGraph checkpoints, multi-model routers, Graphify KG agent.

### 3.3 Data flow (lab paths)

```text
journals/radar/config.yaml
        │
        ▼
ingest (adapters)  →  _pipeline/YYYY-MM-DD/signals.jsonl
        │
        ▼
enrich             →  enriched.jsonl
        │
        ▼
correlate + score  →  clusters.json
        │
        ▼
synthesize         →  YYYY-MM-DD.md
        │
        ▼
obsidian export    →  topics.yaml + topics/<slug>.md + _index.md
        │
        ▼
run_meta.json (always written; includes degraded providers)
```

Legacy `_raw/YYYY-MM-DD.jsonl` may alias or be written as a copy of `signals.jsonl` for backward compatibility with v2 skill steps.

**Hard path rule:** run artifacts live under `journals/radar/` in the private lab. Do **not** use root `knowledge/` in the public repo (`AGENTS.md`).

---

## 4. Data contracts

Schemas are versioned (Pydantic in Python; mirror JSON Schema under `providers/signals/schema/` where useful).

### 4.1 `Signal` (existing, extended providers)

Required: `id`, `provider`, `url`, `title`, `ts`  
Optional: `author`, `text`, `metrics`, `provenance`

New `provider` values for this patch: `product_hunt`, `rss`, `youtube_api`, `ga4`, `search_console` (plus existing hn, github_trending, arxiv, reddit, lobsters, devto, youtube).

### 4.2 `EnrichedSignal`

`Signal` plus:

- `canonical_url`, `norm_title`
- `entities[]`, `topics_hint[]`
- `language?`
- `enrich_meta{}` (cache hit, version, timestamps)

Embeddings are **not** required in this patch.

### 4.3 `Cluster`

- `cluster_id`, `slug?`, `title`
- `signal_ids[]`, `providers[]`
- `scores{}` (extensible map; same spirit as v2 `score_dimensions`)
- `rationale_hint?`
- `weak_signal: bool`

### 4.4 `RunMeta`

- `date`, `schema_version`
- `providers_ok[]`, `providers_degraded[]`
- `counts` (signals, enriched, clusters, invalid)
- timings / notes for Executive Summary

Optional human-audit Markdown (e.g. enriched dump) is allowed; the machine path is JSON/JSONL.

---

## 5. Stage responsibilities

| Stage | Owner | Python responsibilities | LLM / sub-agent responsibilities |
|-------|-------|-------------------------|----------------------------------|
| **Ingest** | Adapters | Fetch, normalize to `Signal`, degrade | Almost none |
| **Enrich** | `enrich_*` helpers | Canonicalize, dedupe, heuristics (entities/topics from tags/titles) | Optional batch semantic enrich when heuristics insufficient |
| **Correlate** | cluster helpers | URL/domain/entity overlap; topic-graph hints | Semantic merge into ≤ `max_opportunities` themes |
| **Score** | score helpers | `signal_consensus`, recurrence, metric-based velocity when present | Light judgement (novelty, hype vs substance); apply weights from private config |
| **Synthesize** | — | Template fill helpers optional | Write daily note answering leverage questions; not a headline dump |
| **Obsidian export** | topics I/O (v2) | Dual-write YAML + Markdown + index | Prefer no extra LLM; rolling summary may reuse synthesize output |

### Personal signals (GA4, Search Console)

Choice locked: **boost only**.

- Contribute evidence used to adjust `personal_relevance` (and thus ranking).
- Daily narrative stays **ecosystem-centered**.
- Do not paste raw page paths, query strings, or traffic numbers into OSS docs or into notes intended for promotion.

---

## 6. Providers

### 6.1 Retained

Hacker News, GitHub Trending, arXiv, Reddit, Lobsters, DEV.to, YouTube channel RSS.

### 6.2 Added in this patch

| Provider | Auth | Config surface | Notes |
|----------|------|----------------|-------|
| Product Hunt | Token via env if required | `providers.product_hunt` | Launches / product momentum |
| RSS blogs | None | `providers.rss.feeds[]` in private config | Curated tech/engineering/AI blogs |
| YouTube Data API | `YOUTUBE_API_KEY` | search/channels beyond RSS; respect quotas | No transcripts in this patch |
| GA4 | OAuth / service account in lab | property ids in private config | Personal boost only |
| Search Console | OAuth in lab | site URL in private config | Personal boost only |

Adapter contract unchanged:

```text
fetch(**kwargs) -> list[Signal]
```

Register in `fetch_enabled.py`. Fixture tests; no live network in CI.

### 6.3 Agent-assisted provider setup

When the user asks to configure providers (or a run finds enabled-but-incomplete config), the supervisor skill:

1. Reads private `journals/radar/config.yaml` and reports enabled / missing / degraded.
2. Walks **one provider at a time**: required secrets, where to create them, env var names, safe config snippet.
3. Runs a **low-limit dry-run fetch** and reports ok vs degraded.
4. Never commits secrets; reminds that `config.yaml` and personal pipeline outputs are gitignored / lab-only.

Public support: extend `templates/radar/config.example.yaml` and `docs/radar/providers.md` with connect steps for each new source. Live credentials stay in the lab.

---

## 7. Error handling

| Failure | Behavior |
|---------|----------|
| Provider HTTP / auth / quota | Mark `degraded` in `run_meta`; continue |
| Invalid schema row | Drop/skip; increment `invalid_count` |
| Partial enrich/correlate | Persist partial artifact + flag; synthesize with available clusters |
| Missing secrets for enabled provider | Skip provider; surface setup-assist hint; do not fail entire daily |
| Corrupt/missing `topics.yaml` | Recreate empty topic index (v2 behavior); note in Executive Summary |

---

## 8. Testing

- Per-adapter fixture tests (monkeypatch HTTP).
- Pydantic (or schema) round-trips: Signal → EnrichedSignal → Cluster.
- Stage unit tests: fixture input → expected artifact shape for enrich/correlate cheap paths.
- Config gate test: enabled provider without credentials → degraded + setup hint (no live API).
- Smoke: render daily note from `clusters.json` fixture (extend existing smoke patterns).

---

## 9. Skill / docs updates

- Update `leverage-radar` skill (and mirrors) to orchestrate pipeline stages and setup assist; keep HITL Decide semantics from v2.
- Update `docs/radar/protocol.md`, `providers.md`, `scoring.md` for stages, artifacts, and new providers.
- Ban remains: **no** OpenAI/Anthropic SDKs or vendor LLM HTTP from this repository; session models do semantic work.
- No user-facing product CLI/daemon requirement; Python entrypoints remain agent-invoked tools.

---

## 10. Implementation shape (for planning)

Suggested public modules (names indicative):

```text
radar/
  providers/           # existing + product_hunt, rss, youtube_api, ga4, search_console
  pipeline/
    ingest.py
    enrich.py
    correlate.py
    score.py
    synthesize_io.py   # optional helpers; prose stays agent-owned
    run_meta.py
  schema/              # signal + enriched + cluster (+ pydantic if adopted)
  lib/                 # dedupe, topics_io, …
```

Skill prompts (or `contracts/prompts/` if added) for: enrich batch, correlate, score judgement, synthesize daily, configure provider.

OSS PR must not include live `journals/radar/**` personal data.

---

## 11. Roadmap after this patch (explicitly deferred)

1. LangGraph (or similar) optional stateful supervisor  
2. Multi-model routing  
3. GraphRAG / deeper KG queries  
4. Transcript / video-deep providers  
5. Newsletter-style notify  
6. Richer ecosystem memory (velocity/decay beyond current topic fields) — related to existing OSS issue themes  

---

## 12. Sanitization gate (public PR)

1. Does this change depend on a private document? **No** (design is generic).  
2. Inspired directly by personal notes? **No.**  
3. Non-case-study personal/employer examples? **No.**  
4. Private file used as reference for committed text? **No.**  
5. Claims knowable only to the author? **No.**

Private lab configs, GA4/GSC outputs, and API keys must never be committed upstream.
