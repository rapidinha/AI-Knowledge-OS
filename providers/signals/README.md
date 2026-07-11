# Signals (reference provider)

Reference implementation for **Signal** discovery used by the Leverage Radar agent workflow. This package is a provider under `providers/`, not the product identity of the Context Engine.

## Layout

- `fetch_enabled.py` — agent entrypoint: reads private config, runs enabled source fetchers, writes JSONL
- `sources/` — per-source fetch modules (`hn`, `arxiv`, `reddit`, …)
- `lib/` — config I/O, dedupe, topic helpers
- `schema/` — Signal JSON Schema
- `fixtures/` — HTTP fixtures for tests

## Usage (agents only)

From the repository root:

```bash
python providers/signals/fetch_enabled.py \
  --config journals/radar/config.yaml \
  --out journals/radar/_raw/YYYY-MM-DD.jsonl
```

Do not treat this tree as a user-facing CLI product; skills and agents invoke these scripts.

## Tests

```bash
pytest tests/providers/signals -v
```
