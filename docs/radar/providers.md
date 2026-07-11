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
