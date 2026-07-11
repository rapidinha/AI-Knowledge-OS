# Contract: Synthesis

**Purpose:** What changed and what matters — distilled claims with evidence and implications.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| claim | string | Core assertion |
| evidence[] | object[] | `{ source, excerpt }` |
| implications | string | Why it matters |
| confidence | string | `low` \| `medium` \| `high` |

## Emitters

Synthesis Agent.

## Consumers

Knowledge Curator, Insight Agent, Decision Log.

## Wiki touchpoints

- Often becomes `wiki/trend-analysis/` or `principles` drafts.
