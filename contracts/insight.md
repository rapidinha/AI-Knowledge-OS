# Contract: Insight

**Purpose:** Actionable answer to a question, grounded in knowledge.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| question | string | What was asked |
| answer | string | Concise response |
| action | string | Recommended next step |
| based_on[] | string[] | Knowledge entry slugs or synthesis ids |

## Emitters

Insight Agent.

## Consumers

Content Agent, Project workflows, Decision Log.
