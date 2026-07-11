# Contract: Knowledge Entry

**Purpose:** Wiki note metadata for durable, linkable knowledge.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| category | string | Wiki section (e.g. `principles`, `research`) |
| slug | string | Stable path key |
| when_to_use | string | Applicability guidance |
| links[] | string[] | Related wiki slugs |
| origin | string | Source synthesis or research brief id |

## Emitters

Knowledge Curator.

## Consumers

Context Agent, Insight Agent, Content Agent.

## Wiki touchpoints

Written to instance `wiki/`; public tree receives sanitized exports only.
