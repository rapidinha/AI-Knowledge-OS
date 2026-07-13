# Scoring

Leverage Radar scoring is **LLM-assisted inside the agent session** — Cursor or Claude Code — not a hardcoded formula in this repository.

## Hard rule

**Never call OpenAI, Anthropic, or other vendor LLM HTTP APIs from this repo.** Do not add LLM SDKs (`openai`, `anthropic`, etc.). Clustering, dimension scores, and narrative rationale are produced by the **agent using its session model** while writing the daily note.

## Extensible dimensions

Scores are an **extensible map**, not a fixed weighted sum in core code. Suggested defaults (listed in `templates/radar/config.example.yaml` under `score_dimensions`):

| Dimension | What it captures |
|-----------|------------------|
| `knowledge_gain` | Will this make you a better engineer? |
| `influence` | Early content / thought-leadership leverage |
| `market_opportunity` | Career, business, or platform upside |
| `buildability` | Could this become a project or integration? |
| `source_authority` | Trustworthiness of originating sources |
| `signal_consensus` | Same story across multiple providers |
| `growth_velocity` | How fast interest is accelerating |
| `novelty` | Genuinely new vs. rehashed |
| `personal_relevance` | Optional; private only — enable in your lab config |

Add or rename dimensions in private `raw/ops/radar/config.yaml`. The agent reads `score_dimensions` and fills scores per opportunity in the daily note.

## Weights and personal relevance

Weights and `personal_relevance` live **only** in private `raw/ops/radar/config.yaml`. They are scoring hints for the agent, not executed Python. Never promote personal weights to the public repo.

## Pre-filtering (non-LLM)

Cheap heuristics run before the agent scores:

- URL canonicalization and dedupe (`radar/lib/dedupe.py`)
- Provider enablement from config
- Optional caps (`defaults.max_opportunities`)

Ranking, clustering, and prose remain agent-produced.

## How the agent scores (workflow)

1. Read `raw/ops/radar/_raw/YYYY-MM-DD.jsonl` and `raw/ops/radar/topics.yaml`.
2. Cluster related signals into ≤ `max_opportunities` opportunities.
3. Assign a leverage **category** (Knowledge, Influence, Opportunity, Builder).
4. For each opportunity, set dimension scores (e.g. 1–5 or low/medium/high — be consistent within the note).
5. Write rationale and populate `templates/radar/daily.md` placeholders.
6. Pick **Highest ROI** rows (Learning, Content, Project).
7. Populate **Worth Watching** and **Ignore** from lower-priority clusters.

## Recurrence (v2)

Each opportunity links to a durable topic in `raw/ops/radar/topics/<slug>.md`. The daily note shows recurrence inline:

```markdown
- **Recurrence:** hits 3 · first 2026-07-09 · providers hn, lobsters
```

Topic graph fields (in `topics.yaml` and topic notes):

| Field | Meaning |
|-------|---------|
| `hit_count` | Distinct days the topic appeared |
| `first_seen` | First day surfaced |
| `last_seen` | Most recent day |
| `provider_set` | Providers that contributed signals |
| `status` | `emerging`, `validated`, or `retired` |

**YouTube bias:** Themes with strong YouTube evidence should lean toward **Influence** (content leverage) when assigning category.

## Output format

In the daily note, scores appear inline per opportunity:

```markdown
- **Scores:** knowledge_gain: 4, influence: 3, buildability: 5, …
```

The agent may use a compact table or bullet list — consistency within a single daily note matters more than global formatting.

## Related

- [Protocol](protocol.md) — opportunity and decision model
- [Using agents](using-agents.md) — where scoring runs
