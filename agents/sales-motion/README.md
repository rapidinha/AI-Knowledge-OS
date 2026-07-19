# Sales Motion

Portable skill pack for validation-first go-to-market: listen for public pain signals,
render an auditable market verdict, and only then draft brand-voiced content — never
auto-sent.

## Responsibility

Validate whether a market exists for a product/positioning before generating a single
character of marketing content. Sibling of `agents/trend-radar/`: Trend Radar finds
*trends*, Demand Radar (this pack's S2–S4) finds *pain/leads*.

## Emits

- **QualifiedSignal** — a Signal (from `providers/signals/`) plus pain-lexicon scores
  (intensity, workaround evidence, willingness-to-pay hint)
- **Beachhead** — a cluster of qualified signals with a composite score and evidence counts
- **Verdict** — Go / Watch / Pivot / No-Go, decided by a human in chat, with an audit trail
- **Lead** / **brand post drafts** — permission-first drafts, always human-approved before send

## Never does

- Auto-send a DM, email, or reply
- Auto-publish a brand post
- Scrape or automate against a platform's ToS (X intake is paste-only)
- Advance past the Go/No-Go gate without an explicit human answer
- Invent brand tone or palette — reads whatever your instance already defines

## Canonical skill

`agents/sales-motion/SKILL.md` is the source of truth.

## Sync after edits

Copy to IDE adapter paths so Cursor and Claude Code pick up changes:

```bash
cp agents/sales-motion/SKILL.md .cursor/skills/sales-motion/SKILL.md
cp agents/sales-motion/SKILL.md .claude/skills/sales-motion/SKILL.md
```

Commit all three copies together.

## Usage

Open the instance lab repo root, then ask: **"Run sales motion"**.

See `docs/sales/using-agents.md` for the full workflow.
