# Contract: Research Brief

**Purpose:** Focused exploration of a topic with sourced notes and open questions.

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| topic | string | Subject under investigation |
| questions | string[] | Questions to answer |
| sources[] | object[] | `{ url, title, excerpt? }` |
| notes | string | Working synthesis |
| open_questions | string[] | Unresolved items |

## Emitters

Research Agent.

## Consumers

Synthesis Agent, Knowledge Curator.
