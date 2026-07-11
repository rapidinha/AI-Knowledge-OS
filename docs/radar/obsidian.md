> **Note:** Leverage Radar is a **reference signal provider** for AI Knowledge OS, not the product identity. See [ARCHITECTURE.md](../../ARCHITECTURE.md).

# Obsidian morning UX

Obsidian is the primary reading surface for Leverage Radar. The agent writes; you read and decide.

## Morning ritual

1. Open your private lab vault in Obsidian.
2. Navigate to `journals/radar/YYYY-MM-DD.md` (today's date).
3. Read **Executive Summary** (2–4 sentences) for the day's leverage picture.
4. Scan **Top Opportunities** — each has topic wikilink, recurrence, category, scores, rationale, sources, and a **Decide** line.
5. Skim **Highest ROI** (Learning / Content / Project picks) and **Worth Watching**.
6. Ignore **Ignore** unless you want to sanity-check what was deprioritized.
7. Expand **Signals** only if you need raw provenance — link points to `_raw/YYYY-MM-DD.jsonl`.

Quality over quantity: this is not an RSS feed. Expect a small set of curated opportunities, not every headline.

## Making decisions

**In Obsidian (optional):** edit the **Decide** line on an opportunity:

```markdown
- **Decide:** `research`
```

Then ask your agent to apply decisions (e.g. "Apply my radar decisions for today").

**In agent chat (recommended):** say what you want:

- "Ignore opportunity #2"
- "Watch #4"
- "Research opportunity #1"
- "Already known — link to [[my-existing-note]]"
- "Merge #3 into [[research/some-topic]]"

The agent updates the daily note, appends `decisions.yaml`, and creates research stubs when you choose `research`.

## Note shape

Frontmatter tracks metadata for filtering and dashboards:

| Field | Meaning |
|-------|---------|
| `date` | Report date |
| `status` | `open` until you close the day |
| `generated_by` | `cursor` or `claude-code` |
| `providers` | Sources that contributed signals |
| `signal_count` | Raw signals after dedupe |
| `opportunity_count` | Clustered opportunities surfaced |

## Vault setup

1. Copy `templates/instance/` into your private instance if you have not already.
2. Ensure `journals/radar/` exists (see `templates/instance/journals/radar/README.md`).
3. Copy `templates/radar/config.example.yaml` → `journals/radar/config.yaml`.
4. Run the trend-radar skill in Cursor or Claude Code before your morning read.

`_raw/` signal caches are gitignored — they are ephemeral fetch output, not notes you curate.

## Topic memory (v2)

Durable theme notes live under `journals/radar/topics/`:

1. Open `journals/radar/topics/_index.md` for the MOC (active and retired topics).
2. Click a topic wikilink from the daily note or index to open `topics/<slug>.md`.
3. Read **Rolling summary** for the cumulative abstract; **Timeline** for day-by-day history with links back to daily notes.

Optional Dataview query for active topics:

```dataview
TABLE status, hit_count, last_seen FROM "journals/radar/topics" WHERE radar_topic = true SORT hit_count DESC
```

Topic Markdown notes are **not** gitignored — they are durable vault memory. `topics.yaml` (machine index) is gitignored.

## Wikilinks

Daily notes and research stubs use Obsidian-style links:

- `[[journals/radar/2026-07-11]]` — back to the originating daily
- `[[journals/radar/topics/agent-skills]]` — durable topic note with rolling summary
- `[[research/radar/some-slug]]` — research stub from a decision

Keep links relative to your vault root.

## Related

- [Protocol](protocol.md) — paths and decision semantics
- [Using agents](using-agents.md) — how reports get written
