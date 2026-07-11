# Design: Leverage Radar v2 (AI Knowledge OS)

**Status:** Accepted for planning  
**Date:** 2026-07-11  
**Repo roles:** Public library (`rapidinha/AI-Knowledge-OS`) + private personal SoT (lab)  
**Approach:** Skill-first vault protocol (same as v1) — Approach 1  
**Depends on:** [Leverage Radar v1](2026-07-11-leverage-radar-design.md)

---

## 0. Document shape

This spec has two layers:

1. **North star** — long-term vision (tracked as OSS GitHub issues; not all built in v2).
2. **v2 slice** — the next shippable increment designed in detail below.

---

## 1. North star (vision)

The Radar should become a **global signal intelligence layer** for software engineering.

Instead of asking “What is trending on Hacker News?”, it should answer:

> “What important movement is emerging across the software engineering ecosystem?”

Providers are evidence. The output is an **ecosystem-level observation**.

### Deferred themes (OSS issues)

| Theme | Intent | Issue |
|-------|--------|-------|
| Social / X | Weak early signals via social networks | [#6](https://github.com/rapidinha/AI-Knowledge-OS/issues/6) |
| IndieHackers (+ more communities) | Builder/pain-point communities beyond Lobsters/DEV | [#7](https://github.com/rapidinha/AI-Knowledge-OS/issues/7) |
| Video deep (transcripts) | Concept similarity across long-form video | [#8](https://github.com/rapidinha/AI-Knowledge-OS/issues/8) |
| Product / launches | Product Hunt, YC, funding momentum | [#9](https://github.com/rapidinha/AI-Knowledge-OS/issues/9) |
| Full signal lifecycle productization | Weak → Emerging → Validated → Research → Knowledge → History as first-class UX | [#10](https://github.com/rapidinha/AI-Knowledge-OS/issues/10) |
| Personalization layer | Optional ranking from projects/goals/wiki (OSS default stays generic) | [#11](https://github.com/rapidinha/AI-Knowledge-OS/issues/11) |
| Knowledge-gap auditor | Radar as wiki coverage auditor | [#12](https://github.com/rapidinha/AI-Knowledge-OS/issues/12) |
| Ecosystem memory beyond hit_count | Velocity, momentum, decay, maturity metrics | [#13](https://github.com/rapidinha/AI-Knowledge-OS/issues/13) |

v1 constraint remains: Radar **prioritizes**; research and wiki synthesis stay human-gated. Not an RSS reader.

---

## 2. v2 slice — goal

**Ship:** (1) lightweight **cross-day topic graph**, (2) **Dev communities** providers (**Lobsters** + **DEV.to**), (3) **YouTube light** (channel RSS only) for Influence/Content spice.

**Explicitly not in this slice:** X/Twitter fetch (too fragile for agent browse / ToS), transcript pipelines, daemon collectors, vendor LLM APIs, user-facing CLI.

### Success criteria

- After several daily runs, Opportunities can show **recurrence** (`hit_count`, `first_seen`, `provider_set`).
- When evidence exists, an Opportunity cites **≥2 providers** (e.g. HN + Lobsters, or GitHub + DEV + YouTube).
- Lobsters + DEV.to fetch via Python adapters with fixture tests (v1 style).
- YouTube opt-in via configured channel RSS; shallow Signals only (title, url, channel, published).
- Provider failure degrades; the rest of the run continues.
- OSS stays generic; personal channel lists and live `topics.yaml` stay private.

### Non-goals (v2 slice)

- Official X API or X WebFetch scraping
- TikTok / Twitch / global YouTube trending scrape
- Transcript download or speech/concept embedding
- IndieHackers (parked for follow-up issue)
- Deterministic ML topic model in Python (agent owns semantic merge)
- Always-on collector daemon
- Autonomous `wiki/` edits or knowledge-gap auditor

---

## 3. Architecture

### 3.1 Product shape

Unchanged from v1: **vault-native protocol** driven by Cursor or Claude Code. Markdown/YAML are SoT. Agent is the only writer of radar artifacts.

Python: stable HTTP fetchers + optional topics I/O helpers. **Clustering and topic merge semantics run in the session model only.**

### 3.2 Data flow

```text
config.yaml
  providers: … + lobsters + devto + youtube
  youtube.channels[] (RSS)
        │
        ▼
fetch_enabled.py
  ├─ v1 providers
  ├─ lobsters/fetch.py  → provider: lobsters
  ├─ devto/fetch.py     → provider: devto
  └─ youtube/fetch.py   → provider: youtube  (channel RSS only)
        │
        ▼
journals/radar/_raw/YYYY-MM-DD.jsonl
        │
        ▼
agent: load topics.yaml + today signals
  · cluster → Opportunities (multi-provider when graph agrees)
  · update topic nodes (aliases, hit_count, provider_set, last_seen, recent_urls)
  · YouTube-heavy themes bias Influence / Content in rationale
        ▼
journals/radar/YYYY-MM-DD.md  +  topics.yaml
        │
        ▼
HITL Decide (v1) → decisions.yaml / research stubs
```

Optional `youtube.search_queries`: best-effort **agent** browse only; not required in Python; failure is non-fatal.

### 3.3 Components

| Component | Role |
|-----------|------|
| Skill `leverage-radar` | Orchestrate fetch → cluster+graph → daily note |
| `lobsters` / `devto` adapters | Stdlib HTTP + parse; fixtures in CI |
| `youtube` adapter | `youtube.com/feeds/videos.xml?channel_id=…` |
| `topics.yaml` | Cross-day topic memory (private) |
| `topics.example.yaml` | Public empty template |
| Daily template | Recurrence line + multi-provider sources |
| `radar/lib/topics_io.py` (optional) | Load/save YAML only — no ML |

---

## 4. Topic graph

Path: `journals/radar/topics.yaml` (gitignore; never promote).

```yaml
version: 1
updated_at: 2026-07-11T12:00:00Z
topics:
  - slug: agent-skills-packaging
    title: Agent skills as packaging layer
    aliases: ["claude skills", "agent skills"]
    first_seen: 2026-07-11
    last_seen: 2026-07-11
    hit_count: 3
    provider_set: [hn, github_trending, lobsters]
    recent_urls: ["https://..."]
    status: emerging   # weak | emerging | validated | watching | retired
```

### Merge rules (skill-enforced)

1. Same-day: cluster signals into ≤ `defaults.max_opportunities` Opportunities; assign/create topic slugs.
2. Cross-day: overlap on alias/title/url with an existing topic → increment `hit_count` (per distinct day), union `provider_set`, refresh `recent_urls` (cap ~8).
3. Status hints in-session (e.g. `hit_count ≥ 3` and `≥ 2` providers → `validated`). Not a separate UI product.
4. Cap ~200 topics; mark oldest low-hit as `retired` when over cap.
5. Missing/corrupt file → recreate empty `topics: []` and note in Executive Summary.

---

## 5. Config (example additions)

```yaml
providers:
  lobsters:
    enabled: true
    tag: ""
    limit: 30

  devto:
    enabled: true
    tag: "ai"
    limit: 30

  youtube:
    enabled: false
    channels:
      - id: UCxxxx
        label: "Example Eng"
    search_queries: []
    max_videos_per_channel: 5
```

Personal channel IDs and tags stay in private `config.yaml`.

---

## 6. Signal & daily note

- Signal schema unchanged; new `provider` values: `lobsters`, `devto`, `youtube`.
- YouTube Signals are shallow: `id`, `provider`, `url`, `title`, `ts`, optional `author` (channel), optional `metrics`.
- Daily note frontmatter lists enabled providers that contributed.
- Per Opportunity: **Recurrence** from linked topic (`hit_count`, `first_seen`, `provider_set`).
- Scoring dimensions remain v1’s extensible map; YouTube evidence should bias **Influence** (and content leverage) in agent rationale — no mandatory new dimension in this slice.

---

## 7. Errors

- Any provider empty/error → count `0`, continue; summarize degraded providers.
- Invalid YouTube `channel_id` → skip channel; all channels fail → `youtube: degraded`.
- Do not abort the run for a single provider failure.

---

## 8. Testing & docs

- Fixture tests for Lobsters, DEV.to, YouTube RSS parsers (no live network in CI).
- `fetch_enabled` includes new providers when enabled.
- Optional round-trip test for `topics_io`.
- No CI assertion on clustering quality (session-only).
- Update `docs/radar/{protocol,providers,scoring,using-agents}.md` and sync all three skill trees.

---

## 9. Governance

| Artifact | Public OSS? |
|----------|-------------|
| Adapters, fixtures, docs, skills, `config.example.yaml`, `topics.example.yaml` | Yes |
| `journals/radar/topics.yaml`, live config, `_raw/` | No (gitignore) |

Promote via sanitized `feature/public/*` worktree per `GOVERNANCE.md`.

---

## 10. Implementation sketch (for planning — not a task list)

1. Gitignore `journals/radar/topics.yaml`; add `topics.example.yaml`.
2. Implement `lobsters` + `devto` + `youtube` fetchers + tests; wire `fetch_enabled`.
3. Extend config example + providers docs.
4. Extend skill: load/update topics; recurrence on daily note; degrade rules.
5. Bump `templates/radar/daily.md` with Recurrence field.
6. Manual E2E in private lab (multi-day smoke for graph).

---

## 11. Relationship to v1

v2 **extends** v1. All v1 bans remain: no vendor LLM HTTP APIs/SDKs from the repo, no user-facing `radar` CLI, no autonomous wiki merges from Stage 1.
