# Stage: Score (judgement layer)

## Input

- `journals/radar/_pipeline/YYYY-MM-DD/clusters.json` (deterministic scores already applied by Python)

## Output expectations

- Fill **judgement dimensions** on top of deterministic fields already present:
  - `novelty` — how new vs recurring in the ecosystem
  - hype vs substance — separate signal from durable leverage
  - Optional: `knowledge_gain`, `influence`, `market_opportunity`, `buildability`, `source_authority` per cluster
- Apply private `score_dimensions` and any weight hints from `journals/radar/config.yaml` as **guidance only** (not hard-coded in repo).
- **`personal_relevance` is boost-only** — may increase ranking weight but must not drive narrative.
- **Do not leak** GA4/GSC raw metrics, page paths, query strings, or traffic numbers into cluster prose or daily text.

## Caps

- Score only clusters present in `clusters.json`; do not invent new clusters here.

## Bans

- **No** vendor LLM HTTP from repo tools.
- **No** pasting personal analytics into promotable or OSS-bound text.
