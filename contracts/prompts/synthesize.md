# Stage: Synthesize

## Input

- **Top-k clusters only** from `journals/radar/_pipeline/YYYY-MM-DD/clusters.json` (≤ `max_opportunities`; avoid loading full raw signals if not needed)
- `journals/radar/topics.yaml` for recurrence and wikilinks
- `journals/radar/_pipeline/YYYY-MM-DD/run_meta.json` for degraded providers and counts

## Output

- Write `journals/radar/YYYY-MM-DD.md` from `templates/radar/daily.md`.

## Answer these leverage questions (not a news list)

- What changed today?
- What have few people noticed yet?
- What deserves attention?
- What looks like hype?
- What will likely keep growing?
- What may impact software engineers in the coming months?

## Required behaviors

- **Dual-write topics** per v2 rules: update `topics.yaml`, `topics/<slug>.md`, and `topics/_index.md`.
- Bias YouTube-heavy themes toward **Influence** (content leverage).
- Executive Summary must note **degraded providers** from `run_meta.providers_degraded` and counts from `run_meta.counts`.
- Cap ~200 topics; retire oldest low-hit — **do not delete** Markdown notes.

## Bans

- **No** headline dump or per-feed link lists as the primary structure.
- **No** GA4/GSC raw metrics in prose.
- **No** vendor LLM HTTP from repo tools; synthesis is session-only.
