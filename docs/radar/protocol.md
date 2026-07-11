> **Note:** Leverage Radar is a **reference signal provider** for AI Knowledge OS, not the product identity. See [ARCHITECTURE.md](../../ARCHITECTURE.md).

# Leverage Radar protocol

Vault-native protocol for Stage 1 discovery. Markdown under `journals/radar/` is the source of truth; agents are the only writers of radar artifacts.

## Paths (private lab)

| Path | Purpose |
|------|---------|
| `journals/radar/YYYY-MM-DD.md` | Daily Leverage Radar report (Obsidian) |
| `journals/radar/decisions.yaml` | Optional append-only decision log (agent-maintained) |
| `journals/radar/_raw/YYYY-MM-DD.jsonl` | Per-day signal cache (gitignored) |
| `journals/radar/config.yaml` | Private weights, subs, keys, personal relevance (**never promote**) |
| `journals/radar/topics.yaml` | Machine topic graph (gitignored) |
| `journals/radar/topics/<slug>.md` | Obsidian topic notes + rolling summary (durable) |
| `journals/radar/topics/_index.md` | Topic MOC |
| `research/radar/<slug>/README.md` | Stage 2 research stub (v1: queue only) |

Bootstrap: copy `templates/radar/config.example.yaml` → `journals/radar/config.yaml`.

## Data flow

```text
Providers (adapters)
    → journals/radar/_raw/YYYY-MM-DD.jsonl
    → cheap URL/title dedupe
    → agent: cluster → Opportunities + leverage category
    → agent: extensible score map + rationale
    → agent: dual-write topic graph (topics.yaml + topics/<slug>.md + _index.md)
    → journals/radar/YYYY-MM-DD.md
    → Human decision (in-note or via agent chat)
    → agent updates note + decisions.yaml
    → if research: research/radar/<slug>/README.md stub
```

**Topic memory dual-write (v2):** The agent writes both `journals/radar/topics.yaml` (machine index, gitignored) and per-topic Markdown notes under `journals/radar/topics/<slug>.md` (Obsidian-durable). Future AI summarization should prefer topic notes (`## Rolling summary`, `## Timeline`, `## Sources`) over `_raw/` history.

Nothing from Stage 1 enters durable `wiki/principles/` or public case studies.

## Entities

**Signal** — one provider item: `id`, `provider`, `url`, `title`, `ts`, `author?`, `text?`, `metrics{}`, `provenance`. See `radar/schema/signal.schema.json`.

**Opportunity** — clustered trend: `slug`, `category`, `scores{}`, `sources[]`, `rationale`, `status`.

**Decision** — one of: `ignore` | `watch` | `research` | `known` | `merge`.

## Leverage categories

| Category | Question |
|----------|----------|
| **Knowledge** | Makes the engineer better? (papers, architectures, techniques) |
| **Influence** | Early content leverage? (emerging discussions, paradigm shifts) |
| **Opportunity** | Career/business leverage? (hiring, funding, platforms) |
| **Builder** | Can become a project? (APIs, SDKs, OSS, hackathons) |

## Daily note frontmatter

```yaml
date: 2026-07-11
status: open
generated_by: claude-code | cursor
providers: [hn, github_trending, arxiv, reddit]
signal_count: 84
opportunity_count: 7
```

Body sections (required): Executive Summary, Top Opportunities, Highest ROI, Worth Watching, Ignore, Signals. Template: `templates/radar/daily.md`.

Each opportunity in Top Opportunities includes a **Decide** line:

```markdown
- **Decide:** `pending` <!-- agent sets: ignore | watch | research | known | merge -->
```

## Decisions

Every opportunity requires an explicit human decision before Stage 2 work.

| Action | Effect (v1) |
|--------|-------------|
| **ignore** | Close; optionally suppress similar signals briefly |
| **watch** | Keep on radar for N days (default from `defaults.watch_days`) |
| **research** | Create `research/radar/<slug>/README.md` stub from `templates/radar/research-stub.md` |
| **known** | Link existing note if present |
| **merge** | Attach to existing research/wiki topic (wikilink only; no auto-edit of principles) |

Decisions may be written in the daily Markdown or requested in agent chat. The **agent applies** file updates and appends `decisions.yaml`.

**No autonomous research** without approval.

## Stage 2 (v1)

Research stubs only — queued under `research/radar/<slug>/` with provenance and a manual checklist. No collect→draft→PR pipeline in v1.

## Related docs

- [Obsidian morning UX](obsidian.md)
- [Providers](providers.md)
- [Scoring](scoring.md)
- [Using agents](using-agents.md)
- [Design spec](../specs/2026-07-11-leverage-radar-design.md)
