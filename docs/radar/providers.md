> **Note:** Leverage Radar is a **reference signal provider** for AI Knowledge OS, not the product identity. See [ARCHITECTURE.md](../../ARCHITECTURE.md).

# Providers

Source-agnostic adapters fetch raw signals for the agent to cluster and score. Provider scripts are **agent-invoked tools**, not a user-facing CLI.

## Connect a source in 60 seconds

1. Copy `templates/radar/config.example.yaml` → `journals/radar/config.yaml` (private, gitignored).
2. Set `providers.<name>.enabled: true` for each source you want.
3. If using Reddit: set `user_agent` and `subreddits` in config (PyYAML recommended). v1 uses public JSON only — no OAuth.
4. Ask the agent: **"Run today's Leverage Radar"**.

That is the entire connect flow — no daemon, no product CLI, no API keys in the public repo.

### PyYAML (recommended)

`radar/lib/io.py` includes a minimal YAML fallback, but **PyYAML is recommended** in your private lab for full nested config (categories, subreddits, weights). Install once:

```bash
pip install pyyaml
```

Without PyYAML, only top-level `providers.<id>.enabled` flags are parsed reliably.

## v1 reference providers

| ID | Config key | Notes |
|----|------------|-------|
| Hacker News | `hn` | No secrets |
| GitHub Trending | `github_trending` | `since`: daily \| weekly \| monthly |
| arXiv | `arxiv` | `categories`, `max_results` |
| Reddit | `reddit` | `subreddits`, `user_agent` (public JSON; OAuth is future) |
| Lobsters | `lobsters` | `tag` (optional filter), `limit` — no secrets |
| DEV.to | `devto` | `tag` (e.g. `ai`), `limit` — no secrets |
| YouTube (light) | `youtube` | Channel RSS only (`channels[].id`, `max_videos_per_channel`); no transcripts |

## v2 providers — connect steps

### Lobsters

1. Set `providers.lobsters.enabled: true` in `journals/radar/config.yaml`.
2. Optional: set `tag` to filter by Lobsters tag (empty = hottest).
3. Run the leverage-radar skill.

### DEV.to

1. Set `providers.devto.enabled: true`.
2. Optional: set `tag` (e.g. `ai`, `productivity`) to filter articles.
3. Run the leverage-radar skill.

### YouTube (light — channel RSS only)

1. Set `providers.youtube.enabled: true`.
2. Add one or more channels under `channels`:
   ```yaml
   channels:
     - id: UCxxxxxxxx
       label: "Channel Name"
   ```
3. Set `max_videos_per_channel` (default 5).
4. `search_queries` is optional — reserved for future agent browse; v2 does **not** fetch transcripts or use the YouTube Data API.

**No X/Twitter** fetcher in v2.

Provider failures degrade per-provider; the run continues with remaining sources.

## Provider contract

```text
fetch(**kwargs) → list[Signal]
```

Each signal must match `radar/schema/signal.schema.json`:

- `id`, `provider`, `url`, `title`, `ts` (required)
- `author`, `text`, `metrics`, `provenance` (optional)

## Agent fetch entrypoint

The agent aggregates enabled providers:

```bash
python radar/providers/fetch_enabled.py \
  --config journals/radar/config.yaml \
  --out journals/radar/_raw/2026-07-11.jsonl
```

Individual providers can also be run for debugging:

```bash
python radar/providers/hn/fetch.py --out journals/radar/_raw/hn.jsonl
```

## Add a new provider

1. Create `radar/providers/<id>/fetch.py` with `fetch(**kwargs) -> list[dict]` matching the Signal schema.
2. Register the fetcher in `radar/providers/fetch_enabled.py` (`PROVIDER_FETCHERS` map).
3. Add a `providers.<id>:` block under `templates/radar/config.example.yaml` with `enabled: false` by default.
4. Add a fixture test under `tests/radar/test_<id>_fetch.py` (monkeypatch HTTP; no live network in CI).
5. Document connect steps here if secrets or env vars are required.

No core ranking formula changes — new sources plug in at the adapter layer.

## GitHub Trending note

The unofficial HTML page (`https://github.com/trending?since=daily`) may drift. The stdlib parser is tested against fixtures; if parsing fails in production, the agent may fall back to `WebFetch` and still emit Signals — document any fallback in the provider docstring.

## Reddit note

v1 uses public JSON only with a descriptive `User-Agent`. OAuth (`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`) for higher rate limits is a future enhancement — keep any secrets in the environment only.

## Related

- [Protocol](protocol.md)
- [Using agents](using-agents.md)
