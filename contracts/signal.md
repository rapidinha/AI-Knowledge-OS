# Contract: Signal

**Purpose:** Typed raw event from the world (market, community, research feed).

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| id | string | Stable unique id |
| provider | string | Provider key |
| url | string | Canonical URL |
| title | string | |
| ts | string | ISO-8601 |

Optional: `author`, `text`, `metrics`, `provenance`.

## JSON schema (reference)

See `providers/signals/schema/signal.schema.json` after relocate.

## Emitters

Signal providers (e.g. Trend Radar sources).

## Consumers

Research Agent, Trend Radar clustering, Knowledge Curator (indirect).

## Wiki touchpoints

- Typically does not write wiki directly.
- May later inform `wiki/trend-analysis/` entries.
