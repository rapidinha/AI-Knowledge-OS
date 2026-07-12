# Providers

Source-agnostic adapters fetch raw signals for the agent to cluster and score. Provider scripts are **agent-invoked tools**, not a user-facing CLI.

## Connect a source in 60 seconds

1. Copy `templates/radar/config.example.yaml` → `journals/radar/config.yaml` (private, gitignored).
2. Set `providers.<name>.enabled: true` for each source you want.
3. If using Reddit: set `user_agent` and `subreddits` in config (PyYAML recommended). v1 uses public JSON only — no OAuth.
4. Ask the agent: **"Run today's Leverage Radar"**.

That is the entire connect flow — no daemon, no product CLI, no API keys in the public repo.

### PyYAML (recommended)

`providers/signals/lib/io.py` includes a minimal YAML fallback, but **PyYAML is recommended** in your private lab for full nested config (categories, subreddits, weights). Install once:

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

### Product Hunt

1. Create a developer application at [Product Hunt API](https://api.producthunt.com/v2/oauth/applications).
2. Set `providers.product_hunt.enabled: true` and optional `limit` (default 20).
3. Export the token in your shell (never commit):

   ```bash
   export PRODUCTHUNT_TOKEN="your-token"
   ```

4. Dry-run ingest with only Product Hunt enabled; verify `run_meta.providers_ok` includes `product_hunt`.

### RSS

1. Set `providers.rss.enabled: true`.
2. Add feed URLs under `feeds` and optional `limit_per_feed`:

   ```yaml
   feeds:
     - https://example.com/atom.xml
   limit_per_feed: 10
   ```

3. No secrets required. Run ingest; check `signals.jsonl` for `provider: rss` rows.

### YouTube Data API (`youtube_api`)

Distinct from **YouTube (light)** channel RSS (`providers.youtube`). Uses the Google YouTube Data API v3 search endpoint.

1. Enable **YouTube Data API v3** in Google Cloud; create an API key.
2. Set `providers.youtube_api.enabled: true`.
3. Set `queries` and/or `channel_ids` and `max_results`:

   ```yaml
   queries:
     - "ai agents"
   channel_ids:
     - UCxxxxxxxx
   max_results: 5
   ```

4. Export the key via env (never commit):

   ```bash
   export YOUTUBE_API_KEY="your-key"
   ```

5. Dry-run ingest; expect `provider: youtube_api` signals.

### GA4 (personal relevance — boost only)

Signals feed **personal_relevance** token overlap only. Raw page views and paths must not appear in daily prose.

1. Set `providers.ga4.enabled: true`, `property_id`, and optional `limit`.
2. **Lab / CI-friendly:** point `export_path` at a local `runReport` JSON export (no live API).
3. **Live API (lab only):** export a short-lived access token:

   ```bash
   export GA4_ACCESS_TOKEN="oauth-access-token"
   ```

   Optional: `GOOGLE_APPLICATION_CREDENTIALS` or `providers.ga4.credentials_file` for service-account flows (keep JSON outside the repo).
4. Dry-run ingest; GA4 rows appear as `GA4 rising page theme: …` titles — themes only, no metric leakage in agent output.

### Search Console (personal relevance — boost only)

Same boost-only rule as GA4. Query strings and click counts stay out of promotable text.

1. Set `providers.search_console.enabled: true`, `site_url` (e.g. `https://yoursite.com/`), and optional `limit`.
2. **Lab / CI-friendly:** set `export_path` to a saved Search Analytics query JSON.
3. **Live API (lab only):**

   ```bash
   export GSC_ACCESS_TOKEN="oauth-access-token"
   ```

   Optional: `GOOGLE_APPLICATION_CREDENTIALS` or `providers.search_console.credentials_file` (lab only; never commit).
4. Dry-run ingest; verify `provider: search_console` in `signals.jsonl`.

Provider failures degrade per-provider; the run continues with remaining sources. Inspect `run_meta.json` for `providers_degraded` and follow setup assist when needed.

## Provider contract

```text
fetch(**kwargs) → list[Signal]
```

Each signal must match `providers/signals/schema/signal.schema.json`:

- `id`, `provider`, `url`, `title`, `ts` (required)
- `author`, `text`, `metrics`, `provenance` (optional)

## Agent fetch entrypoint

Preferred path: pipeline **ingest** stage (writes `_pipeline/` artifacts and legacy `_raw/`):

```bash
python providers/signals/pipeline/run_stages.py \
  --config journals/radar/config.yaml \
  --radar-root journals/radar \
  --date YYYY-MM-DD \
  --stage ingest
```

Legacy direct fetch (debug only):

```bash
python providers/signals/sources/fetch_enabled.py \
  --config journals/radar/config.yaml \
  --out journals/radar/_raw/2026-07-11.jsonl
```

Individual providers can also be run for debugging:

```bash
python providers/signals/sources/hn/fetch.py --out journals/radar/_raw/hn.jsonl
```

## Add a new provider

1. Create `providers/signals/sources/<id>/fetch.py` with `fetch(**kwargs) -> list[dict]` matching the Signal schema.
2. Register the fetcher in `providers/signals/sources/fetch_enabled.py` (`PROVIDER_FETCHERS` map).
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
