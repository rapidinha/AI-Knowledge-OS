# Contract: Decision Log

**Purpose:** Record of choices made and alternatives explicitly ignored.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| decision | string | What was chosen |
| ignored | string[] | Options passed over |
| rationale | string | Why |
| date | string | ISO-8601 |

## Emitters

Human or agent at decision points in the cycle.

## Consumers

Learning Agent, future Context assembly.

## Wiki touchpoints

- Writes to `wiki/decision-logs/`.
