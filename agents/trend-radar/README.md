# Trend Radar

Portable skill pack for daily signal discovery and attention scoring.

## Responsibility

Capture, cluster, and score signals; answer "what deserves attention today."

## Emits

- **Signal** — typed raw events from providers
- **Insight** (attention) — ranked opportunities with recurrence context

## Never does

- Decide career direction alone
- Flood the wiki without curation

## Canonical skill

`agents/trend-radar/SKILL.md` is the source of truth.

## Sync after edits

Copy to IDE adapter paths so Cursor and Claude Code pick up changes:

```bash
cp agents/trend-radar/SKILL.md .cursor/skills/trend-radar/SKILL.md
cp agents/trend-radar/SKILL.md .claude/skills/trend-radar/SKILL.md
```

Commit all three copies together.

## Usage

Open the instance lab repo root, then ask: **"Run today's Leverage Radar"** (or "daily radar", "what deserves attention today").

See `docs/radar/using-agents.md` for the full workflow.
