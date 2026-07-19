# Leverage Radar protocol

Vault-native protocol for Stage 1 discovery. Markdown under `raw/ops/radar/` is the source of truth; agents are the only writers of radar artifacts.

## Paths (private lab)

| Path | Purpose |
|------|---------|
| `raw/ops/radar/YYYY-MM-DD.md` | Daily Leverage Radar report (Obsidian) |
| `raw/ops/radar/decisions.yaml` | Optional append-only decision log (agent-maintained) |
| `raw/ops/radar/_pipeline/YYYY-MM-DD/` | Pipeline artifacts: `signals.jsonl`, `enriched.jsonl`, `clusters.json`, `run_meta.json` (gitignored) |
| `raw/ops/radar/_raw/YYYY-MM-DD.jsonl` | Legacy per-day signal cache (mirrored from ingest; gitignored) |
| `raw/ops/radar/config.yaml` | Private weights, subs, keys, personal relevance (**never promote**) |
| `raw/ops/radar/topics.yaml` | Machine topic graph (gitignored) |
| `raw/ops/radar/topics/<slug>.md` | Obsidian topic notes + rolling summary (durable) |
| `raw/ops/radar/topics/_index.md` | Topic MOC |
| `raw/research/<slug>/README.md` | Stage 2 research stub (v1: queue only) |

Bootstrap: copy `templates/radar/config.example.yaml` → `raw/ops/radar/config.yaml`.

## Data flow

Python stages write auditable artifacts under `raw/ops/radar/_pipeline/YYYY-MM-DD/`. The agent runs stages via `providers/signals/pipeline/run_stages.py`, then performs cluster refinement, judgement scoring, and synthesis **inside the session** (no vendor LLM APIs from repo tools).

```text
Providers (adapters)
    → [ingest]  signals.jsonl + run_meta.json (+ legacy _raw/YYYY-MM-DD.jsonl)
    → [enrich]  enriched.jsonl (cheap Python + optional session refine per contracts/prompts/enrich.md)
    → [correlate] clusters.json (hint-cluster + deterministic score fields)
    → [session] semantic merge/refine → Opportunities + leverage category
    → [session] judgement scores (novelty, hype vs substance) on top of deterministic fields
    → [session] dual-write topic graph (topics.yaml + topics/<slug>.md + _index.md)
    → [session] raw/ops/radar/YYYY-MM-DD.md (contracts/prompts/synthesize.md)
    → Human decision (in-note or via agent chat)
    → agent updates note + decisions.yaml
    → if research: raw/research/<slug>/README.md stub
```

### Pipeline entrypoint

```bash
python providers/signals/pipeline/run_stages.py \
  --config raw/ops/radar/config.yaml \
  --radar-root raw/ops/radar \
  --date YYYY-MM-DD \
  --stage ingest|enrich|correlate|all
```

Stages `score` and `synthesize` are reserved hooks; v2 runs deterministic scoring inside `correlate` and leaves final synthesis to the agent session.

### Personal relevance (boost-only)

`personal_relevance` may come from GA4/Search Console token overlap in Python (`providers/signals/pipeline/score.py`) and from private config hints. It **boosts ranking only** — never drives narrative. The agent must **not** leak GA4/GSC raw metrics, page paths, or query strings into daily prose.

### Setup assist

When `run_meta.json` lists setup-related entries in `providers_degraded`, the agent follows `contracts/prompts/configure-provider.md`: one provider at a time, secrets via environment variables, dry-run `--stage ingest` with only that provider enabled. **Never commit** tokens, service-account JSON, or personal `config.yaml`.

**Topic memory dual-write (v2):** The agent writes both `raw/ops/radar/topics.yaml` (machine index, gitignored) and per-topic Markdown notes under `raw/ops/radar/topics/<slug>.md` (Obsidian-durable). Future AI summarization should prefer topic notes (`## Rolling summary`, `## Timeline`, `## Sources`) over `_raw/` history.

Nothing from Stage 1 enters durable `wiki/principles/` or public case studies.

## Entities

**Signal** — one provider item: `id`, `provider`, `url`, `title`, `ts`, `author?`, `text?`, `metrics{}`, `provenance`. See `providers/signals/schema/signal.schema.json`.

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
| **research** | Create `raw/research/<slug>/README.md` stub from `templates/radar/research-stub.md` |
| **known** | Link existing note if present |
| **merge** | Attach to existing research/wiki topic (wikilink only; no auto-edit of principles) |

Decisions may be written in the daily Markdown or requested in agent chat. The **agent applies** file updates and appends `decisions.yaml`.

**No autonomous research** without approval.

## Stage 2 (v1)

Research stubs only — queued under `raw/research/<slug>/` with provenance and a manual checklist. No collect→draft→PR pipeline in v1.

## Related docs

- [Obsidian morning UX](obsidian.md)
- [Providers](providers.md)
- [Scoring](scoring.md)
- [Using agents](using-agents.md)
- [Design spec](../superpowers/specs/2026-07-11-leverage-radar-design.md)
