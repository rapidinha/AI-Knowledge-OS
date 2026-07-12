# Scoring

Leverage Radar scoring is split: **deterministic Python fields** in `providers/signals/pipeline/score.py` (run during the `correlate` stage) plus **session judgement** in Cursor or Claude Code. There is no vendor LLM HTTP API in this repository.

## Hard rule

**Never call OpenAI, Anthropic, or other vendor LLM HTTP APIs from this repo.** Do not add LLM SDKs (`openai`, `anthropic`, etc.). Semantic clustering, judgement dimensions, and narrative rationale are produced by the **agent using its session model** while writing the daily note.

## Deterministic Python fields

Applied in `correlate` (and re-runnable via `--stage score`) to each cluster in `clusters.json`:

| Field | Source |
|-------|--------|
| `signal_consensus` | Count of distinct providers in the cluster |
| `growth_velocity` | Topic `hit_count` when title tokens overlap existing topics |
| `personal_relevance` | Token overlap with GA4/Search Console theme tokens from ingest (integer boost; 0 if no match) |

These are **hints**, not final rankings. The agent may reorder opportunities using session judgement.

## Session judgement (agent)

Follow `contracts/prompts/score.md` on top of `clusters.json`:

- `novelty` — genuinely new vs recurring ecosystem noise
- Hype vs substance — separate flash from durable leverage
- Optional fills for `knowledge_gain`, `influence`, `market_opportunity`, `buildability`, `source_authority` per cluster
- Private `score_dimensions` and weight hints from `journals/radar/config.yaml` — guidance only, not executed Python

### Personal relevance (boost-only)

`personal_relevance` from Python or config may **increase ranking weight only**. It must **not** drive narrative. The agent must **not** leak GA4/GSC raw metrics, page paths, query strings, or traffic numbers into cluster prose or the daily note.

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

Add or rename dimensions in private `journals/radar/config.yaml`. The agent reads `score_dimensions` and fills scores per opportunity in the daily note.

## Weights and personal relevance

Weights and `personal_relevance` live **only** in private `journals/radar/config.yaml`. They are scoring hints for the agent, not executed Python. Never promote personal weights to the public repo.

## Pre-filtering (non-LLM)

Cheap heuristics run before the agent scores:

- URL canonicalization and dedupe (`providers/signals/lib/dedupe.py`)
- Provider enablement from config
- Optional caps (`defaults.max_opportunities`)

Ranking, clustering, and prose remain agent-produced.

## How the agent scores (workflow)

1. Run pipeline stages through `correlate` (see `providers/signals/pipeline/run_stages.py`).
2. Read `journals/radar/_pipeline/YYYY-MM-DD/clusters.json`, `run_meta.json`, and `journals/radar/topics.yaml` — avoid full raw signals unless needed.
3. Session-refine clusters into ≤ `max_opportunities` opportunities (`contracts/prompts/correlate.md`).
4. Apply judgement dimensions on top of deterministic fields (`contracts/prompts/score.md`).
5. Assign a leverage **category** (Knowledge, Influence, Opportunity, Builder).
6. Write rationale and populate `templates/radar/daily.md` placeholders (`contracts/prompts/synthesize.md`).
7. Pick **Highest ROI** rows (Learning, Content, Project).
8. Populate **Worth Watching** and **Ignore** from lower-priority clusters.

## Recurrence (v2)

Each opportunity links to a durable topic in `journals/radar/topics/<slug>.md`. The daily note shows recurrence inline:

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
